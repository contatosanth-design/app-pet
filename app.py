import streamlit as st
from datetime import datetime
import urllib.parse
import ast

# 1. CONFIGURAÇÃO E MEMÓRIA
st.set_page_config(page_title="Ribeira Vet Pro", layout="centered")

for k in ['clientes', 'pets', 'historico', 'caixa', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"

# Função para calcular idade
def calcular_idade(nascimento):
    try:
        nasc = datetime.strptime(nascimento, "%d/%m/%Y")
        hoje = datetime.now()
        idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
        return f"{idade} anos" if idade > 0 else "Menos de 1 ano"
    except:
        return "Idade N/I"

# --- 2. MENU LATERAL ---
with st.sidebar:
    st.title("🐾 Ribeira Vet")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    escolha = st.radio("NAVEGAÇÃO", opcoes, index=opcoes.index(st.session_state.aba_atual))
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- 3. MÓDULO TUTORES ---
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    t_sel = st.selectbox("Buscar ou Novo:", ["--- Novo ---"] + nomes)
    
    v_nome, v_cpf, v_tel, v_email, v_end = ("", "", "", "", "")
    if t_sel != "--- Novo ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == t_sel)
        v_nome, v_cpf, v_tel, v_email, v_end = c.get('NOME',''), c.get('CPF',''), c.get('TEL',''), c.get('EMAIL',''), c.get('END','')

    with st.form("f_tutor"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        f_cpf = st.text_input("CPF", value=v_cpf)
        f_tel = st.text_input("WhatsApp", value=v_tel)
        f_email = st.text_input("E-mail", value=v_email)
        f_end = st.text_area("Endereço Completo", value=v_end)
        if st.form_submit_button("💾 SALVAR TUTOR", use_container_width=True):
            if f_nome:
                d = {"NOME": f_nome, "CPF": f_cpf, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if t_sel == "--- Novo ---": st.session_state['clientes'].append(d)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == t_sel: st.session_state['clientes'][i] = d
                st.success("Tutor salvo!")
                st.rerun()

# --- 4. MÓDULO PETS (IDADE E RAÇA) ---
elif st.session_state.aba_atual == "🐾 Pets":
    st.subheader("🐾 Pacientes")
    tuts = sorted([c['NOME'] for c in st.session_state['clientes']])
    if not tuts:
        st.warning("Cadastre um tutor primeiro.")
    else:
        t_f = st.selectbox("Selecione o Tutor:", ["--- Selecione ---"] + tuts)
        if t_f != "--- Selecione ---":
            meus_pets = [p for p in st.session_state['pets'] if p['TUTOR'] == t_f]
            for p in meus_pets:
                idade = calcular_idade(p.get('NASCIMENTO', ''))
                st.info(f"🐕 **{p['PET']}** | Raça: {p['RAÇA']} | {idade}")
                if st.button(f"🩺 Atender {p['PET']}", use_container_width=True):
                    st.session_state.aba_atual = "📋 Prontuário"
                    st.rerun()
            
            with st.expander("➕ Novo Pet"):
                with st.form("f_pet"):
                    n_p = st.text_input("Nome").upper()
                    r_p = st.text_input("Raça").upper()
                    d_n = st.text_input("Nascimento (DD/MM/AAAA)")
                    if st.form_submit_button("Salvar Pet"):
                        st.session_state['pets'].append({"PET": n_p, "RAÇA": r_p, "NASCIMENTO": d_n, "TUTOR": t_f})
                        st.rerun()

# --- 5. MÓDULO PRONTUÁRIO ---
elif st.session_state.aba_atual == "📋 Prontuário":
    st.subheader("📋 Prontuário")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    paciente = st.selectbox("Selecione o Paciente:", ["--- Selecione ---"] + p_lista)
    if paciente != "--- Selecione ---":
        with st.form("f_pront"):
            f_peso = st.text_input("Peso (kg)")
            f_temp = st.text_input("Temp (°C)")
            f_texto = st.text_area("Anamnese e Conduta:", height=250)
            if st.form_submit_button("💾 SALVAR CONSULTA", use_container_width=True):
                st.session_state['historico'].append({"DATA": datetime.now().strftime("%d/%m/%Y"), "PACIENTE": paciente, "TEXTO": f_texto, "PESO": f_peso, "TEMP": f_temp})
                st.success("Salvo!")

# --- 6. MÓDULO FINANCEIRO ---
elif st.session_state.aba_atual == "💰 Financeiro":
    st.subheader("💰 Financeiro")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    paciente_fin = st.selectbox("Cobrar de:", ["--- Selecione ---"] + p_lista)
    if paciente_fin != "--- Selecione ---":
        serv = st.text_input("Serviço")
        valor = st.number_input("Valor R$", min_value=0.0)
        if st.button("📲 Gerar Recibo WhatsApp", use_container_width=True):
            t_nome = paciente_fin.split(" (Tutor: ")[1].replace(")", "")
            t_dados = next((c for c in st.session_state['clientes'] if c['NOME'] == t_nome), {})
            msg = f"Recibo Ribeira Vet: {serv}. Valor: R$ {valor:.2f}"
            if t_dados.get('TEL'):
                link = f"https://wa.me/55{t_dados['TEL']}?text={urllib.parse.quote(msg)}"
                st.link_button("Abrir WhatsApp", link)

# --- 7. MÓDULO BACKUP ---
elif st.session_state.aba_atual == "💾 Backup":
    st.subheader("💾 Segurança")
    dados = {'clientes': st.session_state.clientes, 'pets': st.session_state.pets, 'historico': st.session_state.historico}
    st.download_button("📥 BAIXAR BACKUP", str(dados), file_name="backup_vet.txt", use_container_width=True)
    st.divider()
    arquivo = st.file_uploader("Restaurar arquivo:", type="txt")
    if arquivo and st.button("🔄 RESTAURAR TUDO", use_container_width=True):
        d_rec = ast.literal_eval(arquivo.read().decode("utf-8"))
        st.session_state.clientes = d_rec.get('clientes', [])
        st.session_state.pets = d_rec.get('pets', [])
        st.session_state.historico = d_rec.get('historico', [])
        st.success("Dados restaurados!")
