import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# 1. Configuração e Estilo
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# 2. Banco de Dados Inicial
if 'estoque' not in st.session_state or len(st.session_state['estoque']) <= 3:
    st.session_state['estoque'] = [
        {"Item": "Vacina V10 (Importada)", "Preco": 120.00},
        {"Item": "Consulta Clínica", "Preco": 150.00},
        {"Item": "Hemograma", "Preco": 90.00},
        {"Item": "Simparic 10-20kg", "Preco": 85.00}
    ]

for key in ['clientes', 'pets', 'historico']:
    if key not in st.session_state: st.session_state[key] = []

# 3. Menu Lateral
with st.sidebar:
    st.title("Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "💰 Financeiro"])

# --- SESSÃO 1: TUTORES (COM CPF, E-MAIL E ENDEREÇO) ---
if menu == "👤 Tutores":
    st.subheader("📝 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        id_t = f"T{len(st.session_state['clientes']) + 1:03d}"
        nome = st.text_input("Nome do Cliente*")
        
        col1, col2 = st.columns(2)
        cpf = col1.text_input("CPF")  # CPF Reintroduzido conforme solicitado
        zap = col2.text_input("WhatsApp (Ex: 22985020463)*")
        
        email = st.text_input("E-mail")
        endereco = st.text_area("Endereço Completo")
        
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({
                    "id": id_t, "nome": nome.upper(), "cpf": cpf, 
                    "zap": zap, "email": email, "endereco": endereco
                })
                st.success(f"Tutor {nome} cadastrado!")

# --- SESSÃO 2: PETS (COM CÁLCULO DE IDADE) ---
elif menu == "🐾 Pets":
    st.subheader("🐾 Ficha do Paciente")
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            t_lista = {f"{c['id']} - {c['nome']}": c for c in st.session_state['clientes']}
            t_sel = st.selectbox("Proprietário", list(t_lista.keys()))
            nome_p = st.text_input("Nome do Animal*")
            
            c1, c2 = st.columns(2)
            data_nasc = c1.date_input("Data de Nascimento", value=date(2022, 1, 1))
            
            # Cálculo de Idade Automático
            hoje = date.today()
            idade_anos = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
            c2.info(f"Idade Atual: {idade_anos} anos")
            
            raca = st.selectbox("Raça", ["SRD", "Spitz Alemão", "Poodle", "Shih Tzu", "Outra"])
            sexo = st.radio("Sexo", ["Macho", "Fêmea"], horizontal=True)
            
            if st.form_submit_button("✅ Salvar Pet"):
                st.session_state['pets'].append({
                    "id": f"P{len(st.session_state['pets'])+1:03d}", "nome": nome_p.upper(),
                    "idade": f"{idade_anos} anos", "tutor": t_lista[t_sel]['nome'], "raca": raca
                })
                st.success(f"Pet {nome_p} cadastrado!")

# --- SESSÃO 3: PRONTUÁRIO (COM TRANSCRIÇÃO DE VOZ) ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento com Transcrição de Voz")
    st.info("💡 Dica: Clique no campo de texto e aperte 'Windows + H' no teclado para ditar o atendimento.")
    
    if not st.session_state['pets']:
        st.info("Nenhum pet cadastrado.")
    else:
        with st.form("f_prontuario"):
            p_lista = {p['nome']: p for p in st.session_state['pets']}
            pet_atend = st.selectbox("Paciente", list(p_lista.keys()))
            
            col1, col2 = st.columns(2)
            peso = col1.text_input("Peso (kg)")
            temp = col2.text_input("Temperatura (°C)")
            
            # Campo de Transcrição
            relato = st.text_area("Relato Clínico (DITE AQUI USANDO Win+H)", height=250)
            
            if st.form_submit_button("💾 Salvar Atendimento"):
                st.session_state['historico'].append({
                    "Data": date.today().strftime("%d/%m/%Y"),
                    "Pet": pet_atend, "Peso": peso, "Temp": temp, "Relato": relato
                })
                st.success("Histórico salvo!")

# --- SESSÃO 4: FINANCEIRO ---
elif menu == "💰 Financeiro":
    st.subheader("💰 Financeiro")
    if st.session_state['clientes']:
        t_lista = {c['nome']: c for c in st.session_state['clientes']}
        t_nome = st.selectbox("Tutor", list(t_lista.keys()))
        servicos = st.multiselect("Itens", [i['Item'] for i in st.session_state['estoque']])
        
        if st.button("Gerar Cobrança"):
            valor = sum([i['Preco'] for i in st.session_state['estoque'] if i['Item'] in servicos])
            st.write(f"### Total: R$ {valor:.2f}")

# --- DASHBOARD ---
elif menu == "🏠 Dashboard":
    st.metric("Pacientes", len(st.session_state['pets']))
    if st.session_state['historico']:
        st.table(pd.DataFrame(st.session_state['historico']))
