import streamlit as st
import pandas as pd

# CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Ribeira Vet Pro v7.0", layout="wide")

# BANCO DE DATOS (MEMÓRIA)
if 'clientes' not in st.session_state: st.session_state['clientes'] = []
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'carrinho' not in st.session_state: st.session_state['carrinho'] = []
if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [
        {"Item": "VACINA V10 (IMPORTADA)", "Preco": 120.0},
        {"Item": "VACINA ANTIRRÁBICA", "Preco": 60.0},
        {"Item": "CONSULTA CLÍNICA", "Preco": 150.0},
        {"Item": "HEMOGRAMA COMPLETO", "Preco": 95.0},
        {"Item": "CASTRAÇÃO MACHO", "Preco": 350.0}
    ]

# MENU LATERAL
with st.sidebar:
    st.title("Ribeira Vet Pro")
    st.info("Versão 7.0 - Estável")
    menu = st.sidebar.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário IA", "💰 Financeiro"])

# MÓDULO 1: TUTORES (ESTÁVEL)
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Tutores")
    with st.form("form_tutor_v7"):
        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo *")
        zap = c2.text_input("Telefone")
        end = st.text_input("Endereço Completo")
        if st.form_submit_button("Salvar Cadastro"):
            if nome:
                st.session_state['clientes'].append({"NOME": nome.upper(), "TEL": zap, "ENDEREÇO": end})
                st.success("Tutor cadastrado!")
                st.rerun()

    if st.session_state['clientes']:
        st.table(pd.DataFrame(st.session_state['clientes']))

# MÓDULO 2: PETS (CORRIGIDO)
elif menu == "🐾 Pets":
    st.subheader("🐾 Gestão de Pacientes")
    with st.form("form_pet_v7"):
        c1, c2 = st.columns([3, 1])
        nome_p = c1.text_input("Nome do Pet *")
        esp = c2.selectbox("Espécie", ["Cão", "Gato", "Outro"])
        rac = st.text_input("Raça")
        if st.form_submit_button("Salvar Pet"):
            if nome_p:
                st.session_state['pets'].append({"PET": nome_p.upper(), "ESPÉCIE": esp, "RAÇA": rac})
                st.success("Pet cadastrado!")
                st.rerun()
    if st.session_state['pets']:
        st.table(pd.DataFrame(st.session_state['pets']))

# MÓDULO 4: FINANCEIRO (PREÇOS FORMATADOS)
elif menu == "💰 Financeiro":
    st.markdown("""<div style='border: 2px solid black; padding: 10px; text-align: center;'>
                <b>CONSULTÓRIO VETERINÁRIO RIBEIRA</b><br>CRVV-RJ 9862 Ricardo Santos</div>""", unsafe_allow_html=True)
    
    with st.expander("🔍 TABELA DE PREÇOS"):
        for idx, item in enumerate(st.session_state['estoque']):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(item['Item'])
            c2.write(f"R$ {item['Preco']:.2f}")
            if c3.button("➕", key=f"add_{idx}"):
                st.session_state['carrinho'].append(item)
                st.rerun()

    if st.session_state['carrinho']:
        st.write("### 📝 Orçamento Atual")
        df_c = pd.DataFrame(st.session_state['carrinho'])
        df_c['Preco'] = df_c['Preco'].map('R$ {:,.2f}'.format)
        st.table(df_c.rename(columns={'Item': 'DESCRIÇÃO', 'Preco': 'VALOR'}))
        
        total = sum(i['Preco'] for i in st.session_state['carrinho'])
        st.write(f"**TOTAL: R$ {total:.2f}**")
        if st.button("🗑️ Limpar"):
            st.session_state['carrinho'] = []
            st.rerun()
