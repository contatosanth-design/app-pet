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

# No Módulo 1 (Tutores), vamos adicionar uma busca rápida que já valida o que existe
if menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    
    # Se já existem clientes, permite selecionar um para ver detalhes ou editar
    if st.session_state['clientes']:
        nomes_tutores = [c['NOME'] for c in st.session_state['clientes']]
        escolha = st.selectbox("⚡ Selecionar Tutor já cadastrado:", ["--- Novo Cadastro ---"] + nomes_tutores)
        
        if escolha != "--- Novo Cadastro ---":
            tutor_dados = next(c for c in st.session_state['clientes'] if c['NOME'] == escolha)
            st.info(f"✅ **Tutor Selecionado:** {tutor_dados['NOME']} | CPF: {tutor_dados['CPF']}")
            if st.button("📋 Iniciar Atendimento deste Tutor"):
                st.session_state['tutor_clicado'] = tutor_dados['NOME']
                st.success("Tutor enviado para o Prontuário!")
                # Aqui o sistema já prepara o salto para a aba de prontuário

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
