import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO E LISTA DE PREÇOS (O SEU ESTOQUE)
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

# --- AQUI ESTÁ A SUA LISTA DE SERVIÇOS QUE O SENHOR PEDIU ---
if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [
        {"Item": "CONSULTA CLÍNICA", "Preco": 150.00},
        {"Item": "REVISÃO (RETORNO)", "Preco": 0.00},
        {"Item": "VACINA V10", "Preco": 120.00},
        {"Item": "VACINA ANTIRRÁBICA", "Preco": 80.00},
        {"Item": "HEMOGRAMA", "Preco": 90.00},
        {"Item": "LIMPEZA DE TÁRTARO", "Preco": 350.00}
    ]

# 2. MENU LATERAL
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"])

# 3. MÓDULO 1: TUTORES (A-Z)
if menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    nomes_ordenados = sorted([c['NOME'] for c in st.session_state['clientes']])
    escolha = st.selectbox("⚡ Selecionar ou Criar Novo:", ["--- Novo Cadastro ---"] + nomes_ordenados)
    
    with st.form("f_tutor_v85"):
        if escolha == "--- Novo Cadastro ---":
            v_nome, v_tel, v_cpf, v_email, v_end = "", "", "", "", ""
        else:
            dados = next(c for c in st.session_state['clientes'] if c['NOME'] == escolha)
            v_nome, v_tel, v_cpf, v_email, v_end = dados['NOME'], dados['TEL'], dados['CPF'], dados['E-MAIL'], dados['ENDEREÇO']

        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo *", value=v_nome).upper()
        zap = c2.text_input("Telefone", value=v_tel)
        c3, c4 = st.columns([1, 1])
        cpf = c3.text_input("CPF", value=v_cpf)
        email = c4.text_input("E-mail", value=v_email)
        end = st.text_input("Endereço Completo", value=v_end)
        
        if st.form_submit_button("💾 Salvar Cadastro"):
            if nome and escolha == "--- Novo Cadastro ---":
                st.session_state['clientes'].append({"NOME": nome, "CPF": cpf, "TEL": zap, "ENDEREÇO": end, "E-MAIL": email})
                st.rerun()

# 4. MÓDULO 2: PETS (A-Z)
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    tutores_disp = sorted([c['NOME'] for c in st.session_state['clientes']])
    if not tutores_disp: st.warning("⚠️ Cadastre um Tutor primeiro!")
    else:
        with st.form("f_pet_v85"):
            tutor_sel = st.selectbox("Tutor Responsável *", tutores_disp)
            n_pet = st.text_input("Nome do Pet *").upper()
            nasc = st.text_input("Nascimento", value=datetime.now().strftime('%d/%m/%Y'))
            esp = st.selectbox("Espécie", ["Cão", "Gato", "Outro"])
            rac = st.text_input("Raça").upper()
            if st.form_submit_button("💾 Salvar Pet"):
                if n_pet:
                    st.session_state['pets'].append({"PET": n_pet, "TUTOR": tutor_sel, "ESP": esp, "RAÇA": rac, "NASC": nasc})
                    st.rerun()

# 5. MÓDULO 3: PRONTUÁRIO (SEM LANÇAMENTO AUTOMÁTICO)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    opcoes = sorted([f"{p['PET']} (Tutor: {p.get('TUTOR', 'N/D')})" for p in st.session_state['pets']])
    
    with st.form("f_pronto_v85"):
        paciente = st.selectbox("Buscar Paciente *", ["--- Selecione ---"] + opcoes)
        c1, c2 = st.columns(2)
        peso = c1.text_input("Peso (kg)")
        temp = c2.text_input("Temperatura (°C)")
        anamnese = st.text_area("🎙️ Anamnese (Win+H):", height=250, key="anamnese_input")
        
        if st.form_submit_button("💾 Salvar Prontuário"):
            if paciente != "--- Selecione ---" and anamnese:
                st.session_state['historico'].append({
                    "DATA": datetime.now().strftime('%d/%m/%Y %H:%M'),
                    "PACIENTE": paciente, "PESO": peso, "TEMP": temp, "RELATO": anamnese
                })
                st.success("✅ Salvo! Agora vá ao Financeiro para cobrar se necessário.")
                st.rerun()

    if st.session_state['historico']:
        st.table(pd.DataFrame(st.session_state['historico']))

# 6. MÓDULO 4: FINANCEIRO (COM LISTA DE PRODUTOS/SERVIÇOS)
elif menu == "💰 Financeiro":
    st.subheader("💰 Financeiro e Caixa")
    
    # Lista para o seletor (Estoque)
    lista_servicos = [f"{s['Item']} - R$ {s['Preco']:.2f}" for s in st.session_state['estoque']]
    
    with st.form("f_financeiro_v85"):
        st.write("🛒 **Adicionar Item ao Atendimento**")
        escolha_prod = st.selectbox("Escolha da sua Tabela:", ["--- Selecione ou digite manual abaixo ---"] + lista_servicos)
        
        st.write("--- ou digite um novo ---")
        servico_manual = st.text_input("Descrição Manual (Ex: Cirurgia Especial)")
        valor_manual = st.number_input("Valor (R$)", min_value=0.0, step=1.0, format="%.2f")
        
        if st.form_submit_button("➕ Adicionar ao Carrinho"):
            if escolha_prod != "--- Selecione ou digite manual abaixo ---":
                # Puxa o item selecionado da lista
                nome_item = escolha_prod.split(" - R$")[0]
                preco_item = float(escolha_prod.split("R$ ")[1])
                st.session_state['carrinho'].append({"Item": nome_item, "Preco": preco_item})
                st.rerun()
            elif servico_manual:
                # Usa o que o senhor digitou na mão
                st.session_state['carrinho'].append({"Item": servico_manual.upper(), "Preco": valor_manual})
                st.rerun()

    # Exibição do Carrinho (Fatura)
    if st.session_state['carrinho']:
        st.write("---")
        df = pd.DataFrame(st.session_state['carrinho'])
        st.table(df.assign(Preco=df['Preco'].map("R$ {:.2f}".format)))
        total = sum(i['Preco'] for i in st.session_state['carrinho'])
        st.metric("Total a Pagar", f"R$ {total:.2f}")
        
        if st.button("🏁 Finalizar Atendimento"):
            st.session_state['carrinho'] = []
            st.success("Caixa fechado!")
            st.rerun()

# 7. BACKUP
elif menu == "💾 Backup":
    st.subheader("💾 Exportar Dados")
    if st.session_state['clientes']:
        st.download_button("📥 Excel", pd.DataFrame(st.session_state['clientes']).to_csv(index=False).encode('utf-8-sig'), "dados_vet.csv")
