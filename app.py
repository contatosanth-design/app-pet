import streamlit as st
from datetime import datetime
import urllib.parse

# 1. CONFIGURAÇÃO E MEMÓRIA
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'historico', 'caixa', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"
if 'tutor_foco' not in st.session_state: st.session_state.tutor_foco = None
if 'pet_foco' not in st.session_state: st.session_state.pet_foco = None

# --- 2. MENU LATERAL ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
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
    v_nome, v_cpf, v_tel = ("", "", "")
    if t_sel != "--- Novo ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == t_sel)
        v_nome, v_cpf, v_tel = c.get('NOME',''), c.get('CPF',''), c.get('TEL','')
    with st.form("f_tutor"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        f_cpf = st.text_input("CPF (Para Recibos)", value=v_cpf)
        f_tel = st.text_input("WhatsApp (Somente números)", value=v_tel)
        if st.form_submit_button("💾 Salvar"):
            if f_nome:
                d = {"NOME": f_nome, "CPF": f_cpf, "TEL": f_tel}
                if t_sel == "--- Novo ---": st.session_state['clientes'].append(d)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == t_sel: st.session_state['clientes'][i] = d
                st.rerun()

# --- 4. MÓDULO PETS ---
elif st.session_state.aba_atual == "🐾 Pets":
    st.subheader("🐾 Pacientes")
    tuts = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    tutor_f = st.selectbox("Tutor:", ["--- Selecione ---"] + tuts)
    if tutor_f != "--- Selecione ---":
        for p in [p for p in st.session_state['pets'] if p['TUTOR'] == tutor_f]:
            st.info(f"🐕 **{p['PET']}** | Raça: {p['RAÇA']} | Idade: {p.get('IDADE','N/I')}")
            if st.button(f"🩺 Atender {p['PET']}"):
                st.session_state.pet_foco = f"{p['PET']} (Tutor: {tutor_f})"
                st.session_state.aba_atual = "📋 Prontuário"
                st.rerun()
        with st.expander("➕ Novo Pet"):
            with st.form("f_pet"):
                n_p = st.text_input("Nome").upper()
                r_p = st.text_input("Raça").upper()
                i_p = st.text_input("Idade")
                if st.form_submit_button("💾 Salvar Pet"):
                    st.session_state['pets'].append({"PET": n_p, "RAÇA": r_p, "TUTOR": tutor_f, "IDADE": i_p})
                    st.rerun()

# --- 5. MÓDULO PRONTUÁRIO ---
elif st.session_state.aba_atual == "📋 Prontuário":
    st.subheader("📋 Prontuário")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    paciente = st.selectbox("Paciente:", ["--- Selecione ---"] + p_lista)
    if paciente != "--- Selecione ---":
        with st.form("f_pront"):
            c1, c2 = st.columns(2)
            f_peso = c1.text_input("Peso (kg)")
            f_temp = c2.text_input("Temp (°C)")
            f_texto = st.text_area("Anamnese (Dite com Win+H)", height=200)
            if st.form_submit_button("💾 Salvar Atendimento"):
                st.session_state['historico'].append({"DATA": datetime.now().strftime("%d/%m/%Y"), "PACIENTE": paciente, "TEXTO": f_texto})
                st.success("Salvo!")

# --- 6. MÓDULO FINANCEIRO COM WHATSAPP ---
elif st.session_state.aba_atual == "💰 Financeiro":
    st.subheader("💰 Fechamento e Recibo WhatsApp")
    precos = {"Consulta Local": 150.0, "Consulta Residencial": 250.0, "Vacina": 120.0, "Medicamento": 50.0}
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    paciente_fin = st.selectbox("Paciente:", ["--- Selecione ---"] + p_lista)

    if paciente_fin != "--- Selecione ---":
        c1, c2, c3 = st.columns([2,1,1])
        serv = c1.selectbox("Serviço:", list(precos.keys()) + ["Outro"])
        valor = c2.number_input("R$:", value=precos.get(serv, 0.0))
        if c3.button("➕ Adicionar"):
            st.session_state.carrinho.append({"ITEM": serv, "VALOR": valor})
            st.rerun()

        if st.session_state.carrinho:
            total = 0
            for i, item in enumerate(st.session_state.carrinho):
                st.write(f"✅ {item['ITEM']} - R$ {item['VALOR']:.2f}")
                total += item['VALOR']
            
            st.write(f"### Total: R$ {total:.2f}")
            forma = st.selectbox("Pagamento:", ["Pix", "Dinheiro", "Cartão"])
            
            if st.button("💾 Finalizar e Gerar Recibo"):
                itens_str = ", ".join([x['ITEM'] for x in st.session_state.carrinho])
                # Salva no histórico do caixa
                st.session_state.caixa.append({"DATA": datetime.now().strftime("%d/%m/%Y"), "PACIENTE": paciente_fin, "ITENS": itens_str, "VALOR": total, "PAGTO": forma})
                
                # Prepara o WhatsApp
                tutor = paciente_fin.split(" (Tutor: ")[1].replace(")", "")
                tutor_d = next((c for c in st.session_state['clientes'] if c['NOME'] == tutor), {})
                tel = tutor_d.get('TEL', '')
                
                msg = f"*RECIBO RIBEIRA VET*\nPet: {paciente_fin.split(' (')[0]}\nServiços: {itens_str}\nTotal: R$ {total:.2f}\nPgto: {forma}"
                st.success("Venda Salva!")
                if tel:
                    link = f"https://wa.me/55{tel}?text={urllib.parse.quote(msg)}"
                    st.link_button("📲 Enviar para WhatsApp", link)
                st.session_state.carrinho = []

# --- 7. BACKUP ---
elif st.session_state.aba_atual == "💾 Backup":
    st.subheader("💾 Backup")
    if st.download_button("📥 Baixar Tudo", str(st.session_state.to_dict()), "backup.txt"):
        st.success("Arquivo salvo em Downloads!")
