import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PARAMETROS DE MEMÓRIA (Rollback v7.0 integrado)
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

# Controle de fluxo para evitar telas brancas
if 'aba_atual' not in st.session_state: st.session_state['aba_atual'] = "👤 Tutores"
if 'tutor_selecionado' not in st.session_state: st.session_state['tutor_selecionado'] = None
if 'pet_selecionado' not in st.session_state: st.session_state['pet_selecionado'] = None

# 2. NAVEGAÇÃO FIXA
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    # Garante que o menu acompanhe a mudança de aba automática
    idx = opcoes.index(st.session_state['aba_atual'])
    menu = st.radio("NAVEGAÇÃO", opcoes, index=idx)
    st.session_state['aba_atual'] = menu

# 3. MÓDULO TUTORES: CARREGAMENTO IMEDIATO
if menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    busca = st.selectbox("⚡ Buscar Tutor Cadastrado:", ["--- Novo Cadastro ---"] + nomes)

    # Recupera dados se não for novo cadastro
    if busca != "--- Novo Cadastro ---":
        dados = next(c for c in st.session_state['clientes'] if c['NOME'] == busca)
        v_nome, v_tel, v_cpf = dados['NOME'], dados['TEL'], dados['CPF']
        
        # ATALHO PARA PRÓXIMA TELA (Sem precisar salvar)
        st.success(f"✅ Cadastro de {busca} carregado.")
        if st.button(f"➡️ Ir para Pets de {busca}"):
            st.session_state['tutor_selecionado'] = busca
            st.session_state['aba_atual'] = "🐾 Pets"
            st.rerun()
    else:
        v_nome, v_tel, v_cpf = "", "", ""

    with st.form("f_tutores"):
        c1, c2 = st.columns([3, 1])
        f_nome = c1.text_input("Nome Completo *", value=v_nome).upper()
        f_tel = c2.text_input("WhatsApp", value=v_tel)
        f_cpf = st.text_input("CPF/Documento", value=v_cpf)
        
        if st.form_submit_button("💾 Salvar/Atualizar"):
            if f_nome:
                if busca == "--- Novo Cadastro ---":
                    st.session_state['clientes'].append({"NOME": f_nome, "TEL": f_tel, "CPF": f_cpf})
                else:
                    for c in st.session_state['clientes']:
                        if c['NOME'] == busca: c.update({"NOME": f_nome, "TEL": f_tel, "CPF": f_cpf})
                st.rerun()

# 4. MÓDULO PETS: LISTAGEM E ATALHO PRONTUÁRIO
elif menu == "🐾 Pets":
    st.subheader("🐾 Pacientes")
    tutores = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    
    # Auto-seleção vinda do atalho
    idx_t = 0
    if st.session_state['tutor_selecionado'] in tutores:
        idx_t = tutores.index(st.session_state['tutor_selecionado']) + 1
    
    t_sel = st.selectbox("Selecione o Cliente:", ["--- Escolha ---"] + tutores, index=idx_t)
    
    if t_sel != "--- Escolha ---":
        pets = [p for p in st.session_state['pets'] if p['TUTOR'] == t_sel]
        for p in pets:
            col_n, col_b = st.columns([4, 1])
            col_n.info(f"🐕 {p['PET']} ({p['RAÇA']})")
            if col_b.button(f"🩺 Atender", key=f"at_{p['PET']}"):
                st.session_state['pet_selecionado'] = f"{p['PET']} (Tutor: {t_sel})"
                st.session_state['aba_atual'] = "📋 Prontuário"
                st.rerun()
        
        with st.expander("➕ Novo Animal"):
            with st.form("f_pet"):
                n_p = st.text_input("Nome").upper()
                r_p = st.text_input("Raça").upper()
                if st.form_submit_button("Salvar Pet"):
                    st.session_state['pets'].append({"PET": n_p, "RAÇA": r_p, "TUTOR": t_sel})
                    st.rerun()

# 5. MÓDULO PRONTUÁRIO: TELA DIVIDIDA COM HISTÓRICO
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    
    idx_p = 0
    if st.session_state['pet_selecionado'] in lista:
        idx_p = lista.index(st.session_state['pet_selecionado']) + 1
    
    p_atual = st.selectbox("Paciente:", ["--- Selecione ---"] + lista, index=idx_p)
    
    if p_atual != "--- Selecione ---":
        c_at, c_hi = st.columns([2, 1])
        with c_at:
            with st.form("f_clinico"):
                peso = st.text_input("Peso (kg)")
                texto = st.text_area("Anamnese", height=300)
                if st.form_submit_button("💾 Finalizar"):
                    st.session_state['historico'].append({"DATA": datetime.now().strftime("%d/%m/%Y %H:%M"), "PACIENTE": p_atual, "RELATO": texto, "PESO": peso})
                    st.session_state['pet_selecionado'] = None
                    st.rerun()
        with c_hi:
            st.write("### 📜 Histórico Pet")
            h_pet = [h for h in st.session_state['historico'] if h['PACIENTE'] == p_atual]
            for h in reversed(h_pet):
                with st.expander(f"📅 {h['DATA']}"):
                    st.write(f"**Peso:** {h['PESO']}kg\n\n{h['RELATO']}")
