import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

# Variáveis de Controle de Fluxo
if 'paciente_carregado' not in st.session_state: 
    st.session_state['paciente_carregado'] = None

# 2. MENU LATERAL (Sincronizado)
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    # Se houver um paciente carregado, o menu pula automaticamente para Prontuário (índice 2)
    default_index = 2 if st.session_state['paciente_carregado'] else 0
    menu = st.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"], index=default_index)

# 3. MÓDULO DE PETS (O GATILHO)
if menu == "🐾 Pets":
    st.subheader("🐾 Central do Paciente")
    tutores_disp = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    tutor_sel = st.selectbox("🔍 Selecione o Cliente:", ["--- Escolha ---"] + tutores_disp)
    
    if tutor_sel != "--- Escolha ---":
        pets_do_tutor = [p for p in st.session_state['pets'] if p.get('TUTOR') == tutor_sel]
        if pets_do_tutor:
            for p in pets_do_tutor:
                col1, col2 = st.columns([4, 1])
                col1.info(f"🐶 **{p['PET']}** ({p['RAÇA']})")
                # Botão que "Carrega" o paciente e muda a tela
                if col2.button(f"🩺 Atender", key=f"atender_{p['PET']}"):
                    st.session_state['paciente_carregado'] = f"{p['PET']} (Tutor: {tutor_sel})"
                    st.rerun()

# 4. MÓDULO DE PRONTUÁRIO (COM HISTÓRICO LATERAL)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    
    opcoes_pets = sorted([f"{p['PET']} (Tutor: {p.get('TUTOR', 'N/D')})" for p in st.session_state['pets']])
    
    # Define o paciente inicial se vier do salto
    idx_auto = 0
    if st.session_state['paciente_carregado'] in opcoes_pets:
        idx_auto = opcoes_pets.index(st.session_state['paciente_carregado']) + 1

    # Busca de Paciente
    paciente_sel = st.selectbox("Buscar Paciente *", ["--- Selecione ---"] + opcoes_pets, index=idx_auto)
    
    if paciente_sel != "--- Selecione ---":
        col_dados, col_hist = st.columns([2, 1])
        
        with col_dados:
            st.write("### 📝 Nova Evolução")
            with st.form("f_atendimento", clear_on_submit=True):
                c1, c2 = st.columns(2)
                peso = c1.text_input("Peso (kg)")
                temp = c2.text_input("Temp (°C)")
                relato = st.text_area("🎙️ Relato da Consulta:", height=300)
                
                if st.form_submit_button("💾 Salvar Atendimento"):
                    st.session_state['historico'].append({
                        "DATA": datetime.now().strftime('%d/%m/%Y %H:%M'),
                        "PACIENTE": paciente_sel, "PESO": peso, "TEMP": temp, "RELATO": relato
                    })
                    st.session_state['paciente_carregado'] = None # Limpa após salvar
                    st.success("Atendimento registrado!")
                    st.rerun()

        with col_hist:
            st.write("### 📜 Histórico Pet")
            # Filtra o histórico específico deste animal
            h_filtrado = [h for h in st.session_state['historico'] if h['PACIENTE'] == paciente_sel]
            if h_filtrado:
                for h in reversed(h_filtrado): # Mais recentes primeiro
                    with st.expander(f"📅 {h['DATA']}"):
                        st.write(f"**Peso:** {h['PESO']}kg | **Temp:** {h['TEMP']}°C")
                        st.write(f"**Relato:** {h['RELATO']}")
            else:
                st.info("Primeiro atendimento deste paciente.")

# Mantendo os outros módulos para não quebrar o sistema...
elif menu == "👤 Tutores":
    st.info("Módulo de tutores ativo. Selecione um tutor para gerenciar dados.")
