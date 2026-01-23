import streamlit as st
from datetime import datetime
import urllib.parse

# 1. CONFIGURAÇÃO E MEMÓRIA
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicialização de todas as gavetas de memória
for k in ['clientes', 'pets', 'historico', 'caixa', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"

# --- 2. MENU LATERAL ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    escolha = st.radio("NAVEGAÇÃO", opcoes, index=opcoes.index(st.session_state.aba_atual))
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- 3. MÓDULO TUTORES (AGORA COMPLETO) ---
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes (Cadastro Completo)")
    
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    t_sel = st.selectbox("Buscar ou Editar Cliente:", ["--- Novo ---"] + nomes)
    
    # Preenche os campos se o cliente já existir
    v_nome, v_cpf, v_tel, v_email, v_end = ("", "", "", "", "")
    if t_sel != "--- Novo ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == t_sel)
        v_nome = c.get('NOME','')
        v_cpf = c.get('CPF','')
        v_tel = c.get('TEL','')
        v_email = c.get('EMAIL','')
        v_end = c.get('END','')

    with st.form("f_tutor_completo"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        f_cpf = st.text_input("CPF (Para Recibos)", value=v_cpf)
        col1, col2 = st.columns(2)
        f_tel = col1.text_input("WhatsApp (DDD + Número)", value=v_tel)
        f_email = col2.text_input("E-mail", value=v_email).lower()
        f_end = st.text_area("Endereço Completo", value=v_end)
        
        if st.form_submit_button("💾 Salvar Dados do Cliente"):
            if f_nome:
                dados = {"NOME": f_nome, "CPF": f_cpf, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if t_sel == "--- Novo ---": 
                    st.session_state['clientes'].append(dados)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == t_sel: st.session_state['clientes'][i] = dados
                st.success(f"Dados de {f_nome} salvos com sucesso!")
                st.rerun()

# --- (Mantenha os módulos de Pets, Prontuário e Financeiro da v9.7) ---
# ...
