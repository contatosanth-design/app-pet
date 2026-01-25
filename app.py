import streamlit as st
from datetime import datetime
import urllib.parse
import ast

# 1. CONFIGURAÇÃO MOBILE
st.set_page_config(page_title="Ribeira Vet Pro", layout="centered")

# Inicialização de memória
for k in ['clientes', 'pets', 'historico', 'caixa', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

# --- NOVO: AVISO DE DADOS ZERADOS ---
if not st.session_state.clientes:
    st.warning("⚠️ O sistema reiniciou. Vá em '💾 Backup' para restaurar seus dados.")

if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"

# --- 2. MENU LATERAL ---
with st.sidebar:
    st.title("🐾 Ribeira Vet")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    escolha = st.radio("MENU", opcoes, index=opcoes.index(st.session_state.aba_atual))
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- 7. MÓDULO BACKUP E RESTAURAÇÃO (O MAIS IMPORTANTE AGORA) ---
elif st.session_state.aba_atual == "💾 Backup":
    st.subheader("💾 Recuperar ou Salvar Dados")
    
    # BOTÃO DE SUBIR (RESTAURAR) - FAÇA ISSO AO ABRIR O LINK
    st.write("### 📤 1. Restaurar o que sumiu")
    arquivo = st.file_uploader("Escolha o arquivo 'backup_vet.txt':", type="txt")
    if arquivo and st.button("🔄 RESTAURAR DADOS AGORA", use_container_width=True):
        try:
            d_rec = ast.literal_eval(arquivo.read().decode("utf-8"))
            st.session_state.clientes = d_rec.get('clientes', [])
            st.session_state.pets = d_rec.get('pets', [])
            st.session_state.historico = d_rec.get('historico', [])
            st.session_state.caixa = d_rec.get('caixa', [])
            st.success("✅ Tudo de volta! Pode trabalhar.")
        except:
            st.error("Erro ao ler o arquivo. Use o backup mais recente.")
    
    st.divider()
    
    # BOTÃO DE BAIXAR (SALVAR) - FAÇA ISSO ANTES DE FECHAR
    st.write("### 📥 2. Salvar trabalho de agora")
    dados = {
        'clientes': st.session_state.clientes, 
        'pets': st.session_state.pets, 
        'historico': st.session_state.historico, 
        'caixa': st.session_state.caixa
    }
    st.download_button("📥 BAIXAR BACKUP NO CELULAR", str(dados), file_name="backup_vet.txt", use_container_width=True)
