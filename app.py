import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. ESTABILIDADE DO SISTEMA
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicialização de banco de dados e fluxos para evitar telas brancas
for k in ['clientes', 'pets', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_ativa' not in st.session_state: st.session_state.aba_ativa = "👤 Tutores"
if 'tutor_foco' not in st.session_state: st.session_state.tutor_foco = None
if 'pet_foco' not in st.session_state: st.session_state.pet_foco = None

# 2. MENU LATERAL SEM DUPLICIDADE
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    aba_idx = opcoes.index(st.session_state.aba_ativa)
    escolha = st.radio("NAVEGAÇÃO", opcoes, index=aba_idx, key="nav_v81")
    
    if escolha != st.session_state.aba_ativa:
        st.session_state.aba_ativa = escolha
        st.rerun()

# --- 3. MÓDULOS ---

# ABA TUTORES: Recupera WhatsApp e Endereço
if st.session_state.aba_ativa == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes (Tutores)")
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    tutor_sel = st.selectbox("Buscar ou Novo:", ["--- Novo ---"] + nomes)

    v_nome, v_tel, v_email, v_end = ("", "", "", "")
    if tutor_sel != "--- Novo ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == tutor_sel)
        v_nome, v_tel, v_email, v_end = c['NOME'], c.get('TEL', ""), c.get('EMAIL', ""), c.get('END', "")
        
        if st.button(f"➡️ Ver Pets de {v_nome}"):
            st.session_state.tutor_foco = v_nome
            st.session_state.aba_ativa = "🐾 Pets"
            st.rerun()

    with st.form("f_tutor_v81"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        col1, col2 = st.columns(2)
        f_tel = col1.text_input("WhatsApp / Telefone", value=v_tel)
        f_email = col2.text_input("E-mail (Obrigatório) *", value=v_email).lower()
        f_end = st.text_area("Endereço Completo *", value=v_end)
        
        if st.form_submit_button("💾 Salvar Cliente"):
            if f_nome and f_email and f_end:
                novo_dado = {"NOME": f_nome, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if tutor_sel == "--- Novo ---":
                    st.session_state['clientes'].append(novo_dado)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == tutor_sel: st.session_state['clientes'][i] = novo_dado
                st.rerun()

# ABA PETS: Exibe Raças e corrige o Atender
elif st.session_state.aba_ativa == "🐾 Pets":
    st.subheader("🐾 Pacientes e Raças")
    t_lista = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    idx_t = (t_lista.index(st.session_state.tutor_foco) + 1) if st.session_state.tutor_foco in t_lista else 0
    foco = st.selectbox("Selecione o Tutor:", ["--- Selecione ---"] + t_lista, index=idx_t)

    if foco != "--- Selecione ---":
        pets = [p for p in st.session_state['pets'] if p['TUTOR'] == foco]
        for p in pets:
            c1, c2 = st.columns([4, 1])
            # Raça agora visível e protegida
            c1.info(f"🐕 **{p['PET']}** | Raça: **{p['RAÇA']}** | Idade: {p.get('NASC', 'N/I')}")
            if c2.button(f"🩺 Atender", key=f"btn_{p['PET']}"):
                st.session_state.pet_foco = f"{p['PET']} (Tutor: {foco})"
                st.session_state.aba_ativa = "📋 Prontuário"
                st.rerun()
        
        with st.expander("➕ Cadastrar Novo Animal"):
            with st.form("f_pet_v81"):
                n_p = st.text_input("Nome do Pet *").upper()
                r_p = st.text_input("Raça (Ex: Poodle, SRD) *").upper()
                nasc = st.text_input("Idade/Nascimento", value="18/01/2026")
                if st.form_submit_button("💾 Salvar Pet"):
                    if n_p and r_p:
                        st.session_state['pets'].append({"PET": n_p, "RAÇA": r_p, "TUTOR": foco, "NASC": nasc})
                        st.rerun()

# ABA PRONTUÁRIO: Finaliza e limpa o foco
elif st.session_state.aba_ativa == "📋 Prontuário":
    st.subheader("📋 Prontuário Médico")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    idx_p = (p_lista.index(st.session_state.pet_foco) + 1) if st.session_state.pet_foco in p_lista else 0
    paciente = st.selectbox("Paciente:", ["--- Selecione ---"] + p_lista, index=idx_p)

    if paciente != "--- Selecione ---":
        col_reg, col_his = st.columns([2, 1])
        with col_reg:
            with st.form("f_atend_v81"):
                anamnese = st.text_area("Anamnese e Evolução:", height=300)
                if st.form_submit_button("💾 Finalizar Consulta"):
                    st.session_state['historico'].append({
                        "DATA": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "PACIENTE": paciente, "TEXTO": anamnese
                    })
                    st.session_state.pet_foco = None
                    st.session_state.aba_ativa = "👤 Tutores"
                    st.rer
