import streamlit as st
from datetime import datetime
import urllib.parse
import ast

# 1. AJUSTE PARA CELULAR E MEMÓRIA
st.set_page_config(page_title="Ribeira Vet Pro", layout="centered") # 'centered' fica melhor no celular

for k in ['clientes', 'pets', 'historico', 'caixa', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"

# --- 2. MENU LATERAL (Sincronizado) ---
with st.sidebar:
    st.title("🐾 Ribeira Vet")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    escolha = st.radio("MENU", opcoes, index=opcoes.index(st.session_state.aba_atual))
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- 3. MÓDULO TUTORES (COMPLETO COM ENDEREÇO E EMAIL) ---
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    t_sel = st.selectbox("Buscar Cliente:", ["--- Novo ---"] + nomes)
    
    v_nome, v_cpf, v_tel, v_email, v_end = ("", "", "", "", "")
    if t_sel != "--- Novo ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == t_sel)
        v_nome, v_cpf, v_tel, v_email, v_end = c.get('NOME',''), c.get('CPF',''), c.get('TEL',''), c.get('EMAIL',''), c.get('END','')

    with st.form("f_tutor_v99"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        f_cpf = st.text_input("CPF", value=v_cpf)
        f_tel = st.text_input("WhatsApp (DDD+Número)", value=v_tel)
        f_email = st.text_input("E-mail", value=v_email)
        f_end = st.text_area("Endereço Completo", value=v_end)
        if st.form_submit_button("💾 SALVAR CLIENTE"):
            if f_nome:
                d = {"NOME": f_nome, "CPF": f_cpf, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if t_sel == "--- Novo ---": st.session_state['clientes'].append(d)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == t_sel: st.session_state['clientes'][i] = d
                st.success("Salvo!")
                st.rerun()

# --- (Os módulos de Pets e Prontuário seguem a lógica anterior, com foco em botões grandes) ---

# --- 7. MÓDULO BACKUP E RESTAURAÇÃO (PARA NÃO PERDER DADOS) ---
elif st.session_state.aba_atual == "💾 Backup":
    st.subheader("💾 Segurança dos Dados")
    
    # Botão para baixar (Exportar)
    dados_atuais = {
        'clientes': st.session_state.clientes,
        'pets': st.session_state.pets,
        'historico': st.session_state.historico,
        'caixa': st.session_state.caixa
    }
    st.download_button("📥 BAIXAR BACKUP (Salvar no Celular)", str(dados_atuais), file_name="backup_vet.txt")
    
    st.divider()
    
    # Botão para subir (Restaurar)
    st.write("### 📤 Restaurar Dados")
    arquivo_subido = st.file_uploader("Se os dados sumirem, escolha o arquivo backup_vet.txt aqui:", type="txt")
    if arquivo_subido is not None:
        if st.button("🔄 RESTAURAR TUDO AGORA"):
            conteudo = arquivo_subido.read().decode("utf-8")
            dados_recuperados = ast.literal_eval(conteudo)
            st.session_state.clientes = dados_recuperados.get('clientes', [])
            st.session_state.pets = dados_recuperados.get('pets', [])
            st.session_state.historico = dados_recuperados.get('historico', [])
            st.session_state.caixa = dados_recuperados.get('caixa', [])
            st.success("Dados restaurados com sucesso! Pode voltar a trabalhar.")import streamlit as st
from datetime import datetime
import urllib.parse
import ast

# 1. AJUSTE PARA CELULAR E MEMÓRIA
st.set_page_config(page_title="Ribeira Vet Pro", layout="centered") # 'centered' fica melhor no celular

for k in ['clientes', 'pets', 'historico', 'caixa', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"

# --- 2. MENU LATERAL (Sincronizado) ---
with st.sidebar:
    st.title("🐾 Ribeira Vet")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    escolha = st.radio("MENU", opcoes, index=opcoes.index(st.session_state.aba_atual))
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- 3. MÓDULO TUTORES (COMPLETO COM ENDEREÇO E EMAIL) ---
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    t_sel = st.selectbox("Buscar Cliente:", ["--- Novo ---"] + nomes)
    
    v_nome, v_cpf, v_tel, v_email, v_end = ("", "", "", "", "")
    if t_sel != "--- Novo ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == t_sel)
        v_nome, v_cpf, v_tel, v_email, v_end = c.get('NOME',''), c.get('CPF',''), c.get('TEL',''), c.get('EMAIL',''), c.get('END','')

    with st.form("f_tutor_v99"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        f_cpf = st.text_input("CPF", value=v_cpf)
        f_tel = st.text_input("WhatsApp (DDD+Número)", value=v_tel)
        f_email = st.text_input("E-mail", value=v_email)
        f_end = st.text_area("Endereço Completo", value=v_end)
        if st.form_submit_button("💾 SALVAR CLIENTE"):
            if f_nome:
                d = {"NOME": f_nome, "CPF": f_cpf, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if t_sel == "--- Novo ---": st.session_state['clientes'].append(d)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == t_sel: st.session_state['clientes'][i] = d
                st.success("Salvo!")
                st.rerun()

# --- (Os módulos de Pets e Prontuário seguem a lógica anterior, com foco em botões grandes) ---

# --- 7. MÓDULO BACKUP E RESTAURAÇÃO (PARA NÃO PERDER DADOS) ---
elif st.session_state.aba_atual == "💾 Backup":
    st.subheader("💾 Segurança dos Dados")
    
    # Botão para baixar (Exportar)
    dados_atuais = {
        'clientes': st.session_state.clientes,
        'pets': st.session_state.pets,
        'historico': st.session_state.historico,
        'caixa': st.session_state.caixa
    }
    st.download_button("📥 BAIXAR BACKUP (Salvar no Celular)", str(dados_atuais), file_name="backup_vet.txt")
    
    st.divider()
    
    # Botão para subir (Restaurar)
    st.write("### 📤 Restaurar Dados")
    arquivo_subido = st.file_uploader("Se os dados sumirem, escolha o arquivo backup_vet.txt aqui:", type="txt")
    if arquivo_subido is not None:
        if st.button("🔄 RESTAURAR TUDO AGORA"):
            conteudo = arquivo_subido.read().decode("utf-8")
            dados_recuperados = ast.literal_eval(conteudo)
            st.session_state.clientes = dados_recuperados.get('clientes', [])
            st.session_state.pets = dados_recuperados.get('pets', [])
            st.session_state.historico = dados_recuperados.get('historico', [])
            st.session_state.caixa = dados_recuperados.get('caixa', [])
            st.success("Dados restaurados com sucesso! Pode voltar a trabalhar.")
