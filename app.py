import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------

st.set_page_config(
    page_title="Ribeira Vet Pro AI",
    layout="wide",
    page_icon="🐾"
)

# ---------------- CSS MODERNO ----------------

st.markdown("""
<style>

.main {
background-color:#f8fafc;
font-family: 'Inter', sans-serif;
}

.stMetric{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0 4px 6px rgba(0,0,0,0.1);
border-bottom:4px solid #3b82f6;
}

.stButton>button{
width:100%;
border-radius:10px;
height:3em;
background-color:#3b82f6;
color:white;
font-weight:bold;
border:none;
transition:0.3s;
}

.stButton>button:hover{
background-color:#2563eb;
}

[data-testid="stSidebar"]{
background-color:#1e293b;
}

[data-testid="stSidebar"] .stMarkdown{
color:white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- BANCO DE DADOS ----------------

conn = sqlite3.connect("ribeira_pro_v7.db", check_same_thread=False)
c = conn.cursor()

def init_db():

    c.execute("""
    CREATE TABLE IF NOT EXISTS tutores(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    zap TEXT,
    endereco TEXT,
    cpf TEXT)
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS pets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    raca TEXT,
    nasc TEXT,
    tutor_id INTEGER)
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS prontuario(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER,
    data TEXT,
    anamnese TEXT,
    conduta TEXT,
    valor REAL)
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS financeiro(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    desc TEXT,
    valor REAL)
    """)

    conn.commit()

init_db()

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.image("https://cdn-icons-png.flaticon.com/512/194/194279.png", width=80)

    st.title("Ribeira Vet Pro")

    menu = st.radio(
        "MENU",
        [
            "🏠 Dashboard",
            "👥 Tutores",
            "🐾 Pacientes",
            "🩺 Atendimento",
            "💰 Financeiro",
            "⚙️ Dados"
        ]
    )

    st.divider()
    st.caption("Versão 7.0")

# ---------------- DASHBOARD ----------------

if menu == "🏠 Dashboard":

    st.title("Resumo da Clínica")

    col1, col2, col3, col4 = st.columns(4)

    total_tutores = c.execute("SELECT COUNT(*) FROM tutores").fetchone()[0]
    total_pets = c.execute("SELECT COUNT(*) FROM pets").fetchone()[0]
    total_atend = c.execute("SELECT COUNT(*) FROM prontuario").fetchone()[0]

    faturamento = c.execute("SELECT SUM(valor) FROM financeiro").fetchone()[0]

    if faturamento is None:
        faturamento = 0

    col1.metric("Clientes", total_tutores)
    col2.metric("Pacientes", total_pets)
    col3.metric("Atendimentos", total_atend)
    col4.metric("Faturamento", f"R$ {faturamento:.2f}")

# ---------------- TUTORES ----------------

elif menu == "👥 Tutores":

    st.header("Cadastro de Clientes")

    with st.form("novo_tutor", clear_on_submit=True):

        col1, col2 = st.columns(2)

        nome = col1.text_input("Nome")
        cpf = col2.text_input("CPF")

        zap = col1.text_input("WhatsApp")
        endereco = col2.text_input("Endereço")

        salvar = st.form_submit_button("Salvar")

        if salvar:

            if nome:

                c.execute(
                    "INSERT INTO tutores(nome,zap,endereco,cpf) VALUES (?,?,?,?)",
                    (nome.upper(), zap, endereco, cpf)
                )

                conn.commit()

                st.success("Cliente cadastrado")

                st.rerun()

    st.divider()

    busca = st.text_input("Pesquisar cliente")

    dados = c.execute(
        "SELECT nome,zap,endereco FROM tutores WHERE nome LIKE ?",
        (f"%{busca}%",)
    ).fetchall()

    if dados:

        df = pd.DataFrame(dados, columns=["Nome", "WhatsApp", "Endereço"])

        st.dataframe(df, use_container_width=True)

# ---------------- PACIENTES ----------------

elif menu == "🐾 Pacientes":

    st.header("Cadastro de Pacientes")

    tutores = c.execute("SELECT id,nome FROM tutores").fetchall()

    if not tutores:

        st.warning("Cadastre um tutor primeiro")

    else:

        with st.form("pet_form", clear_on_submit=True):

            tutor = st.selectbox(
                "Tutor",
                tutores,
                format_func=lambda x: x[1]
            )

            nome_pet = st.text_input("Nome do pet")

            raca = st.text_input("Raça")

            nasc = st.date_input("Nascimento")

            salvar = st.form_submit_button("Cadastrar")

            if salvar:

                c.execute(
                    "INSERT INTO pets(nome,raca,nasc,tutor_id) VALUES (?,?,?,?)",
                    (nome_pet.upper(), raca, str(nasc), tutor[0])
                )

                conn.commit()

                st.success("Pet cadastrado")

# ---------------- ATENDIMENTO ----------------

elif menu == "🩺 Atendimento":

    st.header("Consulta")

    pets = c.execute("""
    SELECT pets.id,pets.nome,pets.raca,tutores.nome
    FROM pets
    JOIN tutores ON pets.tutor_id=tutores.id
    """).fetchall()

    if not pets:

        st.info("Nenhum paciente cadastrado")

    else:

        pet = st.selectbox(
            "Paciente",
            pets,
            format_func=lambda x: f"{x[1]} - {x[3]}"
        )

        with st.form("consulta", clear_on_submit=True):

            anamnese = st.text_area("Anamnese")
            conduta = st.text_area("Conduta")
            valor = st.number_input("Valor", min_value=0.0)

            finalizar = st.form_submit_button("Finalizar")

            if finalizar:

                data = datetime.now().strftime("%d/%m/%Y")

                c.execute(
                    "INSERT INTO prontuario(pet_id,data,anamnese,conduta,valor) VALUES (?,?,?,?,?)",
                    (pet[0], data, anamnese, conduta, valor)
                )

                c.execute(
                    "INSERT INTO financeiro(data,desc,valor) VALUES (?,?,?)",
                    (data, f"Consulta {pet[1]}", valor)
                )

                conn.commit()

                st.success("Consulta registrada")

# ---------------- FINANCEIRO ----------------

elif menu == "💰 Financeiro":

    st.header("Financeiro")

    dados = c.execute(
        "SELECT data,desc,valor FROM financeiro ORDER BY id DESC"
    ).fetchall()

    if dados:

        df = pd.DataFrame(dados, columns=["Data", "Descrição", "Valor"])

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Baixar CSV",
            csv,
            "financeiro.csv",
            "text/csv"
        )

    else:

        st.info("Sem movimentações")

# ---------------- RESET ----------------

elif menu == "⚙️ Dados":

    st.warning("Limpar todo sistema")

    if st.button("APAGAR TUDO"):

        c.execute("DROP TABLE IF EXISTS tutores")
        c.execute("DROP TABLE IF EXISTS pets")
        c.execute("DROP TABLE IF EXISTS prontuario")
        c.execute("DROP TABLE IF EXISTS financeiro")

        conn.commit()

        init_db()

        st.success("Sistema reiniciado")

        st.rerun()
