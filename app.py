import streamlit as st
import pd
import os
from datetime import datetime

# 1. CONFIGURAÇÕES E ESTILO (O FIM DO BOTÃO PRETO)
st.set_page_config(page_title="Ribeira Vet Pro v16", layout="wide", page_icon="🏥")

st.markdown("""
    <style>
    .stApp { background-color: white !important; color: #1E293B !important; }
    
    /* LOGO 40x40 */
    .stImage > img { width: 40px !important; height: 40px !important; border-radius: 5px; }

    /* BOTÃO AMARELO GLOBAL (CSS ULTRA-FORTE) */
    button, .stButton>button, div[data-testid="stForm"] button {
        background-color: #FFD700 !important; 
        color: #000000 !important; 
        font-weight: bold !important;
        border: 2px solid #B8860B !important;
        width: 100% !important;
        border-radius: 8px !important;
    }
    
    /* CURSOR E INPUTS */
    input, textarea, select { 
        background-color: #F8FAFC !important; 
        color: black !important; 
        caret-color: black !important; 
        border: 1px solid #CBD5E1 !important; 
    }
    label { color: #1E293B !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS (v16)
def carregar(nome, cols):
    if os.path.exists(nome): return pd.read_csv(nome)
    return pd.DataFrame(columns=cols)

# Inicializando arquivos
if 'df_tutores' not in st.session_state:
    st.session_state.df_tutores = carregar('tutores_v16.csv', ["CPF", "Tutor", "WhatsApp"])
if 'df_pets' not in st.session_state:
    st.session_state.df_pets = carregar('pets_v16.csv', ["CPF_Tutor", "Pet", "Espécie", "Raça"])
if 'df_prontuario' not in st.session_state:
    st.session_state.df_prontuario = carregar('prontuario_v16.csv', ["Data", "Pet", "Relato"])

# TABELAS DE PREÇOS (FINANCEIRO)
precos_servicos = {"Consulta Geral": "R$ 150,00", "Vacina V10": "R$ 120,00", "Vacina Raiva": "R$ 80,00", "Vermifugação": "R$ 45,00"}
precos_produtos = {"Antibiótico A": "R$ 65,00", "Shampoo Med.": "R$ 89,00", "Ração 1kg": "R$ 35,00"}

# 3. MENU LATERAL
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png")
    st.markdown("### Ribeira Vet Pro")
    st.info("📍 **VERSÃO 16.0 - COMPLETA**")
    menu = st.radio("Módulos:", ["📊 Painel", "👤 Tutores", "🐾 Animais", "⚕️ Prontuário", "💰 Financeiro"])

# 4. PÁGINAS

if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Tutor")
    with st.form("f_tutor"):
        nome = st.text_input("Nome do Tutor")
        cpf = st.text_input("CPF")
        whats = st.text_input("WhatsApp")
        if st.form_submit_button("SALVAR TUTOR"):
            novo = pd.DataFrame([{"CPF": cpf, "Tutor": nome, "WhatsApp": whats}])
            st.session_state.df_tutores = pd.concat([st.session_state.df_tutores, novo], ignore_index=True)
            st.session_state.df_tutores.to_csv('tutores_v16.csv', index=False)
            st.success("Tutor salvo!")

elif menu == "🐾 Animais":
    st.subheader("🐾 Cadastro de Animal")
    if st.session_state.df_tutores.empty: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            tutor_ref = st.selectbox("Dono:", st.session_state.df_tutores['Tutor'])
            nome_p = st.text_input("Nome do Pet")
            especie = st.selectbox("Espécie", ["Canina", "Felina", "Exótico"])
            if st.form_submit_button("SALVAR ANIMAL"):
                novo_p = pd.DataFrame([{"CPF_Tutor": "Ref", "Pet": nome_p, "Espécie": especie}])
                st.session_state.df_pets = pd.concat([st.session_state.df_pets, novo_p], ignore_index=True)
                st.session_state.df_pets.to_csv('pets_v16.csv', index=False)
                st.success(f"{nome_p} cadastrado!")

elif menu == "⚕️ Prontuário":
    st.subheader("⚕️ Histórico e Evolução Clínica")
    if st.session_state.df_pets.empty:
        st.warning("Não há animais cadastrados para consulta.")
    else:
        with st.form("f_prontuario"):
            pet_sel = st.selectbox("Selecione o Paciente:", st.session_state.df_pets['Pet'])
            relato = st.text_area("Evolução do Paciente / Prescrição:", height=200)
            if st.form_submit_button("GRAVAR NO PRONTUÁRIO"):
                data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
                novo_pront = pd.DataFrame([{"Data": data_hoje, "Pet": pet_sel, "Relato": relato}])
                st.session_state.df_prontuario = pd.concat([st.session_state.df_prontuario, novo_pront], ignore_index=True)
                st.session_state.df_prontuario.to_csv('prontuario_v16.csv', index=False)
                st.success("Consulta gravada com sucesso!")
        
        st.divider()
        st.subheader("📜 Histórico Recente")
        st.table(st.session_state.df_prontuario.tail(5))

elif menu == "💰 Financeiro":
    st.subheader("💰 Tabela de Preços e Serviços")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ⚕️ Serviços")
        st.table(pd.DataFrame(list(precos_servicos.items()), columns=['Serviço', 'Valor']))
    with col2:
        st.markdown("### 💊 Produtos / Farmácia")
        st.table(pd.DataFrame(list(precos_produtos.items()), columns=['Produto', 'Valor']))

else:
    st.subheader("📊 Painel Geral")
    st.write(f"Total de Tutores: {len(st.session_state.df_tutores)}")
    st.write(f"Total de Pets: {len(st.session_state.df_pets)}")
