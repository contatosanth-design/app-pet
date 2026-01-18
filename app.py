import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO E PERSISTÊNCIA ---
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicialização de dados (Banco de Dados em Memória)
for k in ['clientes', 'pets', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

if 'fluxo' not in st.session_state:
    st.session_state['fluxo'] = {"aba": "👤 Tutores", "tutor": None, "pet": None}

# --- NAVEGAÇÃO ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro"]
    aba_idx = opcoes.index(st.session_state['fluxo']['aba'])
    menu = st.radio("MENU PRINCIPAL", opcoes, index=aba_idx, key="nav_vet_final")
    st.session_state['fluxo']['aba'] = menu

# --- MÓDULO 1: TUTORES (FOCO EM E-MAIL E CONTATO) ---
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes (Tutores)")
    nomes_cadastrados = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    tutor_selecionado = st.selectbox("🔍 Buscar ou Criar:", ["--- Novo Cadastro ---"] + nomes_cadastrados)

    # Lógica de preenchimento automático para edição
    v_nome, v_tel, v_email = ("", "", "")
    if tutor_selecionado != "--- Novo Cadastro ---":
        dados = next(c for c in st.session_state['clientes'] if c['NOME'] == tutor_selecionado)
        v_nome, v_tel, v_email = dados['NOME'], dados['TEL'], dados.get('EMAIL', "")
        
        if st.button(f"➡️ Ver Animais de {v_nome}"):
            st.session_state['fluxo'].update({"aba": "🐾 Pets", "tutor": v_nome})
            st.rerun()

    with st.form("f_tutor"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        col1, col2 = st.columns(2)
        f_tel = col1.text_input("WhatsApp", value=v_tel)
        f_email = col2.text_input("E-mail (Obrigatório) *", value=v_email).lower() #
        if st.form_submit_button("💾 Salvar Tutor"):
            if f_nome and f_email:
                novo_dado = {"NOME": f_nome, "TEL": f_tel, "EMAIL": f_email}
                if tutor_selecionado == "--- Novo Cadastro ---":
                    st.session_state['clientes'].append(novo_dado)
                else:
                    for i, c in enumerate(st.session_state['clientes']):
                        if c['NOME'] == tutor_selecionado: st.session_state['clientes'][i] = novo_dado
                st.rerun()

# --- MÓDULO 2: PACIENTES E RAÇAS ---
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    t_lista = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    idx_t = (t_lista.index(st.session_state['fluxo']['tutor']) + 1) if st.session_state['fluxo']['tutor'] in t_lista else 0
    tutor_foco = st.selectbox("Tutor Responsável:", ["--- Selecione ---"] + t_lista, index=idx_t)

    if tutor_foco != "--- Selecione ---":
        # Exibe Pets já cadastrados com Raça visível
        meus_pets = [p for p in st.session_state['pets'] if p['TUTOR'] == tutor_foco]
        for p in meus_pets:
            c1, c2 = st.columns([4, 1])
            c1.warning(f"🐕 {p['PET']} | Espécie: {p['ESP']} | Raça: {p['RAÇA']}")
            if c2.button(f"🩺 Atender", key=f"at_{p['PET']}"):
                st.session_state['fluxo'].update({"aba": "📋 Prontuário", "pet": f"{p['PET']} (Tutor: {tutor_foco})"})
                st.rerun()

        with st.expander("➕ Cadastrar Novo Animal"):
            with st.form("f_pet"):
                n_p = st.text_input("Nome do Pet *").upper()
                c1, c2 = st.columns(2)
                e_p = c1.selectbox("Espécie", ["Cão", "Gato", "Outro"])
                r_p = c2.text_input("Raça *").upper() #
                if st.form_submit_button("💾 Salvar Pet"):
                    if n_p and r_p:
                        st.session_state['pets'].append({"PET": n_p, "ESP": e_p, "RAÇA": r_p, "TUTOR": tutor_foco})
                        st.rerun()

# --- MÓDULO 3: PRONTUÁRIO E HISTÓRICO DUAL ---
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    idx_p = (p_lista.index(st.session_state['fluxo']['pet']) + 1) if st.session_state['fluxo']['pet'] in p_lista else 0
    paciente = st.selectbox("Paciente:", ["--- Selecione ---"] + p_lista, index=idx_p)

    if paciente != "--- Selecione ---":
        col_reg, col_hist = st.columns([2, 1])
        with col_reg:
            with st.form("f_clinico"):
                peso = st.text_input("Peso (kg)")
                anamnese = st.text_area("Evolução Clínica / Vacinas:", height=250)
                retorno = st.date_input("Lembrete de Retorno", value=datetime.now() + timedelta(days=15))
                if st.form_submit_button("💾 Finalizar Consulta"):
                    st.session_state['historico'].append({
                        "DATA": datetime.now().strftime("%d/%m/%Y"), "PACIENTE": paciente,
                        "RELATO": anamnese, "RETORNO": retorno.strftime("%d/%m/%Y")
                    })
                    st.rerun()
        with col_hist:
            st.write("### 📜 Passado Médico")
            h_p = [h for h in st.session_state['historico'] if h['PACIENTE'] == paciente]
            for h in reversed(h_p):
                with st.expander(f"📅 {h['DATA']}"):
                    st.write(h['RELATO'])
                    st.info(f"🔔 Retorno: {h['RETORNO']}")
