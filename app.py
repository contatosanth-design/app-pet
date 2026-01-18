import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [
        {"Item": "CONSULTA CLÍNICA", "Preco": 150.0},
        {"Item": "VACINA V10", "Preco": 120.0}
    ]

# 2. MENU LATERAL
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"])

# 3. MÓDULO 1: TUTORES
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    with st.form("f_tutor"):
        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo *")
        zap = c2.text_input("Telefone")
        c3, c4 = st.columns([1, 1])
        cpf = c3.text_input("CPF")
        email = c4.text_input("E-mail")
        end = st.text_input("Endereço Completo")
        if st.form_submit_button("💾 Salvar"):
            if nome:
                st.session_state['clientes'].append({"NOME": nome.upper(), "CPF": cpf, "TEL": zap, "ENDEREÇO": end, "E-MAIL": email})
                st.rerun()
    if st.session_state['clientes']: st.table(pd.DataFrame(st.session_state['clientes']))

# 4. MÓDULO 2: PETS (COM VÍNCULO)
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    lista_tutores = ["--- Selecione o Tutor ---"]
    if st.session_state['clientes']:
        lista_tutores.extend([c['NOME'] for c in st.session_state['clientes']])

    with st.form("f_pet"):
        tutor_vinculo = st.selectbox("Tutor (Dono) *", lista_tutores)
        c1, c2 = st.columns([2, 1])
        n_pet = c1.text_input("Nome do Pet *")
        data_nasc = c2.text_input("Nascimento (DD/MM/AAAA)", value=datetime.now().strftime('%d/%m/%Y'))
        esp = st.selectbox("Espécie", ["Cão", "Gato", "Outro"])
        rac = st.text_input("Raça")
        if st.form_submit_button("💾 Salvar Pet"):
            if n_pet and tutor_vinculo != "--- Selecione o Tutor ---":
                st.session_state['pets'].append({
                    "PET": n_pet.upper(), "TUTOR": tutor_vinculo, 
                    "ESPÉCIE": esp, "RAÇA": rac.upper(), "NASCIMENTO": data_nasc
                })
                st.rerun()
    if st.session_state['pets']: st.table(pd.DataFrame(st.session_state['pets']))

# 5. MÓDULO 3: PRONTUÁRIO (BUSCA AUTOMÁTICA BLINDADA)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    
    # Lógica que evita o erro 'KeyError: TUTOR'
    opcoes_busca = ["--- Escolha o Paciente ---"]
    for p in st.session_state['pets']:
        tutor_nome = p.get('TUTOR', 'Não Informado') # Se não achar o tutor, coloca 'Não Informado'
        opcoes_busca.append(f"{p['PET']} (Tutor: {tutor_nome})")

    with st.form("f_pronto"):
        pet_selecionado = st.selectbox("Buscar Paciente *", opcoes_busca)
        c1, c2 = st.columns(2)
        peso = c1.text_input("Peso (kg)")
        temp = c2.text_input("Temp (°C)")
        anamnese = st.text_area("🎙️ Anamnese (Win + H):", height=200)
        
        if st.form_submit_button("💾 Salvar Atendimento"):
            if pet_selecionado != "--- Escolha o Paciente ---" and anamnese:
                st.session_state['historico'].append({
                    "DATA": datetime.now().strftime('%d/%m/%Y %H:%M'),
                    "PACIENTE": pet_selecionado, "PESO": peso, "TEMP": temp, "RELATO": anamnese
                })
                st.session_state['carrinho'].append({"Item": f"CONSULTA: {pet_selecionado}", "Preco": 150.0})
                st.success("Salvo e lançado no financeiro!")
                st.rerun()
    if st.session_state['historico']: st.table(pd.DataFrame(st.session_state['historico']))

# 6. MÓDULO 4: FINANCEIRO
elif menu == "💰 Financeiro":
    st.subheader("💰 Caixa")
    if st.session_state['carrinho']:
        st.table(pd.DataFrame(st.session_state['carrinho']))
        if st.button("🏁 Fechar Caixa"):
            st.session_state['carrinho'] = []
            st.rerun()

# 7. MÓDULO 5: BACKUP
elif menu == "💾 Backup":
    st.subheader("💾 Backup")
    if st.session_state['clientes']:
        st.download_button("📥 Clientes", pd.DataFrame(st.session_state['clientes']).to_csv(index=False).encode('utf-8-sig'), "clientes.csv")
    if st.session_state['pets']:
        st.download_button("📥 Pets", pd.DataFrame(st.session_state['pets']).to_csv(index=False).encode('utf-8-sig'), "pets.csv")
