import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO (ESSENCIAL PARA NÃO DAR NAMEERROR)
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

# 2. MENU LATERAL
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"])

# 3. MÓDULO 1: TUTORES (ENDEREÇO E E-MAIL RECUPERADOS)
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    busca = st.text_input("🔍 Buscar por Nome:")
    if busca:
        res = [c for c in st.session_state['clientes'] if busca.upper() in c['NOME']]
        if res: st.table(pd.DataFrame(res))
    
    with st.form("f_tutor_v16"):
        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo *")
        zap = c2.text_input("Telefone")
        
        c3, c4 = st.columns([1, 1])
        cpf = c3.text_input("CPF")
        email = c4.text_input("E-mail") # RESTAURADO
        
        end = st.text_input("Endereço Completo") # RESTAURADO
        
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
    with st.form("f_pet_v16"):
        p = st.text_input("Nome do Pet *")
        e = st.selectbox("Espécie", ["Cão", "Gato", "Outro"])
        if st.form_submit_button("💾 Salvar Pet"):
            if p:
                st.session_state['pets'].append({"PET": p.upper(), "TIPO": e})
                st.rerun()
    if st.session_state['pets']: st.table(pd.DataFrame(st.session_state['pets']))

# 5. MÓDULO 6: BACKUP (AGORA COMPLETO)
elif menu == "💾 Backup":
    st.subheader("💾 Exportar para Drive Externo")
    if st.session_state['clientes']:
        df_c = pd.DataFrame(st.session_state['clientes'])
        st.download_button("📥 Baixar Lista Completa", df_c.to_csv(index=False).encode('utf-8-sig'), "clientes_ribeira.csv")

# RESTANTE DOS MÓDULOS
else:
    st.subheader("📋 Prontuário / 💰 Financeiro")
    st.info("Selecione os módulos acima para operar.")
