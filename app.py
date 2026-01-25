import streamlit as st
from datetime import datetime
import urllib.parse
import ast

# 1. CONFIGURAÇÃO (Modo Escuro Nativo)
st.set_page_config(page_title="Ribeira Vet Pro", layout="centered")

for k in ['clientes', 'pets', 'historico', 'caixa', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "🐾 Pets"

# Função para calcular idade
def calcular_idade(nascimento):
    try:
        nasc = datetime.strptime(nascimento, "%d/%m/%Y")
        hoje = datetime.now()
        idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
        return f"{idade} anos" if idade > 0 else "Menos de 1 ano"
    except:
        return "N/I"

# --- 2. MENU LATERAL ---
with st.sidebar:
    st.title("🐾 Ribeira Vet")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    escolha = st.radio("NAVEGAÇÃO", opcoes, index=opcoes.index(st.session_state.aba_atual))
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- 4. MÓDULO PETS (VERSÃO ATUALIZADA 11.0) ---
elif st.session_state.aba_atual == "🐾 Pets":
    st.subheader("🐾 Gestão de Pacientes")
    
    # Notificação de Aniversariantes do Mês
    hoje = datetime.now()
    aniversariantes = []
    for p in st.session_state['pets']:
        try:
            nasc = datetime.strptime(p.get('NASCIMENTO', ''), "%d/%m/%Y")
            if nasc.month == hoje.month:
                aniversariantes.append(f"🎂 {p['PET']} ({p['TUTOR']})")
        except: continue
    
    if aniversariantes:
        with st.expander("🎉 Aniversariantes do Mês"):
            for niver in aniversariantes: st.write(niver)

    tuts = sorted([c['NOME'] for c in st.session_state['clientes']])
    if not tuts:
        st.warning("⚠️ Cadastre um tutor primeiro para vincular o pet.")
    else:
        t_f = st.selectbox("Selecione o Tutor para ver/cadastrar Pets:", ["--- Selecione ---"] + tuts)
        
        if t_f != "--- Selecione ---":
            # Listagem de Pets Existentes
            meus_pets = [p for p in st.session_state['pets'] if p['TUTOR'] == t_f]
            for p in meus_pets:
                idade_str = calcular_idade(p.get('NASCIMENTO', ''))
                st.info(f"🐕 **{p['PET']}** | Raça: {p['RAÇA']} | Idade: {idade_str}")
                if st.button(f"🩺 Atender {p['PET']}", key=f"atender_{p['PET']}", use_container_width=True):
                    st.session_state.aba_atual = "📋 Prontuário"
                    st.rerun()
            
            st.divider()
            with st.expander("➕ CADASTRAR NOVO PET"):
                with st.form("f_novo_pet"):
                    n_p = st.text_input("Nome do Animal *").upper()
                    r_p = st.text_input("Raça (Ex: Poodle, SRD, Persa) *").upper()
                    d_n = st.text_input("Data de Nascimento (DD/MM/AAAA) *")
                    st.caption("Exemplo: 15/01/2020")
                    
                    if st.form_submit_button("💾 SALVAR PET", use_container_width=True):
                        if n_p and r_p and d_n:
                            novo_pet = {
                                "PET": n_p, 
                                "RAÇA": r_p, 
                                "NASCIMENTO": d_n, 
                                "TUTOR": t_f
                            }
                            st.session_state['pets'].append(novo_pet)
                            st.success(f"{n_p} cadastrado com sucesso!")
                            st.rerun()
                        else:
                            st.error("Por favor, preencha Nome, Raça e Data de Nascimento.")

# --- (Mantenha os outros módulos como na v10.9) ---
