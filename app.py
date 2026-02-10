import streamlit as st
import sqlite3
from datetime import date, datetime

# ================= CONFIG =================
st.set_page_config(
    page_title="Ribeira Vet Pro v9.5",
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
    "Menu",
    [
        "Tutores",
        "Pacientes",
        "Prontuário",
        "Telemedicina",
        "Serviços & Produtos",
        "Relatórios",
        "Financeiro"
    ]
)

# ================= TUTORES =================
if menu == "Tutores":
    st.header("👤 Tutores")

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

# ================= PACIENTES =================
elif menu == "Pacientes":
    st.header("🐶 Pets")

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

# ================= PRONTUÁRIO =================
elif menu == "Prontuário":
    st.header("📝 Atendimento Presencial")

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
            anamnese = st.text_area("Anamnese", height=150)
            conduta = st.text_area("Conduta", height=150)
            valor = st.number_input("Valor R$", min_value=0.0)
            if st.form_submit_button("Salvar"):
                c.execute(
                    "INSERT INTO atendimentos VALUES (NULL,?,?,?,?,?,?,?)",
                    (pet[0], str(date.today()), "Presencial", "", anamnese, conduta, valor)
                )
                conn.commit()
                st.success("Atendimento presencial registrado")

# ================= TELEMEDICINA =================
elif menu == "Telemedicina":
    st.header("☁️ Consulta Online")

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

        with st.form("tele"):
            link = st.text_input("Link da chamada (WhatsApp / Meet / Zoom)")
            anamnese = st.text_area("Anamnese", height=150)
            conduta = st.text_area("Conduta", height=150)
            valor = st.number_input("Valor R$", min_value=0.0)
            if st.form_submit_button("Registrar Teleconsulta"):
                c.execute(
                    "INSERT INTO atendimentos VALUES (NULL,?,?,?,?,?,?,?)",
                    (pet[0], str(date.today()), "Online", link, anamnese, conduta, valor)
                )
                conn.commit()
                st.success("Teleconsulta registrada")

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

    for i in c.execute("SELECT tipo, nome, preco FROM itens"):
        st.write(f"{i[0]} – {i[1]} | R$ {i[2]:.2f}")

# ================= RELATÓRIOS =================
elif menu == "Relatórios":
    st.header("📊 Relatórios Mensais")

    mes = st.selectbox("Mês", list(range(1, 13)))
    ano = st.selectbox("Ano", list(range(2024, date.today().year + 1)))

    dados = c.execute("""
        SELECT data, tipo, valor FROM atendimentos
    """).fetchall()

    total = 0
    qtd = 0
    for d in dados:
        data = datetime.strptime(d[0], "%Y-%m-%d")
        if data.month == mes and data.year == ano:
            total += d[2]
            qtd += 1

    st.metric("Atendimentos", qtd)
    st.metric("Faturamento", f"R$ {total:.2f}")

# ================= FINANCEIRO =================
elif menu == "Financeiro":
    st.header("💰 Financeiro Geral")
    total = c.execute("SELECT SUM(valor) FROM atendimentos").fetchone()[0] or 0
    st.metric("Total Geral", f"R$ {total:.2f}")
