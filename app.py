import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. FORÇAR TEMA CLARO E CORES VIVAS (PARA NÃO FICAR TUDO CINZA)
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide", page_icon="🏥")

st.markdown("""
    <style>
    /* Reset de Cores para ignorar o Modo Escuro do Navegador */
    .stApp { background-color: #FFFFFF !important; color: #1E293B !important; }
    
    /* Cabeçalho Profissional */
    .header-box {
        background-color: #075E54; padding: 20px; border-radius: 10px;
        color: white; text-align: center; margin-bottom: 25px;
    }

    /* Cartões de Métricas Coloridos (Igual ao seu exemplo) */
    .card {
        padding: 20px; border-radius: 10px; color: white;
        text-align: center; font-weight: bold; box-shadow: 4px 4px 10px rgba(0,0,0,0.1);
    }
    .vencido { background-color: #FF5252; } /* Vermelho */
    .pendente { background-color: #FFAB40; } /* Laranja */
    .hoje { background-color: #448AFF; } /* Azul */
    .total { background-color: #4CAF50; } /* Verde */

    /* Ajuste de Tabelas e Inputs */
    .stTextInput>div>div>input { background-color: #F8F9FA !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS
def carregar_dados():
    if os.path.exists('banco_vet_oficial.csv'):
        return pd.read_csv('banco_vet_oficial.csv')
    return pd.DataFrame(columns=["ID", "Responsável", "CPF", "Endereço", "Animais", "Prontuário"])

if 'dados' not in st.session_state:
    st.session_state.dados = carregar_dados()

# 3. NAVEGAÇÃO COM ÍCONES
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=100)
    st.markdown("### 🏥 MENU GESTÃO")
    menu = st.radio("Selecione:", ["📊 Painel Administrativo", "📝 Cadastrar Cliente", "⚕️ Prontuário & IA", "💊 Bulário Digital"])
    st.divider()
    csv = st.session_state.dados.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Exportar para Excel/CSV", data=csv, file_name="backup_vet.csv")

# 4. PÁGINAS

if menu == "📊 Painel Administrativo":
    st.markdown('<div class="header-box"><h1>🐾 Ribeira Vet Pro - Painel de Controle</h1></div>', unsafe_allow_html=True)
    
    # OS CARDS COLORIDOS QUE VOCÊ PEDIU
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown('<div class="card vencido">VENCIDOS<br><h2>15</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="card pendente">PENDENTES<br><h2>08</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="card hoje">CONSULTAS HOJE<br><h2>12</h2></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="card total">CLIENTES<br><h2>'+str(len(st.session_state.dados))+'</h2></div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("📋 Lista de Clientes e Pacientes")
    # Tabela Clicável para correção imediata
    df_edit = st.data_editor(st.session_state.dados, use_container_width=True, hide_index=True)
    if st.button("💾 Salvar Alterações na Nuvem"):
        st.session_state.dados = df_edit
        df_edit.to_csv('banco_vet_oficial.csv', index=False)
        st.success("Dados atualizados!")

elif menu == "📝 Cadastrar Cliente":
    st.markdown("### 📝 Ficha de Cadastro (Responsável e Animal)")
    with st.form("cad_form"):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome do Responsável")
        cpf = col1.text_input("CPF")
        end = col2.text_area("Endereço Completo")
        pets = st.text_input("Animais (Nome, Espécie, Raça)")
        
        if st.form_submit_button("Finalizar Registro"):
            nova_linha = pd.DataFrame([{"ID": datetime.now().strftime("%y%m%d%H%M"), "Responsável": nome, "CPF": cpf, "Endereço": end, "Animais": pets, "Prontuário": ""}])
            st.session_state.dados = pd.concat([st.session_state.dados, nova_linha], ignore_index=True)
            st.session_state.dados.to_csv('banco_vet_oficial.csv', index=False)
            st.balloons()

elif menu == "⚕️ Prontuário & IA":
    st.markdown("### ⚕️ Prontuário Digital e Assistência IA")
    if not st.session_state.dados.empty:
        escolha = st.selectbox("Buscar Paciente:", st.session_state.dados["Responsável"])
        # Aqui entra a lógica de IA e o texto do prontuário que discutimos
        st.info("💡 Dica da IA: Verifique o histórico de vacinação deste paciente.")
        st.text_area("Evolução Médica:", height=300)
    else:
        st.warning("Nenhum cliente cadastrado.")

elif menu == "💊 Bulário Digital":
    st.markdown("### 💊 Consulta Rápida de Medicamentos")
    st.text_input("Digite o nome do remédio:")
    st.write("Exemplo: **Apoquel** - Antipruriginoso. Dose sugerida: 0.4 a 0.6 mg/kg.")
