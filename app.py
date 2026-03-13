import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. ESTILO E CONFIGURAÇÃO
st.set_page_config(page_title="Ribeira Vet Pro v20", layout="wide", page_icon="🏥")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #0F172A !important; }
    
    /* BOTÃO AMARELO VIBRANTE */
    div.stButton > button {
        background-color: #FFD700 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 2px solid #B8860B !important;
        border-radius: 8px !important;
        width: 100% !important;
    }
    
    /* TABELAS E CARDS */
    .stDataFrame { background-color: #F8FAFC !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNÇÕES DE BANCO DE DADOS
def salvar_dados(df, arquivo):
    df.to_csv(arquivo, index=False)

def carregar_dados(arquivo, colunas):
    if os.path.exists(arquivo):
        return pd.read_csv(arquivo)
    return pd.DataFrame(columns=colunas)

# Arquivos Versão 20
ARQ_TUTORES = 'db_tutores_v20.csv'
ARQ_PETS = 'db_pets_v20.csv'
ARQ_VENDAS = 'db_vendas_v20.csv'

# Inicialização
if 'dt_tutores' not in st.session_state:
    st.session_state.dt_tutores = carregar_dados(ARQ_TUTORES, ["CPF", "Nome", "Email", "WhatsApp", "Endereço", "Bairro", "Cidade"])
if 'dt_pets' not in st.session_state:
    st.session_state.dt_pets = carregar_dados(ARQ_PETS, ["Dono_CPF", "Pet_Nome", "Especie", "Raca", "Sexo", "Peso", "Idade"])

# 3. BARRA LATERAL
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=40)
    st.title("Ribeira Vet Pro")
    menu = st.radio("Navegação:", ["👤 Clientes", "🐾 Animais", "⚕️ Prontuário", "💰 Financeiro"])
    st.divider()
    st.info("Versão 20.0 - Estável")

# 4. MÓDULOS

if menu == "👤 Clientes":
    st.header("👤 Cadastro de Proprietário")
    
    # Lista de Clientes já cadastrados
    if not st.session_state.dt_tutores.empty:
        st.subheader("Clientes Cadastrados")
        st.dataframe(st.session_state.dt_tutores, use_container_width=True, hide_index=True)
    
    st.divider()
    st.subheader("Novo Cadastro")
    with st.form("novo_tutor", clear_on_submit=True):
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome Completo*")
        cpf = c2.text_input("CPF (identificador único)*")
        email = c1.text_input("E-mail")
        whats = c2.text_input("WhatsApp com DDD")
        end = st.text_input("Endereço Completo (Rua, Nº)")
        c3, c4 = st.columns(2)
        bairro = c3.text_input("Bairro")
        cidade = c4.text_input("Cidade")
        
        if st.form_submit_button("SALVAR PROPRIETÁRIO"):
            if nome and cpf:
                if cpf in st.session_state.dt_tutores['CPF'].values:
                    st.error("Este CPF já está cadastrado!")
                else:
                    novo = pd.DataFrame([{"CPF": cpf, "Nome": nome, "Email": email, "WhatsApp": whats, "Endereço": end, "Bairro": bairro, "Cidade": cidade}])
                    st.session_state.dt_tutores = pd.concat([st.session_state.dt_tutores, novo], ignore_index=True)
                    salvar_dados(st.session_state.dt_tutores, ARQ_TUTORES)
                    st.success(f"Tutor {nome} salvo com sucesso!")
                    st.rerun() # FORÇA A ATUALIZAÇÃO PARA APARECER NA LISTA DO PET
            else:
                st.error("Nome e CPF são obrigatórios!")

elif menu == "🐾 Animais":
    st.header("🐾 Cadastro de Animal")
    
    if st.session_state.dt_tutores.empty:
        st.warning("⚠️ Você precisa cadastrar um Cliente antes de cadastrar um animal.")
    else:
        with st.form("novo_pet"):
            # Aqui buscamos a lista de tutores atualizada
            tutor_opcoes = st.session_state.dt_tutores['Nome'] + " (" + st.session_state.dt_tutores['CPF'] + ")"
            selecionado = st.selectbox("Selecione o Dono:", tutor_opcoes)
            
            st.divider()
            c1, c2, c3 = st.columns(3)
            p_nome = c1.text_input("Nome do Pet")
            p_esp = c2.selectbox("Espécie", ["Canina", "Felina", "Ave", "Exótico"])
            p_raca = c3.text_input("Raça")
            
            c4, c5, c6 = st.columns(3)
            p_sexo = c4.selectbox("Sexo", ["Macho", "Fêmea"])
            p_peso = c5.text_input("Peso (kg)")
            p_idade = c6.text_input("Idade")
            
            if st.form_submit_button("VINCULAR ANIMAL AO DONO"):
                if p_nome:
                    cpf_vinc = selecionado.split("(")[-1].replace(")", "")
                    novo_p = pd.DataFrame([{"Dono_CPF": cpf_vinc, "Pet_Nome": p_nome, "Especie": p_esp, "Raca": p_raca, "Sexo": p_sexo, "Peso": p_peso, "Idade": p_idade}])
                    st.session_state.dt_pets = pd.concat([st.session_state.dt_pets, novo_p], ignore_index=True)
                    salvar_dados(st.session_state.dt_pets, ARQ_PETS)
                    st.success(f"{p_nome} vinculado a {selecionado}!")
                else:
                    st.error("O nome do animal é obrigatório.")

    st.subheader("Lista de Animais")
    st.dataframe(st.session_state.dt_pets, use_container_width=True, hide_index=True)

elif menu == "💰 Financeiro":
    st.header("💰 Gestão Financeira")
    t1, t2 = st.tabs(["🏷️ Serviços e Preços", "🧾 Gerar Recibo"])
    
    with t1:
        st.subheader("Tabela de Valores")
        servicos = {
            "Item": ["Consulta Geral", "Vacina V10", "Vacina Raiva", "Castração Cão", "Castração Gato", "Exame de Sangue"],
            "Preço": ["R$ 150,00", "R$ 130,00", "R$ 90,00", "R$ 450,00", "R$ 300,00", "R$ 110,00"]
        }
        st.table(pd.DataFrame(servicos))
        
    with t2:
        st.subheader("Emissão de Recibo")
        if st.session_state.dt_tutores.empty:
            st.info("Cadastre um cliente para gerar recibos.")
        else:
            cli_recibo = st.selectbox("Para quem é o recibo?", st.session_state.dt_tutores['Nome'])
            serv_recibo = st.text_input("Descrição do Serviço/Produto")
            valor_recibo = st.text_input("Valor total (R$)")
            
            if st.button("GERAR TEXTO DO RECIBO"):
                data_atual = datetime.now().strftime("%d/%m/%Y")
                recibo_final = f"""
                ==========================================
                RECIBO - RIBEIRA VET PRO
                ==========================================
                DATA: {data_atual}
                CLIENTE: {cli_recibo}
                
                REFERENTE A: {serv_recibo}
                VALOR TOTAL: R$ {valor_recibo}
                
                ------------------------------------------
                Assinatura do Responsável
                """
                st.code(recibo_final)
                st.info("Copie o texto acima e envie via WhatsApp.")
