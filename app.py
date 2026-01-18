import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO E ESTABILIDADE ---
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicialização segura de dados
for k in ['clientes', 'pets', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

# Controle de Navegação (Corrige as telas brancas)
if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"
if 'tutor_foco' not in st.session_state: st.session_state.tutor_foco = None
if 'pet_foco' not in st.session_state: st.session_state.pet_foco = None

# --- 2. BARRA LATERAL (MENU) ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    idx_menu = opcoes.index(st.session_state.aba_atual)
    escolha = st.radio("MENU", opcoes, index=idx_menu, key="nav_v8")
    
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- 3. MÓDULOS ---

# ABA TUTORES (Com Telefone e Endereço)
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    busca = st.selectbox("Selecione o Tutor:", ["--- Novo Cadastro ---"] + nomes)

    v_nome, v_tel, v_email, v_end = ("", "", "", "")
    if busca != "--- Novo Cadastro ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == busca)
        v_nome, v_tel, v_email, v_end = c['NOME'], c.get('TEL', ""), c.get('EMAIL', ""), c.get('END', "")
        
        # BOTÃO ATALHO PARA PETS
        if st.button(f"➡️ Ver Animais de {v_nome}"):
            st.session_state.tutor_foco = v_nome
            st.session_state.aba_atual = "🐾 Pets"
            st.rerun()

    with st.form("f_tutor_v8"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        col1, col2 = st.columns(2)
        f_tel = col1.text_input("WhatsApp / Telefone", value=v_tel)
        f_email = col2.text_input("E-mail (Obrigatório) *", value=v_email).lower()
        f_end = st.text_area("Endereço Completo (Localização) *", value=v_end)
        
        if st.form_submit_button("💾 Salvar Tutor"):
            if f_nome and f_email and f_end:
                dados = {"NOME": f_nome, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if busca == "--- Novo Cadastro ---":
                    st.session_state['clientes'].append(dados)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == busca: st.session_state['clientes'][i] = dados
                st.rerun()
            else:
                st.error("Preencha Nome, E-mail e Endereço.")

# ABA PETS (Raças cadastradas agora aparecem aqui)
elif st.session_state.aba_atual == "🐾 Pets":
    st.subheader("🐾 Pacientes e Raças")
    tuts = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    idx_t = (tuts.index(st.session_state.tutor_foco) + 1) if st.session_state.tutor_foco in tuts else 0
    tutor_sel = st.selectbox("Tutor Responsável:", ["--- Selecione ---"] + tuts, index=idx_t)

    if tutor_sel != "--- Selecione ---":
        # LISTA DE RAÇAS JÁ CADASTRADAS
        pets_lista = [p for p in st.session_state['pets'] if p['TUTOR'] == tutor_sel]
        for p in pets_lista:
            c_info, c_at = st.columns([4, 1])
            c_info.warning(f"🐕 **{p['PET']}** | Raça: **{p['RAÇA']}**")
            if c_at.button(f"🩺 Atender", key=f"at_{p['PET']}"):
                st.session_state.pet_foco = f"{p['PET']} (Tutor: {tutor_sel})"
                st.session_state.aba_atual = "📋 Prontuário"
                st.rerun()
        
        with st.expander("➕ Cadastrar Novo Animal para este Tutor"):
            with st.form("f_pet_v8"):
                n_pet = st.text_input("Nome do Pet").upper()
                r_pet = st.text_input("Raça (Ex: Poodle, SRD, Persa) *").upper()
                if st.form_submit_button("💾 Salvar Pet"):
                    if n_pet and r_pet:
                        st.session_state['pets'].append({"PET": n_pet, "RAÇA": r_pet, "TUTOR": tutor_sel})
                        st.rerun()

# ABA PRONTUÁRIO
elif st.session_state.aba_atual == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    lista_p = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    idx_p = (lista_p.index(st.session_state.pet_foco) + 1) if st.session_state.pet_foco in lista_p else 0
    paciente = st.selectbox("Paciente:", ["--- Selecione ---"] + lista_p, index=idx_p)

    if paciente != "--- Selecione ---":
        c1, c2 = st.columns([2, 1])
        with c1:
            with st.form("f_atend_v8"):
                anamnese = st.text_area("Descrição da Consulta:", height=300)
                if st.form_submit_button("💾 Finalizar"):
                    st.
