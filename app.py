import streamlit as st
from datetime import datetime
import urllib.parse
import ast

# 1. FORÇAR MODO CLARO E CONFIGURAÇÃO
st.set_page_config(page_title="Ribeira Vet Pro", layout="centered")

# Estilo para garantir que o fundo seja branco e o texto preto (resolve o 'preto no celular')
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    label, p, span { color: black !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #f0f2f6 !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização de memória
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
    st.subheader("👤 Cadastro de Tutores")
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    t_sel = st.selectbox("Buscar Cliente:", ["--- Novo ---"] + nomes)
    v_nome, v_cpf, v_tel, v_email, v_end = ("", "", "", "", "")
    if t_sel != "--- Novo ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == t_sel)
        v_nome, v_cpf, v_tel, v_email, v_end = c.get('NOME',''), c.get('CPF',''), c.get('TEL',''), c.get('EMAIL',''), c.get('END','')
    with st.form("f_tutor"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        f_cpf = st.text_input("CPF", value=v_cpf)
        f_tel = st.text_input("WhatsApp", value=v_tel)
        f_end = st.text_area("Endereço", value=v_end)
        if st.form_submit_button("💾 SALVAR TUTOR", use_container_width=True):
            if f_nome:
                d = {"NOME": f_nome, "CPF": f_cpf, "TEL": f_tel, "END": f_end}
                if t_sel == "--- Novo ---": st.session_state['clientes'].append(d)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == t_sel: st.session_state['clientes'][i] = d
                st.success("Tutor Salvo!")
                st.rerun()

# --- 4. MÓDULO PETS ---
elif st.session_state.aba_atual == "🐾 Pets":
    st.subheader("🐾 Cadastro de Animais")
    lista_tutores = sorted([c['NOME'] for c in st.session_state['clientes']])
    if not lista_tutores:
        st.warning("⚠️ Cadastre um Tutor primeiro.")
    else:
        tutor_f = st.selectbox("Dono:", ["--- Selecione ---"] + lista_tutores)
        if tutor_f != "--- Selecione ---":
            for p in [p for p in st.session_state['pets'] if p['TUTOR'] == tutor_f]:
                st.info(f"🐕 **{p['PET']}**")
                if st.button(f"Atender {p['PET']}", use_container_width=True):
                    st.session_state.pet_foco = f"{p['PET']} (Tutor: {tutor_f})"
                    st.session_state.aba_atual = "📋 Prontuário"
                    st.rerun()
            with st.expander("➕ Novo Pet"):
                with st.form("f_pet"):
                    n_p = st.text_input("Nome").upper()
                    r_p = st.text_input("Raça").upper()
                    if st.form_submit_button("Salvar Pet"):
                        st.session_state['pets'].append({"PET": n_p, "RAÇA": r_p, "TUTOR": tutor_f})
                        st.rerun()

# --- 5. MÓDULO PRONTUÁRIO ---
elif st.session_state.aba_atual == "📋 Prontuário":
    st.subheader("📋 Prontuário")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    if not p_lista:
        st.warning("⚠️ Nenhum pet cadastrado.")
    else:
        paciente = st.selectbox("Paciente:", ["--- Selecione ---"] + p_lista)
        if paciente != "--- Selecione ---":
            with st.form("f_pront"):
                c1, c2 = st.columns(2)
                f_peso = c1.text_input("Peso")
                f_temp = c2.text_input("Temp")
                f_texto = st.text_area("Anamnese/Conduta:", height=200)
                if st.form_submit_button("💾 SALVAR", use_container_width=True):
                    st.session_state['historico'].append({"DATA": datetime.now().strftime("%d/%m/%Y"), "PACIENTE": paciente, "TEXTO": f_texto, "PESO": f_peso, "TEMP": f_temp})
                    st.success("Salvo!")

# --- 7. MÓDULO BACKUP ---
elif st.session_state.aba_atual == "💾 Backup":
    st.subheader("💾 Backup")
    dados = {'clientes': st.session_state.clientes, 'pets': st.session_state.pets, 'historico': st.session_state.historico, 'caixa': st.session_state.caixa}
    st.download_button("📥 BAIXAR BACKUP", str(dados), file_name="backup_vet.txt", use_container_width=True)
    st.divider()
    arquivo = st.file_uploader("Restaurar:", type="txt")
    if arquivo and st.button("🔄 RESTAURAR TUDO", use_container_width=True):
        st.session_state.clientes = ast.literal_eval(arquivo.read().decode("utf-8")).get('clientes', [])
        # ... (restaura as outras listas)
        st.success("✅ Restaurado!")
