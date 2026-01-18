import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO E MEMÓRIA
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Garantir que as listas existam
for k in ['clientes', 'pets', 'carrinho', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

# Controle de Navegação Automática
if 'pagina' not in st.session_state: st.session_state['pagina'] = "👤 Tutores"
if 'tutor_foco' not in st.session_state: st.session_state['tutor_foco'] = None
if 'pet_foco' not in st.session_state: st.session_state['pet_foco'] = None

# 2. BARRA LATERAL (MENU)
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    # O menu segue a vontade do código (index dinâmico)
    idx_menu = opcoes.index(st.session_state['pagina'])
    menu = st.radio("NAVEGAÇÃO", opcoes, index=idx_menu)
    st.session_state['pagina'] = menu

# 3. MÓDULO 1: TUTORES (Onde estava o erro)
if menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    
    # Lista de nomes para a busca
    nomes_cadastrados = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    tutor_selecionado = st.selectbox("⚡ Buscar Tutor Cadastrado:", ["--- Novo Cadastro ---"] + nomes_cadastrados)

    # Lógica de preenchimento
    if tutor_selecionado != "--- Novo Cadastro ---":
        dados = next(c for c in st.session_state['clientes'] if c['NOME'] == tutor_selecionado)
        
        # ATALHO DIRETO (O que o senhor pediu)
        st.success(f"✅ Cadastro de {tutor_selecionado} pronto!")
        if st.button(f"➡️ Ir para Pets de {tutor_selecionado}"):
            st.session_state['tutor_foco'] = tutor_selecionado
            st.session_state['pagina'] = "🐾 Pets"
            st.rerun()
            
        # Campos preenchidos para consulta/edição
        v_nome, v_tel, v_cpf = dados['NOME'], dados['TEL'], dados['CPF']
    else:
        v_nome, v_tel, v_cpf = "", "", ""

    # Formulário de Cadastro/Edição
    with st.form("f_tutor_v13"):
        c1, c2 = st.columns([3, 1])
        nome_f = c1.text_input("Nome Completo *", value=v_nome).upper()
        tel_f = c2.text_input("WhatsApp", value=v_tel)
        cpf_f = st.text_input("CPF/Documento", value=v_cpf)
        
        btn_txt = "💾 Salvar Novo" if tutor_selecionado == "--- Novo Cadastro ---" else "🔄 Atualizar Dados"
        if st.form_submit_button(btn_txt):
            if nome_f:
                if tutor_selecionado == "--- Novo Cadastro ---":
                    st.session_state['clientes'].append({"NOME": nome_f, "TEL": tel_f, "CPF": cpf_f})
                else:
                    # Atualiza na lista
                    for c in st.session_state['clientes']:
                        if c['NOME'] == tutor_selecionado:
                            c.update({"NOME": nome_f, "TEL": tel_f, "CPF": cpf_f})
                st.rerun()

# 4. MÓDULO 2: PETS (Conexão com Tutores)
elif menu == "🐾 Pets":
    st.subheader("🐾 Pacientes")
    tutores_lista = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    
    # Se veio do atalho, já marca o tutor
    idx_t = 0
    if st.session_state['tutor_foco'] in tutores_lista:
        idx_t = tutores_lista.index(st.session_state['tutor_foco']) + 1
    
    t_sel = st.selectbox("Selecione o Tutor:", ["--- Escolha ---"] + tutores_lista, index=idx_t)
    
    if t_sel != "--- Escolha ---":
        meus_pets = [p for p in st.session_state['pets'] if p['TUTOR'] == t_sel]
        if meus_pets:
            for p in meus_pets:
                col_n, col_b = st.columns([4, 1])
                col_n.warning(f"🐕 {p['PET']} ({p['RAÇA']})")
                if col_b.button(f"🩺 Atender", key=f"at_{p['PET']}"):
                    st.session_state['pet_foco'] = f"{p['PET']} (Tutor: {t_sel})"
                    st.session_state['pagina'] = "📋 Prontuário"
                    st.rerun()
        
        # Cadastro de novo pet para este tutor
        with st.expander("➕ Novo Animal"):
            with st.form("f_novo_pet"):
                n_p = st.text_input("Nome do Pet").upper()
                r_p = st.text_input("Raça").upper()
                if st.form_submit_button("Salvar"):
                    st.session_state['pets'].append({"PET": n_p, "RAÇA": r_p, "TUTOR": t_sel})
                    st.rerun()

# 5. MÓDULO 3: PRONTUÁRIO (Lado a Lado)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento")
    todos_pets = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    
    idx_p = 0
    if st.session_state['pet_foco'] in todos_pets:
        idx_p = todos_pets.index(st.session_state['pet_foco']) + 1
    
    p_atual = st.selectbox("Paciente:", ["--- Selecione ---"] + todos_pets, index=idx_p)
    
    if p_atual != "--- Selecione ---":
        c_at, c_hi = st.columns([2, 1])
        with c_at:
            with st.form("f_atend"):
                pes = st.text_input("Peso")
                rel = st.text_area("Anamnese", height=250)
                if st.form_submit_button("💾 Salvar"):
                    st.session_state['historico'].append({"DATA": datetime.now().strftime("%d/%m/%Y"), "PACIENTE": p_atual, "RELATO": rel, "PESO": pes})
                    st.session_state['pet_foco'] = None
                    st.rerun()
        with c_hi:
            st.write("### 📜 Histórico")
            meu_h = [h for h in st.session_state['historico'] if h['PACIENTE'] == p_atual]
            for h in reversed(meu_h):
                with st.expander(f"📅 {h['DATA']}"):
                    st.write(h['RELATO'])
