import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN PROFISSIONAL ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 5px; width: 100%; }
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1e3d59 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO BANCO DE DADOS ---
if 'clientes' not in st.session_state: st.session_state['clientes'] = {}
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'estoque' not in st.session_state: st.session_state['estoque'] = []
if 'vendas' not in st.session_state: st.session_state['vendas'] = []
if 'historico' not in st.session_state: st.session_state['historico'] = []
if 'prox_c' not in st.session_state: st.session_state['prox_c'] = 1
if 'prox_p' not in st.session_state: st.session_state['prox_p'] = 1

# --- MENU LATERAL ---
with st.sidebar:
    # Logotipo Squash_pet
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", use_container_width=True)
    st.markdown("<h2 style='text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MENU", ["Dashboard", "Tutores", "Animais", "Prontuário", "Histórico", "Estoque", "Faturamento"])

# --- LÓGICA DAS PÁGINAS ---

if menu == "Dashboard":
    st.title("📊 Painel Administrativo")
    c1, c2 = st.columns(2)
    c1.metric("Tutores Cadastrados", len(st.session_state['clientes']))
    c2.metric("Pacientes Atendidos", len(st.session_state['pets']))

elif menu == "Tutores":
    st.title("👤 Cadastro de Tutor")
    with st.form("f_tutor"):
        cod = f"T-{st.session_state['prox_c']:04d}"
        col1, col2 = st.columns(2)
        n = col1.text_input("Nome Completo")
        cpf = col2.text_input("CPF")
        zap = col1.text_input("WhatsApp")
        email = col2.text_input("E-mail")
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("Salvar Tutor"):
            if n and zap:
                st.session_state['clientes'][cod] = {"nome": n, "cpf": cpf, "zap": zap, "email": email, "end": end}
                st.session_state['prox_c'] += 1
                st.success(f"Tutor {n} salvo!")
            else: st.error("Nome e WhatsApp são obrigatórios.")

elif menu == "Animais":
    st.title("🐶 Cadastro de Paciente")
    if not st.session_state['clientes']: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            cod_p = f"P-{st.session_state['prox_p']:04d}"
            t_lista = [f"{k} - {v['nome']}" for k, v in st.session_state['clientes'].items()]
            tutor = st.selectbox("Tutor Responsável", t_lista)
            c1, c2 = st.columns(2)
            nome_p = c1.text_input("Nome do Pet")
            raca = c2.text_input("Raça")
            foto = st.file_uploader("Foto do Pet", type=['jpg','png','jpeg'])
            if st.form_submit_button("Registrar Pet"):
                st.session_state['pets'].append({"id": cod_p, "dono": tutor, "nome": nome_p, "raca": raca, "foto": foto})
                st.session_state['prox_p'] += 1
                st.success(f"Pet {nome_p} registrado!")

elif menu == "Prontuário":
    st.title("🩺 Exame Clínico")
    if not st.session_state['pets']: st.info("Cadastre um animal primeiro.")
    else:
        with st.form("f_atend"):
            p_lista = [f"{p['id']} - {p['nome']}" for p in st.session_state['pets']]
            paciente = st.selectbox("Paciente", p_lista)
            c1, c2, c3 = st.columns(3)
            peso, temp, cor = c1.text_input("Peso (kg)"), c2.text_input("Temp (°C)"), c3.text_input("Cor")
            diag = st.text_area("Anamnese e Conduta (Use Win+H para ditar)")
            if st.form_submit_button("Arquivar Atendimento"):
                st.session_state['historico'].append({
                    "data": datetime.now().strftime("%d/%m/%Y"), 
                    "paciente": paciente, "peso": peso, "temp": temp, "diag": diag
                })
                st.success("Atendimento arquivado!")

elif menu == "Histórico":
    st.title("📋 Histórico Clínico")
    if not st.session_state['historico']: st.info("Nenhum atendimento registrado.")
    else:
        for h in reversed(st.session_state['historico']):
            with st.expander(f"{h['data']} - {h['paciente']}"):
                st.write(f"**Peso:** {h['peso']}kg | **Temp:** {h['temp']}°C")
                st.write(f"**Conduta:** {h['diag']}")

elif menu == "Estoque":
    st.title("💊 Medicamentos e Vacinas")
    with st.form("f_est"):
        i = st.text_input("Item/Serviço")
        p = st.number_input("Preço (R$)", min_value=0.0)
        if st.form_submit_button("Adicionar"):
            st.session_state['estoque'].append({"item": i, "preco": p})
            st.success("Item adicionado!")
    st.table(st.session_state['estoque'])

elif menu == "Faturamento":
    st.title("💰 Fechamento de Conta")
    if not st.session_state['estoque']: st.info("Cadastre itens no estoque primeiro.")
    else:
        with st.form("f_fin"):
            tutor_nomes = [v['nome'] for v in st.session_state['clientes'].values()]
            tutor = st.selectbox("Tutor", tutor_nomes)
            servicos = st.multiselect("Itens Utilizados", [i['item'] for i in st.session_state['estoque']])
            if st.form_submit_button("Gerar Total"):
                total = sum(i['preco'] for i in st.session_state['estoque'] if i['item'] in servicos)
                st.markdown(f"### Total a Pagar: R$ {total:.2f}")
