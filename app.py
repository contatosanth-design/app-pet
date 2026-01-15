import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- CSS PARA ESTILO PROFISSIONAL (Inspirado na sua imagem) ---
st.markdown("""
    <style>
    .main { background-color: #f1f3f6; }
    [data-testid="stSidebar"] { background-color: #1e3d59; border-right: 2px solid #2e7bcf; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .header-box { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #e1e4e8; border-radius: 5px 5px 0 0; padding: 10px 20px; color: #1e3d59; }
    .stTabs [aria-selected="true"] { background-color: #2e7bcf !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
for key in ['clientes', 'pets', 'historico', 'estoque']:
    if key not in st.session_state: st.session_state[key] = {} if key == 'clientes' else []

# --- BARRA LATERAL (LOGO E MENU) ---
with st.sidebar:
    # Logo Provisório (Substitua o link abaixo pelo seu link do GitHub quando quiser)
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=100)
    st.markdown("<h2 style='color: white; text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pacientes", "🩺 Prontuário IA", "📦 Estoque", "💰 Financeiro", "🎂 Aniversários"])

# --- CONTEÚDO PRINCIPAL ---
st.markdown(f"<div class='header-box'><h1>Ribeira Vet Pro</h1><p>Sistema de Gestão de Dados - {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- LÓGICA DE ABAS/MENU ---
if menu == "🏠 Dashboard":
    st.subheader("Painel Geral")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tutores", len(st.session_state['clientes']))
    c2.metric("Pacientes", len(st.session_state['pets']))
    
    if st.session_state['historico']:
        df = pd.DataFrame(st.session_state['historico'])
        st.download_button("📥 Baixar Planilha Excel", data=df.to_csv().encode('utf-8'), file_name="dados_ribeira.csv")
        st.dataframe(df)

elif menu == "👤 Tutores":
    st.subheader("Cadastro de Tutores")
    with st.form("tutor"):
        nome = st.text_input("Nome Completo")
        c1, c2 = st.columns(2)
        cpf, zap = c1.text_input("CPF"), c2.text_input("WhatsApp")
        end = st.text_area("Endereço")
        if st.form_submit_button("Salvar Tutor"):
            st.session_state['clientes'][nome] = {"cpf": cpf, "zap": zap, "end": end}
            st.success("Salvo!")

elif menu == "🩺 Prontuário IA":
    st.subheader("Atendimento com Transcrição por Voz")
    st.info("🎤 Atalho: Clique no campo e aperte 'Windows + H' para ditar.")
    with st.form("prontuario"):
        paciente = st.selectbox("Paciente", [p['nome'] for p in st.session_state['pets']] if st.session_state['pets'] else ["Nenhum cadastrado"])
        c1, c2 = st.columns(2)
        peso, temp = c1.text_input("Peso (kg)"), c2.text_input("Temp (°C)")
        transcricao = st.text_area("Transcrição da Consulta / Diagnóstico", height=250)
        if st.form_submit_button("Finalizar e Arquivar"):
            st.session_state['historico'].append({"Data": datetime.now().strftime("%d/%m/%Y"), "Pet": paciente, "Relato": transcricao})
            st.success("Arquivado!")

elif menu == "📦 Estoque":
    st.subheader("Medicamentos, Vacinas e Serviços")
    with st.form("estoque"):
        item = st.text_input("Nome do Item")
        preco = st.number_input("Preço", min_value=0.0)
        if st.form_submit_button("Adicionar"):
            st.session_state['estoque'].append({"Item": item, "Preco": preco})
    st.table(st.session_state['estoque'])

elif menu == "💰 Financeiro":
    st.subheader("Fechamento de Conta")
    if not st.session_state['estoque']: st.info("Cadastre itens no estoque primeiro.")
    else:
        selecionados = st.multiselect("Itens utilizados", [i['Item'] for i in st.session_state['estoque']])
        total = sum(i['Preco'] for i in st.session_state['estoque'] if i['Item'] in selecionados)
        st.markdown(f"## Total: R$ {total:.2f}")

elif menu == "🎂 Aniversários":
    st.subheader("Felicitações do Dia")
    st.info("Aqui aparecerão os aniversariantes cadastrados.")
