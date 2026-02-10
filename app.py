import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Clínica Veterinária", layout="wide")

# ======================
# BANCO DE DADOS
# ======================
conn = sqlite3.connect("clinica_vet.db", check_same_thread=False)
c = conn.cursor()

# ======================
# TABELAS
# ======================
c.execute("""
CREATE TABLE IF NOT EXISTS tutores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT,
    nome TEXT,
    cpf TEXT,
    whatsapp TEXT,
    endereco TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT,
    nome TEXT,
    especie TEXT,
    raca TEXT,
    tutor_id INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS prontuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER,
    data TEXT,
    rascunho TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS servicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT,
    descricao TEXT,
    tipo TEXT,
    preco REAL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS financeiro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    descricao TEXT,
    valor REAL
)
""")

conn.commit()

# ======================
# DADOS INICIAIS
# ======================
c.execute("SELECT COUNT(*) FROM servicos")
if c.fetchone()[0] == 0:
    c.executemany("""
        INSERT INTO servicos (codigo, descricao, tipo, preco)
        VALUES (?,?,?,?)
    """, [
        ("S001", "Consulta Clínica", "Serviço", 120),
        ("S002", "Vacinação", "Serviço", 90),
        ("S003", "Telemedicina", "Serviço", 80),
        ("P001", "Vermífugo", "Produto", 40),
        ("P002", "Antipulgas", "Produto", 110),
        ("P003", "Ração Terapêutica", "Produto", 180)
    ])
    conn.commit()

# ======================
# MENU
# ======================
menu = st.sidebar.radio(
    "Menu",
    ["Tutores", "Pets", "Prontuário", "Serviços & Produtos", "Financeiro"]
)

# ======================
# TUTORES
# ======================
if menu == "Tutores":
    st.header("👤 Cadastro de Tutores")

    codigo = st.text_input("Código do Tutor")
    nome = st.text_input("Nome")
    cpf = st.text_input("CPF")
    zap = st.text_input("WhatsApp")
    end = st.text_input("Endereço")

    if st.button("Salvar Tutor"):
        c.execute("""
            INSERT INTO tutores (codigo, nome, cpf, whatsapp, endereco)
            VALUES (?,?,?,?,?)
        """, (codigo, nome, cpf, zap, end))
        conn.commit()
        st.success("Tutor cadastrado")

    st.subheader("Tutores cadastrados")
    st.table(c.execute("SELECT codigo, nome, cpf, whatsapp FROM tutores").fetchall())

# ======================
# PETS
# ======================
elif menu == "Pets":
    st.header("🐾 Cadastro de Pets")

    codigo = st.text_input("Código do Pet")
    nome = st.text_input("Nome do Pet")
    especie = st.text_input("Espécie")
    raca = st.text_input("Raça")

    tutores = c.execute("SELECT id, nome FROM tutores").fetchall()
    tutor = st.selectbox("Tutor", tutores, format_func=lambda x: x[1])

    if st.button("Salvar Pet"):
        c.execute("""
            INSERT INTO pets (codigo, nome, especie, raca, tutor_id)
            VALUES (?,?,?,?,?)
        """, (codigo, nome, especie, raca, tutor[0]))
        conn.commit()
        st.success("Pet cadastrado")

    st.table(c.execute("SELECT codigo, nome, especie, raca FROM pets").fetchall())

# ======================
# PRONTUÁRIO
# ======================
elif menu == "Prontuário":
    st.header("📄 Prontuário / Rascunho")

    pets = c.execute("SELECT id, nome FROM pets").fetchall()
    pet = st.selectbox("Pet", pets, format_func=lambda x: x[1])

    rascunho = st.text_area("Anotações livres", height=250)

    if st.button("Salvar Prontuário"):
        c.execute("""
            INSERT INTO prontuario (pet_id, data, rascunho)
            VALUES (?,?,?)
        """, (pet[0], datetime.now().strftime("%d/%m/%Y"), rascunho))
        conn.commit()
        st.success("Prontuário salvo")

# ======================
# SERVIÇOS
# ======================
elif menu == "Serviços & Produtos":
    st.header("🧾 Serviços e Produtos")

    st.table(c.execute(
        "SELECT codigo, descricao, tipo, preco FROM servicos"
    ).fetchall())

# ======================
# FINANCEIRO
# ======================
elif menu == "Financeiro":
    st.header("💰 Financeiro")

    desc = st.text_input("Descrição")
    valor = st.number_input("Valor", step=1.0)

    if st.button("Registrar"):
        c.execute("""
            INSERT INTO financeiro (data, descricao, valor)
            VALUES (?,?,?)
        """, (datetime.now().strftime("%Y-%m-%d"), desc, valor))
        conn.commit()
        st.success("Registro salvo")

    total = c.execute("SELECT SUM(valor) FROM financeiro").fetchone()[0]
    st.metric("Total Geral", f"R$ {total if total else 0:.2f}")
