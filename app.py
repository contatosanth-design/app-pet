import streamlit as st
import uuid
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ribeira Vet Pro AI", layout="wide")

# --- ESTILIZAÇÃO CUSTOMIZADA (Tailwind-like) ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        border-radius: 15px;
        height: 3em;
        font-weight: bold;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO (Simulando o localStorage) ---
if 'tutores' not in st.session_state: st.session_state.tutores = []
if 'pets' not in st.session_state: st.session_state.pets = []
if 'records' not in st.session_state: st.session_state.records = []

# --- SIDEBAR (Navegação) ---
with st.sidebar:
    st.title("🐾 Ribeira Vet")
    menu = st.radio("Menu", ["Tutores", "Pacientes", "Prontuário", "Dados"])
    st.info("IA Conectada 🟢")

# --- LÓGICA DE VISUALIZAÇÃO ---

if menu == "Tutores":
    st.header("Cadastro de Tutores")
    with st.form("form_tutor"):
        nome = st.text_input("Nome do Tutor").upper()
        cpf = st.text_input("CPF")
        col1, col2 = st.columns(2)
        tel = col1.text_input("WhatsApp")
        email = col2.text_input("E-mail")
        if st.form_submit_button("SALVAR TUTOR"):
            st.session_state.tutores.append({"id": str(uuid.uuid4()), "nome": nome, "cpf": cpf})
            st.success("Tutor cadastrado!")

elif menu == "Pacientes":
    st.header("Pacientes")
    if not st.session_state.tutores:
        st.warning("Cadastre um tutor primeiro!")
    else:
        with st.form("form_pet"):
            tutor_nome = st.selectbox("Responsável", [t['nome'] for t in st.session_state.tutores])
            pet_nome = st.text_input("Nome do Pet").upper()
            raca = st.text_input("Raça").upper()
            if st.form_submit_button("CADASTRAR PACIENTE"):
                st.session_state.pets.append({"id": str(uuid.uuid4()), "nome": pet_nome, "raca": raca, "tutor": tutor_nome})
                st.success(f"{pet_nome} cadastrado!")

elif menu == "Prontuário":
    st.header("Atendimento")
    if not st.session_state.pets:
        st.warning("Nenhum paciente cadastrado.")
    else:
        pet_selecionado = st.selectbox("Escolha o Paciente", [p['nome'] for p in st.session_state.pets])
        
        st.subheader("Anamnese / Sintomas")
        sintomas = st.text_area("O que o pet está apresentando?", height=150)
        
        if st.button("✨ CONSULTAR IA VETERINÁRIA"):
            with st.spinner("Analisando..."):
                # Aqui chamaremos sua geminiService depois
                st.write("--- Sugestão Pro AI ---")
                st.info("Simulação: Baseado nos sintomas, recomenda-se checkup renal.")

        conduta = st.text_area("Conduta / Tratamento", height=150)
        
        if st.button("FINALIZAR CONSULTA"):
            st.session_state.records.append({
                "pet": pet_selecionado,
                "data": datetime.now().strftime("%d/%m/%Y"),
                "sintomas": sintomas,
                "conduta": conduta
            })
            st.success("Consulta salva no histórico!")

elif menu == "Dados":
    st.header("Backup e Restauração")
    st.write(st.session_state) # Visualização bruta para teste
