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

# --- 6. MÓDULO FINANCEIRO COM LISTA DE PRODUTOS (v9.4) ---
elif st.session_state.aba_atual == "💰 Financeiro":
    st.subheader("💰 Fechamento de Conta e Recibo")
    
    # 1. Tabela de Preços Sugeridos (O senhor pode alterar os valores aqui no código depois)
    tabela_precos = {
        "Consulta Local": 150.0,
        "Consulta Residencial": 250.0,
        "Vacina V10": 120.0,
        "Vacina Raiva": 80.0,
        "Medicamento (Geral)": 50.0,
        "Procedimento Simples": 100.0
    }

    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    paciente_fin = st.selectbox("Selecione o Paciente para Cobrança:", ["--- Selecione ---"] + p_lista)

    if paciente_fin != "--- Selecione ---":
        # Inicializa um "carrinho" temporário para a sessão se não existir
        if 'carrinho' not in st.session_state: st.session_state.carrinho = []

        col1, col2, col3 = st.columns([2, 1, 1])
        servico_nome = col1.selectbox("Selecione o Produto/Serviço:", list(tabela_precos.keys()) + ["Outro"])
        
        # Define o preço inicial baseado na tabela, mas permite edição
        preco_sugerido = tabela_precos.get(servico_nome, 0.0)
        valor_final = col2.number_input("Preço (R$):", min_value=0.0, value=preco_sugerido, step=5.0)
        
        if col3.button("➕ Adicionar à Conta"):
            st.session_state.carrinho.append({"ITEM": servico_nome, "VALOR": valor_final})
            st.rerun()

        # Exibe o que está sendo cobrado no momento
        if st.session_state.carrinho:
            st.write("---")
            st.write("### 📝 Itens da Guia Atual")
            total_atual = 0
            for i, item in enumerate(st.session_state.carrinho):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.text(f"• {item['ITEM']}")
                c2.text(f"R$ {item['VALOR']:.2f}")
                if c3.button("❌", key=f"del_{i}"):
                    st.session_state.carrinho.pop(i)
                    st.rerun()
                total_atual += item['VALOR']

            st.markdown(f"#### **Total a Pagar: R$ {total_atual:.2f}**")
            
            with st.form("finalizar_v94"):
                forma = st.selectbox("Forma de Pagamento:", ["Pix", "Dinheiro", "Cartão"])
                if st.form_submit_button("💾 Finalizar Atendimento e Salvar no Caixa"):
                    # Salva no histórico permanente
                    st.session_state.caixa.append({
                        "DATA": datetime.now().strftime("%d/%m/%Y"),
                        "PACIENTE": paciente_fin,
                        "ITENS": ", ".join([x['ITEM'] for x in st.session_state.carrinho]),
                        "VALOR": total_atual,
                        "PAGTO": forma
                    })
                    st.session_state.carrinho = [] # Limpa o carrinho para o próximo
                    st.success("Pagamento registrado com sucesso!")
                    st.rerun()

    # 📊 Resumo Geral do Dia (Histórico de Recebimentos)
    if st.session_state.caixa:
        st.divider()
        st.write("### 📊 Histórico de Hoje")
        st.table(st.session_state.caixa)
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
