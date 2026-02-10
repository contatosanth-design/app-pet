import streamlit as st
import sqlite3
from datetime import date, datetime

# ================= CONFIG =================
st.set_page_config(
    page_title="Ribeira Vet Pro v10.1",
    layout="wide",
    page_icon="🐾"
)

# ================= BANCO ==================
conn = sqlite3.connect("ribeira_vet.db", check_same_thread=False)
c = conn.cursor()

# ================= TABELAS =================
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
    tutor_id INTEGER,
    nome TEXT,
    raca TEXT,
    nascimento TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER,
    data TEXT,
    tipo TEXT,
    link TEXT,
    rascunho TEXT,
    anamnese TEXT,
    conduta TEXT,
    valor REAL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    nome TEXT,
    preco REAL
)
""")

conn.commit()

# ================= DADOS DE EXEMPLO =================
def popular_itens():
    c.execute("SELECT COUNT(*) FROM itens")
    if c.fetchone()[0] == 0:
        exemplos = [
            ("Serviço", "Consulta Clínica", 120),
            ("Serviço", "Vacinação V8", 90),
            ("Serviço", "Vacinação Antirrábica", 70),
            ("Serviço", "Castração Canina", 600),
            ("Serviço", "Exame de Sangue", 150),
            ("Produto", "Vermífugo", 35),
            ("Produto", "Antipulgas", 120),
            ("Produto", "Ração Premium", 280),
            ("Produto", "Shampoo Veterinário", 45),
        ]
        c.executemany(
            "INSERT INTO itens (tipo, nome, preco) VALUES (?,?,?)",
            exemplos
        )
        conn.commit()

popular_itens()

# ================= FUNÇÕES =================
def novo_codigo(prefixo, tabela):
    c.execute(f"SELECT COUNT(*) FROM {tabela}")
    total = c.fetchone()[0] + 1
    return f"{prefixo}-{str(total).zfill(4)}"

def idade(nasc):
    if not nasc:
        return "N/D"
    nasc = datetime.strptime(nasc, "%Y-%m-%d").date()
    hoje = date.today()
    return hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))

# ================= MENU =
