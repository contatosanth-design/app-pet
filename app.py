import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. CONFIGURAÇÃO E ESTILO PROFISSIONAL
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide", page_icon="🐾")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    html, body, [class*="css"] { font-size: 0.88rem !important; }
    .metric-card {
        background-color: white; padding: 15px; border-radius: 10px;
        border-left: 5px solid #22c55e; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center; color: #1e293b;
    }
    .card-red { border-left-color: #ef4444; }
    .card-blue { border-left-color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS
def carregar_dados():
    arquivo = 'banco_vet_v7.csv'
    if os.path.exists(arquivo):
        return pd.read_csv(arquivo)
    return pd.DataFrame(columns=["ID", "Nome Responsável", "CPF", "Telefone", "Animais", "Prontuário", "Data"])

if 'dados' not in st.session_state:
    st.session_state.dados = carregar_dados()

# 3. MENU LATERAL
with st.sidebar:
    st.markdown("# 🏥 Ribeira Vet Pro")
    menu = st.radio("Navegação", ["📊 Painel Geral", "📝 Cadastro", "⚕️ Prontuário & IA", "💊 Consultar Bulas"])
    st.divider()
    # Botão de Exportação (Backup Local)
    csv = st.session_state.dados.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Backup (Excel/CSV)", data=csv, file_name="backup_ribeira_vet.csv", mime="text/csv")

# 4. LÓGICA DAS PÁGINAS

if menu == "📊 Painel Geral":
    st.markdown("### 📈 Dashboard de Gestão")
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="metric-card card-blue"><strong>Consultas Hoje</strong><h2 style="margin:0; color:#3b82f6;">12</h2></div>', unsafe_allow_html=True)
    c2.markdown('<div class="metric-card"><strong>Clientes Ativos</strong><h2 style="margin:0; color:#22c55e;">'+str(len(st.session_state.dados))+'</h2></div>', unsafe_allow_html=True)
    c3.markdown('<div class="metric-card card-red"><strong>Alertas</strong><h2 style="margin:0; color:#ef4444;">03</h2></div>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown("#### 🔍 Lista Clicável de Clientes")
    df_editado = st.data_editor(st.session_state.dados, use_container_width=True, hide_index=True)
    if st.button("💾 Salvar Alterações"):
        st.session_state.dados = df_editado
        df_editado.to_csv('banco_vet_v7.csv', index=False)
        st.success("Dados sincronizados!")

elif menu == "📝 Cadastro":
    st.subheader("📝 Novo Registro Profissional")
    with st.form("form_cad"):
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome do Responsável")
        cpf = c1.text_input("CPF")
        tel = c2.text_input("Telefone")
        pets = c2.text_area("Animais (Nome, Raça, Idade)")
        if st.form_submit_button("Cadastrar e Salvar"):
            nova_linha = pd.DataFrame([{"ID": datetime.now().strftime("%Y%m%d"), "Nome Responsável": nome, "CPF": cpf, "Telefone": tel, "Animais": pets, "Prontuário": "", "Data": datetime.now().strftime("%d/%m/%Y")}])
            st.session_state.dados = pd.concat([st.session_state.dados, nova_linha], ignore_index=True)
            st.session_state.dados.to_csv('banco_vet_v7.csv', index=False)
            st.success("Cadastrado na Nuvem!")

elif menu == "⚕️ Prontuário & IA":
    st.subheader("⚕️ Assistente Clínico Inteligente")
    if not st.session_state.dados.empty:
        cliente = st.selectbox("Selecione o Paciente", st.session_state.dados["Nome Responsável"].unique())
        
        # Área da IA
        with st.expander("🤖 IA: Assistente de Diagnóstico", expanded=False):
            sintomas = st.text_area("Descreva os sintomas observados:")
            if st.button("Analisar com IA"):
                st.write("**Sugestão da IA:** Com base nos sintomas, considere exames de imagem e hemograma completo. Verifique protocolos para zoonoses locais.")
        
        # Prontuário
        st.divider()
        idx = st.session_state.dados[st.session_state.dados["Nome Responsável"] == cliente].index[0]
        hist = st.text_area("Evolução do Prontuário", value=st.session_state.dados.at[idx, "Prontuário"], height=250)
        if st.button("Gravar Prontuário"):
            st.session_state.dados.at[idx, "Prontuário"] = hist
            st.session_state.dados.to_csv('banco_vet_v7.csv', index=False)
            st.success("Histórico Clínico Gravado!")
    else:
        st.warning("Cadastre um cliente primeiro.")

elif menu == "💊 Consultar Bulas":
    st.subheader("💊 Dicionário Farmacológico Rápido")
    busca_med = st.text_input("Buscar medicamento (ex: Amoxicilina, Meloxicam)")
    st.info("Aqui você integrará links de bulários oficiais ou uma base própria de medicamentos.")
    # Exemplo de tabela de consulta rápida
    bulas = {"Amoxicilina": "Antibiótico. Dose: 12.5 a 25mg/kg.", "Meloxicam": "Anti-inflamatório. Dose: 0.1 a 0.2mg/kg."}
    if busca_med in bulas:
        st.write(f"**Indicação:** {bulas[busca_med]}")
