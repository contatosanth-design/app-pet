import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO E MEMÓRIA
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [{"Item": "CONSULTA CLÍNICA", "Preco": 150.0}]

# 2. MENU
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"])

# 3. MÓDULO 1: TUTORES (Cadastro do Responsável)
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    with st.form("f_tutor"):
        nome = st.text_input("Nome do Tutor *").upper()
        zap = st.text_input("WhatsApp")
        if st.form_submit_button("💾 Salvar Tutor"):
            if nome:
                st.session_state['clientes'].append({"NOME": nome, "TEL": zap})
                st.rerun()
    if st.session_state['clientes']: st.table(pd.DataFrame(st.session_state['clientes']))

# 4. MÓDULO 2: PETS (VÍNCULO DIRETO COM TUTOR)
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    # Puxa a lista de tutores já cadastrados
    tutores_disp = [c['NOME'] for c in st.session_state['clientes']] if st.session_state['clientes'] else []
    
    if not tutores_disp:
        st.warning("⚠️ Cadastre um Tutor primeiro no menu ao lado!")
    else:
        with st.form("f_pet"):
            tutor_sel = st.selectbox("Quem é o Dono/Tutor? *", tutores_disp)
            n_pet = st.text_input("Nome do Pet *").upper()
            esp = st.selectbox("Espécie", ["Cão", "Gato", "Outro"])
            rac = st.text_input("Raça")
            nasc = st.text_input("Nascimento (DD/MM/AAAA)", value=datetime.now().strftime('%d/%m/%Y'))
            
            if st.form_submit_button("💾 Vincular Pet ao Tutor"):
                if n_pet:
                    st.session_state['pets'].append({
                        "PET": n_pet, "TUTOR": tutor_sel, 
                        "ESP": esp, "RAÇA": rac.upper(), "NASC": nasc
                    })
                    st.success(f"{n_pet} agora é dependente de {tutor_sel}!")
                    st.rerun()
    if st.session_state['pets']: st.table(pd.DataFrame(st.session_state['pets']))

# 5. MÓDULO 3: PRONTUÁRIO (BUSCA INTELIGENTE)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    # Cria a lista de busca unindo Pet + Tutor automaticamente
    opcoes = ["--- Selecione ---"]
    for p in st.session_state['pets']:
        opcoes.append(f"{p['PET']} (Tutor: {p.get('TUTOR', 'N/D')})")

    with st.form("f_atendimento"):
        pet_completo = st.selectbox("Buscar Paciente *", opcoes)
        c1, c2 = st.columns(2)
        peso = c1.text_input("Peso (kg)")
        temp = c2.text_input("Temperatura (°C)")
        anamnese = st.text_area("🎙️ Anamnese e Exame (Win+H):", height=200)
        
        if st.form_submit_button("💾 Salvar Atendimento"):
            if pet_completo != "--- Selecione ---" and anamnese:
                st.session_state['historico'].append({
                    "DATA": datetime.now().strftime('%d/%m/%Y %H:%M'),
                    "PACIENTE": pet_completo, "PESO": peso, "TEMP": temp, "RELATO": anamnese
                })
                # Lança direto no financeiro com o nome do pet e tutor
                st.session_state['carrinho'].append({"Item": f"CONSULTA: {pet_completo}", "Preco": 150.0})
                st.success("Tudo salvo! O valor da consulta já está no financeiro.")
                st.rerun()
    if st.session_state['historico']: st.table(pd.DataFrame(st.session_state['historico']))

# 6. MÓDULOS 4 E 5 (FINANCEIRO E BACKUP)
elif menu == "💰 Financeiro":
    st.subheader("💰 Caixa")
    if st.session_state['carrinho']:
        st.table(pd.DataFrame(st.session_state['carrinho']))
        if st.button("🏁 Fechar"): st.session_state['carrinho'] = []; st.rerun()
elif menu == "💾 Backup":
    st.subheader("💾 Backup")
    if st.session_state['pets']:
        st.download_button("📥 Baixar Planilha de Pacientes", pd.DataFrame(st.session_state['pets']).to_csv(index=False).encode('utf-8-sig'), "pets.csv")
        
