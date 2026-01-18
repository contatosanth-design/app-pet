import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. NÚCLEO DE DADOS E CONFIGURAÇÃO
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'historico', 'financeiro']:
    if k not in st.session_state: st.session_state[k] = []

# Controle de Navegação Automática
if 'fluxo' not in st.session_state:
    st.session_state['fluxo'] = {"aba": "👤 Tutores", "tutor": None, "pet": None}

# 2. MENU LATERAL
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    idx_atual = opcoes.index(st.session_state['fluxo']['aba'])
    menu = st.radio("NAVEGAÇÃO", opcoes, index=idx_atual, key="nav_main")
    st.session_state['fluxo']['aba'] = menu

# --- MÓDULOS ---

# MÓDULO 1: TUTORES (E-mail Obrigatório)
if menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    nomes_lista = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    busca = st.selectbox("⚡ Selecionar Tutor:", ["--- Novo Cadastro ---"] + nomes_lista)

    v_nome, v_tel, v_email, v_cpf, v_end = ("", "", "", "", "")
    if busca != "--- Novo Cadastro ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == busca)
        v_nome, v_tel, v_email, v_cpf, v_end = c['NOME'], c['TEL'], c.get('EMAIL', ""), c['CPF'], c.get('END', "")
        
        if st.button(f"➡️ Ver Pets de {v_nome}"):
            st.session_state['fluxo'].update({"aba": "🐾 Pets", "tutor": v_nome})
            st.rerun()

    with st.form("form_tutor_v14"):
        col1, col2 = st.columns([2, 1])
        f_nome = col1.text_input("Nome Completo *", value=v_nome).upper()
        f_tel = col2.text_input("WhatsApp", value=v_tel)
        f_email = st.text_input("E-mail (Obrigatório para Lembretes) *", value=v_email).lower()
        f_cpf = st.text_input("CPF/Documento", value=v_cpf)
        f_end = st.text_input("Endereço Completo", value=v_end)
        
        if st.form_submit_button("💾 Salvar/Atualizar"):
            if f_nome and f_email:
                dados = {"NOME": f_nome, "TEL": f_tel, "EMAIL": f_email, "CPF": f_cpf, "END": f_end}
                if busca == "--- Novo Cadastro ---":
                    st.session_state['clientes'].append(dados)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == busca: st.session_state['clientes'][i] = dados
                st.rerun()
            else:
                st.error("Nome e E-mail são obrigatórios.")

# MÓDULO 2: PETS (Raça e Espécie Fixas)
elif menu == "🐾 Pets":
    st.subheader("🐾 Pacientes")
    tuts = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    idx_t = (tuts.index(st.session_state['fluxo']['tutor']) + 1) if st.session_state['fluxo']['tutor'] in tuts else 0
    t_sel = st.selectbox("Tutor:", ["--- Selecione ---"] + tuts, index=idx_t)

    if t_sel != "--- Selecione ---":
        pets_filtro = [p for p in st.session_state['pets'] if p['TUTOR'] == t_sel]
        for p in pets_filtro:
            c_p, c_a = st.columns([4, 1])
            c_p.info(f"🐶 **{p['PET']}** ({p['ESP']} - {p['RAÇA']})")
            if c_a.button(f"🩺 Atender", key=f"at_{p['PET']}"):
                st.session_state['fluxo'].update({"aba": "📋 Prontuário", "pet": f"{p['PET']} (Tutor: {t_sel})"})
                st.rerun()
        
        with st.expander("➕ Novo Animal"):
            with st.form("form_pet_v14"):
                cp1, cp2 = st.columns(2)
                nome_p = cp1.text_input("Nome do Pet *").upper()
                esp_p = cp2.selectbox("Espécie", ["Cão", "Gato", "Outro"])
                raca_p = st.text_input("Raça *").upper() #
