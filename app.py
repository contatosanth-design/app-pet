import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO E MEMÓRIA CENTRAL (Persistência de Dados)
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'historico', 'financeiro']:
    if k not in st.session_state: st.session_state[k] = []

# Variáveis de Fluxo para Navegação sem Cliques Extras
if 'fluxo' not in st.session_state: 
    st.session_state['fluxo'] = {"pagina": "👤 Tutores", "tutor": None, "pet": None}

# 2. BARRA LATERAL (Controle de Navegação)
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    # Sincroniza o menu com o fluxo automático
    idx = opcoes.index(st.session_state['fluxo']['pagina'])
    menu = st.radio("NAVEGAÇÃO", opcoes, index=idx)
    st.session_state['fluxo']['pagina'] = menu

# --- MÓDULOS ---

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. PARAMETROS DE MEMÓRIA E PERSISTÊNCIA
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'historico', 'financeiro']:
    if k not in st.session_state: st.session_state[k] = []

# Variáveis de Controle de Fluxo (Evita a "Tela Branca")
if 'sessao' not in st.session_state: 
    st.session_state['sessao'] = {"aba": "👤 Tutores", "tutor": None, "pet": None}

# 2. NAVEGAÇÃO INTEGRADA (Menu Lateral)
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes_menu = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    idx_menu = opcoes_menu.index(st.session_state['sessao']['aba'])
    menu = st.radio("NAVEGAÇÃO", opcoes_menu, index=idx_menu)
    st.session_state['sessao']['aba'] = menu

# --- MÓDULOS REVISADOS ---

# MÓDULO 1: TUTORES (Com E-mail e Atalho Direto)
if menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    nomes_db = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    selecao = st.selectbox("🔍 Buscar Tutor:", ["--- Novo Cadastro ---"] + nomes_db)

    v_nome, v_tel, v_email, v_cpf, v_end = ("", "", "", "", "")
    
    if selecao != "--- Novo Cadastro ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == selecao)
        v_nome, v_tel, v_email, v_cpf, v_end = c['NOME'], c['TEL'], c.get('EMAIL', ""), c['CPF'], c.get('END', "")
        
        st.success(f"✅ Cadastro de {selecao} pronto.")
        if st.button(f"➡️ Ver Pets de {selecao}"):
            st.session_state['sessao'].update({"aba": "🐾 Pets", "tutor": selecao})
            st.rerun()

    with st.form("f_tutor_final"):
        c1, c2 = st.columns([2, 2])
        f_nome = c1.text_input("Nome Completo *", value=v_nome).upper()
        f_tel = c2.text_input("WhatsApp", value=v_tel)
        # O CAMPO CRÍTICO: E-mail obrigatório para o fluxo
        f_email = st.text_input("E-mail para Recibos/Vacinas *", value=v_email).lower()
        c3, c4 = st.columns(2)
        f_cpf = c3.text_input("CPF/CNPJ", value=v_cpf)
        f_end = c4.text_input("Endereço", value=v_end)
        
        if st.form_submit_button("💾 Salvar/Atualizar Cadastro"):
            if f_nome and f_email:
                novo_dado = {"NOME": f_nome, "TEL": f_tel, "EMAIL": f_email, "CPF": f_cpf, "END": f_end}
                if selecao == "--- Novo Cadastro ---":
                    st.session_state['clientes'].append(novo_dado)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == selecao: st.session_state['clientes'][i] = novo_dado
                st.rerun()
            else:
                st.error("Nome e E-mail são campos obrigatórios.")

# MÓDULO 2: PETS (Fixação da Raça e Espécie)
elif menu == "🐾 Pets":
    st.subheader("🐾 Central do Paciente")
    lista_t = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    
    idx_t = 0
    if st.session_state['sessao']['tutor'] in lista_t:
        idx_t = lista_t.index(st.session_state['sessao']['tutor']) + 1

    t_foco = st.selectbox("Selecione o Tutor:", ["--- Escolha ---"] + lista_t, index=idx_t)

    if t_foco != "--- Escolha ---":
        pets_t = [p for p in st.session_state['pets'] if p['TUTOR'] == t_foco]
        if pets_t:
            for p in pets_t:
                col_p, col_b = st.columns([4, 1])
                col_p.info(f"🐶 **{p['PET']}** ({p['ESP']} - {p['RAÇA']})")
                if col_b.button(f"🩺 Atender", key=f"btn_{p['PET']}"):
                    st.session_state['sessao'].update({"aba": "📋 Prontuário", "pet": f"{p['PET']} (Tutor: {t_foco})"})
                    st.rerun()
        
        with st.expander("➕ Novo Animal"):
            with st.form("f_pet_final"):
                c1, c2 = st.columns(2)
                np = c1.text_input("Nome do Animal *").upper()
                ep = c2.selectbox("Espécie", ["Cão", "Gato", "Outro"])
                # Raça corrigida para não desaparecer
                rp = st.text_input("Raça (Ex: Bulldog, SRD) *").upper()
                if st.form_submit_button("💾 Salvar Animal"):
                    if np and rp:
                        st.session_state['pets'].append({"PET": np, "ESP": ep, "RAÇA": rp, "TUTOR": t_foco})
                        st.rerun()

# MÓDULO 3: PRONTUÁRIO (Anamnese + Histórico + Lembretes)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    
    idx_p = 0
    if st.session_state['sessao']['pet'] in p_lista:
        idx_p = p_lista.index(st.session_state['sessao']['pet']) + 1

    paciente = st.selectbox("Paciente em Atendimento:", ["--- Selecione ---"] + p_lista, index=idx_p)

    if paciente != "--- Selecione ---":
        col_at, col_hi = st.columns([2, 1])
        
        with col_at:
            with st.form("f_atendimento_final"):
                st.markdown("### 📝 Evolução Atual")
                c1, c2 = st.columns(2)
                peso = c1.text_input("Peso (kg)")
                temp = c2.text_input("Temperatura (°C)")
                relato = st.text_area("Relato da Consulta / Prescrição:", height=250)
                aviso = st.date_input("Próximo Lembrete (Vacina/Retorno)", value=datetime.now() + timedelta(days=21))
                
                if st.form_submit_button("💾 Salvar e Finalizar"):
                    st.session_state['historico'].append({
                        "DATA": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "PACIENTE": paciente, "PESO": peso, "TEMP": temp, 
                        "RELATO": relato, "RETORNO": aviso.strftime("%d/%m/%Y")
                    })
                    st.session_state['sessao']['pet'] = None
                    st.success("Prontuário salvo!")
                    st.rerun()

        with col_hist:
            st.markdown("### 📜 Histórico Lado a Lado")
            h_pet = [h for h in st.session_state['historico'] if h['PACIENTE'] == paciente]
            for h in reversed(h_pet):
                with st.expander(f"📅 {h['DATA']} - {h['PESO']}kg"):
                    st.write(h['RELATO'])
                    st.info(f"🔔 Retorno em: {h['RETORNO']}")
# MÓDULO 2: GESTÃO DE PETS (Raças e Histórico Rápido)
elif menu == "🐾 Pets":
    st.subheader("🐾 Central do Paciente")
    tutores_disp = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    
    # Auto-seleção vinda do Módulo 1
    idx_t = 0
    if st.session_state['fluxo']['tutor'] in tutores_disp:
        idx_t = tutores_disp.index(st.session_state['fluxo']['tutor']) + 1

    tutor_sel = st.selectbox("Tutor Responsável:", ["--- Selecione ---"] + tutores_disp, index=idx_t)

    if tutor_sel != "--- Selecione ---":
        st.info(f"📋 Animais cadastrados para {tutor_sel}:")
        meus_pets = [p for p in st.session_state['pets'] if p['TUTOR'] == tutor_sel]
        
        for p in meus_pets:
            col_info, col_btn = st.columns([4, 1])
            # Exibição clara da Raça (o item que desaparecia)
            col_info.warning(f"🐕 **{p['PET']}** | Espécie: {p['ESP']} | Raça: {p['RAÇA']}")
            if col_btn.button(f"🩺 Atender {p['PET']}", key=f"at_{p['PET']}"):
                st.session_state['fluxo'].update({"pagina": "📋 Prontuário", "pet": f"{p['PET']} (Tutor: {tutor_sel})"})
                st.rerun()

        with st.expander("➕ Cadastrar Novo Animal para este Tutor"):
            with st.form("f_novo_pet"):
                c1, c2 = st.columns(2)
                n_p = c1.text_input("Nome do Pet *").upper()
                esp_p = c2.selectbox("Espécie", ["Cão", "Gato", "Outro"])
                r_p = st.text_input("Raça * (Obrigatório)").upper() # Fixado
                nasc_p = st.text_input("Data Nascimento/Idade")
                if st.form_submit_button("💾 Salvar Pet"):
                    if n_p and r_p:
                        st.session_state['pets'].append({"PET": n_p, "ESP": esp_p, "RAÇA": r_p, "TUTOR": tutor_sel, "NASC": nasc_p})
                        st.rerun()

# MÓDULO 3: PRONTUÁRIO E REVISÃO (Histórico Lado a Lado)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento e Histórico")
    lista_completa = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    
    idx_p = 0
    if st.session_state['fluxo']['pet'] in lista_completa:
        idx_p = lista_completa.index(st.session_state['fluxo']['pet']) + 1

    p_atual = st.selectbox("Selecione o Paciente:", ["--- Selecione ---"] + lista_completa, index=idx_p)

    if p_atual != "--- Selecione ---":
        col_form, col_hist = st.columns([2, 1])
        
        with col_form:
            st.markdown("### ✍️ Evolução do Caso")
            with st.form("f_atendimento"):
                c1, c2 = st.columns(2)
                peso = c1.text_input("Peso (kg)")
                temp = c2.text_input("Temp (°C)")
                anamnese = st.text_area("Descrição Clínica / Vacinas / Exames:", height=300)
                # Lembrete de Retorno/Vacina
                retorno = st.date_input("Previsão de Retorno/Vacinação", value=datetime.now() + timedelta(days=15))
                
                if st.form_submit_button("💾 Finalizar Atendimento"):
                    st.session_state['historico'].append({
                        "DATA": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "PACIENTE": p_atual, "PESO": peso, "TEMP": temp, 
                        "RELATO": anamnese, "RETORNO": retorno.strftime("%d/%m/%Y")
                    })
                    st.session_state['fluxo']['pet'] = None # Limpa para o próximo
                    st.success("Atendimento salvo com sucesso!")
                    st.rerun()

        with col_hist:
            st.markdown("### 📜 Passado Médico")
            h_filtrado = [h for h in st.session_state['historico'] if h['PACIENTE'] == p_atual]
            if h_filtrado:
                for h in reversed(h_filtrado):
                    with st.expander(f"📅 {h['DATA']} (Peso: {h['PESO']}kg)"):
                        st.write(f"**Relato:** {h['RELATO']}")
                        st.write(f"**📍 Retorno previsto:** {h.get('RETORNO', 'N/D')}")
            else:
                st.info("Nenhum histórico encontrado.")
