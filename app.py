import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- CSS PARA CORES E FONTES (BRANCO NO MENU) ---
st.markdown("""
    <style>
    .main { background-color: #f1f3f6; }
    [data-testid="stSidebar"] { background-color: #1e3d59 !important; }
    
    /* Força o texto do menu lateral a ficar branco e visível */
    [data-testid="stSidebar"] .stRadio label p {
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    
    /* Títulos e textos gerais no menu */
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p {
        color: white !important;
    }

    .header-box { 
        background-color: white; padding: 20px; border-radius: 10px; 
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px;
        border-left: 6px solid #2e7bcf;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO BANCO (Persistente na sessão) ---
if 'clientes' not in st.session_state: st.session_state['clientes'] = {}
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'historico' not in st.session_state: st.session_state['historico'] = []
if 'estoque' not in st.session_state: st.session_state['estoque'] = []

# --- MENU LATERAL ---
with st.sidebar:
    # Logo do cachorrinho que você aprovou
    st.image("https://cdn-icons-png.flaticon.com/512/620/620851.png", width=120)
    st.markdown("<h2 style='text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("NAVEGAÇÃO", [
        "🏠 Dashboard", "👤 Tutores", "🐾 Pacientes", 
        "🩺 Prontuário IA", "📦 Estoque & Vacinas", 
        "💰 Financeiro", "🎂 Aniversários"
    ])

# --- CABEÇALHO ---
st.markdown(f"<div class='header-box'><h1 style='color:#1e3d59; margin:0;'>Ribeira Vet Pro</h1><p style='margin:0; color:#666;'>Gestão Veterinária • {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- TELAS ---

if menu == "🏠 Dashboard":
    c1, c2 = st.columns(2)
    c1.metric("Total de Tutores", len(st.session_state['clientes']))
    c2.metric("Total de Pacientes", len(st.session_state['pets']))
    
    if st.session_state['historico']:
        st.subheader("📋 Histórico Recente")
        df = pd.DataFrame(st.session_state['historico'])
        st.dataframe(df, use_container_width=True)
        # Download simples para evitar o erro de ModuleNotFoundError
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Baixar Dados (Excel/CSV)", data=csv, file_name="atendimentos.csv", mime="text/csv")
    else:
        st.info("Cadastre um atendimento no Prontuário IA para visualizar os dados aqui.")

elif menu == "👤 Tutores":
    st.subheader("Cadastro de Proprietários")
    with st.form("tutor_form", clear_on_submit=True):
        nome = st.text_input("Nome do Tutor")
        c1, c2 = st.columns(2)
        zap, cpf = c1.text_input("WhatsApp"), c2.text_input("CPF")
        end = st.text_area("Endereço")
        if st.form_submit_button("Salvar Tutor"):
            st.session_state['clientes'][nome] = {"zap": zap, "cpf": cpf, "end": end}
            st.success(f"Tutor {nome} salvo!")

elif menu == "🐾 Pacientes":
    st.subheader("Cadastro de Pets")
    if not st.session_state['clientes']: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("pet_form", clear_on_submit=True):
            dono = st.selectbox("Escolha o Tutor", list(st.session_state['clientes'].keys()))
            nome_p = st.text_input("Nome do Pet")
            nasc = st.date_input("Nascimento", format="DD/MM/YYYY")
            if st.form_submit_button("Salvar Pet"):
                st.session_state['pets'].append({"nome": nome_p, "tutor": dono, "nasc": nasc})
                st.success(f"Pet {nome_p} registrado!")

elif menu == "🩺 Prontuário IA":
    st.subheader("Novo Atendimento")
    st.info("🎤 Clique no campo abaixo e use 'Windows + H' para ditar.")
    if not st.session_state['pets']: st.info("Cadastre um pet primeiro.")
    else:
        with st.form("atend_form"):
            pet = st.selectbox("Paciente", [p['nome'] for p in st.session_state['pets']])
            c1, c2 = st.columns(2)
            peso, temp = c1.text_input("Peso (kg)"), c2.text_input("Temp (°C)")
            relato = st.text_area("Evolução Clínica / Diagnóstico", height=200)
            if st.form_submit_button("Salvar e Ir para Início"):
                st.session_state['historico'].append({
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Paciente": pet, "Peso": peso, "Temp": temp, "Diagnóstico": relato
                })
                st.success("Salvo com sucesso!")

# --- (Demais abas permanecem preparadas para uso) ---
