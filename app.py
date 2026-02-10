import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# ========================
# BANCO DE DADOS
# ========================
conn = sqlite3.connect("ribeira_vet.db", check_same_thread=False)
c = conn.cursor()

# ========================
# TABELAS
# ========================
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

c.execute("""
CREATE TABLE IF NOT EXISTS prontuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER,
    data TEXT,
    anotacoes TEXT
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
CREATE TABLE IF NOT EXISTS atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    tipo TEXT,
    valor REAL
)
""")

conn.commit()

# ========================
# DADOS DE EXEMPLO
# ========================
c.execute("SELECT COUNT(*) FROM servicos")
if c.fetchone()[0] == 0:
    exemplos = [
        ("S001", "Consulta Clínica", "Serviço", 120),
        ("S002", "Vacinação V10", "Serviço", 90),
        ("S003", "Telemedicina", "Serviço", 80),
        ("P001", "Vermífugo", "Produto", 45),
        ("P002", "Antipulgas", "Produto", 110),
        ("P003", "Ração Terapêutica", "Produto", 180)
    ]
    c.executemany(
        "INSERT INTO servicos (codigo, descricao, tipo, preco) VALUES (?,?,?,?)",
        exemplos
    )
    conn.commit()

# ========================
# MENU
# ========================
menu = st.sidebar.radio(
    "Menu",
    ["Tutores", "Pacientes", "Prontuário", "Telemedicina", "Serviços & Produtos", "Relatórios", "Financeiro"]
)

# ========================
# TUTORES
# ========================
if menu == "Tutores":
    st.header("👤 Tutores")

    codigo = st.text_input("Código")
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
        st.success("Tutor salvo")

    st.table(c.execute("SELECT codigo, nome, cpf, whatsapp FROM tutores").fetchall())

# ========================
# PACIENTES
# ========================
elif menu == "Pacientes":
    st.header("🐾 Pacientes")

    codigo = st.text_input("Código do Pet")
    nome = st.text_input("Nome")
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

    st.table(c.execute("SELECT codigo, nome, especie, raca FROM pacientes").fetchall())

# ========================
# PRONTUÁRIO
# ========================
elif menu == "Prontuário":
    st.header("📄 Prontuário / Rascunho")

    pacientes = c.execute("SELECT id, nome FROM pacientes").fetchall()
    paciente = st.selectbox("Paciente", pacientes, format_func=lambda x: x[1])

    anotacoes = st.text_area("Anotações livres", height=200)

    if st.button("Salvar Prontuário"):
        c.execute(
            "INSERT INTO prontuario (paciente_id, data, anotacoes) VALUES (?,?,?)",
            (paciente[0], datetime.now().strftime("%d/%m/%Y"), anotacoes)
        )
        conn.commit()
        st.success("Prontuário salvo")

# ========================
# TELEMEDICINA
# ========================
elif menu == "Telemedicina":
    st.header("☁️ Telemedicina")

    relato = st.text_area("Relato da consulta", height=200)
    valor = st.number_input("Valor", value=80.0)

    if st.button("Registrar Teleconsulta"):
        c.execute(
            "INSERT INTO atendimentos (data, tipo, valor) VALUES (?,?,?)",
            (datetime.now().strftime("%Y-%m-%d"), "Telemedicina", valor)
        )
        conn.commit()
        st.success("Teleconsulta registrada")

# ========================
# SERVIÇOS
# ========================
elif menu == "Serviços & Produtos":
    st.header("🧾 Serviços & Produtos")

    codigo = st.text_input("Código")
    desc = st.text_input("Descrição")
    tipo = st.selectbox("Tipo", ["Serviço", "Produto"])
    preco = st.number_input("Preço", step=1.0)

    if st.button("Salvar"):
        c.execute(
            "INSERT INTO servicos (codigo, descricao, tipo, preco) VALUES (?,?,?,?)",
            (codigo, desc, tipo, preco)
        )
        conn.commit()
        st.success("Salvo")

    st.table(c.execute("SELECT codigo, descricao, tipo, preco FROM servicos").fetchall())

# ========================
# RELATÓRIOS
# ========================
elif menu == "Relatórios":
    st.header("📊 Relatórios")

    dados = c.execute("SELECT data, tipo, valor FROM atendimentos").fetchall()
    st.table(dados)

# ========================
# FINANCEIRO
# ========================
elif menu == "Financeiro":
    st.header("💰 Financeiro")

    total = c.execute("SELECT SUM(valor) FROM atendimentos").fetchone()[0]
    st.metric("Faturamento Total", f"R$ {total if total else 0:.2f}")
