import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# 1. Configuração de Base
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# 2. Inicialização do Banco de Dados
if 'clientes' not in st.session_state: st.session_state['clientes'] = []
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'historico' not in st.session_state: st.session_state['historico'] = []
if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [
        {"Item": "Vacina V10", "Preco": 120.00}, 
        {"Item": "Consulta Geral", "Preco": 150.00},
        {"Item": "Castração Macho", "Preco": 350.00}
    ]

# 3. Menu de Navegação (Proteção contra tela em branco)
with st.sidebar:
    st.title("Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "💰 Financeiro"])

# --- SESSÃO 1: TUTORES ---
if menu == "👤 Tutores":
    st.subheader("📝 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        id_t = f"T{len(st.session_state['clientes']) + 1:03d}"
        nome = st.text_input("Nome do Cliente*")
        zap = st.text_input("WhatsApp (Somente números)*")
        cpf = st.text_input("CPF")
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({"id": id_t, "nome": nome.upper(), "zap": zap, "cpf": cpf})
                st.success(f"Tutor {nome} cadastrado!")

# --- SESSÃO 2: PETS (CORREÇÃO DA LINHA 67 E IDADE) ---
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet", clear_on_submit=True):
            id_p = f"P{len(st.session_state['pets']) + 1:03d}"
            # Correção da lista que causou o erro anterior
            t_lista = {f"{c['id']} - {c['nome']}": c for c in st.session_state['clientes']}
            t_sel = st.selectbox("Selecione o Proprietário*", list(t_lista.keys()))
            
            nome_p = st.text_input("Nome do Pet*")
            nasc = st.date_input("Data de Nascimento", value=date(2020, 1, 1))
            
            # Cálculo automático de idade
            hoje = date.today()
            anos = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
            st.info(f"Idade Calculada: {anos} anos")
            
            raca = st.selectbox("Raça", ["SRD", "Spitz", "Poodle", "Shih Tzu", "Outra"])
            sexo = st.selectbox("Sexo", ["Macho", "Fêmea"])
            
            if st.form_submit_button("✅ Cadastrar Pet"):
                if nome_p:
                    st.session_state['pets'].append({
                        "id": id_p, "nome": nome_p.upper(), "idade": f"{anos} anos",
                        "tutor": t_lista[t_sel]['nome'], "raca": raca, "sexo": sexo
                    })
                    st.success(f"Pet {nome_p} registrado!")

# --- SESSÃO 3: PRONTUÁRIO (PREENCHIDO) ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento Clínico")
    if not st.session_state['pets']:
        st.info("Cadastre um pet para habilitar o prontuário.")
    else:
        with st.form("f_pront"):
            p_lista = {p['nome']: p for p in st.session_state['pets']}
            pet_atendimento = st.selectbox("Paciente", list(p_lista.keys()))
            col1, col2 = st.columns(2)
            peso = col1.text_input("Peso (kg)")
            temp = col2.text_input("Temperatura (°C)")
            relato = st.text_area("Relato da Consulta (Win+H)", height=200)
            if st.form_submit_button("Salvar Histórico"):
                st.session_state['historico'].append({
                    "Data": date.today().strftime("%d/%m/%Y"),
                    "Pet": pet_atendimento, "Peso": peso, "Temp": temp, "Relato": relato
                })
                st.success("Prontuário arquivado!")

# --- SESSÃO 4: FINANCEIRO E DASHBOARD ---
elif menu == "💰 Financeiro":
    st.subheader("💰 Cobrança")
    if not st.session_state['clientes']:
        st.error("Sem clientes para cobrança.")
    else:
        with st.form("f_pag"):
            t_nomes = [c['nome'] for c in st.session_state['clientes']]
            t_cobrar = st.selectbox("Tutor", t_nomes)
            servicos = st.multiselect("Serviços", [i['Item'] for i in st.session_state['estoque']])
            if st.form_submit_button("Gerar Recibo"):
                st.success("Recibo gerado com sucesso!")

elif menu == "🏠 Dashboard":
    st.write(f"### Bem-vindo, Doutor!")
    st.metric("Total de Clientes", len(st.session_state['clientes']))
    st.metric("Total de Pets", len(st.session_state['pets']))
    if st.session_state['historico']:
        st.table(pd.DataFrame(st.session_state['historico']))
