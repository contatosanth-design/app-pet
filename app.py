import streamlit as st
from datetime import datetime
import urllib.parse
import ast

# 1. CONFIGURAÇÃO E MEMÓRIA REFORÇADA
st.set_page_config(page_title="Ribeira Vet Pro", layout="centered")

# Garante que as listas existam
for k in ['clientes', 'pets', 'historico', 'caixa', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"

# --- 2. MENU LATERAL ---
with st.sidebar:
    st.title("🐾 Ribeira Vet")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    escolha = st.radio("MENU", opcoes, index=opcoes.index(st.session_state.aba_atual))
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- 3. MÓDULO TUTORES (COM CPF GARANTIDO) ---
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    t_sel = st.selectbox("Buscar Cliente:", ["--- Novo ---"] + nomes)
    
    # Carrega dados existentes (inclusive CPF)
    v_nome, v_cpf, v_tel, v_email, v_end = ("", "", "", "", "")
    if t_sel != "--- Novo ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == t_sel)
        v_nome = c.get('NOME','')
        v_cpf = c.get('CPF','')
        v_tel = c.get('TEL','')
        v_email = c.get('EMAIL','')
        v_end = c.get('END','')

    with st.form("f_tutor_v104"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        f_cpf = st.text_input("CPF (Importante para Recibos)", value=v_cpf)
        f_tel = st.text_input("WhatsApp (DDD+Número)", value=v_tel)
        f_email = st.text_input("E-mail", value=v_email)
        f_end = st.text_area("Endereço Completo", value=v_end)
        
        if st.form_submit_button("💾 SALVAR DADOS", use_container_width=True):
            if f_nome:
                # Salva todos os parâmetros na lista
                d = {"NOME": f_nome, "CPF": f_cpf, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if t_sel == "--- Novo ---": 
                    st.session_state['clientes'].append(d)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == t_sel: st.session_state['clientes'][i] = d
                st.success(f"Dados de {f_nome} (CPF: {f_cpf}) salvos!")
                st.rerun()

# --- Mantenha os outros módulos (Pets, Prontuário, Financeiro e Backup) como na v10.3 ---
# ... (O restante do código permanece igual para evitar novos erros de sintaxe)
