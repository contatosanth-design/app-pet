import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO E MEMÓRIA VOLÁTIL
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicialização de dados para evitar telas brancas
for k in ['clientes', 'pets', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

# Controle de estado para navegação direta entre telas
if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"
if 'tutor_selecionado' not in st.session_state: st.session_state.tutor_selecionado = None
if 'pet_selecionado' not in st.session_state: st.session_state.pet_selecionado = None

# 2. MENU LATERAL SINCRONIZADO
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    idx_menu = opcoes.index(st.session_state.aba_atual)
    escolha = st.radio("NAVEGAÇÃO", opcoes, index=idx_menu, key="nav_principal")
    
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- MÓDULOS ---

# ABA TUTORES: Onde incluímos o TELEFONE e ENDEREÇO
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    nomes_existentes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    busca = st.selectbox("Selecione para Editar ou Criar Novo:", ["--- Novo Cadastro ---"] + nomes_existentes)

    # Preenchimento para edição
    v_nome, v_tel, v_email, v_end = ("", "", "", "")
    if busca != "--- Novo Cadastro ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == busca)
        v_nome, v_tel, v_email, v_end = c['NOME'], c.get('TEL', ""), c.get('EMAIL', ""), c.get('END', "")
        
        # BOTÃO "IR PARA PETS" CORRIGIDO
        if st.button(f"➡️ Ver Animais de {v_nome}"):
            st.session_state.tutor_selecionado = v_nome
            st.session_state.aba_atual = "🐾 Pets"
            st.rerun()

    with st.form("f_tutor_final"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        col1, col2 = st.columns(2)
        # AQUI ESTÁ O TELEFONE QUE O SENHOR PRECISAVA
        f_tel = col1.text_input("WhatsApp / Telefone", value=v_tel)
        f_email = col2.text_input("E-mail (Para Lembretes) *", value=v_email).lower()
        f_end = st.text_area("Endereço Completo *", value=v_end)
        
        if st.form_submit_button("💾 Salvar Cliente"):
            if f_nome and f_email and f_end:
                dados_cli = {"NOME": f_nome, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if busca == "--- Novo Cadastro ---":
                    st.session_state['clientes'].append(dados_cli)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == busca: st.session_state['clientes'][i] = dados_cli
                st.rerun()
            else:
                st.warning("Por favor, preencha Nome, E-mail e Endereço.")

# ABA PETS: Com Raça fixa e Botão Atender
elif st.session_state.aba_atual == "🐾 Pets":
    st.subheader("🐾 Pacientes e Raças")
    tuts = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    idx_t = (tuts.index(st.session_state.tutor_selecionado) + 1) if st.session_state.tutor_selecionado in tuts else 0
    t_foco = st.selectbox("Tutor Responsável:", ["--- Selecione ---"] + tuts, index=idx_t)

    if t_foco != "--- Selecione ---":
        pets_tutor = [p for p in st.session_state['pets'] if p['TUTOR'] == t_foco]
        for p in pets_tutor:
            c_info, c_btn = st.columns([4, 1])
            c_info.info(f"🐕 **{p['PET']}** (Raça: {p['RAÇA']})")
            # BOTÃO ATENDER CORRIGIDO
            if c_btn.button(f"🩺 Atender", key=f"at_{p['PET']}"):
                st.session_state.pet_selecionado = f"{p['PET']} (Tutor: {t_foco})"
                st.session_state.aba_atual = "📋 Prontuário"
                st.rerun()
        
        with st.expander("➕ Novo Animal"):
            with st.form("f_pet_final"):
                col_p1, col_p2 = st.columns(2)
                n_p = col_p1.text_input("Nome do Pet").upper()
                r_p = col_p2.text_input("Raça *").upper() #
                if st.form_submit_button("💾 Salvar Pet"):
                    if n_p and r_p:
                        st.session_state['pets'].append({"PET": n_p, "RAÇA": r_p, "TUTOR": t_foco})
                        st.rerun()

# ABA PRONTUÁRIO: Registro e Histórico Lado a Lado
elif st.session_state.aba_atual == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    idx_p = (p_lista.index(st.session_state.pet_selecionado) + 1) if st.session_state.pet_selecionado in p_lista else 0
    paciente = st.selectbox("Paciente:", ["--- Selecione ---"] + p_lista, index=idx_p)

    if paciente != "--- Selecione ---":
        c_at, c_hi = st.columns([2, 1])
        with c_at:
            with st.form("f_consulta"):
                relato = st.text_area("Anamnese / Conduta:", height=300)
                if st.form_submit_button("💾 Finalizar"):
                    st.session_state['historico'].append({
                        "DATA": datetime.now().strftime("%d/%m/%Y"), "PACIENTE": paciente, "TEXTO": relato
                    })
                    st.success("Atendimento salvo!")
                    st.rerun()
        with c_hi:
            st.write("### 📜 Histórico")
            h_filtrado = [h for h in st.session_state['historico'] if h['PACIENTE'] == paciente]
            for h in reversed(h_filtrado):
                with st.expander(f"📅 {h['DATA']}"):
                    st.write(h['TEXTO'])
