import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicializa as listas se não existirem
for k in ['clientes', 'pets', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

# Estoque fixo inicial
if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [
        {"Item": "CONSULTA CLÍNICA", "Preco": 150.0},
        {"Item": "VACINA V10", "Preco": 120.0},
        {"Item": "VACINA ANTIRRÁBICA", "Preco": 60.0}
    ]

# 2. MENU LATERAL
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"])

# 3. MÓDULO 1: TUTORES (COM CPF E BUSCA)
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    busca = st.text_input("🔍 Buscar por Nome:")
    if busca:
        res = [c for c in st.session_state['clientes'] if busca.upper() in c['NOME']]
        if res: st.table(pd.DataFrame(res))
    
    with st.form("f_tutor"):
        n = st.text_input("Nome Completo *")
        c = st.text_input("CPF")
        t = st.text_input("Telefone")
        if st.form_submit_button("💾 Salvar"):
            if n:
                st.session_state['clientes'].append({"NOME": n.upper(), "CPF": c, "TEL": t})
                st.session_state['clientes'] = sorted(st.session_state['clientes'], key=lambda x: x['NOME'])
                st.rerun()
    if st.session_state['clientes']: st.table(pd.DataFrame(st.session_state['clientes']))

# 4. MÓDULO 2: PETS
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    with st.form("f_pet"):
        p = st.text_input("Nome do Pet *")
        e = st.selectbox("Espécie", ["Cão", "Gato", "Outro"])
        if st.form_submit_button("💾 Salvar Pet"):
            if p:
                st.session_state['pets'].append({"PET": p.upper(), "TIPO": e})
                st.rerun()
    if st.session_state['pets']: st.table(pd.DataFrame(st.session_state['pets']))

# 5. MÓDULO 3: PRONTUÁRIO
elif menu == "📋 Prontuário":
    st.subheader("📋 Prontuário (Ditado: Win+H)")
    st.text_area("Descreva o atendimento clínico:", height=300)

# 6. MÓDULO 4: FINANCEIRO
elif menu == "💰 Financeiro":
    st.subheader("💰 Orçamento e Preços")
    for i, item in enumerate(st.session_state['estoque']):
        if st.button(f"➕ {item['Item']} (R$ {item['Preco']:.2f})", key=i):
            st.session_state['carrinho'].append(item)
            st.success(f"{item['Item']} adicionado!")
    if st.session_state['carrinho']:
        st.divider()
        st.table(pd.DataFrame(st.session_state['carrinho']))
        if st.button("🗑️ Limpar Tudo"):
            st.session_state['carrinho'] = []; st.rerun()

# 7. MÓDULO 6: BACKUP (DRIVE EXTERNO)
elif menu == "💾 Backup":
    st.subheader("💾 Exportar para Drive Externo")
    if st.session_state['clientes']:
        df_c = pd.DataFrame(st.session_state['clientes'])
        st.download_button("📥 Baixar Excel de Clientes", df_c.to_csv(index=False).encode('utf-8-sig'), "clientes.csv")
    if st.session_state['pets']:
        df_p = pd.DataFrame(st.session_state['pets'])
        st.download_button("📥 Baixar Excel de Pets", df_p.to_csv(index=False).encode('utf-8-sig'), "pets.csv")
