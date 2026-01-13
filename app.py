import streamlit as st

# Configuração da Página com visual limpo
st.set_page_config(page_title="PetControl Pro", layout="wide", initial_sidebar_state="expanded")

# --- ESTILO CSS CUSTOMIZADO ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; border: none; height: 3em; }
    .stButton>button:hover { background-color: #0056b3; color: white; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    .stHeader { color: #1e3d59; }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border-left: 5px solid #007bff;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicialização do Banco de Dados em Memória
if 'clientes' not in st.session_state: st.session_state['clientes'] = {}
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'proximo_cod_cliente' not in st.session_state: st.session_state['proximo_cod_cliente'] = 1
if 'proximo_cod_pet' not in st.session_state: st.session_state['proximo_cod_pet'] = 1

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/194/194279.png", width=100)
    st.title("PetControl Pro")
    menu = st.radio("Navegação", ["Dashboard", "Cadastrar Cliente", "Cadastrar Pet", "Relatório Geral"])
    st.info("Sistema v5.0 - Premium Design")

# --- PÁGINA: DASHBOARD ---
if menu == "Dashboard":
    st.title("📊 Painel de Controle")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Clientes", len(st.session_state['clientes']))
    col2.metric("Total de Pets", len(st.session_state['pets']))
    col3.metric("Último Cód", f"{st.session_state['proximo_cod_cliente']-1:04d}")

# --- PÁGINA: CADASTRAR CLIENTE ---
elif menu == "Cadastrar Cliente":
    st.title("👤 Novo Cliente")
    cod_cliente = f"{st.session_state['proximo_cod_cliente']:04d}"
    
    with st.container():
        st.markdown(f'<div class="card">Código do Registro: <b>{cod_cliente}</b></div>', unsafe_allow_html=True)
        with st.form("form_cliente"):
            col1, col2 = st.columns(2)
            nome = col1.text_input("Nome Completo")
            cpf = col2.text_input("CPF")
            email = col1.text_input("E-mail")
            whatsapp = col2.text_input("WhatsApp")
            endereco = st.text_area("Endereço")
            
            if st.form_submit_button("Finalizar Cadastro"):
                if nome:
                    st.session_state['clientes'][cod_cliente] = nome
                    st.session_state['proximo_cod_cliente'] += 1
                    st.success("Cadastro realizado!")
                    st.balloons()
                else: st.error("Nome obrigatório")

# --- PÁGINA: CADASTRAR PET ---
elif menu == "Cadastrar Pet":
    st.title("🐶 Novo Pet")
    if not st.session_state['clientes']:
        st.warning("Cadastre um cliente primeiro.")
    else:
        cod_pet = f"{st.session_state['proximo_cod_pet']:04d}"
        with st.form("form_pet"):
            opcoes = [f"{id} - {nome}" for id, nome in st.session_state['clientes'].items()]
            dono = st.selectbox("Selecione o Dono", opcoes)
            nome_pet = st.text_input("Nome do Pet")
            raca = st.text_input("Raça")
            
            col_id1, col_id2 = st.columns(2)
            idade_v = col_id1.number_input("Idade", min_value=0)
            idade_u = col_id2.selectbox("Unidade", ["Anos", "Meses"])
            
            foto = st.file_uploader("Foto do Pet", type=['png','jpg','jpeg'])
            
            if st.form_submit_button("Cadastrar Pet"):
                st.session_state['pets'].append({
                    "id": cod_pet, "dono": dono, "nome": nome_pet,
                    "raca": raca, "idade": f"{idade_v} {idade_u}", "foto": foto
                })
                st.session_state['proximo_cod_pet'] += 1
                st.success("Pet cadastrado!")

# --- PÁGINA: RELATÓRIO GERAL ---
elif menu == "Relatório Geral":
    st.title("📋 Relatório de Clientes e Pets")
    if not st.session_state['pets']:
        st.info("Nenhum pet cadastrado.")
    else:
        for p in st.session_state['pets']:
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <h3>🐾 {p['nome']} (ID: {p['id']})</h3>
                    <p><b>Dono:</b> {p['dono']}<br>
                    <b>Raça:</b> {p['raca']} | <b>Idade:</b> {p['idade']}</p>
                </div>
                """, unsafe_allow_html=True)
                if p['foto']:
                    st.image(p['foto'], width=250)
