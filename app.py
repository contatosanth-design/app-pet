import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO E NAVEGAÇÃO INTEGRADA
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

# Variável de controle para o "salto" entre telas
if 'pular_para_pet' not in st.session_state:
    st.session_state['pular_para_pet'] = None

# 2. MENU LATERAL
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    # A navegação agora pode ser alterada via código
    menu = st.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"], 
                    index=2 if st.session_state['pular_para_pet'] else 0)

# 3. MÓDULO 1: TUTORES (A-Z)
if menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    nomes_ordenados = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    escolha = st.selectbox("⚡ Selecionar ou Criar Novo:", ["--- Novo Cadastro ---"] + nomes_ordenados)
    
    with st.form("f_tutor_v10"):
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
        if st.form_submit_button("💾 Salvar Tutor"):
            if nome and escolha == "--- Novo Cadastro ---":
                st.session_state['clientes'].append({"NOME": nome, "CPF": cpf, "TEL": zap, "ENDEREÇO": end, "E-MAIL": email})
                st.rerun()

# 4. MÓDULO 2: PETS (COM BOTÃO DE ATENDIMENTO DIRETO)
elif menu == "🐾 Pets":
    st.subheader("🐾 Central do Paciente")
    tutores_disp = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    
    tutor_sel = st.selectbox("🔍 Selecione o Cliente:", ["--- Escolha ---"] + tutores_disp)
    
    if tutor_sel != "--- Escolha ---":
        pets_do_tutor = [p for p in st.session_state['pets'] if p.get('TUTOR') == tutor_sel]
        
        if pets_do_tutor:
            st.write(f"📋 **Pacientes de {tutor_sel}:**")
            for p in pets_do_tutor:
                col1, col2 = st.columns([4, 1])
                col1.write(f"🐶 **{p['PET']}** ({p['RAÇA']})")
                # BOTÃO MÁGICO: Envia o pet direto para o prontuário
                if col2.button(f"🩺 Atender {p['PET']}", key=f"btn_{p['PET']}"):
                    st.session_state['pular_para_pet'] = f"{p['PET']} (Tutor: {tutor_sel})"
                    st.rerun()
        
        with st.expander("➕ Cadastrar Novo Animal"):
            with st.form("f_novo_pet_v10"):
                n_pet = st.text_input("Nome do Pet *").upper()
                rac = st.text_input("Raça *").upper()
                if st.form_submit_button("💾 Salvar"):
                    if n_pet and rac:
                        st.session_state['pets'].append({"PET": n_pet, "TUTOR": tutor_sel, "RAÇA": rac, "NASC": datetime.now().strftime('%d/%m/%Y'), "ESP": "Cão"})
                        st.rerun()

# 5. MÓDULO 3: PRONTUÁRIO (RECONHECE O "SALTO")
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    
    opcoes_pets = sorted([f"{p['PET']} (Tutor: {p.get('TUTOR', 'N/D')})" for p in st.session_state['pets']])
    
    # Se veio do botão "Atender", já seleciona o pet automático
    indice_auto = 0
    if st.session_state['pular_para_pet'] in opcoes_pets:
        indice_auto = opcoes_pets.index(st.session_state['pular_para_pet']) + 1
        st.info(f"🚀 Atendimento iniciado para: **{st.session_state['pular_para_pet']}**")

    paciente_sel = st.selectbox("Buscar Paciente *", ["--- Selecione ---"] + opcoes_pets, index=indice_auto)
    
    if paciente_sel != "--- Selecione ---":
        with st.form("f_pronto_v10"):
            c1, c2 = st.columns(2)
            peso = c1.text_input("Peso (kg)")
            temp = c2.text_input("Temperatura (°C)")
            anamnese = st.text_area("🎙️ Descrição do Caso:", height=250)
            if st.form_submit_button("💾 Finalizar e Salvar"):
                st.session_state['historico'].append({
                    "DATA": datetime.now().strftime('%d/%m/%Y %H:%M'),
                    "PACIENTE": paciente_sel, "PESO": peso, "TEMP": temp, "RELATO": anamnese
                })
                st.session_state['pular_para_pet'] = None # Limpa o salto
                st.success("Prontuário salvo!")
                st.rerun()

# Módulos Financeiro e Backup mantidos para estabilidade...
elif menu == "💰 Financeiro":
    st.subheader("💰 Financeiro")
    serv = st.text_input("Serviço")
    val = st.number_input("Valor", min_value=0.0, format="%.2f")
    if st.button("➕ Lançar"):
        st.session_state['carrinho'].append({"Item": serv.upper(), "Preco": val})
    if st.session_state['carrinho']:
        st.table(pd.DataFrame(st.session_state['carrinho']))
        if st.button("🏁 Fechar"): st.session_state['carrinho'] = []; st.rerun()
