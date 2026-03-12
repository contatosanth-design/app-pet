import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide", page_icon="🐾")

# 2. ESTILO CSS (CORRIGIDO)
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    html, body, [class*="css"] { font-size: 0.85rem !important; }
    
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        text-align: center;
        color: #333;
    }
    .card-red { border-left-color: #d32f2f; }
    .card-orange { border-left-color: #f57c00; }
    .card-blue { border-left-color: #1976d2; }
    </style>
    """, unsafe_allow_html=True)

# 3. BANCO DE DADOS SIMPLIFICADO
def carregar_dados():
    if os.path.exists('responsaveis.csv'):
        return pd.read_csv('responsaveis.csv')
    return pd.DataFrame(columns=["ID", "Nome", "CPF", "Endereço", "Animais", "Status"])

if 'dados' not in st.session_state:
    st.session_state.dados = carregar_dados()

# 4. BARRA LATERAL
with st.sidebar:
    st.title("🏥 Ribeira Vet")
    menu = st.radio("Navegação", ["📊 Painel Geral", "📝 Cadastros", "⚕️ Prontuários"])

# 5. CONTEÚDO
if menu == "📊 Painel Geral":
    st.markdown("### 📈 Dashboard de Gestão")
    
    # Cartões Coloridos Estilo o Exemplo que você enviou
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card card-red"><strong>Vencidos</strong><h2 style="color:#d32f2f; margin:0;">15</h2></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card card-orange"><strong>Pendentes</strong><h2 style="color:#f57c00; margin:0;">08</h2></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card card-blue"><strong>Consultas Hoje</strong><h2 style="color:#1976d2; margin:0;">12</h2></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><strong>Total Clientes</strong><h2 style="color:#2E7D32; margin:0;">'+str(len(st.session_state.dados))+'</h2></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 🔍 Lista de Clientes (Clique para editar)")
    
    # Tabela Editável
    df_editado = st.data_editor(st.session_state.dados, use_container_width=True, num_rows="dynamic")
    
    if st.button("💾 Salvar Alterações"):
        st.session_state.dados = df_editado
        df_editado.to_csv('responsaveis.csv', index=False)
        st.success("Dados salvos!")

else:
    st.info("Página em construção... Use o Painel Geral para ver o novo visual!")
