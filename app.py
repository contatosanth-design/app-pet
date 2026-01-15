import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN E CORES ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
for key in ['clientes', 'pets', 'historico']:
    if key not in st.session_state: st.session_state[key] = {} if key == 'clientes' else []

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", use_container_width=True)
    st.markdown("<h2 style='text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MENU", ["🎉 Aniversariantes", "👤 Cadastro Tutor", "🐶 Cadastro Pet", "🩺 Prontuário"])

# --- 🎉 PÁGINA: ANIVERSARIANTES (Fidelização) ---
if menu == "🎉 Aniversariantes":
    st.title("🎂 Pacientes que fazem aniversário hoje")
    hoje = datetime.now().strftime("%d/%m")
    niver_encontrado = False
    
    for p in st.session_state['pets']:
        if p['nascimento'].strftime("%d/%m") == hoje:
            niver_encontrado = True
            tutor_info = st.session_state['clientes'].get(p['cod_tutor'], {})
            col1, col2 = st.columns([3, 1])
            col1.success(f"🐾 **{p['nome']}** está completando mais um ano de vida!")
            
            # Botão para facilitar o envio do Zap
            msg = f"Olá {tutor_info.get('nome')}, o Consultório da Ribeira deseja um parabéns especial para o {p['nome']}! 🎂🐶"
            link_zap = f"https://wa.me/{tutor_info.get('zap')}?text={msg.replace(' ', '%20')}"
            col2.markdown(f"[📲 Enviar Parabéns]({link_zap})")
            
    if not niver_encontrado:
        st.info("Nenhum pet faz aniversário hoje.")

# --- 👤 PÁGINA: CADASTRO TUTOR ---
elif menu == "👤 Cadastro Tutor":
    st.title("Ficha do Proprietário")
    with st.form("f_tutor"):
        id_t = f"T-{len(st.session_state['clientes'])+1:04d}"
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF")
        zap = st.text_input("WhatsApp (com DDD)")
        email = st.text_input("E-mail")
        if st.form_submit_button("Salvar Tutor"):
            st.session_state['clientes'][id_t] = {"nome": nome, "zap": zap, "email": email, "cpf": cpf}
            st.success("Tutor cadastrado!")

# --- 🐶 PÁGINA: CADASTRO PET ---
elif menu == "🐶 Cadastro Pet":
    st.title("Ficha do Paciente")
    if not st.session_state['clientes']:
        st.warning("Cadastre o tutor primeiro.")
    else:
        with st.form("f_pet"):
            tutores = [f"{k} - {v['nome']}" for k, v in st.session_state['clientes'].items()]
            tutor_sel = st.selectbox("Proprietário", tutores)
            nome_p = st.text_input("Nome do Animal")
            nasc = st.date_input("Data de Nascimento", min_value=datetime(2000, 1, 1))
            raca = st.text_input("Raça")
            if st.form_submit_button("Salvar Pet"):
                st.session_state['pets'].append({
                    "nome": nome_p, "nascimento": nasc, "raca": raca, 
                    "cod_tutor": tutor_sel.split(" - ")[0]
                })
                st.success("Pet cadastrado com sucesso!")

# --- 🩺 PÁGINA: PRONTUÁRIO ---
elif menu == "🩺 Prontuário":
    st.title("Atendimento Clínico")
    if not st.session_state['pets']:
        st.info("Nenhum pet cadastrado.")
    else:
        with st.form("f_atend"):
            pet_sel = st.selectbox("Paciente", [p['nome'] for p in st.session_state['pets']])
            col1, col2 = st.columns(2)
            peso = col1.text_input("Peso (kg)")
            temp = col2.text_input("Temperatura (°C)")
            anamnese = st.text_area("Anamnese / Evolução Clínica")
            if st.form_submit_button("Finalizar Consulta"):
                st.success("Prontuário atualizado!")
