import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59 !important; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold !important; }
    .header-box { background: white; padding: 20px; border-radius: 10px; border-left: 6px solid #2e7bcf; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS (SESSION STATE) ---
if 'clientes' not in st.session_state: st.session_state['clientes'] = []
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'estoque' not in st.session_state: 
    st.session_state['estoque'] = [
        {"Item": "Vacina V10", "Preco": 120.00}, {"Item": "Consulta", "Preco": 150.00},
        {"Item": "Castração Macho", "Preco": 350.00}, {"Item": "Vermífugo", "Preco": 35.00}
    ]

# --- MENU LATERAL (EVITA O ERRO DE TELA EM BRANCO) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=80)
    st.title("Ribeira Vet Pro")
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "📦 Produtos", "💰 Financeiro"])

# --- CABEÇALHO ---
st.markdown(f"<div class='header-box'><h1 style='color:#1e3d59; margin:0;'>Ribeira Vet Pro</h1><p style='margin:0;'>Sistema de Gestão • {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- 1. SESSÃO: TUTORES ---
if menu == "👤 Tutores":
    st.subheader("📝 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        id_t = f"T{len(st.session_state['clientes']) + 1:03d}"
        st.info(f"Código Gerado: **{id_t}**")
        nome = st.text_input("Nome do Cliente*")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        zap = c2.text_input("WhatsApp (Ex: 22985020463)*")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({"id": id_t, "nome": nome.upper(), "cpf": cpf, "zap": zap, "email": email, "endereco": end})
                st.success("Tutor salvo!")
            else: st.error("Nome e WhatsApp são obrigatórios.")

# --- 2. SESSÃO: PETS (PARÂMETROS COMPLETOS) ---
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pets")
    if not st.session_state['clientes']:
        st.warning("⚠️ Cadastre um Tutor primeiro.")
    else:
        with st.form("f_pet", clear_on_submit=True):
            id_p = f"P{len(st.session_state['pets']) + 1:03d}"
            st.info(f"Código do Pet: **{id_p}**")
            t_lista = {f"{c['id']} - {c['nome']}": c['id'] for c in st.session_state['clientes']}
            tutor_ref = st.selectbox("Proprietário*", list(t_lista.keys()))
            nome_p = st.text_input("Nome do Animal*")
            
            c1, c2, c3 = st.columns(3)
            raca = c1.selectbox("Raça", ["SRD", "Spitz Alemão", "Poodle", "Shih Tzu", "Yorkshire", "Bulldog", "Golden", "Outra"])
            sexo = c2.selectbox("Sexo", ["Macho", "Fêmea"])
            idade = c3.text_input("Idade")
            
            c4, c5 = st.columns(2)
            cor = c4.text_input("Cor do Pêlo")
            chip = c5.text_input("Microchip")
            
            castrado = st.radio("Animal Castrado?", ["Sim", "Não", "Não informado"], horizontal=True)
            
            if st.form_submit_button("✅ CADASTRAR PET"):
                if nome_p:
                    st.session_state['pets'].append({"id": id_p, "tutor": t_lista[tutor_ref], "nome": nome_p.upper(), "raca": raca, "sexo": sexo, "idade": idade, "castrado": castrado})
                    st.success(f"Pet {nome_p} cadastrado!")
                else: st.error("Nome do animal é obrigatório.")

# --- 3. SESSÃO: DASHBOARD ---
elif menu == "🏠 Dashboard":
    st.subheader("📊 Painel Geral")
    c1, c2 = st.columns(2)
    c1.metric("Tutores", len(st.session_state['clientes']))
    c2.metric("Pacientes", len(st.session_state['pets']))
    
    if st.session_state['clientes']:
        st.write("### Últimos Clientes")
        st.table(pd.DataFrame(st.session_state['clientes'])[['id', 'nome', 'zap']])
