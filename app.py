import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. TRAVA TOTAL DE INTERFACE (VERSÃO 14.0)
st.set_page_config(page_title="Ribeira Vet Pro v14", layout="wide", page_icon="🏥")

st.markdown("""
    <style>
    /* Reset total para ignorar modo escuro do navegador e forçar branco */
    .stApp { background-color: white !important; color: #1E293B !important; }
    h1, h2, h3, h4, label, p { color: #1E293B !important; }

    /* --- O BOTÃO TEIMOSO AGORA É AMARELO --- */
    /* Este seletor específico vence qualquer teimosia */
    div[data-testid="stForm"] div.stButton button {
        background-color: #FFD700 !important; /* Amarelo Ouro */
        color: #000000 !important; /* Texto Preto */
        font-weight: bold !important;
        border: 2px solid #B8860B !important;
        width: 100% !important;
        height: 3.5em !important;
        transition: 0.3s;
    }
    div[data-testid="stForm"] div.stButton button:hover {
        background-color: #FFC400 !important;
    }

    /* --- AJUSTE DE IMAGEM PARA LOGOTIPO 40x40 --- */
    .stImage > img {
        width: 40px !important;
        height: 40px !important;
        object-fit: contain !important; /* Mantém a proporção */
    }

    /* Inputs sempre brancos com borda visível */
    input, textarea, select { 
        background-color: white !important; 
        color: black !important; 
        caret-color: black !important; /* Cursor preto */
        border: 1px solid #D1D5DB !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS (v14)
def carregar_banco(nome, colunas):
    if os.path.exists(nome):
        return pd.read_csv(nome)
    return pd.DataFrame(columns=colunas)

if 'df_tutores' not in st.session_state:
    st.session_state.df_tutores = carregar_banco('tutores_v14.csv', ["CPF", "Nome do Tutor", "WhatsApp", "Endereço"])

# 3. INTERFACE LATERAL
with st.sidebar:
    # Insira aqui o link da imagem do seu logotipo 40x40
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=40)
    st.markdown("## 🏥 Ribeira Vet Pro")
    st.info("📌 **VERSÃO 14.0 - CORREÇÃO VISUAL**")
    menu = st.radio("Selecione:", ["📊 Painel Geral", "👤 Cadastro de Tutor", "🐾 Cadastro de Animal"])
    st.divider()
    csv = st.session_state.df_tutores.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Backup Completo (CSV)", data=csv, file_name="backup_vet.csv")

# 4. PÁGINAS

if menu == "👤 Cadastro de Tutor":
    st.subheader("👤 Novo Proprietário")
    with st.form("form_tutor_v14", clear_on_submit=True):
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome Completo do Tutor")
        cpf = c2.text_input("CPF (identificador único)")
        
        c3, c4 = st.columns([1, 2])
        whats = c3.text_input("WhatsApp com DDD")
        end = c4.text_input("Endereço Completo")
        
        # O BOTÃO QUE VENCEU A TEIMOSIA
        if st.form_submit_button("CADASTRAR TUTOR (AMARELO v14)"):
            if nome and cpf:
                novo = pd.DataFrame([{"CPF": cpf, "Nome do Tutor": nome, "WhatsApp": whats, "Endereço": end}])
                st.session_state.df_tutores = pd.concat([st.session_state.df_tutores, novo], ignore_index=True)
                st.session_state.df_tutores.to_csv('tutores_v14.csv', index=False)
                st.success("Tutor cadastrado!")
            else: st.error("Por favor, preencha Nome e CPF.")
else:
    st.write("Outras páginas em construção... Use o Cadastro de Tutor para ver a mudança!")
