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

# --- 6. MÓDULO FINANCEIRO COMPLETO (v9.3) ---
elif st.session_state.aba_atual == "💰 Financeiro":
    st.subheader("💰 Controle de Pagamentos e Serviços")
    
    # Lista de pacientes para vincular a cobrança
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    paciente_fin = st.selectbox("Vincular ao paciente:", ["--- Selecione ---"] + p_lista)
    
    if paciente_fin != "--- Selecione ---":
        with st.form("form_fin_v93"):
            col1, col2 = st.columns(2)
            
            # Tipos de serviços combinados
            tipo_servico = col1.selectbox("Tipo de Serviço:", [
                "Consulta Local", 
                "Consulta Residencial", 
                "Vacina", 
                "Medicamento", 
                "Outros"
            ])
            
            valor = col1.number_input("Valor (R$):", min_value=0.0, step=5.0)
            forma = col2.selectbox("Forma de Pagamento:", ["Pix", "Dinheiro", "Cartão Débito", "Cartão Crédito"])
            detalhes = col2.text_input("Detalhes (Ex: Nome da Vacina/Remédio):")

            if st.form_submit_button("💵 Registrar e Gerar Recibo"):
                novo_lancamento = {
                    "DATA": datetime.now().strftime("%d/%m/%Y"),
                    "PACIENTE": paciente_fin,
                    "SERVIÇO": tipo_servico,
                    "DETALHES": detalhes,
                    "VALOR": valor,
                    "PAGTO": forma
                }
                st.session_state.caixa.append(novo_lancamento)
                st.success(f"Lançamento de {tipo_servico} realizado com sucesso!")
                st.rerun()

    # Exibição do histórico de hoje
    if st.session_state.caixa:
        st.write("### 📊 Movimentação do Dia")
        st.table(st.session_state.caixa)
        
        # Soma total (Corrigindo o erro da linha 198)
        total_dia = sum(item['VALOR'] for item in st.session_state.caixa)
        st.metric("Total Acumulado", f"R$ {total_dia:.2f}")

# --- 7. BACKUP ---
elif st.session_state.aba_atual == "💾 Backup":
    st.subheader("💾 Salvar Dados")
    dados_total = str(st.session_state)
    st.download_button("📥 Baixar Arquivo de Segurança", data=dados_total, file_name=f"backup_vet_{datetime.now().strftime('%d_%m')}.txt")
