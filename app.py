import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO E BANCO DE DADOS
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

if 'clientes' not in st.session_state: st.session_state['clientes'] = []
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'carrinho' not in st.session_state: st.session_state['carrinho'] = []
if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [
        {"Item": "CONSULTA CLÍNICA", "Preco": 150.0},
        {"Item": "VACINA V10", "Preco": 120.0},
        {"Item": "VACINA ANTIRRÁBICA", "Preco": 60.0}
    ]

# 2. MENU LATERAL
with st.sidebar:
    st.title("Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário IA", "💰 Financeiro"])

# 3. MÓDULO 1: TUTORES (COM CPF E BUSCA)
if menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    
    # Busca por nome
    busca = st.text_input("🔍 Buscar Cliente:")
    if busca:
        res = [c for c in st.session_state['clientes'] if busca.upper() in c['NOME']]
        if res: st.table(pd.DataFrame(res))

    with st.form("form_tutor_v12", clear_on_submit=True):
        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo *")
        zap = c2.text_input("Telefone")
        c3, c4 = st.columns([1, 1])
        cpf = c3.text_input("CPF")
        email = c4.text_input("E-mail")
        end = st.text_input("Endereço Completo")
        if st.form_submit_button("💾 Salvar Cadastro"):
            if nome:
                novo = {"NOME": nome.upper(), "CPF": cpf, "TEL": zap, "ENDEREÇO": end, "E-MAIL": email}
                st.session_state['clientes'].append(novo)
                st.session_state['clientes'] = sorted(st.session_state['clientes'], key=lambda x: x['NOME'])
                st.rerun()

    if st.session_state['clientes']:
        df_t = pd.DataFrame(st.session_state['clientes'])
        df_t.index = [f"{i+1:02d}" for i in range(len(df_t))]
        st.table(df_t)

# 4. MÓDULO 2: PETS
elif menu == "🐾 Pets":
    st.subheader("🐾 Gestão de Pacientes")
    with st.form("form_pet_v12"):
        c1, c2 = st.columns([3, 1])
        n_pet = c1.text_input("Nome do Pet *")
        esp = c2.selectbox("Espécie", ["Cão", "Gato", "Outro"])
        rac = st.text_input("Raça")
        if st.form_submit_button("💾 Salvar Pet"):
            if n_pet:
                st.session_state['pets'].append({"PET": n_pet.upper(), "ESPÉCIE": esp, "RAÇA": rac})
                st.rerun()
    if st.session_state['pets']:
        st.table(pd.DataFrame(st.session_state['pets']))

# 5. MÓDULO 4: FINANCEIRO (FORMATADO)
elif menu == "💰 Financeiro":
    st.markdown("<div style='border:2px solid black;padding:10px;text-align:center;'><b>CONSULTÓRIO RIBEIRA</b></div>", unsafe_allow_html=True)
    with st.expander("🔍 TABELA DE PREÇOS"):
        for i, p in enumerate(st.session_state['estoque']):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(p['Item'])
            c2.write(f"R$ {p['Preco']:.2f}")
            if c3.button("➕", key=f"btn_{i}"):
                st.session_state['carrinho'].append(p)
                st.rerun()
    if st.session_state['carrinho']:
        df_c = pd.DataFrame(st.session_state['carrinho'])
        df_c['Preco'] = df_c['Preco'].map('R$ {:,.2f}'.format)
        st.table(df_c.rename(columns={'Item': 'DESCRIÇÃO', 'Preco': 'VALOR'}))
        if st.button("🗑️ Limpar"):
            st.session_state['carrinho'] = []
            st.rerun()

# 6. MÓDULO 3: PRONTUÁRIO
else:
    st.subheader("📋 Prontuário (Ditado: Win+H)")
    st.text_area("Relato Clínico:", height=300)
# =========================================================
# MÓDULO 6: BACKUP (DRIVE EXTERNO)
# =========================================================
elif menu == "💾 Backup Externo":
    st.subheader("💾 Salvar no Pendrive/HD")
    
    # Clientes
    if st.session_state['clientes']:
        df_c = pd.DataFrame(st.session_state['clientes'])
        st.download_button("📥 Baixar Clientes (Excel)", df_c.to_csv(index=False).encode('utf-8-sig'), "clientes.csv", "text/csv")
    
    # Pets
    if st.session_state['pets']:
        df_p = pd.DataFrame(st.session_state['pets'])
        st.download_button("📥 Baixar Pets (Excel)", df_p.to_csv(index=False).encode('utf-8-sig'), "pets.csv", "text/csv")
