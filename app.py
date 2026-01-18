import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO E MEMÓRIA (CURA NAMEERROR)
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [{"Item": "CONSULTA CLÍNICA", "Preco": 150.0}]

# 2. MENU LATERAL
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"])

# 3. MÓDULO 1: TUTORES (TODOS OS PARÂMETROS RECUPERADOS)
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    with st.form("f_tutor_completo"):
        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo *").upper()
        zap = c2.text_input("Telefone/WhatsApp")
        
        c3, c4 = st.columns([1, 1])
        cpf = c3.text_input("CPF")
        email = c4.text_input("E-mail")
        
        end = st.text_input("Endereço Completo")
        
        if st.form_submit_button("💾 Salvar Tutor"):
            if nome:
                st.session_state['clientes'].append({
                    "NOME": nome, "CPF": cpf, "TEL": zap, "ENDEREÇO": end, "E-MAIL": email
                })
                st.rerun()
    if st.session_state['clientes']: 
        st.write("📋 **Lista de Tutores Cadastrados**")
        st.table(pd.DataFrame(st.session_state['clientes']))

# 4. MÓDULO 2: PETS (VÍNCULO COM TUTOR)
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    tutores_disp = [c['NOME'] for c in st.session_state['clientes']] if st.session_state['clientes'] else []
    
    if not tutores_disp:
        st.warning("⚠️ Cadastre um Tutor primeiro!")
    else:
        with st.form("f_pet_v25"):
            tutor_sel = st.selectbox("Tutor Responsável *", tutores_disp)
            c1, c2 = st.columns([2, 1])
            n_pet = c1.text_input("Nome do Pet *").upper()
            nasc = c2.text_input("Nascimento (DD/MM/AAAA)", value=datetime.now().strftime('%d/%m/%Y'))
            
            esp = st.selectbox("Espécie", ["Cão", "Gato", "Outro"])
            rac = st.text_input("Raça")
            
            if st.form_submit_button("💾 Salvar Pet"):
                if n_pet:
                    st.session_state['pets'].append({
                        "PET": n_pet, "TUTOR": tutor_sel, "ESP": esp, "RAÇA": rac.upper(), "NASC": nasc
                    })
                    st.rerun()
    if st.session_state['pets']: st.table(pd.DataFrame(st.session_state['pets']))

# 5. MÓDULO 3: PRONTUÁRIO (PESO, TEMP E BUSCA)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    opcoes = ["--- Selecione o Paciente ---"]
    for p in st.session_state['pets']:
        opcoes.append(f"{p['PET']} (Tutor: {p.get('TUTOR', 'N/D')})")

    with st.form("f_atend_completo"):
        pet_completo = st.selectbox("Buscar Paciente *", opcoes)
        c1, c2 = st.columns(2)
        peso = c1.text_input("Peso (kg)")
        temp = c2.text_input("Temperatura (°C)")
        
        st.write("🎙️ **Anamnese e Exame Clínico** (Win+H)")
        anamnese = st.text_area("Relato:", height=200)
        
        if st.form_submit_button("💾 Salvar Atendimento"):
            if pet_completo != "--- Selecione o Paciente ---" and anamnese:
                st.session_state['historico'].append({
                    "DATA": datetime.now().strftime('%d/%m/%Y %H:%M'),
                    "PACIENTE": pet_completo, "PESO": peso, "TEMP": temp, "RELATO": anamnese
                })
                st.session_state['carrinho'].append({"Item": f"CONSULTA: {pet_completo}", "Preco": 150.0})
                st.success("Prontuário salvo!")
                st.rerun()
    if st.session_state['historico']: st.table(pd.DataFrame(st.session_state['historico']))

# 6. MÓDULOS FINAIS
elif menu == "💰 Financeiro":
    st.subheader("💰 Caixa")
    if st.session_state['carrinho']:
        st.table(pd.DataFrame(st.session_state['carrinho']))
        if st.button("🏁 Fechar"): st.session_state['carrinho'] = []; st.rerun()
elif menu == "💾 Backup":
    st.subheader("💾 Backup")
    if st.session_state['clientes']:
        st.download_button("📥 Clientes", pd.DataFrame(st.session_state['clientes']).to_csv(index=False).encode('utf-8-sig'), "clientes.csv")
