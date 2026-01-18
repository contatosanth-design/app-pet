import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. NÚCLEO E ESTABILIDADE
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'historico', 'financeiro']:
    if k not in st.session_state: st.session_state[k] = []

if 'fluxo' not in st.session_state:
    st.session_state['fluxo'] = {"aba": "👤 Tutores", "tutor": None, "pet": None}

# 2. NAVEGAÇÃO SEM ERROS
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    # Proteção contra KeyError no índice
    aba_atual = st.session_state['fluxo']['aba']
    idx_menu = opcoes.index(aba_atual) if aba_atual in opcoes else 0
    menu = st.radio("NAVEGAÇÃO", opcoes, index=idx_menu, key="nav_final")
    st.session_state['fluxo']['aba'] = menu

# --- MÓDULO 1: TUTORES (Com Endereço e E-mail)
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes (Tutores)")
    nomes_db = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    busca = st.selectbox("🔍 Selecionar ou Buscar:", ["--- Novo Cadastro ---"] + nomes_db)

    v_nome, v_tel, v_email, v_cpf, v_end = ("", "", "", "", "")
    if busca != "--- Novo Cadastro ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == busca)
        v_nome, v_tel, v_email, v_cpf, v_end = c['NOME'], c['TEL'], c.get('EMAIL', ""), c['CPF'], c.get('END', "")
        
        if st.button(f"➡️ Ir para Pets de {v_nome}"):
            st.session_state['fluxo'].update({"aba": "🐾 Pets", "tutor": v_nome})
            st.rerun()

    with st.form("form_tutor_v7"):
        col1, col2 = st.columns([2, 1])
        f_nome = col1.text_input("Nome Completo *", value=v_nome).upper()
        f_tel = col2.text_input("WhatsApp", value=v_tel)
        
        c3, c4 = st.columns(2)
        f_email = c3.text_input("E-mail (Obrigatório) *", value=v_email).lower()
        f_cpf = c4.text_input("CPF/CNPJ", value=v_cpf)
        
        # Campo de Endereço essencial para localização
        f_end = st.text_area("Endereço Completo (Rua, Nº, Bairro, Cidade) *", value=v_end)
        
        if st.form_submit_button("💾 Salvar/Atualizar Dados"):
            if f_nome and f_email and f_end:
                dados = {"NOME": f_nome, "TEL": f_tel, "EMAIL": f_email, "CPF": f_cpf, "END": f_end}
                if busca == "--- Novo Cadastro ---":
                    st.session_state['clientes'].append(dados)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == busca: st.session_state['clientes'][i] = dados
                st.rerun()
            else:
                st.error("Nome, E-mail e Endereço são obrigatórios para o cadastro.")

# --- MÓDULO 2: PETS (Raça Fixa)
elif menu == "🐾 Pets":
    st.subheader("🐾 Pacientes e Raças")
    tutores = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    idx_t = (tutores.index(st.session_state['fluxo']['tutor']) + 1) if st.session_state['fluxo']['tutor'] in tutores else 0
    t_sel = st.selectbox("Tutor Responsável:", ["--- Selecione ---"] + tutores, index=idx_t)

    if t_sel != "--- Selecione ---":
        meus_pets = [p for p in st.session_state['pets'] if p['TUTOR'] == t_sel]
        for p in meus_pets:
            ci, ca = st.columns([4, 1])
            ci.info(f"🐕 **{p['PET']}** ({p['ESP']} - {p['RAÇA']})")
            if ca.button(f"🩺 Atender", key=f"btn_{p['PET']}"):
                st.session_state['fluxo'].update({"aba": "📋 Prontuário", "pet": f"{p['PET']} (Tutor: {t_sel})"})
                st.rerun()
        
        with st.expander("➕ Cadastrar Novo Pet para este Tutor"):
            with st.form("form_pet_v7"):
                c1, c2 = st.columns(2)
                np = c1.text_input("Nome do Pet *").upper()
                ep = c2.selectbox("Espécie", ["Cão", "Gato", "Outro"])
                rp = st.text_input("Raça *").upper()
                if st.form_submit_button("💾 Salvar Pet"):
                    if np and rp:
                        st.session_state['pets'].append({"PET": np, "ESP": ep, "RAÇA": rp, "TUTOR": t_sel})
                        st.rerun()

# --- MÓDULO 3: PRONTUÁRIO (Histórico Dual)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    idx_p = (p_lista.index(st.session_state['fluxo']['pet']) + 1) if st.session_state['fluxo']['pet'] in p_lista else 0
    p_foco = st.selectbox("Paciente em Atendimento:", ["--- Selecione ---"] + p_lista, index=idx_p)

    if p_foco != "--- Selecione ---":
        c_at, c_hi = st.columns([2, 1])
        with c_at:
            with st.form("f_atend"):
                anamnese = st.text_area("Anamnese e Conduta:", height=300)
                aviso = st.date_input("Lembrete de Vacina/Retorno", value=datetime.now() + timedelta(days=21))
                if st.form_submit_button("💾 Salvar Consulta"):
                    st.session_state['historico'].append({
                        "DATA": datetime.now().strftime("%d/%m/%Y %H:%M"), "PACIENTE": p_foco,
                        "RELATO": anamnese, "RETORNO": aviso.strftime("%d/%m/%Y")
                    })
                    st.session_state['fluxo']['pet'] = None
                    st.rerun()
        with c_hi:
            st.markdown("### 📜 Histórico")
            h_filtrado = [h for h in st.session_state['historico'] if h['PACIENTE'] == p_foco]
            for h in reversed(h_filtrado):
                with st.expander(f"📅 {h['DATA']}"):
                    st.write(h['RELATO'])
                    st.info(f"🔔 Retorno: {h['RETORNO']}")
