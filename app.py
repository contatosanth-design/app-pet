import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. NÚCLEO DE DADOS E CONFIGURAÇÃO
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicialização de listas fundamentais
for k in ['clientes', 'pets', 'historico', 'financeiro']:
    if k not in st.session_state: st.session_state[k] = []

# Controle de Fluxo para evitar erros de navegação
if 'fluxo' not in st.session_state:
    st.session_state['fluxo'] = {"aba": "👤 Tutores", "tutor": None, "pet": None}

# 2. MENU LATERAL SINCRONIZADO
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    # Garante que o rádio acompanhe a aba ativa no fluxo
    aba_idx = opcoes.index(st.session_state['fluxo']['aba'])
    menu = st.radio("NAVEGAÇÃO", opcoes, index=aba_idx, key="nav_vet")
    st.session_state['fluxo']['aba'] = menu

# --- MÓDULOS INTEGRADOS ---

# MÓDULO 1: TUTORES (Campo E-mail obrigatório para envios)
if menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    nomes_db = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    selecao = st.selectbox("⚡ Selecionar Tutor:", ["--- Novo Cadastro ---"] + nomes_db)

    # Preenchimento automático de campos existentes
    v_nome, v_tel, v_email, v_cpf, v_end = ("", "", "", "", "")
    if selecao != "--- Novo Cadastro ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == selecao)
        v_nome, v_tel, v_email, v_cpf, v_end = c['NOME'], c['TEL'], c.get('EMAIL', ""), c['CPF'], c.get('END', "")
        
        # Atalho direto para otimizar o atendimento
        if st.button(f"➡️ Ver Animais de {v_nome}"):
            st.session_state['fluxo'].update({"aba": "🐾 Pets", "tutor": v_nome})
            st.rerun()

    with st.form("form_tutor_final"):
        col1, col2 = st.columns([2, 1])
        f_nome = col1.text_input("Nome Completo *", value=v_nome).upper()
        f_tel = col2.text_input("WhatsApp", value=v_tel)
        # Fixação do E-mail como parâmetro essencial
        f_email = st.text_input("E-mail (Lembretes/Vacinas) *", value=v_email).lower()
        f_cpf = st.text_input("CPF/CNPJ", value=v_cpf)
        f_end = st.text_input("Endereço Completo", value=v_end)
        
        if st.form_submit_button("💾 Salvar/Atualizar Cadastro"):
            if f_nome and f_email:
                dados_cli = {"NOME": f_nome, "TEL": f_tel, "EMAIL": f_email, "CPF": f_cpf, "END": f_end}
                if selecao == "--- Novo Cadastro ---":
                    st.session_state['clientes'].append(dados_cli)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == selecao: st.session_state['clientes'][i] = dados_cli
                st.rerun()
            else:
                st.error("Campos Nome e E-mail são obrigatórios.")

# MÓDULO 2: PETS (Raça visível e persistente)
elif menu == "🐾 Pets":
    st.subheader("🐾 Pacientes")
    tuts = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    idx_t = (tuts.index(st.session_state['fluxo']['tutor']) + 1) if st.session_state['fluxo']['tutor'] in tuts else 0
    tutor_foco = st.selectbox("Selecione o Tutor:", ["--- Escolha ---"] + tuts, index=idx_t)

    if tutor_foco != "--- Escolha ---":
        # Listagem de pets com detalhamento de raça
        pets_do_tutor = [p for p in st.session_state['pets'] if p['TUTOR'] == tutor_foco]
        for p in pets_do_tutor:
            cp, ca = st.columns([4, 1])
            cp.info(f"🐶 **{p['PET']}** ({p['ESP']} - {p['RAÇA']})")
            if ca.button(f"🩺 Atender", key=f"at_{p['PET']}"):
                st.session_state['fluxo'].update({"aba": "📋 Prontuário", "pet": f"{p['PET']} (Tutor: {tutor_foco})"})
                st.rerun()
        
        with st.expander("➕ Adicionar Novo Animal"):
            with st.form("form_pet_final"):
                c_p1, c_p2 = st.columns(2)
                n_pet = c_p1.text_input("Nome do Animal *").upper()
                e_pet = c_p2.selectbox("Espécie", ["Cão", "Gato", "Outro"])
                # Raça protegida contra desaparecimento
                r_pet = st.text_input("Raça (Ex: SRD, Poodle) *").upper()
                n_pet_idade = st.text_input("Data de Nascimento / Idade")
                if st.form_submit_button("💾 Salvar Pet"):
                    if n_pet and r_pet:
                        st.session_state['pets'].append({"PET": n_pet, "ESP": e_pet, "RAÇA": r_pet, "TUTOR": tutor_foco, "NASC": n_pet_idade})
                        st.rerun()

# MÓDULO 3: PRONTUÁRIO (Anamnese + Histórico Lateral)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    idx_p = (p_lista.index(st.session_state['fluxo']['pet']) + 1) if st.session_state['fluxo']['pet'] in p_lista else 0
    paciente_foco = st.selectbox("Paciente:", ["--- Selecione ---"] + p_lista, index=idx_p)

    if paciente_foco != "--- Selecione ---":
        col_registro, col_historico = st.columns([2, 1])
        with col_registro:
            with st.form("form_atend_final"):
                st.markdown("### 📝 Evolução do Atendimento")
                ca1, ca2 = st.columns(2)
                peso, temp = ca1.text_input("Peso (kg)"), ca2.text_input("Temp (°C)")
                anamnese = st.text_area("Descrição Clínica / Conduta / Vacinas:", height=300)
                proximo = st.date_input("Previsão de Retorno / Vacinação", value=datetime.now() + timedelta(days=21))
                if st.form_submit_button("💾 Salvar e Finalizar"):
                    st.session_state['historico'].append({
                        "DATA": datetime.now().strftime("%d/%m/%Y %H:%M"), "PACIENTE": paciente_foco,
                        "PESO": peso, "TEMP": temp, "RELATO": anamnese, "RETORNO": proximo.strftime("%d/%m/%Y")
                    })
                    st.session_state['fluxo']['pet'] = None
                    st.rerun()
        with col_historico:
            st.markdown("### 📜 Histórico Passado")
            h_filtrado = [h for h in st.session_state['historico'] if h['PACIENTE'] == paciente_foco]
            for h in reversed(h_filtrado):
                with st.expander(f"📅 {h['DATA']} (Peso: {h['PESO']}kg)"):
                    st.write(f"**Relato:** {h['RELATO']}")
                    st.info(f"🔔 Retorno agendado: {h['RETORNO']}")
