import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN PROFISSIONAL ---
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

# --- 🎉 PÁGINA: ANIVERSARIANTES ---
if menu == "🎉 Aniversariantes":
    st.title("🎂 Aniversariantes de Hoje")
    hoje = datetime.now().strftime("%d/%m")
    encontrou = False
    for p in st.session_state['pets']:
        if p['nascimento'].strftime("%d/%m") == hoje:
            encontrou = True
            tutor = st.session_state['clientes'].get(p['cod_tutor'], {})
            col1, col2 = st.columns([3, 1])
            col1.success(f"🐾 **{p['nome']}** faz anos hoje!")
            msg = f"Olá {tutor.get('nome')}, o Consultório da Ribeira deseja um feliz aniversário ao {p['nome']}! 🎂"
            link = f"https://wa.me/{tutor.get('zap')}?text={msg.replace(' ', '%20')}"
            col2.markdown(f"[📲 Enviar WhatsApp]({link})")
    if not encontrou: st.info("Sem aniversários para hoje.")

# --- 👤 PÁGINA: CADASTRO TUTOR (COM ENDEREÇO) ---
elif menu == "👤 Cadastro Tutor":
    st.title("Ficha do Proprietário")
    with st.form("f_tutor"):
        id_t = f"T-{len(st.session_state['clientes'])+1:04d}"
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome Completo")
        cpf = col2.text_input("CPF")
        zap = col1.text_input("WhatsApp (com DDD)")
        email = col2.text_input("E-mail")
        endereco = st.text_area("Endereço Completo") # CAMPO REINSTALADO
        if st.form_submit_button("Salvar Tutor"):
            st.session_state['clientes'][id_t] = {
                "nome": nome, "zap": zap, "email": email, "cpf": cpf, "end": endereco
            }
            st.success("Tutor cadastrado com sucesso!")

# --- 🐶 PÁGINA: CADASTRO PET (COM DATA NASCIMENTO) ---
elif menu == "🐶 Cadastro Pet":
    st.title("Ficha do Paciente")
    if not st.session_state['clientes']: st.warning("Cadastre o tutor primeiro.")
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
                st.success("Pet cadastrado!")

# --- 🩺 PÁGINA: PRONTUÁRIO ---
elif menu == "🩺 Prontuário":
    st.title("Atendimento Clínico")
    if not st.session_state['pets']: st.info("Nenhum pet cadastrado.")
    else:
        with st.form("f_atend"):
            pet_sel = st.selectbox("Paciente", [p['nome'] for p in st.session_state['pets']])
            c1, c2 = st.columns(2)
            peso, temp = c1.text_input("Peso (kg)"), c2.text_input("Temp (°C)")
            anamnese = st.text_area("Anamnese / Evolução Clínica")
            if st.form_submit_button("Finalizar Consulta"):
                st.success("Prontuário guardado!")
