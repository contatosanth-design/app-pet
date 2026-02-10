import streamlit as st
import sqlite3
from datetime import date, datetime

# ================= CONFIG =================
st.set_page_config(page_title="Ribeira Vet Pro v8.5", layout="wide", page_icon="🐾")

# ================= BANCO ==================
conn = sqlite3.connect("ribeira_vet.db", check_same_thread=False)
c = conn.cursor()

# ---------- TABELAS ----------
c.execute("""
CREATE TABLE IF NOT EXISTS tutores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT,
    nome TEXT,
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

# ================= MENU ====================
menu = st.sidebar.radio(
    "Navegação",
    ["Tutores", "Pacientes", "Prontuário", "Serviços & Produtos", "Financeiro"]
)

# ================= TUTORES =================
if menu == "Tutores":
    st.header("👤 Cadastro de Tutores")

    with st.form("tutor"):
        nome = st.text_input("Nome completo").upper()
        zap = st.text_input("WhatsApp")
        end = st.text_input("Endereço")
        if st.form_submit_button("Salvar"):
            codigo = novo_codigo("CLI", "tutores")
            c.execute(
                "INSERT INTO tutores VALUES (NULL,?,?,?,?)",
                (codigo, nome, zap, end)
            )
            conn.commit()
            st.success(f"Tutor cadastrado: {codigo}")

    st.divider()
    st.subheader("📋 Tutores Cadastrados")
    for t in c.execute("SELECT codigo, nome FROM tutores"):
        st.write(f"{t[0]} – {t[1]}")

# ================= PACIENTES =================
elif menu == "Pacientes":
    st.header("🐶 Cadastro de Pets")

    tutores = c.execute("SELECT id, codigo, nome FROM tutores").fetchall()
    if not tutores:
        st.warning("Cadastre um tutor primeiro.")
    else:
        tutor = st.selectbox(
            "Tutor",
            tutores,
            format_func=lambda x: f"{x[1]} – {x[2]}"
        )

        with st.form("pet"):
            nome = st.text_input("Nome do pet").upper()
            raca = st.text_input("Raça")
            nasc = st.date_input("Nascimento")
            if st.form_submit_button("Salvar"):
                codigo = novo_codigo("PET", "pets")
                c.execute(
                    "INSERT INTO pets VALUES (NULL,?,?,?,?,?)",
                    (codigo, tutor[0], nome, raca, str(nasc))
                )
                conn.commit()
                st.success(f"Pet cadastrado: {codigo}")

    st.divider()
    st.subheader("🐾 Pets Cadastrados")
    for p in c.execute("""
        SELECT pets.codigo, pets.nome, pets.raca, pets.nascimento, tutores.nome
        FROM pets JOIN tutores ON pets.tutor_id = tutores.id
    """):
        st.write(f"{p[0]} – {p[1]} ({p[2]}) | Tutor: {p[4]} | {idade(p[3])} anos")

# ================= PRONTUÁRIO =================
elif menu == "Prontuário":
    st.header("📝 Atendimento")

    pets = c.execute("""
        SELECT pets.id, pets.codigo, pets.nome, tutores.nome
        FROM pets JOIN tutores ON pets.tutor_id = tutores.id
    """).fetchall()

    if pets:
        pet = st.selectbox(
            "Paciente",
            pets,
            format_func=lambda x: f"{x[1]} – {x[2]} | Tutor: {x[3]}"
        )

        with st.form("consulta"):
            anamnese = st.text_area("Anamnese")
            conduta = st.text_area("Conduta")
            valor = st.number_input("Valor R$", min_value=0.0)
            if st.form_submit_button("Salvar Atendimento"):
                c.execute(
                    "INSERT INTO atendimentos VALUES (NULL,?,?,?,?,?)",
                    (pet[0], str(date.today()), anamnese, conduta, valor)
                )
                conn.commit()
                st.success("Atendimento registrado")

# ================= SERVIÇOS =================
elif menu == "Serviços & Produtos":
    st.header("🧾 Serviços e Produtos")

    with st.form("item"):
        tipo = st.selectbox("Tipo", ["Serviço", "Produto"])
        nome = st.text_input("Nome")
        preco = st.number_input("Preço R$", min_value=0.0)
        if st.form_submit_button("Adicionar"):
            c.execute(
                "INSERT INTO itens VALUES (NULL,?,?,?)",
                (tipo, nome, preco)
            )
            conn.commit()
            st.success("Item cadastrado")

    st.divider()
    for i in c.execute("SELECT tipo, nome, preco FROM itens"):
        st.write(f"{i[0]} – {i[1]} | R$ {i[2]:.2f}")

# ================= FINANCEIRO =================
elif menu == "Financeiro":
    st.header("💰 Financeiro")

    total = c.execute("SELECT SUM(valor) FROM atendimentos").fetchone()[0] or 0
    st.metric("Faturamento Total", f"R$ {total:.2f}")
