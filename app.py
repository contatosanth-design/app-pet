import streamlit as st
from datetime import datetime

# 1. CONFIGURAÇÃO INICIAL E MEMÓRIA
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicializa as listas de dados se estiverem vazias
for k in ['clientes', 'pets', 'historico', 'caixa']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"
if 'tutor_foco' not in st.session_state: st.session_state.tutor_foco = None
if 'pet_foco' not in st.session_state: st.session_state.pet_foco = None

# --- 2. MENU LATERAL ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    idx = opcoes.index(st.session_state.aba_atual)
    escolha = st.radio("NAVEGAÇÃO", opcoes, index=idx)
    
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- 3. MÓDULO TUTORES (COM CPF) ---
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes (Tutores)")
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    t_sel = st.selectbox("Buscar ou Novo:", ["--- Novo ---"] + nomes)

    v_nome, v_cpf, v_tel, v_email, v_end = ("", "", "", "", "")
    if t_sel != "--- Novo ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == t_sel)
        v_nome, v_cpf, v_tel, v_email, v_end = c.get('NOME',''), c.get('CPF',''), c.get('TEL',''), c.get('EMAIL',''), c.get('END','')
        if st.button(f"➡️ Ver Animais de {v_nome}"):
            st.session_state.tutor_foco = v_nome
            st.session_state.aba_atual = "🐾 Pets"
            st.rerun()

    with st.form("form_tutor_v92"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        f_cpf = st.text_input("CPF (Para Recibos)", value=v_cpf)
        col1, col2 = st.columns(2)
        f_tel = col1.text_input("WhatsApp / Telefone", value=v_tel)
        f_email = col2.text_input("E-mail (Obrigatório) *", value=v_email).lower()
        f_end = st.text_area("Endereço Completo *", value=v_end)
        if st.form_submit_button("💾 Salvar Cliente"):
            if f_nome and f_email:
                dados = {"NOME": f_nome, "CPF": f_cpf, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if t_sel == "--- Novo ---": st.session_state['clientes'].append(dados)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == t_sel: st.session_state['clientes'][i] = dados
                st.rerun()

# --- 4. MÓDULO PETS (RAÇAS E IDADE) ---
elif st.session_state.aba_atual == "🐾 Pets":
    st.subheader("🐾 Pacientes e Raças")
    racas = sorted(["SRD (Cão)", "SRD (Gato)", "Poodle", "Pinscher", "Shih Tzu", "Yorkshire", "Golden Retriever", "Border Collie", "Persa", "Siamês"])
    tuts = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    idx_t = (tuts.index(st.session_state.tutor_foco) + 1) if st.session_state.tutor_foco in tuts else 0
    tutor_f = st.selectbox("Tutor Responsável:", ["--- Selecione ---"] + tuts, index=idx_t)

    if tutor_f != "--- Selecione ---":
        for p in [p for p in st.session_state['pets'] if p['TUTOR'] == tutor_f]:
            c1, c2 = st.columns([4, 1])
            c1.info(f"🐕 **{p['PET']}** | Raça: **{p['RAÇA']}** | Idade: **{p.get('IDADE', 'N/I')}**")
            if c2.button(f"🩺 Atender", key=f"at_{p['PET']}"):
                st.session_state.pet_foco = f"{p['PET']} (Tutor: {tutor_f})"
                st.session_state.aba_atual = "📋 Prontuário"
                st.rerun()
        with st.expander("➕ Cadastrar Novo Animal"):
            with st.form("form_pet_v92"):
                n_p = st.text_input("Nome do Pet *").upper()
                r_p = st.selectbox("Raça:", ["Outra"] + racas)
                if r_p == "Outra": r_p = st.text_input("Qual raça?").upper()
                i_p = st.text_input("Idade ou Nascimento (Ex: 18/01/2020)")
                if st.form_submit_button("💾 Salvar Pet"):
                    if n_p:
                        st.session_state['pets'].append({"PET": n_p, "RAÇA": r_p, "TUTOR": tutor_f, "IDADE": i_p})
                        st.rerun()

# --- 5. MÓDULO PRONTUÁRIO ---
elif st.session_state.aba_atual == "📋 Prontuário":
    st.subheader("📋 Prontuário Médico")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    idx_p = (p_lista.index(st.session_state.pet_foco) + 1) if st.session_state.pet_foco in p_lista else 0
    paciente = st.selectbox("Paciente:", ["--- Selecione ---"] + p_lista, index=idx_p)
    if paciente != "--- Selecione ---":
        with st.form("form_pront_v92"):
            col1, col2 = st.columns(2)
            f_peso = col1.text_input("Peso (kg):")
            f_temp = col2.text_input("Temperatura (°C):")
            f_texto = st.text_area("Anamnese (Dica: Use Windows + H para ditar):", height=250)
            if st.form_submit_button("💾 Salvar Atendimento"):
                st.session_state['historico'].append({"DATA": datetime.now().strftime("%d/%m/%Y %H:%M"), "PACIENTE": paciente, "PESO": f_peso, "TEMP": f_temp, "TEXTO": f_texto})
                st.success("Consulta Salva!")

import urllib.parse

# --- 6. MÓDULO FINANCEIRO COM WHATSAPP (v9.6) ---
elif st.session_state.aba_atual == "💰 Financeiro":
    # ... (mantenha a parte de seleção de paciente e carrinho igual à v9.4)
    
    # Após finalizar o pagamento no formulário:
    if st.session_state.caixa:
        ultimo = st.session_state.caixa[-1]
        tutor_nome = ultimo['PACIENTE'].split(" (Tutor: ")[1].replace(")", "")
        
        # Busca o telefone do tutor cadastrado
        tutor_data = next((c for c in st.session_state['clientes'] if c['NOME'] == tutor_nome), {})
        telefone = tutor_data.get('TEL', '').replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        st.divider()
        st.write("### 📄 Recibo do Último Atendimento")
        
        # Monta o texto do recibo
        texto_recibo = (
            f"*RECIBO - RIBEIRA VET PRO*\n\n"
            f"Olá, {tutor_nome}!\n"
            f"Segue o comprovante de atendimento do(a) *{ultimo['PACIENTE'].split(' (')[0]}*.\n"
            f"--------------------------\n"
            f"*Serviços:* {ultimo['ITENS']}\n"
            f"*Total:* R$ {ultimo['VALOR']:.2f}\n"
            f"*Pagamento:* {ultimo['PAGTO']}\n"
            f"--------------------------\n"
            f"Data: {ultimo['DATA']}\n\n"
            f"Obrigado pela confiança!"
        )
        
        st.info(texto_recibo)
        
        # Link para o WhatsApp
        texto_url = urllib.parse.quote(texto_recibo)
        link_zap = f"https://wa.me/55{telefone}?text={texto_url}"
        
        if telefone:
            st.link_button("📲 Enviar Recibo por WhatsApp", link_zap)
        else:
            st.warning("⚠️ Telefone não cadastrado para este tutor. Cadastre na aba 'Tutores'.")

    # Tabela de resumo (mantenha a mesma da v9.4)
        
# --- 7. MÓDULO BACKUP PROFISSIONAL (v9.5) ---
elif st.session_state.aba_atual == "💾 Backup":
    st.subheader("💾 Central de Segurança dos Dados")
    
    st.write("### 1. Exportar para Excel (Financeiro)")
    if st.session_state.caixa:
        import pandas as pd
        df_fin = pd.DataFrame(st.session_state.caixa)
        csv = df_fin.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Baixar Planilha de Ganhos (Excel)", data=csv, file_name=f"financeiro_vet_{datetime.now().strftime('%d_%m')}.csv", mime='text/csv')
    else:
        st.info("Ainda não há lançamentos financeiros para exportar.")

    st.divider()
    st.write("### 2. Backup Completo do Sistema")
    st.warning("Este arquivo abaixo serve para restaurar o sistema inteiro em caso de pane.")
    dados_total = str(st.session_state.to_dict()) # Transforma tudo em texto para segurança
    st.download_button("📥 Baixar Backup Geral (Sistema)", data=dados_total, file_name=f"sistema_completo_{datetime.now().strftime('%d_%m')}.txt")
