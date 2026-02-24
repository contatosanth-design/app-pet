import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ribeira Vet Pro v7.0", layout="wide", page_icon="🐾")

# --- BANCO DE DADOS (Persistência Total) ---
conn = sqlite3.connect("ribeira_vet_estavel.db", check_same_thread=False)
c = conn.cursor()

def init_db():
    # Tutores com todos os parâmetros de contato
    c.execute("""CREATE TABLE IF NOT EXISTS tutores 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cpf TEXT, zap TEXT, email TEXT, endereco TEXT)""")
    # Pets com Raça, Nascimento e Revacina
    c.execute("""CREATE TABLE IF NOT EXISTS pets 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, raca TEXT, nascimento TEXT, ultima_vacina TEXT, tutor_id INTEGER)""")
    # Prontuário focado em Anamnese e Conduta
    c.execute("""CREATE TABLE IF NOT EXISTS prontuario 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, pet_id INTEGER, data TEXT, anamnese TEXT, conduta TEXT, valor REAL)""")
    # Financeiro e Exames
    c.execute("""CREATE TABLE IF NOT EXISTS financeiro (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, desc TEXT, valor REAL)""")
    c.execute("""CREATE TABLE IF NOT EXISTS exames (id INTEGER PRIMARY KEY AUTOINCREMENT, pet_id INTEGER, tipo TEXT, data TEXT, resultado TEXT)""")
    conn.commit()

init_db()

# --- RAÇAS (Versão 2.0 Recuperada) ---
RACAS_COMUNS = ["SRD", "Shih Tzu", "Poodle", "Pinscher", "Golden Retriever", "Pit Bull", "Bulldog", "Yorkshire", "Persa", "Siamês", "Outra"]

# --- FUNÇÕES AUXILIARES ---
def calcular_idade(nasc_str):
    if not nasc_str: return "N/D"
    try:
        nasc = datetime.strptime(nasc_str, "%Y-%m-%d").date()
        hoje = date.today()
        idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
        return f"{idade} anos"
    except: return "N/D"

# --- SIDEBAR ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("Menu", ["Tutores", "Pacientes", "Prontuário", "Exames", "Financeiro", "Dados & Backup"])
    st.divider()
    st.info("🎤 **Voz:** Clique no campo e use **Win + H**")

# --- 1. TUTORES (Endereço Completo) ---
if menu == "Tutores":
    st.header("👤 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome = col1.text_input("NOME COMPLETO *").upper()
        cpf = col2.text_input("CPF")
        zap = col1.text_input("WHATSAPP (DDD) *")
        email = col2.text_input("E-MAIL")
        end = st.text_input("ENDEREÇO COMPLETO")
        if st.form_submit_button("SALVAR TUTOR"):
            if nome and zap:
                c.execute("INSERT INTO tutores (nome, cpf, zap, email, endereco) VALUES (?,?,?,?,?)", (nome, cpf, zap, email, end))
                conn.commit()
                st.success("Tutor salvo!")

# --- 2. PACIENTES (Diferenciação por Raça e Idade) ---
elif menu == "Pacientes":
    st.header("🐶 Cadastro de Pacientes")
    tutores = c.execute("SELECT id, nome FROM tutores").fetchall()
    if not tutores: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet", clear_on_submit=True):
            t_id = st.selectbox("Responsável", tutores, format_func=lambda x: x[1])
            col1, col2 = st.columns(2)
            nome_p = col1.text_input("NOME DO PET *").upper()
            raca = col2.selectbox("RAÇA", RACAS_COMUNS)
            nasc = col1.date_input("DATA DE NASCIMENTO", format="DD/MM/YYYY")
            vac = col2.date_input("DATA ÚLTIMA VACINA", format="DD/MM/YYYY")
            if st.form_submit_button("CADASTRAR PET"):
                c.execute("INSERT INTO pets (nome, raca, nascimento, ultima_vacina, tutor_id) VALUES (?,?,?,?,?)", 
                          (nome_p, raca, str(nasc), str(vac), t_id[0]))
                conn.commit()
                st.success(f"{nome_p} cadastrado!")

# --- 3. PRONTUÁRIO (Gravação e Recibo) ---
elif menu == "Prontuário":
    st.header("📝 Atendimento Médico")
    pets = c.execute("SELECT pets.id, pets.nome, pets.raca, tutores.nome, pets.nascimento FROM pets JOIN tutores ON pets.tutor_id = tutores.id").fetchall()
    if not pets: st.info("Sem pacientes.")
    else:
        pet_sel = st.selectbox("Selecionar Paciente", pets, format_func=lambda x: f"{x[1]} ({x[2]}) - Tutor: {x[3]}")
        idade = calcular_idade(pet_sel[4])
        st.subheader(f"🐾 Atendendo: {pet_sel[1]} | Idade: {idade}")
        
        with st.form("f_atendimento"):
            anamnese = st.text_area("Anamnese (Dite aqui)", height=150)
            conduta = st.text_area("Conduta / Receituário", height=150)
            valor = st.number_input("Valor R$", min_value=0.0)
            if st.form_submit_button("💾 FINALIZAR"):
                hoje = datetime.now().strftime("%d/%m/%Y")
                c.execute("INSERT INTO prontuario (pet_id, data, anamnese, conduta, valor) VALUES (?,?,?,?,?)", (pet_sel[0], hoje, anamnese, conduta, valor))
                c.execute("INSERT INTO financeiro (data, desc, valor) VALUES (?,?,?)", (hoje, f"Consulta: {pet_sel[1]}", valor))
                conn.commit()
                st.success("Gravado com sucesso!")

# --- 4. DADOS & BACKUP (Salvar no PC) ---
elif menu == "Dados & Backup":
    st.header("💾 Gerenciamento de Dados")
    if st.button("Gerar Backup para Download"):
        # Aqui você pode converter as tabelas para CSV e disponibilizar o download
        st.write("Backup pronto para ser processado.")
    if st.button("🚨 LIMPAR TUDO"):
        c.execute("DROP TABLE IF EXISTS tutores"); c.execute("DROP TABLE IF EXISTS pets")
        c.execute("DROP TABLE IF EXISTS prontuario"); c.execute("DROP TABLE IF EXISTS financeiro")
        init_db(); st.rerun()
