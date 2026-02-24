import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ribeira Vet Pro v7.0", layout="wide", page_icon="🐾")

# --- BANCO DE DADOS (SQLite - Permanente) ---
conn = sqlite3.connect("ribeira_vet_v7.db", check_same_thread=False)
c = conn.cursor()

def init_db():
    # Tabela de Tutores com Endereço Completo
    c.execute("""CREATE TABLE IF NOT EXISTS tutores 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cpf TEXT, zap TEXT, email TEXT, endereco TEXT)""")
    # Tabela de Pets com Raça e Nascimento (Padronizada)
    c.execute("""CREATE TABLE IF NOT EXISTS pets 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, raca TEXT, nascimento TEXT, tutor_id INTEGER)""")
    # Prontuário com Anamnese e Conduta
    c.execute("""CREATE TABLE IF NOT EXISTS prontuario 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, pet_id INTEGER, data TEXT, anamnese TEXT, conduta TEXT, valor REAL)""")
    # Financeiro integrado
    c.execute("""CREATE TABLE IF NOT EXISTS financeiro 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, descricao TEXT, valor REAL, tipo TEXT)""")
    conn.commit()

init_db()

# --- RAÇAS (Recuperadas da Versão 2.0) ---
RACAS_COMUNS = ["SRD", "Shih Tzu", "Poodle", "Pinscher", "Golden Retriever", "Pit Bull", "Bulldog", "Yorkshire", "Persa", "Siamês", "Outra"]

# --- FUNÇÕES DE APOIO ---
def calcular_idade(nasc_str):
    try:
        nasc = datetime.strptime(nasc_str, "%Y-%m-%d").date()
        hoje = date.today()
        return f"{hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))} anos"
    except: return "N/D"

# --- SIDEBAR ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("Navegação", ["Início", "Tutores", "Pacientes", "Atendimento", "Financeiro", "Backup"])
    st.divider()
    st.success("Ditado de Voz Ativo (Win + H) 🟢")

# --- TELA: INÍCIO (DASHBOARD) ---
if menu == "Início":
    st.header("📊 Painel de Controle")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tutores", c.execute("SELECT COUNT(*) FROM tutores").fetchone()[0])
    c2.metric("Pacientes", c.execute("SELECT COUNT(*) FROM pets").fetchone()[0])
    total_fin = c.execute("SELECT SUM(valor) FROM financeiro").fetchone()[0]
    c3.metric("Faturamento", f"R$ {total_fin if total_fin else 0:.2f}")

# --- TELA: TUTORES ---
elif menu == "Tutores":
    st.header("👤 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome = col1.text_input("NOME COMPLETO *").upper()
        cpf = col2.text_input("CPF")
        zap = col1.text_input("WHATSAPP *")
        email = col2.text_input("E-MAIL")
        endereco = st.text_input("ENDEREÇO COMPLETO")
        if st.form_submit_button("SALVAR TUTOR"):
            if nome and zap:
                c.execute("INSERT INTO tutores (nome, cpf, zap, email, endereco) VALUES (?,?,?,?,?)", 
                          (nome, cpf, zap, email, endereco))
                conn.commit()
                st.success(f"Tutor {nome} cadastrado!")
            else: st.error("Nome e WhatsApp são obrigatórios.")

# --- TELA: PACIENTES ---
elif menu == "Pacientes":
    st.header("🐶 Cadastro de Pets")
    tutores = c.execute("SELECT id, nome FROM tutores").fetchall()
    if not tutores: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet", clear_on_submit=True):
            t_id = st.selectbox("Responsável", tutores, format_func=lambda x: x[1])
            col1, col2 = st.columns(2)
            nome_p = col1.text_input("NOME DO PET *").upper()
            raca = col2.selectbox("RAÇA", RACAS_COMUNS)
            nasc = st.date_input("DATA DE NASCIMENTO", format="DD/MM/YYYY")
            if st.form_submit_button("CADASTRAR PET"):
                c.execute("INSERT INTO pets (nome, raca, nascimento, tutor_id) VALUES (?,?,?,?)", 
                          (nome_p, raca, str(nasc), t_id[0]))
                conn.commit()
                st.success(f"{nome_p} cadastrado com sucesso!")

# --- TELA: ATENDIMENTO ---
elif menu == "Atendimento":
    st.header("📝 Atendimento Médico")
    # Busca pets com nome do tutor e raça para diferenciar nomes iguais
    pets = c.execute("""SELECT pets.id, pets.nome, pets.raca, pets.nascimento, tutores.nome 
                        FROM pets JOIN tutores ON pets.tutor_id = tutores.id""").fetchall()
    
    if not pets: st.info("Sem pets cadastrados.")
    else:
        pet_sel = st.selectbox("Selecionar Paciente", pets, 
                               format_func=lambda x: f"{x[1]} ({x[2]}) - Tutor: {x[4]}")
        
        st.info(f"🐾 Atendendo: **{pet_sel[1]}** | Raça: {pet_sel[2]} | Idade: {calcular_idade(pet_sel[3])}")
        
        with st.form("f_consulta"):
            anamnese = st.text_area("Anamnese / Sintomas (Dite com Win + H)", height=150)
            conduta = st.text_area("Conduta / Prescrição", height=150)
            valor = st.number_input("Valor da Consulta (R$)", min_value=0.0)
            if st.form_submit_button("💾 FINALIZAR E GRAVAR"):
                hoje = datetime.now().strftime("%d/%m/%Y")
                c.execute("INSERT INTO prontuario (pet_id, data, anamnese, conduta, valor) VALUES (?,?,?,?,?)",
                          (pet_sel[0], hoje, anamnese, conduta, valor))
                c.execute("INSERT INTO financeiro (data, descricao, valor, tipo) VALUES (?,?,?,?)",
                          (hoje, f"Consulta: {pet_sel[1]} ({pet_sel[2]})", valor, "Receita"))
                conn.commit()
                st.success("Atendimento gravado e financeiro atualizado!")

# --- TELA: FINANCEIRO ---
elif menu == "Financeiro":
    st.header("💰 Controle Financeiro")
    dados = c.execute("SELECT data, descricao, valor FROM financeiro ORDER BY id DESC").fetchall()
    if dados:
        df = pd.DataFrame(dados, columns=["Data", "Descrição", "Valor"])
        st.table(df)
    else: st.info("Nenhum registro encontrado.")

# --- TELA: BACKUP ---
elif menu == "Backup":
    st.header("💾 Salvar Dados")
    if st.button("Exportar Banco de Dados para Excel/CSV"):
        st.info("Funcionalidade de exportação pronta para ser ativada.")
