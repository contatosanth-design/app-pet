import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# 1. Configuração de Estabilidade
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# 2. Banco de Dados e Carga Automática (Resolve o Financeiro Vazio)
if 'estoque' not in st.session_state or len(st.session_state['estoque']) == 0:
    st.session_state['estoque'] = [
        {"Item": "Vacina V10 (Importada)", "Preco": 120.00}, {"Item": "Vacina Antirrábica", "Preco": 60.00},
        {"Item": "Consulta Geral", "Preco": 150.00}, {"Item": "Hemograma", "Preco": 90.00},
        {"Item": "Simparic 10-20kg", "Preco": 85.00}, {"Item": "Castração Macho", "Preco": 350.00},
        {"Item": "Limpeza de Tártaro", "Preco": 250.00}, {"Item": "Ultrassom Abdominal", "Preco": 220.00},
        {"Item": "Internação Diária", "Preco": 180.00}, {"Item": "Vermífugo (Drontal)", "Preco": 35.00}
    ]

for key in ['clientes', 'pets', 'historico']:
    if key not in st.session_state: st.session_state[key] = []

# 3. Estilo Visual (Branding Ribeira Vet)
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59 !important; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold !important; }
    .header-box { background: white; padding: 20px; border-radius: 10px; border-left: 6px solid #2e7bcf; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 4. Menu Lateral Único
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=80)
    st.title("Ribeira Vet Pro")
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "📦 Produtos", "💰 Financeiro"])

# Cabeçalho
st.markdown(f"<div class='header-box'><h1 style='color:#1e3d59; margin:0;'>Ribeira Vet Pro</h1><p style='margin:0;'>Sistema Estabilizado • {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- SESSÃO 1: TUTORES (CAMPOS COMPLETOS) ---
if menu == "👤 Tutores":
    st.subheader("📝 Cadastro de Tutor")
    with st.form("f_tutor", clear_on_submit=True):
        id_t = f"T{len(st.session_state['clientes']) + 1:03d}"
        st.info(f"Código: {id_t}")
        nome = st.text_input("Nome Completo*")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        zap = c2.text_input("WhatsApp (Ex: 22985020463)*")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço")
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({"id": id_t, "nome": nome.upper(), "cpf": cpf, "zap": zap, "email": email, "end": end})
                st.success(f"Tutor {nome} salvo!")
            else: st.error("Preencha Nome e WhatsApp.")

# --- SESSÃO 2: PETS (COM CÁLCULO DE IDADE) ---
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pet")
    if not st.session_state['clientes']: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            t_lista = {f"{c['id']} - {c['nome']}": c for c in st.session_state['clientes']}
            t_sel = st.selectbox("Proprietário", list(t_lista
