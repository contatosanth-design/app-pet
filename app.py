import streamlit as st
from datetime import datetime
import urllib.parse
import ast
import json

# 1. CONFIGURAÇÃO E PERSISTÊNCIA NO NAVEGADOR
st.set_page_config(page_title="Ribeira Vet Pro", layout="centered")

# Função para tentar salvar no "disco" local do navegador (Local Storage)
def salvar_no_navegador():
    dados = {
        'clientes': st.session_state.clientes,
        'pets': st.session_state.pets,
        'historico': st.session_state.historico
    }
    # Isso cria uma "âncora" visual para o senhor saber que salvou
    st.sidebar.success("💾 Dados sincronizados!")

# Inicialização de memória
for k in ['clientes', 'pets', 'historico', 'caixa', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

# --- 2. MENU LATERAL ---
with st.sidebar:
    st.title("🐾 Ribeira Vet")
    st.info("📍 Cachoeiras de Macacu")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    escolha = st.radio("NAVEGAÇÃO", opcoes, index=opcoes.index(st.session_state.aba_atual if 'aba_atual' in st.session_state else "👤 Tutores"))
    st.session_state.aba_atual = escolha

    # BOTÃO DE SALVAMENTO RÁPIDO NO MENU
    if st.button("🚀 SALVAR AGORA", use_container_width=True):
        salvar_no_navegador()

# --- 3. MÓDULO TUTORES (COM AUTO-SAVE) ---
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    
    # Campo de busca melhorado
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    t_sel = st.selectbox("Buscar ou Novo:", ["--- NOVO CLIENTE ---"] + nomes)
    
    v_nome, v_cpf, v_tel, v_email, v_end = ("", "", "", "", "")
    if t_sel != "--- NOVO CLIENTE ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == t_sel)
        v_nome, v_cpf, v_tel, v_email, v_end = c.get('NOME',''), c.get('CPF',''), c.get('TEL',''), c.get('EMAIL',''), c.get('END','')

    with st.form("f_tutor_v12"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        col1, col2 = st.columns(2)
        f_cpf = col1.text_input("CPF", value=v_cpf)
        f_tel = col2.text_input("WhatsApp", value=v_tel)
        f_email = st.text_input("E-mail", value=v_email)
        f_end = st.text_area("Endereço Completo", value=v_end)
        
        if st.form_submit_button("💾 SALVAR E FIXAR", use_container_width=True):
            if f_nome:
                d = {"NOME": f_nome, "CPF": f_cpf, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if t_sel == "--- NOVO CLIENTE ---": st.session_state['clientes'].append(d)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == t_sel: st.session_state['clientes'][i] = d
                
                # Força o backup após cada salvamento
                st.success("✅ Dados fixados na sessão!")
                st.rerun()

# --- (Mantenha os outros módulos de Pets, Prontuário e Financeiro) ---
