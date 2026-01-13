import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Veterinário da Ribeira", layout="wide")

# --- DESIGN PREMIUM E CORES ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59; color: white; }
    [data-testid="stSidebar"] * { color: white !important; font-size: 14px; }
    .stButton>button { background-color: #ff6e40; color: white; border-radius: 5px; border: none; }
    .main { background-color: #f5f7f9; }
    h1 { color: #1e3d59; font-size: 24px !important; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO BANCO DE DADOS ---
for key in ['clientes', 'pets', 'estoque', 'vendas']:
    if key not in st.session_state: st.session_state[key] = {} if key == 'clientes' else []

if 'proximo_cod_cliente' not in st.session_state: st.session_state['proximo_cod_cliente'] = 1
if 'proximo_cod_pet' not in st.session_state: st.session_state['proximo_cod_pet'] = 1

# --- MENU LATERAL ORGANIZADO ---
with st.sidebar:
    # Link direto para o arquivo que você subiu no GitHub
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", use_container_width=True)
    st.markdown("<h2 style='text-align: center;'> Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("NAVEGAÇÃO", [
        "📊 Dashboard", 
        "👤 Cadastro de Tutores", 
        "🐶 Cadastro de Animais", 
        "🩺 Prontuário Clínico",
        "💊 Estoque (Vacinas/Med)",
        "💰 Fechamento / Cobrança"
    ])

# --- 📊 DASHBOARD ---
if menu == "📊 Dashboard":
    st.title("Painel de Controle do Consultório")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tutores", len(st.session_state['clientes']))
    c2.metric("Pacientes", len(st.session_state['pets']))
    c3.metric("Faturamento", f"R$ {sum(v['total'] for v in st.session_state['vendas']):.2f}")

# --- 👤 CADASTRO TUTORES ---
elif menu == "👤 Cadastro de Tutores":
    st.title("Registro de Novo Tutor")
    with st.form("form_tutor"):
        cod = f"T-{st.session_state['proximo_cod_cliente']:04d}"
        nome = st.text_input("Nome do Cliente")
        whatsapp = st.text_input("WhatsApp")
        if st.form_submit_button("Salvar Tutor"):
            st.session_state['clientes'][cod] = nome
            st.session_state['proximo_cod_cliente'] += 1
            st.success("Tutor cadastrado!")

# --- 🐶 CADASTRO DE ANIMAIS (O que estava faltando) ---
elif menu == "🐶 Cadastro de Animais":
    st.title("Ficha do Animal")
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("form_pet"):
            cod_p = f"P-{st.session_state['proximo_cod_pet']:04d}"
            lista_t = [f"{id} - {n}" for id, n in st.session_state['clientes'].items()]
            tutor = st.selectbox("Dono", lista_t)
            nome_p = st.text_input("Nome do Animal")
            raca = st.text_input("Raça")
            foto = st.file_uploader("Foto", type=['jpg','png'])
            if st.form_submit_button("Registrar Paciente"):
                st.session_state['pets'].append({"id": cod_p, "dono": tutor, "nome": nome_p, "raca": raca, "foto": foto})
                st.session_state['proximo_cod_pet'] += 1
                st.success("Animal registrado!")

# --- 💊 ESTOQUE (PRODUTOS/VACINAS) ---
elif menu == "💊 Estoque (Vacinas/Med)":
    st.title("Gerenciar Medicamentos e Vacinas")
    with st.form("form_estoque"):
        item = st.text_input("Nome do Produto/Serviço (Ex: Vacina V10, Consulta)")
        preco = st.number_input("Preço de Venda (R$)", min_value=0.0)
        if st.form_submit_button("Adicionar ao Catálogo"):
            st.session_state['estoque'].append({"item": item, "preco": preco})
            st.success("Item adicionado!")
    st.table(st.session_state['estoque'])

# --- 🩺 PRONTUÁRIO CLÍNICO ---
elif menu == "🩺 Prontuário Clínico":
    st.title("Atendimento Veterinário")
    if not st.session_state['pets']:
        st.warning("Cadastre um animal primeiro.")
    else:
        with st.expander("📝 Nova Evolução Clínica", expanded=True):
            lista_p = [f"{p['id']} - {p['nome']} ({p['dono']})" for p in st.session_state['pets']]
            paciente = st.selectbox("Paciente", lista_p)
            col1, col2 = st.columns(2)
            peso = col1.text_input("Peso (kg)")
            temp = col2.text_input("Temp (°C)")
            obs = st.text_area("Diagnóstico e Prescrição")
            if st.button("Finalizar Atendimento"):
                st.success("Atendimento arquivado!")

# --- 💰 FECHAMENTO / COBRANÇA ---
elif menu == "💰 Fechamento / Cobrança":
    st.title("Financeiro / Relatório de Saída")
    if not st.session_state['estoque']:
        st.info("Cadastre produtos no Estoque primeiro.")
    else:
        with st.form("cobranca"):
            tutor_cob = st.selectbox("Tutor para Cobrança", list(st.session_state['clientes'].values()))
            servicos = st.multiselect("Itens Utilizados", [i['item'] for i in st.session_state['estoque']])
            if st.form_submit_button("Gerar Total"):
                total = sum(i['preco'] for i in st.session_state['estoque'] if i['item'] in servicos)
                st.session_state['vendas'].append({"tutor": tutor_cob, "total": total, "data": datetime.now()})
                st.markdown(f"### Valor Total: R$ {total:.2f}")
                st.balloons()
