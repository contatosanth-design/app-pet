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
    st.header("👤 Cadastro de Tutores")

    with st.form("tutor"):
        nome = st.text_input("Nome completo").upper()
        cpf = st.text_input("CPF (somente números)")
        zap = st.text_input("WhatsApp")
        end = st.text_input("Endereço")
        if st.form_submit_button("Salvar"):
            codigo = novo_codigo("CLI", "tutores")
            c.execute(
                """
                INSERT INTO tutores (codigo, nome, cpf, whatsapp, endereco)
                VALUES (?,?,?,?,?)
                """,
                (codigo, nome, cpf, zap, end)
            )
            conn.commit()
            st.success(f"Tutor cadastrado: {codigo}")

    st.divider()
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
                    """
                    INSERT INTO pets (codigo, tutor_id, nome, raca, nascimento)
                    VALUES (?,?,?,?,?)
                    """,
                    (codigo, tutor[0], nome, raca, str(nasc))
                )
                conn.commit()
                st.success(f"Pet cadastrado: {codigo}")

    st.divider()
    for p in c.execute("""
        SELECT pets.codigo, pets.nome, pets.raca, pets.nascimento, tutores.nome
        FROM pets JOIN tutores ON pets.tutor_id = tutores.id
    """):
        st.write(f"{p[0]} – {p[1]} ({p[2]}) | Tutor: {p[4]} | {idade(p[3])} anos")

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
            rascunho = st.text_area("🗒️ Rascunho (não oficial)", height=100)
            anamnese = st.text_area("Anamnese", height=120)
            conduta = st.text_area("Conduta", height=120)
            valor = st.number_input("Valor R$", min_value=0.0)
            if st.form_submit_button("Salvar Atendimento"):
                c.execute(
                    """
                    INSERT INTO atendimentos
                    (pet_id, data, tipo, link, rascunho, anamnese, conduta, valor)
                    VALUES (?,?,?,?,?,?,?,?)
                    """,
                    (pet[0], str(date.today()), "Presencial", "", rascunho, anamnese, conduta, valor)
                )
                conn.commit()
                st.success("Atendimento registrado")

# ================= TELEMEDICINA =================
elif menu == "Telemedicina":
    st.header("☁️ Teleconsulta")

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
            rascunho = st.text_area("🗒️ Rascunho", height=100)
            anamnese = st.text_area("Anamnese", height=120)
            conduta = st.text_area("Conduta", height=120)
            valor = st.number_input("Valor R$", min_value=0.0)
            if st.form_submit_button("Registrar Teleconsulta"):
                c.execute(
                    """
                    INSERT INTO atendimentos
                    (pet_id, data, tipo, link, rascunho, anamnese, conduta, valor)
                    VALUES (?,?,?,?,?,?,?,?)
                    """,
                    (pet[0], str(date.today()), "Online", link, rascunho, anamnese, conduta, valor)
                )
                conn.commit()
                st.success("Teleconsulta registrada")

# ================= SERVIÇOS =================
elif menu == "Serviços & Produtos":
    st.header("🧾 Serviços e Produtos")
    for i in c.execute("SELECT tipo, nome, preco FROM itens"):
        st.write(f"{i[0]} – {i[1]} | R$ {i[2]:.2f}")

# ================= RELATÓRIOS =================
elif menu == "Relatórios":
    st.header("📊 Relatório Mensal")

    mes = st.selectbox("Mês", range(1, 13))
    ano = st.selectbox("Ano", range(2024, date.today().year + 1))

    registros = c.execute(
        "SELECT data, valor FROM atendimentos"
    ).fetchall()

    total = 0
    qtd = 0
    for r in registros:
        d = datetime.strptime(r[0], "%Y-%m-%d")
        if d.month == mes and d.year == ano:
            total += r[1]
            qtd += 1

    st.metric("Atendimentos", qtd)
    st.metric("Faturamento", f"R$ {total:.2f}")

# ================= FINANCEIRO =================
elif menu == "Financeiro":
    st.header("💰 Financeiro Geral")
    total = c.execute("SELECT SUM(valor) FROM atendimentos").fetchone()[0] or 0
    st.metric("Total Geral", f"R$ {total:.2f}")
