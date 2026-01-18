import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO E MEMÓRIA ---
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicialização segura de variáveis
for k in ['clientes', 'pets', 'historico', 'financeiro']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_ativa' not in st.session_state:
    st.session_state.aba_ativa = "👤 Tutores"
if 'tutor_foco' not in st.session_state:
    st.session_state.tutor_foco = None
if 'pet_foco' not in st.session_state:
    st.session_state.pet_foco = None

# --- 2. MENU LATERAL (CONTROLADO POR ESTADO) ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    
    # O rádio agora é apenas um observador do estado real
    idx_atual = opcoes.index(st.session_state.aba_ativa)
    escolha = st.radio("NAVEGAÇÃO", opcoes, index=idx_atual, key="nav_fix")
    
    # Se o usuário clicar manualmente no menu, atualiza o estado
    if escolha != st.session_state.aba_ativa:
        st.session_state.aba_ativa = escolha
        st.rerun()

# --- 3. MÓDULOS ---

# ABA TUTORES
if st.session_state.aba_ativa == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    selecao = st.selectbox("Buscar Tutor:", ["--- Novo ---"] + nomes)

    # Lógica de preenchimento e Botão "Ir para Pets"
    if selecao != "--- Novo ---":
        dados = next(c for c in st.session_state['clientes'] if c['NOME'] == selecao)
        st.session_state.tutor_foco = selecao # Salva para a próxima tela
        
        if st.button(f"➡️ Ir para Pets de {selecao}"):
            st.session_state.aba_ativa = "🐾 Pets" # Muda a aba
            st.rerun() # Força a atualização da tela

    with st.form("form_tutor"):
        f_nome = st.text_input("Nome Completo *", value=(selecao if selecao != "--- Novo ---" else "")).upper()
        f_email = st.text_input("E-mail (Obrigatório) *").lower()
        f_end = st.text_area("Endereço Completo *")
        if st.form_submit_button("💾 Salvar"):
            if f_nome and f_email:
                st.session_state['clientes'].append({"NOME": f_nome, "EMAIL": f_email, "END": f_end})
                st.rerun()

# ABA PETS
elif st.session_state.aba_ativa == "🐾 Pets":
    st.subheader("🐾 Pacientes e Raças")
    tuts = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    
    # Tenta pré-selecionar o tutor vindo da tela anterior
    idx_t = (tuts.index(st.session_state.tutor_foco) + 1) if st.session_state.tutor_foco in tuts else 0
    t_sel = st.selectbox("Selecione o Tutor:", ["--- Selecione ---"] + tuts, index=idx_t)

    if t_sel != "--- Selecione ---":
        meus_pets = [p for p in st.session_state['pets'] if p['TUTOR'] == t_sel]
        for p in meus_pets:
            col_i, col_b = st.columns([4, 1])
            col_i.info(f"🐕 **{p['PET']}** ({p['RAÇA']})")
            # BOTÃO ATENDER CORRIGIDO
            if col_b.button(f"🩺 Atender", key=f"at_{p['PET']}"):
                st.session_state.pet_foco = f"{p['PET']} (Tutor: {t_sel})"
                st.session_state.aba_ativa = "📋 Prontuário"
                st.rerun()
        
        with st.expander("➕ Novo Animal"):
            with st.form("f_pet"):
                n_p = st.text_input("Nome do Pet").upper()
                r_p = st.text_input("Raça").upper()
                if st.form_submit_button("💾 Salvar Pet"):
                    st.session_state['pets'].append({"PET": n_p, "RAÇA": r_p, "TUTOR": t_sel})
                    st.rerun()

# ABA PRONTUÁRIO
elif st.session_state.aba_ativa == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    
    idx_p = (p_lista.index(st.session_state.pet_foco) + 1) if st.session_state.pet_foco in p_lista else 0
    paciente = st.selectbox("Paciente:", ["--- Selecione ---"] + p_lista, index=idx_p)

    if paciente != "--- Selecione ---":
        col_1, col_2 = st.columns([2, 1])
        with col_1:
            with st.form("f_at"):
                relato = st.text_area("Evolução Clínica:", height=300)
                if st.form_submit_button("💾 Finalizar"):
                    st.session_state['historico'].append({"DATA": datetime.now(), "PACIENTE": paciente, "TEXTO": relato})
                    st.session_state.pet_foco = None
                    st.session_state.aba_ativa = "👤 Tutores" # Volta ao início
                    st.rerun()
