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

# MÓDULO 1: GESTÃO DE TUTORES (Carregamento Automático)
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    nomes_cadastrados = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    busca = st.selectbox("🔍 Selecionar ou Buscar:", ["--- Novo Cadastro ---"] + nomes_cadastrados)

    # Lógica de preenchimento inteligente
    v_nome, v_tel, v_cpf, v_end = ("", "", "", "")
    if busca != "--- Novo Cadastro ---":
        dados = next(c for c in st.session_state['clientes'] if c['NOME'] == busca)
        v_nome, v_tel, v_cpf, v_end = dados['NOME'], dados['TEL'], dados['CPF'], dados.get('END', "")
        
        # ATALHO DE FLUXO: Encontrou? Já oferece o próximo passo.
        st.success(f"✅ Cadastro localizado. Deseja prosseguir?")
        if st.button(f"➡️ Ir para Animais de {v_nome}"):
            st.session_state['fluxo'].update({"pagina": "🐾 Pets", "tutor": v_nome})
            st.rerun()

    with st.form("form_tutor"):
        c1, c2 = st.columns([3, 1])
        f_nome = c1.text_input("Nome Completo *", value=v_nome).upper()
        f_tel = c2.text_input("WhatsApp", value=v_tel)
        f_cpf = st.text_input("CPF", value=v_cpf)
        f_end = st.text_input("Endereço", value=v_end)
        
        if st.form_submit_button("💾 Salvar/Atualizar Dados"):
            if f_nome:
                # Se for novo, adiciona; se existir, atualiza.
                if busca == "--- Novo Cadastro ---":
                    st.session_state['clientes'].append({"NOME": f_nome, "TEL": f_tel, "CPF": f_cpf, "END": f_end})
                else:
                    for c in st.session_state['clientes']:
                        if c['NOME'] == busca: c.update({"NOME": f_nome, "TEL": f_tel, "CPF": f_cpf, "END": f_end})
                st.rerun()

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
