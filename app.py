import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. CONFIGURAÇÕES GERAIS E ESTILO
st.set_page_config(page_title="Ribeira Vet Pro v17", layout="wide", page_icon="🏥")

st.markdown("""
    <style>
    /* FUNDO BRANCO E TEXTO ESCURO */
    .stApp { background-color: white !important; color: #1E293B !important; }
    
    /* LOGOTIPO 40x40 */
    .stImage > img { 
        width: 40px !important; 
        height: 40px !important; 
        border-radius: 4px; 
    }

    /* BOTÃO AMARELO - RESOLUÇÃO DEFINITIVA */
    button, .stButton>button, div[data-testid="stForm"] button {
        background-color: #FFD700 !important; 
        color: #000000 !important; 
        font-weight: bold !important;
        border: 2px solid #B8860B !important;
        width: 100% !important;
        height: 3em !important;
        display: block !important;
    }

    /* INPUTS E CURSOR */
    input, textarea, select { 
        background-color: #F1F5F9 !important; 
        color: black !important; 
        caret-color: black !important; 
        border: 1px solid #CBD5E1 !important; 
    }
    label { color: #1E293B !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTÃO DE DADOS
def carregar_dados(arquivo, colunas):
    if os.path.exists(arquivo):
        return pd.read_csv(arquivo)
    return pd.DataFrame(columns=colunas)

# Inicialização
if 'db_tutores' not in st.session_state:
    st.session_state.db_tutores = carregar_dados('tutores_v17.csv', ["CPF", "Nome", "WhatsApp"])
if 'db_pets' not in st.session_state:
    st.session_state.db_pets = carregar_dados('pets_v17.csv', ["CPF_Dono", "Nome_Pet", "Especie"])
if 'db_consultas' not in st.session_state:
    st.session_state.db_consultas = carregar_dados('prontuario_v17.csv', ["Data", "Paciente", "Relato"])

# TABELAS FINANCEIRAS FIXAS
servicos = {"Consulta": "R$ 150", "Vacina": "R$ 120", "Exame Sangue": "R$ 90"}
produtos = {"Vermífugo": "R$ 45", "Antibiótico": "R$ 65", "Ração 1kg": "R$ 38"}

# 3. MENU LATERAL
with st.sidebar:
    # Insira o link da sua imagem de logo aqui
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png")
    st.title("Ribeira Vet Pro")
    st.info("🚀 **VERSÃO 17.0**")
    aba = st.radio("Navegar:", ["📊 Painel", "👤 Clientes", "🐾 Animais", "⚕️ Prontuário", "💰 Financeiro"])

# 4. CONTEÚDO DAS PÁGINAS

if aba == "👤 Clientes":
    st.header("👤 Cadastro de Proprietário")
    with st.form("form_tutor"):
        nome = st.text_input("Nome do Cliente")
        cpf = st.text_input("CPF")
        whats = st.text_input("WhatsApp")
        if st.form_submit_button("CADASTRAR CLIENTE"):
            if nome and cpf:
                novo = pd.DataFrame([{"CPF": cpf, "Nome": nome, "WhatsApp": whats}])
                st.session_state.db_tutores = pd.concat([st.session_state.db_tutores, novo], ignore_index=True)
                st.session_state.db_tutores.to_csv('tutores_v17.csv', index=False)
                st.success("Cadastrado!")

elif aba == "🐾 Animais":
    st.header("🐾 Cadastro de Pet")
    if st.session_state.db_tutores.empty: st.warning("Cadastre um cliente antes.")
    else:
        with st.form("form_pet"):
            dono = st.selectbox("Selecione o Dono:", st.session_state.db_tutores['Nome'])
            pet = st.text_input("Nome do Animal")
            esp = st.selectbox("Espécie:", ["Cão", "Gato", "Outro"])
            if st.form_submit_button("CADASTRAR PET"):
                novo_p = pd.DataFrame([{"CPF_Dono": dono, "Nome_Pet": pet, "Especie": esp}])
                st.session_state.db_pets = pd.concat([st.session_state.db_pets, novo_p], ignore_index=True)
                st.session_state.db_pets.to_csv('pets_v17.csv', index=False)
                st.success(f"{pet} salvo!")

elif aba == "⚕️ Prontuário":
    st.header("⚕️ Prontuário Clínico")
    if st.session_state.db_pets.empty: st.warning("Nenhum pet cadastrado.")
    else:
        with st.form("form_clinico"):
            paciente = st.selectbox("Paciente:", st.session_state.db_pets['Nome_Pet'])
            obs = st.text_area("Evolução e Prescrição", height=150)
            if st.form_submit_button("SALVAR ATENDIMENTO"):
                hoje = datetime.now().strftime("%d/%m/%Y")
                novo_c = pd.DataFrame([{"Data": hoje, "Paciente": paciente, "Relato": obs}])
                st.session_state.db_consultas = pd.concat([st.session_state.db_consultas, novo_c], ignore_index=True)
                st.session_state.db_consultas.to_csv('prontuario_v17.csv', index=False)
                st.success("Histórico atualizado!")
        st.subheader("📜 Histórico Recente")
        st.dataframe(st.session_state.db_consultas.tail(10), use_container_width=True)

elif aba == "💰 Financeiro":
    st.header("💰 Tabela de Preços")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🏥 Serviços")
        st.table(pd.DataFrame(list(servicos.items()), columns=['Item', 'Preço']))
    with c2:
        st.markdown("### 💊 Produtos")
        st.table(pd.DataFrame(list(produtos.items()), columns=['Item', 'Preço']))

else:
    st.header("📊 Painel Geral")
    st.metric("Total de Clientes", len(st.session_state.db_tutores))
    st.metric("Total de Pets", len(st.session_state.db_pets))
    st.write("---")
    st.subheader("Últimos Cadastros")
    st.dataframe(st.session_state.db_tutores.tail(5))
