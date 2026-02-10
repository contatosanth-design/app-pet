import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="Ribeira Vet Pro",
    layout="wide"
)

# =========================
# CONEXÃO COM BANCO
# =========================
conn = sqlite3.connect("ribeira_vet.db", check_same_thread=False)
c = conn.cursor()

# =========================
# CRIAÇÃO / MIGRAÇÃO TABELAS
# =========================

# TUTORES
c.execute("""
CREATE TABLE IF NOT EXISTS tutores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT,
    nome TEXT,
    whatsapp TEXT,
    endereco TEXT
)
""")

# MIGRAÇÃO CPF
try:
    c.execute("ALTER TABLE tutores ADD COLUMN cpf TEXT")
except:
    pass

# PACIENTES
c.execute("""
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT,
    nome TEXT,
    especie TEXT,
    raca TEXT,
    tutor_id INTEGER
)
""")

# PRONTUÁRIO
c.execute("""
CREATE TABLE IF NOT EXISTS prontuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER,
    data TEXT,
    anotacoes TEXT
)
""")

# SERVIÇOS E PRODUTOS
c.execute("""
CREATE TABLE IF NOT EXISTS servicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT,
    descricao TEXT,
    tipo TEXT,
    preco REAL
)
""")

# ATENDIMENTOS
c.execute("""
CREATE TABLE IF NOT EXISTS atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    tipo TEXT,
    valor REAL
)
""")

conn.commit()

# =========================
# DADOS DE EXEMPLO (AUTOMÁTICO)
# =========================
c.execute("SELECT COUNT(*) FROM servicos")
if c.fetchone()[0] == 0:
    exemplos = [
        ("S001", "Consulta Clínica", "Serviço", 120),
        ("S002", "Vacinação V10", "Serviço", 90),
        ("S003", "Consulta Telemedicina", "Serviço", 80),
        ("P001", "Vermífugo 10kg", "Produto", 45),
        ("P002", "Antipulgas", "Produto", 110),
        ("P003", "Ração Terapêutica", "Produto", 180)
    ]
    c.executemany(
        "INSERT INTO servicos (codigo, descricao, tipo, preco) VALUES (?,?,?,?)",
        exemplos
    )
    conn.commit()

# =========================
# MENU
# =========================
menu = st.sidebar.radio(
    "Menu",
    ["Tutores", "Pacientes", "Prontuário", "Telemedicina", "Serviços & Produtos", "Relatórios", "Financeiro"]
)

# =========================
# TUTORES
# =========================
if menu == "Tutores":
    st.header("👤 Cadastro de Tutores")

    codigo = st.text_input("Código do Tutor")
    nome = st.text_input("Nome")
    cpf = st.text_input("CPF")
    zap = st.text_input("WhatsApp")
    end = st.text_input("Endereço")

    if st.button("Salvar Tutor"):
        c.execute(
            "INSERT INTO tutores (codigo, nome, cpf, whatsapp, endereco) VALUES (?,?,?,?,?)",
            (codigo, nome, cpf, zap, end)
        )
        conn.commit()
        st.success("Tutor salvo com sucesso")

    st.subheader("📋 Tutores Cadastrados")
    dados = c.execute("SELECT codigo, nome, cpf, whatsapp FROM tutores").fetchall()
    st.table(dados)

# =========================
# PACIENTES
# =========================
elif menu == "Pacientes":
    st.header("🐾 Cadastro de Pacientes")

    codigo = st.text_input("Código do Pet")
    nome = st.text_input("Nome do Pet")
    especie = st.text_input("Espécie")
    raca = st.text_input("Raça")

    tutores = c.execute("SELECT id, nome FROM tutores").fetchall()
    tutor = st.selectbox("Tutor", tutores, format_func=lambda x: x[1])

    if st.button("Salvar Paciente"):
        c.execute(
            "INSERT INTO pacientes (codigo, nome, especie, raca, tutor_id) VALUES (?,?,?,?,?)",
            (codigo, nome, especie, raca, tutor[0])
        )
        conn.commit()
        st.success("Paciente salvo")

    st.subheader("📋 Pacientes")
    st.table(c.execute("SELECT codigo, nome, especie, raca FROM pacientes").fetchall())

# =========================
# PRONTUÁRIO
# =========================
elif menu == "Prontuário":
    st.header("📄 Prontuário + Rascunho")

    pacientes = c.execute("SELECT id, nome FROM pacientes").fetchall()
    paciente = st.selectbox("Paciente", pacientes, format_func=lambda x: x[1])

    rascunho = st.text_area("📝 Anotações / Rascunho Livre", height=200)

    if st.button("Salvar Prontuário"):
        c.execute(
            "INSERT INTO prontuario (paciente_id, data, anotacoes) VALUES (?,?,?)",
            (paciente[0], datetime.now().strftime("%d/%m/
