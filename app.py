import streamlit as st
from datetime import datetime
import urllib.parse
import ast

# 1. AJUSTE DE TELA PARA ANDROID
st.set_page_config(page_title="Ribeira Vet Pro", layout="centered")

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

# --- 5. MÓDULO PRONTUÁRIO (BOTÃO LARGO PARA CELULAR) ---
elif st.session_state.aba_atual == "📋 Prontuário":
    st.subheader("📋 Prontuário Médico")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    paciente = st.selectbox("Selecione o Paciente:", ["--- Selecione ---"] + p_lista)
    
    if paciente != "--- Selecione ---":
        with st.form("f_pront_v101"):
            st.info(f"📍 Atendendo: {paciente}")
            c1, c2 = st.columns(2)
            f_peso = c1.text_input("Peso (kg)")
            f_temp = c2.text_input("Temp (°C)")
            
            st.write("🎙️ **Dica:** Clique no campo abaixo e use o **Microfone do seu Teclado** para ditar.")
            f_texto = st.text_area("Descreva a Anamnese/Conduta:", height=300)
            
            # Botão grande para salvar com o dedo
            if st.form_submit_button("💾 SALVAR ATENDIMENTO FINALIZADO", use_container_width=True):
                if f_texto:
                    st.session_state['historico'].append({
                        "DATA": datetime.now().strftime("%d/%m/%Y"),
                        "PACIENTE": paciente,
                        "TEXTO": f_texto,
                        "PESO": f_peso,
                        "TEMP": f_temp
                    })
                    st.success("Prontuário salvo com sucesso!")
                    st.rerun()

# --- 6. FINANCEIRO (BOTÕES LARGOS) ---
elif st.session_state.aba_atual == "💰 Financeiro":
    st.subheader("💰 Financeiro")
    precos = {"Consulta Local": 150.0, "Consulta Residencial": 250.0, "Vacina": 120.0, "Medicamento": 50.0}
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    paciente_fin = st.selectbox("Cobrar de:", ["--- Selecione ---"] + p_lista)
    
    if paciente_fin != "--- Selecione ---":
        serv = st.selectbox("O que foi feito?", list(precos.keys()) + ["Outro"])
        valor = st.number_input("Preço R$:", value=precos.get(serv, 0.0))
        
        if st.button("➕ ADICIONAR AO CARRINHO", use_container_width=True):
            st.session_state.carrinho.append({"ITEM": serv, "VALOR": valor})
            st.rerun()
            
        if st.session_state.carrinho:
            total = sum(item['VALOR'] for item in st.session_state.carrinho)
            st.markdown(f"### **Total: R$ {total:.2f}**")
            
            if st.button("✅ FINALIZAR E GERAR RECIBO", use_container_width=True):
                # ... (Lógica de salvar e gerar link do WhatsApp v9.7)
                st.session_state.caixa.append({"DATA": datetime.now().strftime("%d/%m/%Y"), "PACIENTE": paciente_fin, "VALOR": total})
                st.success("Venda registrada!")
                st.session_state.carrinho = []
                st.rerun()
