import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. DESIGN DE ALTO CONTRASTE (ZERO TEXTO INVISÍVEL)
st.set_page_config(page_title="Ribeira Vet Pro v21", layout="wide")

st.markdown("""
    <style>
    /* Forçar Fundo Branco e Texto Preto em TUDO */
    .stApp { background-color: #FFFFFF !important; }
    * { color: #000000 !important; font-family: sans-serif; }
    
    /* Sidebar com contraste forte */
    [data-testid="stSidebar"] { background-color: #F1F5F9 !important; border-right: 2px solid #000000; }
    
    /* BOTÃO AMARELO COM TEXTO PRETO (MESMO AO CLICAR) */
    div.stButton > button {
        background-color: #FFD700 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 2px solid #000000 !important;
        width: 100% !important;
    }
    div.stButton > button:hover { background-color: #FFC400 !important; border: 2px solid #000000 !important; }

    /* Campos de Entrada com Borda Preta para visibilidade */
    input, textarea, select { 
        background-color: #FFFFFF !important; 
        border: 1px solid #000000 !important; 
        color: #000000 !important;
    }
    
    /* Tabelas Legíveis */
    .stDataFrame, [data-testid="stTable"] { border: 1px solid #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE DADOS SIMPLIFICADO
def carregar(arq, cols):
    if os.path.exists(arq): return pd.read_csv(arq)
    return pd.DataFrame(columns=cols)

# Arquivos Versão 21
tutores_file = 'tutores_v21.csv'
pets_file = 'pets_v21.csv'
vendas_file = 'vendas_v21.csv'

if 'df_tutores' not in st.session_state:
    st.session_state.df_tutores = carregar(tutores_file, ["Nome", "CPF", "WhatsApp", "Email", "Endereco"])
if 'df_pets' not in st.session_state:
    st.session_state.df_pets = carregar(pets_file, ["Dono", "Pet", "Especie", "Raca", "Peso", "Idade"])

# 3. NAVEGAÇÃO
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=40)
    st.subheader("Ribeira Vet Pro")
    menu = st.radio("IR PARA:", ["👤 Clientes", "🐾 Animais", "💰 Financeiro", "📊 Ver Tudo"])

# 4. MÓDULOS (NENHUM CAMPO É OBRIGATÓRIO)

if menu == "👤 Clientes":
    st.header("👤 Cadastro de Clientes")
    with st.form("f_cliente", clear_on_submit=True):
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome")
        cpf = c2.text_input("CPF")
        whats = c1.text_input("WhatsApp")
        email = c2.text_input("E-mail")
        end = st.text_input("Endereço Completo")
        
        if st.form_submit_button("SALVAR CLIENTE"):
            novo = pd.DataFrame([{"Nome": nome, "CPF": cpf, "WhatsApp": whats, "Email": email, "Endereco": end}])
            st.session_state.df_tutores = pd.concat([st.session_state.df_tutores, novo], ignore_index=True)
            st.session_state.df_tutores.to_csv(tutores_file, index=False)
            st.success("Salvo!")
            st.rerun()

    st.subheader("Lista de Clientes")
    st.dataframe(st.session_state.df_tutores, use_container_width=True)

elif menu == "🐾 Animais":
    st.header("🐾 Cadastro de Pets")
    with st.form("f_pet", clear_on_submit=True):
        # Seleção de dono (Se vazio, aceita qualquer texto)
        lista_donos = ["Nenhum"] + st.session_state.df_tutores['Nome'].tolist()
        dono = st.selectbox("Quem é o Dono?", lista_donos)
        
        c1, c2 = st.columns(2)
        p_nome = c1.text_input("Nome do Pet")
        p_esp = c2.selectbox("Espécie", ["Cão", "Gato", "Outro"])
        p_raca = c1.text_input("Raça")
        p_peso = c2.text_input("Peso")
        p_idade = st.text_input("Idade")
        
        if st.form_submit_button("SALVAR PET"):
            novo_p = pd.DataFrame([{"Dono": dono, "Pet": p_nome, "Especie": p_esp, "Raca": p_raca, "Peso": p_peso, "Idade": p_idade}])
            st.session_state.df_pets = pd.concat([st.session_state.df_pets, novo_p], ignore_index=True)
            st.session_state.df_pets.to_csv(pets_file, index=False)
            st.success(f"Pet {p_nome} cadastrado!")
            st.rerun()

    st.subheader("Lista de Pets")
    st.dataframe(st.session_state.df_pets, use_container_width=True)

elif menu == "💰 Financeiro":
    st.header("💰 Financeiro")
    st.subheader("Tabela de Preços")
    precos = pd.DataFrame({
        "Serviço/Produto": ["Consulta", "Vacina V10", "Castração", "Vermífugo"],
        "Valor Sugerido": ["R$ 150,00", "R$ 130,00", "R$ 450,00", "R$ 50,00"]
    })
    st.table(precos)
    
    st.subheader("Gerar Recibo Rápido")
    r_cli = st.text_input("Cliente")
    r_serv = st.text_input("Serviço")
    r_val = st.text_input("Valor")
    if st.button("GERAR RECIBO"):
        st.code(f"RECIBO: {r_cli} - {r_serv} - R$ {r_val}\nRibeira Vet Pro - {datetime.now().strftime('%d/%m/%Y')}")

elif menu == "📊 Ver Tudo":
    st.header("📊 Banco de Dados Completo")
    st.subheader("Todos os Tutores")
    st.dataframe(st.session_state.df_tutores)
    st.subheader("Todos os Pets")
    st.dataframe(st.session_state.df_pets)
