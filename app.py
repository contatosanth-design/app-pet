import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

# Variáveis de navegação automática
if 'tutor_da_vez' not in st.session_state: st.session_state['tutor_da_vez'] = None
if 'pular_para_pet' not in st.session_state: st.session_state['pular_para_pet'] = None

# 2. MENU LATERAL
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    # Define o índice do menu baseado na navegação automática
    idx = 0
    if st.session_state['tutor_da_vez']: idx = 1
    if st.session_state['pular_para_pet']: idx = 2
    
    menu = st.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"], index=idx)

# 3. MÓDULO 1: TUTORES (COM ATALHO DIRETO)
if menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    nomes_ordenados = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    escolha = st.selectbox("⚡ Selecionar ou Criar Novo:", ["--- Novo Cadastro ---"] + nomes_ordenados)
    
    # Se o tutor foi selecionado, mostra o ATALHO para a próxima tela
    if escolha != "--- Novo Cadastro ---":
        st.success(f"✅ Cadastro de **{escolha}** localizado!")
        if st.button(f"➡️ Ver Pets de {escolha}"):
            st.session_state['tutor_da_vez'] = escolha
            st.rerun()

    with st.form("f_tutor_v11"):
        if escolha == "--- Novo Cadastro ---":
            v_nome, v_tel, v_cpf, v_email, v_end = "", "", "", "", ""
        else:
            dados = next(c for c in st.session_state['clientes'] if c['NOME'] == escolha)
            v_nome, v_tel, v_cpf, v_email, v_end = dados['NOME'], dados['TEL'], dados['CPF'], dados['E-MAIL'], dados['ENDEREÇO']

        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome do Tutor *", value=v_nome).upper()
        zap = c2.text_input("WhatsApp", value=v_tel)
        c3, c4 = st.columns([1, 1])
        cpf = c3.text_input("CPF", value=v_cpf)
        email = c4.text_input("E-mail", value=v_email)
        end = st.text_input("Endereço Completo", value=v_end)
        
        # O botão Salvar agora serve apenas para MODIFICAÇÕES
        texto_botao = "💾 Salvar Novo Cadastro" if escolha == "--- Novo Cadastro ---" else "🔄 Atualizar Dados"
        if st.form_submit_button(texto_botao):
            if nome:
                if escolha == "--- Novo Cadastro ---":
                    st.session_state['clientes'].append({"NOME": nome, "CPF": cpf, "TEL": zap, "ENDEREÇO": end, "E-MAIL": email})
                else:
                    # Atualiza o existente
                    for idx, c in enumerate(st.session_state['clientes']):
                        if c['NOME'] == escolha:
                            st.session_state['clientes'][idx] = {"NOME": nome, "CPF": cpf, "TEL": zap, "ENDEREÇO": end, "E-MAIL": email}
                st.success("Dados processados!")
                st.rerun()

# 4. MÓDULO 2: PETS (RECONHECE O ATALHO)
elif menu == "🐾 Pets":
    st.subheader("🐾 Central do Paciente")
    tutores_disp = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    
    # Se veio do atalho, já deixa o tutor selecionado
    idx_tutor = 0
    if st.session_state['tutor_da_vez'] in tutores_disp:
        idx_tutor = tutores_disp.index(st.session_state['tutor_da_vez']) + 1

    tutor_sel = st.selectbox("🔍 Selecione o Cliente:", ["--- Escolha ---"] + tutores_disp, index=idx_tutor)
    
    if tutor_sel != "--- Escolha ---":
        pets_do_tutor = [p for p in st.session_state['pets'] if p.get('TUTOR') == tutor_sel]
        if pets_do_tutor:
            for p in pets_do_tutor:
                col1, col2 = st.columns([4, 1])
                col1.write(f"🐶 **{p['PET']}** ({p['RAÇA']})")
                if col2.button(f"🩺 Atender {p['PET']}", key=f"p_{p['PET']}"):
                    st.session_state['pular_para_pet'] = f"{p['PET']} (Tutor: {tutor_sel})"
                    st.rerun()
        
        with st.expander("➕ Cadastrar Novo Animal"):
            with st.form("f_pet_v11"):
                n_pet = st.text_input("Nome do Pet").upper()
                rac = st.text_input("Raça").upper()
                if st.form_submit_button("Salvar Pet"):
                    st.session_state['pets'].append({"PET": n_pet, "TUTOR": tutor_sel, "RAÇA": rac, "ESP": "Cão", "NASC": ""})
                    st.rerun()

# Limpeza de estados ao mudar manualmente
if menu != "👤 Tutores" and menu != "🐾 Pets":
    st.session_state['tutor_da_vez'] = None

# Módulos Prontuário, Financeiro e Backup seguem integrados...
