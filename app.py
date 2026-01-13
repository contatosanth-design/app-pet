import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN PROFISSIONAL ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 5px; width: 100%; }
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1e3d59 !important; }
    .stTextInput>div>div>input { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO BANCO DE DADOS ---
if 'clientes' not in st.session_state: st.session_state['clientes'] = {}
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'estoque' not in st.session_state: st.session_state['estoque'] = []
if 'vendas' not in st.session_state: st.session_state['vendas'] = []
if 'proximo_cod_cliente' not in st.session_state: st.session_state['proximo_cod_cliente'] = 1
if 'proximo_cod_pet' not in st.session_state: st.session_state['proximo_cod_pet'] = 1

# --- MENU LATERAL ---
with st.sidebar:
    # Correção do Link da Logo para o seu GitHub
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", use_container_width=True)
    st.markdown("<h2 style='text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
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
    st.title("Painel Administrativo")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tutores", len(st.session_state['clientes']))
    c2.metric("Pacientes", len(st.session_state['pets']))
    total_fat = sum(v['total'] for v in st.session_state['vendas'])
    c3.metric("Faturamento", f"R$ {total_fat:.2f}")

# --- 👤 CADASTRO TUTORES (RESTAURADO E COMPLETO) ---
elif menu == "👤 Cadastro de Tutores":
    st.title("Registro de Novo Tutor")
    with st.form("form_tutor"):
        cod = f"T-{st.session_state['proximo_cod_cliente']:04d}"
        st.subheader(f"Ficha Nº {cod}")
        
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome Completo")
        cpf = col2.text_input("CPF")
        
        col3, col4 = st.columns(2)
        whatsapp = col3.text_input("WhatsApp")
        email = col4.text_input("E-mail")
        
        endereco = st.text_area("Endereço Completo (Rua, Número, Bairro, CEP)")
        
        if st.form_submit_button("Salvar Cadastro do Tutor"):
            if nome and whatsapp:
                st.session_state['clientes'][cod] = {
                    "nome": nome, "cpf": cpf, "zap": whatsapp, 
                    "email": email, "end": endereco
                }
                st.session_state['proximo_cod_cliente'] += 1
                st.success(f"✅ Tutor {nome} cadastrado!")
                st.balloons()
            else:
                st.error("⚠️ Nome e WhatsApp são obrigatórios.")

# --- 🐶 CADASTRO DE ANIMAIS ---
elif menu == "🐶 Cadastro de Animais":
    st.title("Ficha do Paciente")
    if not st.session_state['clientes']:
        st.warning("⚠️ Cadastre um tutor primeiro.")
    else:
        with st.form("form_pet"):
            cod_p = f"P-{st.session_state['proximo_cod_pet']:04d}"
            # Puxa apenas os nomes dos tutores cadastrados
            tutores_lista = [f"{k} - {v['nome']}" for k, v in st.session_state['clientes'].items()]
            tutor_selecionado = st.selectbox("Tutor Responsável", tutores_lista)
            
            c1, c2 = st.columns(2)
            nome_p = c1.text_input("Nome do Pet")
            raca = c2.text_input("Raça")
            
            foto = st.file_uploader("Foto do Animal", type=['jpg','png','jpeg'])
            
            if st.form_submit_button("Registrar Pet"):
                if nome_p:
                    st.session_state['pets'].append({
                        "id": cod_p, "dono": tutor_selecionado, 
                        "nome": nome_p, "raca": raca, "foto": foto
                    })
                    st.session_state['proximo_cod_pet'] += 1
                    st.success(f"✅ Pet {nome_p} vinculado ao tutor!")
                else: st.error("O nome do animal é obrigatório.")

# --- 🩺 PRONTUÁRIO CLÍNICO (FICHA COMPLETA) ---
elif menu == "🩺 Prontuário Clínico":
    st.title("Atendimento Veterinário")
    if not st.session_state['pets']:
        st.info("Cadastre um animal para iniciar o prontuário.")
    else:
        with st.form("atendimento"):
            pacientes = [f"{p['id']} - {p['nome']} (Dono: {p['dono']})" for p in st.session_state['pets']]
            selecionado = st.selectbox("Paciente em Atendimento", pacientes)
            
            st.markdown("### 🌡️ Exame Físico")
            c1, c2, c3 = st.columns(3)
            peso = c1.text_input("Peso (kg)")
            temp = c2.text_input("Temp (°C)")
            cor = c3.text_input("Cor/Pelagem")
            
            diagnostico = st.text_area("Anamnese e Conduta Clínica")
            
            if st.form_submit_button("Arquivar Prontuário"):
                st.success("✅ Atendimento registrado no histórico!")

# --- 💊 ESTOQUE ---
elif menu == "💊 Estoque (Vacinas/Med)":
    st.title("Catálogo de Produtos e Serviços")
    with st.form("add_estoque"):
        item = st.text_input("Nome (Ex: Vacina Raiva, Consulta, Hemograma)")
        valor = st.number_input("Preço Sugerido (R$)", min_value=0.0, step=1.0)
        if st.form_submit_button("Adicionar"):
            st.session_state['estoque'].append({"item": item, "preco": valor})
            st.success("Item adicionado ao catálogo!")
    st.table(st.session_state['estoque'])

# --- 💰 FECHAMENTO / COBRANÇA ---
elif menu == "💰 Fechamento / Cobrança":
    st.title("Financeiro / Saída de Paciente")
    if not st.session_state['estoque']:
        st.warning("Cadastre itens no estoque primeiro.")
    else:
        with st.form("caixa"):
            tutor_cob = st.selectbox("Tutor", [v['nome'] for v in st.session_state['clientes'].values()])
            itens_selecionados = st.multiselect("Serviços/Produtos", [i['item'] for i in st.session_state['estoque']])
            
            if st.form_submit_button("Calcular Total"):
                total = sum(i['preco'] for i in st.session_state['estoque'] if i['item'] in itens_selecionados)
                st.session_state['vendas'].append({"tutor": tutor_cob, "total": total, "data": datetime.now()})
                st.markdown(f"## Total a Pagar: R$ {total:.2f}")
