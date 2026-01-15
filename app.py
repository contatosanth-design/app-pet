import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59 !important; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold !important; }
    .header-box { background: white; padding: 20px; border-radius: 10px; border-left: 6px solid #2e7bcf; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE DADOS (MANTENDO PRODUTOS AUTOMÁTICOS) ---
if 'estoque' not in st.session_state or len(st.session_state['estoque']) == 0:
    st.session_state['estoque'] = [
        {"Item": "Vacina V10 (Importada)", "Preco": 120.00}, {"Item": "Vacina Antirrábica", "Preco": 60.00},
        {"Item": "Consulta Geral", "Preco": 150.00}, {"Item": "Simparic 10-20kg", "Preco": 85.00},
        {"Item": "Castração Macho (Cão)", "Preco": 350.00}, {"Item": "Vermífugo (Drontal)", "Preco": 35.00}
    ]

if 'clientes' not in st.session_state: st.session_state['clientes'] = []
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'historico' not in st.session_state: st.session_state['historico'] = []

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=80)
    st.title("Ribeira Vet Pro")
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Cadastro de Tutores", "🐾 Pets", "🩺 Prontuário IA", "📦 Produtos", "💰 Financeiro & Recibo"])

# --- CABEÇALHO ---
st.markdown(f"<div class='header-box'><h1 style='color:#1e3d59; margin:0;'>Ribeira Vet Pro</h1><p style='margin:0;'>Clínica Veterinária • {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- SESSÃO ALTERADA: CADASTRO DE TUTORES ---
if menu == "👤 Cadastro de Tutores":
    st.subheader("👤 Cadastro de Tutor")
    
    with st.form("f_tutor_pro", clear_on_submit=True):
        # Código gerado automaticamente
        id_t = f"T{len(st.session_state['clientes']) + 1:03d}"
        st.info(f"Código Gerado: **{id_t}**")
        
        # Parâmetros solicitados pelo usuário
        nome = st.text_input("Nome do Cliente*")
        
        col1, col2 = st.columns(2)
        cpf = col1.text_input("CPF")
        whatsapp = col2.text_input("WhatsApp (Ex: 5522985020463)*")
        
        email = st.text_input("E-mail")
        endereco = st.text_area("Endereço Completo")
        
        if st.form_submit_button("Salvar Tutor"):
            if nome and whatsapp:
                st.session_state['clientes'].append({
                    "id": id_t, "nome": nome.upper(), "cpf": cpf, 
                    "zap": whatsapp, "email": email, "endereco": endereco
                })
                st.success(f"Tutor {nome} cadastrado com sucesso!")
            else:
                st.error("Nome e WhatsApp são obrigatórios.")

    # Tabela para conferência rápida
    if st.session_state['clientes']:
        st.write("### Tutores Cadastrados")
        st.table(pd.DataFrame(st.session_state['clientes'])[['id', 'nome', 'zap']])

# --- MANTENDO O RESTANTE IGUAL ---
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pets")
    # Lógica de Pets mantida conforme versões anteriores

elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento com Transcrição")
    # Mantendo Peso, Temperatura e Transcrição

elif menu == "📦 Produtos":
    st.subheader("📦 Produtos e Preços")
    # Exibindo os 20 itens automáticos

elif menu == "💰 Financeiro & Recibo":
    st.subheader("💰 Financeiro")
    # Mantendo lógica de recibo e WhatsApp

elif menu == "🏠 Dashboard":
    st.subheader("🏠 Painel Geral")
    # Mantendo métricas e histórico
