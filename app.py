import streamlit as st
from datetime import datetime
import urllib.parse
import ast

# 1. CONFIGURAÇÃO E MEMÓRIA
st.set_page_config(page_title="Ribeira Vet Pro", layout="centered")

# Inicializa as listas de dados se não existirem
for k in ['clientes', 'pets', 'historico', 'caixa', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"

# --- 2. MENU LATERAL ---
with st.sidebar:
    st.title("🐾 Ribeira Vet")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    escolha = st.radio("MENU", opcoes, index=opcoes.index(st.session_state.aba_atual))
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- 3. MÓDULO TUTORES ---
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Clientes")
    if not st.session_state.clientes:
        st.info("👋 Bem-vindo, Doutor! Se os dados sumiram, vá em '💾 Backup' e restaure seu arquivo.")
    
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    t_sel = st.selectbox("Buscar Cliente:", ["--- Novo ---"] + nomes)
    v_nome, v_cpf, v_tel, v_email, v_end = ("", "", "", "", "")
    if t_sel != "--- Novo ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == t_sel)
        v_nome, v_cpf, v_tel, v_email, v_end = c.get('NOME',''), c.get('CPF',''), c.get('TEL',''), c.get('EMAIL',''), c.get('END','')

    with st.form("f_tutor"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        f_tel = st.text_input("WhatsApp (DDD+Número)", value=v_tel)
        f_cpf = st.text_input("CPF", value=v_cpf)
        f_email = st.text_input("E-mail", value=v_email)
        f_end = st.text_area("Endereço Completo", value=v_end)
        if st.form_submit_button("💾 SALVAR", use_container_width=True):
            if f_nome:
                d = {"NOME": f_nome, "CPF": f_cpf, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if t_sel == "--- Novo ---": st.session_state['clientes'].append(d)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == t_sel: st.session_state['clientes'][i] = d
                st.success("Salvo!")
                st.rerun()

# --- 4. MÓDULO PETS ---
elif st.session_state.aba_atual == "🐾 Pets":
    st.subheader("🐾 Pacientes")
    tuts = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    t_f = st.selectbox("Tutor:", ["--- Selecione ---"] + tuts)
    if t_f != "--- Selecione ---":
        for p in [p for p in st.session_state['pets'] if p['TUTOR'] == t_f]:
            st.info(f"🐕 **{p['PET']}** ({p['RAÇA']})")
            if st.button(f"🩺 Atender {p['PET']}", use_container_width=True):
                st.session_state.pet_foco = f"{p['PET']} (Tutor: {t_f})"
                st.session_state.aba_atual = "📋 Prontuário"
                st.rerun()
        with st.expander("➕ Novo Pet"):
            with st.form("f_pet"):
                n_p = st.text_input("Nome").upper()
                r_p = st.text_input("Raça").upper()
                i_p = st.text_input("Idade")
                if st.form_submit_button("💾 Salvar Pet"):
                    st.session_state['pets'].append({"PET": n_p, "RAÇA": r_p, "TUTOR": t_f, "IDADE": i_p})
                    st.rerun()

# --- 5. MÓDULO PRONTUÁRIO ---
elif st.session_state.aba_atual == "📋 Prontuário":
    st.subheader("📋 Atendimento")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    paciente = st.selectbox("Paciente:", ["--- Selecione ---"] + p_lista)
    if paciente != "--- Selecione ---":
        with st.form("f_pront"):
            c1, c2 = st.columns(2)
            f_peso = c1.text_input("Peso (kg)")
            f_temp = c2.text_input("Temp (°C)")
            f_texto = st.text_area("Anamnese (Use o microfone do celular):", height=250)
            if st.form_submit_button("💾 SALVAR CONSULTA", use_container_width=True):
                st.session_state['historico'].append({"DATA": datetime.now().strftime("%d/%m/%Y"), "PACIENTE": paciente, "TEXTO": f_texto, "PESO": f_peso, "TEMP": f_temp})
                st.success("Atendimento salvo!")

# --- 6. MÓDULO FINANCEIRO ---
elif st.session_state.aba_atual == "💰 Financeiro":
    st.subheader("💰 Financeiro")
    precos = {"Consulta Local": 150.0, "Consulta Residencial": 250.0, "Vacina": 120.0, "Medicamento": 50.0}
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    paciente_fin = st.selectbox("Cobrar de:", ["--- Selecione ---"] + p_lista)
    if paciente_fin != "--- Selecione ---":
        serv = st.selectbox("Serviço:", list(precos.keys()) + ["Outro"])
        valor = st.number_input("Preço R$:", value=precos.get(serv, 0.0))
        if st.button("➕ Adicionar", use_container_width=True):
            st.session_state.carrinho.append({"ITEM": serv, "VALOR": valor})
        if st.session_state.carrinho:
            total = sum(item['VALOR'] for item in st.session_state.carrinho)
            st.write(f"### Total: R$ {total:.2f}")
            if st.button("✅ Finalizar e WhatsApp", use_container_width=True):
                # Salva no caixa
                st.session_state.caixa.append({"DATA": datetime.now().strftime("%d/%m/%Y"), "PACIENTE": paciente_fin, "VALOR": total})
                # Gera link WhatsApp
                t_nome = paciente_fin.split(" (Tutor: ")[1].replace(")", "")
                t_dados = next((c for c in st.session_state['clientes'] if c['NOME'] == t_nome), {})
                msg = f"Recibo Ribeira Vet: {paciente_fin.split(' (')[0]}. Total: R$ {total:.2f}"
                st.session_state.carrinho = []
                if t_dados.get('TEL'):
                    st.link_button("📲 Enviar WhatsApp", f"https://wa.me/55{t_dados['TEL']}?text={urllib.parse.quote(msg)}")
                st.rerun()

# --- 7. MÓDULO BACKUP ---
elif st.session_state.aba_atual == "💾 Backup":
    st.subheader("💾 Backup e Restauração")
    dados = {'clientes': st.session_state.clientes, 'pets': st.session_state.pets, 'historico': st.session_state.historico, 'caixa': st.session_state.caixa}
    st.download_button("📥 BAIXAR BACKUP AGORA", str(dados), file_name="backup_vet.txt", use_container_width=True)
    st.divider()
    arquivo = st.file_uploader("Subir arquivo para restaurar:", type="txt")
    if arquivo and st.button("🔄 RESTAURAR TUDO", use_container_width=True):
        d_rec = ast.literal_eval(arquivo.read().decode("utf-8"))
        st.session_state.clientes = d_rec.get('clientes', [])
        st.session_state.pets = d_rec.get('pets', [])
        st.session_state.historico = d_rec.get('historico', [])
        st.session_state.caixa = d_rec.get('caixa', [])
        st.success("✅ Dados restaurados!")
