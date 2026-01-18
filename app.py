import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO INICIAL (Cura o NameError)
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

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

# 3. MÓDULO 1: TUTORES (CAMPOS RECUPERADOS)
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    busca = st.text_input("🔍 Buscar por Nome:")
    if busca:
        res = [c for c in st.session_state['clientes'] if busca.upper() in c['NOME']]
        if res: st.table(pd.DataFrame(res))
    
    with st.form("f_tutor_definitivo"):
        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo *")
        zap = c2.text_input("Telefone")
        
        c3, c4 = st.columns([1, 1])
        cpf = c3.text_input("CPF")
        email = c4.text_input("E-mail") # Recuperado conforme solicitado
        
        end = st.text_input("Endereço Completo") # Recuperado conforme solicitado
        
        if st.form_submit_button("💾 Salvar"):
            if nome:
                novo = {"NOME": nome.upper(), "CPF": cpf, "TEL": zap, "ENDEREÇO": end, "E-MAIL": email}
                st.session_state['clientes'].append(novo)
                st.session_state['clientes'] = sorted(st.session_state['clientes'], key=lambda x: x['NOME'])
                st.rerun()

    if st.session_state['clientes']:
        st.write("📋 **Lista Geral**")
        st.table(pd.DataFrame(st.session_state['clientes']))

# 4. MÓDULO 2: PETS
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    with st.form("f_pet_definitivo"):
        p = st.text_input("Nome do Pet *")
        e = st.selectbox("Espécie", ["Cão", "Gato", "Outro"])
        if st.form_submit_button("💾 Salvar Pet"):
            if p:
                st.session_state['pets'].append({"PET": p.upper(), "TIPO": e})
                st.rerun()
    if st.session_state['pets']:
        st.table(pd.DataFrame(st.session_state['pets']))

# 5. MÓDULO 6: BACKUP (DRIVE EXTERNO)
elif menu == "💾 Backup":
    st.subheader("💾 Exportar para Drive Externo")
    if st.session_state['clientes']:
        df_c = pd.DataFrame(st.session_state['clientes'])
        st.download_button("📥 Baixar Clientes (Excel)", df_c.to_csv(index=False).encode('utf-8-sig'), "clientes_vet.csv")
    if st.session_state['pets']:
        df_p = pd.DataFrame(st.session_state['pets'])
        st.download_button("📥 Baixar Pets (Excel)", df_p.to_csv(index=False).encode('utf-8-sig'), "pets_vet.csv")

# 6. MÓDULOS RESTANTES (PRONTUÁRIO E FINANCEIRO)
else:
    st.subheader("📋 Prontuário / 💰 Financeiro")
    st.info("Utilize as opções acima para registrar atendimentos ou orçamentos.")
