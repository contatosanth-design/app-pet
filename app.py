import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

# Variável que controla em qual página estamos e qual pet foi selecionado
if 'pagina_ativa' not in st.session_state: st.session_state['pagina_ativa'] = "👤 Tutores"
if 'pet_selecionado' not in st.session_state: st.session_state['pet_selecionado'] = None

# 2. MENU LATERAL SINCRONIZADO
# O menu agora obedece à variável 'pagina_ativa'
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes_menu = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    
    # Descobre o índice da página atual para manter o rádio no lugar certo
    idx_atual = opcoes_menu.index(st.session_state['pagina_ativa'])
    
    menu = st.radio("NAVEGAÇÃO", opcoes_menu, index=idx_atual)
    st.session_state['pagina_ativa'] = menu

# 3. MÓDULO DE PETS (O GATILHO DO FLUXO)
if menu == "🐾 Pets":
    st.subheader("🐾 Central do Paciente")
    tutores_disp = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    tutor_sel = st.selectbox("🔍 Selecione o Cliente:", ["--- Escolha ---"] + tutores_disp)
    
    if tutor_sel != "--- Escolha ---":
        pets_do_tutor = [p for p in st.session_state['pets'] if p.get('TUTOR') == tutor_sel]
        if pets_do_tutor:
            for p in pets_do_tutor:
                col_p, col_b = st.columns([4, 1])
                col_p.info(f"🐶 **{p['PET']}** ({p['RAÇA']})")
                # AO CLICAR AQUI, O FLUXO SE COMPLETA
                if col_b.button(f"🩺 Atender", key=f"atend_{p['PET']}"):
                    st.session_state['pet_selecionado'] = f"{p['PET']} (Tutor: {tutor_sel})"
                    st.session_state['pagina_ativa'] = "📋 Prontuário" # MUDA A PÁGINA AQUI
                    st.rerun()

# 4. MÓDULO DE PRONTUÁRIO (TELAS INTEGRADAS)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    
    lista_pets = sorted([f"{p['PET']} (Tutor: {p.get('TUTOR', 'N/D')})" for p in st.session_state['pets']])
    
    # Seleciona automaticamente o pet se vier do fluxo "Atender"
    idx_p = 0
    if st.session_state['pet_selecionado'] in lista_pets:
        idx_p = lista_pets.index(st.session_state['pet_selecionado']) + 1

    pet_atual = st.selectbox("Buscar Paciente *", ["--- Selecione ---"] + lista_pets, index=idx_p)
    
    if pet_atual != "--- Selecione ---":
        # DIVISÃO DA TELA: ESQUERDA (NOVO) | DIREITA (HISTÓRICO)
        col_atend, col_hist = st.columns([2, 1])
        
        with col_atend:
            st.markdown("### 📝 Evolução Atual")
            with st.form("f_prontuario", clear_on_submit=True):
                c1, c2 = st.columns(2)
                peso = c1.text_input("Peso (kg)")
                temp = c2.text_input("Temperatura (°C)")
                anamnese = st.text_area("🎙️ Relato do Atendimento:", height=300)
                
                if st.form_submit_button("💾 Salvar Atendimento"):
                    if anamnese:
                        st.session_state['historico'].append({
                            "DATA": datetime.now().strftime('%d/%m/%Y %H:%M'),
                            "PACIENTE": pet_atual, "PESO": peso, "TEMP": temp, "RELATO": anamnese
                        })
                        st.session_state['pet_selecionado'] = None # Limpa para o próximo
                        st.success(" ✅ Histórico atualizado!")
                        st.rerun()

        with col_hist:
            st.markdown("### 📜 Histórico Pet")
            # Filtra apenas o histórico deste paciente específico
            meu_historico = [h for h in st.session_state['historico'] if h['PACIENTE'] == pet_atual]
            if meu_historico:
                for h in reversed(meu_historico): # O mais novo fica em cima
                    with st.expander(f"📅 {h['DATA']}", expanded=False):
                        st.write(f"**Peso:** {h['PESO']}kg | **Temp:** {h['TEMP']}°C")
                        st.write(f"---")
                        st.write(h['RELATO'])
            else:
                st.info("Nenhum histórico anterior.")
