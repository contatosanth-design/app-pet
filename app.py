import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Veterinário da Ribeira", layout="wide")

# --- CSS PARA DESIGN TÉCNICO ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 13px; }
    .main { background-color: #f0f2f6; }
    h1 { color: #1e3d59; font-size: 20px !important; }
    .stButton>button { background-color: #2e7bcf; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização do Banco de Dados em Memória
if 'clientes' not in st.session_state: st.session_state['clientes'] = {}
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'proximo_cod_cliente' not in st.session_state: st.session_state['proximo_cod_cliente'] = 1
if 'proximo_cod_pet' not in st.session_state: st.session_state['proximo_cod_pet'] = 1

# --- BARRA LATERAL ---
with st.sidebar:
    # Tentativa de carregar o logo do seu GitHub
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", width=120)
    st.markdown("### 🏥 CONSULTÓRIO DA RIBEIRA")
    st.divider()
    # Nomes simplificados para evitar erros de digitação no código
    menu = st.radio("NAVEGAÇÃO", ["Início", "Tutores", "Prontuário", "Banco de Dados"])

# --- PÁGINA: INÍCIO ---
if menu == "Início":
    st.title("📊 Painel de Controle")
    c1, c2 = st.columns(2)
    c1.metric("Tutores", len(st.session_state['clientes']))
    c2.metric("Pacientes", len(st.session_state['pets']))

# --- PÁGINA: TUTORES ---
elif menu == "Tutores":
    st.title("👤 Cadastro de Tutores")
    with st.form("form_tutor"):
        c_id = f"{st.session_state['proximo_cod_cliente']:04d}"
        st.info(f"Ficha Cliente Nº {c_id}")
        nome = st.text_input("Nome do Tutor")
        tel = st.text_input("WhatsApp")
        if st.form_submit_button("Salvar Tutor"):
            if nome and tel:
                st.session_state['clientes'][c_id] = nome
                st.session_state['proximo_cod_cliente'] += 1
                st.success("Cadastrado!")
            else: st.error("Preencha Nome e WhatsApp")

# --- PÁGINA: PRONTUÁRIO (Aqui estava o erro!) ---
elif menu == "Prontuário":
    st.title("🩺 Ficha de Atendimento / Prontuário")
    if not st.session_state['clientes']:
        st.warning("⚠️ Cadastre um Tutor primeiro na aba 'Tutores'.")
    else:
        with st.form("form_clinico"):
            p_id = f"{st.session_state['proximo_cod_pet']:04d}"
            
            # Associação com Tutor
            lista_t = [f"{id} - {n}" for id, n in st.session_state['clientes'].items()]
            tutor = st.selectbox("Selecione o Tutor", lista_t)
            
            col1, col2 = st.columns(2)
            nome_p = col1.text_input("Nome do Animal")
            especie = col2.selectbox("Espécie", ["Canino", "Felino", "Outros"])
            
            st.markdown("---")
            v1, v2, v3 = st.columns(3)
            peso = v1.text_input("Peso (kg)")
            temp = v2.text_input("Temp (°C)")
            cor = v3.text_input("Cor do Pêlo")
            
            diag = st.text_area("Diagnóstico / Observações")
            foto = st.file_uploader("Foto do Paciente", type=['jpg','png','jpeg'])
            
            if st.form_submit_button("✅ Salvar Atendimento"):
                if nome_p:
                    st.session_state['pets'].append({
                        "Cód": p_id, "Tutor": tutor, "Nome": nome_p, 
                        "Espécie": especie, "Peso": peso, "Temp": temp, 
                        "Cor": cor, "Diagnóstico": diag, "Foto": foto
                    })
                    st.session_state['proximo_cod_pet'] += 1
                    st.success(f"Prontuário de {nome_p} salvo!")
                else: st.error("Nome do pet é obrigatório")

# --- PÁGINA: BANCO DE DADOS ---
elif menu == "Banco de Dados":
    st.title("📋 Planilha de Registros")
    if not st.session_state['pets']:
        st.info("Nenhum prontuário encontrado.")
    else:
        # Cabeçalho estilo planilha
        cols = st.columns([1, 2, 2, 1, 1, 1, 3])
        titulos = ["FOTO", "CÓD", "PET", "TUTOR", "PESO", "TEMP", "DIAGNÓSTICO"]
        for i, t in enumerate(titulos): cols[i].write(f"**{t}**")
        
        for p in st.session_state['pets']:
            r = st.columns([1, 2, 2, 1, 1, 1, 3])
            if p['Foto']: r[0].image(p['Foto'], width=50)
            else: r[0].write("🚫")
            r[1].write(p['Cód'])
            r[2].write(p['Nome'])
            r[3].write(p['Tutor'])
            r[4].write(p['Peso'])
            r[5].write(p['Temp'])
            r[6].write(p['Diagnóstico'])
