import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN ESTÁVEL ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 5px; }
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
for key in ['clientes', 'pets', 'estoque', 'vendas', 'historico']:
    if key not in st.session_state: st.session_state[key] = {} if key == 'clientes' else []
if 'prox_c' not in st.session_state: st.session_state['prox_c'] = 1
if 'prox_p' not in st.session_state: st.session_state['prox_p'] = 1

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", use_container_width=True)
    st.markdown("<h2 style='text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["Dashboard", "Tutores", "Animais", "Prontuário", "Histórico", "Estoque", "Faturamento"])

# --- LÓGICA DAS PÁGINAS ---
if menu == "Dashboard":
    st.title("📊 Painel Administrativo")
    c1, c2 = st.columns(2)
    c1.metric("Tutores", len(st.session_state['clientes']))
    c2.metric("Pacientes", len(st.session_state['pets']))

elif menu == "Tutores":
    st.title("👤 Cadastro de Tutores")
    with st.form("f_tutor"):
        cod = f"T-{st.session_state['prox_c']:04d}"
        n = st.text_input("Nome Completo")
        cpf = st.text_input("CPF")
        zap = st.text_input("WhatsApp")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("Salvar"):
            st.session_state['clientes'][cod] = {"nome": n, "cpf": cpf, "zap": zap, "email": email, "end": end}
            st.session_state['prox_c'] += 1
            st.success("Tutor Salvo!")

elif menu == "Animais":
    st.title("🐶 Cadastro de Pacientes")
    if not st.session_state['clientes']: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            cod_p = f"P-{st.session_state['prox_p']:04d}"
            tutores = [f"{k} - {v['nome']}" for k, v in st.session_state['clientes'].items()]
            tutor = st.selectbox("Dono", tutores)
            nome_p = st.text_input("Nome do Animal")
            raca = st.text_input("Raça")
            foto = st.file_uploader("Foto", type=['jpg','png'])
            if st.form_submit_button("Registrar"):
                st.session_state['pets'].append({"id": cod_p, "dono": tutor, "nome": nome_p, "raca": raca, "foto": foto})
                st.session_state['prox_p'] += 1
                st.success("Pet Registrado!")

elif menu == "Prontuário":
    st.title("🩺 Atendimento Clínico")
    if not st.session_state['pets']: st.info("Cadastre um animal primeiro.")
    else:
        with st.form("f_atend"):
            lista = [f"{p['id']} - {p['nome']}" for p in st.session_state['pets']]
            paciente = st.selectbox("Paciente", lista)
            c1, c2, c3 = st.columns(3)
            peso, temp, cor = c1.text_input("Peso"), c2.text_input("Temp"), c3.text_input("Cor")
            diag = st.text_area("Anamnese e Diagnóstico (Use Win+H para ditar)")
            if st.form_submit_button("Arquivar"):
                st.session_state['historico'].append({"data": datetime.now().strftime("%d/%m/%Y"), "paciente": paciente, "diag": diag})
                st.success("Atendimento Salvo!")

elif menu == "Histórico":
    st.title("📋 Histórico Clínico")
    for h in reversed(st.session_state['historico']):
        with st.expander(f"{h['data']} - {h['paciente']}"):
            st.write(h['diag'])

elif menu == "Estoque":
    st.title("💊 Medicamentos e Vacinas")
    with st.form("f_est"):
        i = st.text_input("Item")
        p = st.number_input("Preço", min_value=0.0)
        if st.form_submit_button("Add"):
            st.session_state['estoque'].append({"item": i, "preco": p})

elif menu == "Faturamento":
    st.title("💰 Fechamento")
    if not st.session_state['estoque']: st.info("Cadastre itens no estoque.")
    else:
        with st.form("f_fin"):
            tutor = st.selectbox("Tutor", [v['nome'] for v in st.session_state['clientes'].values()])
            itens = st.multiselect("Itens", [i['item'] for i in st.session_state['estoque']])
            if st.form_submit_button("Gerar Total"):
                total = sum(i['preco'] for i in st.session_state['estoque'] if i['item'] in itens)
                st.session_state['vendas'].append({"total": total})
                st.write(f"### Total: R$ {total:.2f}")
