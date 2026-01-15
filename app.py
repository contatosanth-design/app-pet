import streamlit as st
import pandas as pd
from datetime import datetime, date

# Configurações iniciais
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicialização do banco de dados invisível
for key in ['clientes', 'pets', 'historico', 'estoque']:
    if key not in st.session_state: st.session_state[key] = []

# Menu Lateral (A "âncora" do sistema)
with st.sidebar:
    st.title("Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "💰 Financeiro"])

# Função para calcular idade automaticamente
def calcular_idade(nasc):
    hoje = date.today()
    return hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
