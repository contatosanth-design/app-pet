import streamlit as st
import sqlite3
from datetime import datetime, date

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Ribeira Vet Pro 7.0", layout="wide")

# --- BANCO DE DADOS ATUALIZADO ---
conn = sqlite3.connect("clinica_vet_v7.db", check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute("""CREATE TABLE IF NOT EXISTS tutores 
                 (id INTEGER PRIMARY KEY, nome TEXT, cpf TEXT, zap TEXT, endereco TEXT)""")
    
    # Adicionamos 'nascimento' e 'especie' para o cálculo de idade
    c.execute("""CREATE TABLE IF NOT EXISTS pets 
                 (id INTEGER PRIMARY KEY, nome TEXT, raca TEXT, nascimento TEXT, tutor_id INTEGER)""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS prontuario 
                 (id INTEGER PRIMARY KEY, pet_id INTEGER, data TEXT, anamnese TEXT, conduta TEXT, valor REAL)""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS financeiro 
                 (id INTEGER PRIMARY KEY, data TEXT, descricao TEXT, valor REAL, tipo TEXT)""")
    conn.commit()

init_db()

# --- RAÇAS VERSÃO 2.0 ---
RACAS = ["SRD", "Shih Tzu", "Poodle", "Pinscher", "Golden Retriever", "Pit Bull", "Persa", "Siamês", "Outra"]

# --- SIDEBAR ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("Navegação", ["Início", "Tutores", "Pacientes", "Atendimento", "Financeiro"])
    st.divider()
    st.info("💡 Use Win + H nos campos de texto para ditar.")

# --- TELA: TUTORES ---
if menu == "Tutores":
    st.header("👤 Cadastro de Tutores")
    with st.form("tutor_form"):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome Completo").upper()
        cpf = col2.text_input("CPF")
        zap = col1.text_input("WhatsApp")
        end = col2.text_input("Endereço Completo")
        if st.form_submit_button("Salvar Tutor"):
            c.execute("INSERT INTO tutores (nome, cpf, zap, endereco) VALUES (?,?,?,?)", (nome, cpf, zap, end))
            conn.commit()
            st.success("Tutor cadastrado!")

# --- TELA: PACIENTES ---
elif menu == "Pacientes":
    st.header("🐶 Cadastro de Pets")
    tutores = c.execute("SELECT id, nome FROM tutores").fetchall()
    if not tutores:
        st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("pet_form"):
            tutor_id = st.selectbox("Responsável", tutores, format_func=lambda x: x[1])
            col1, col2 = st.columns(2)
            nome_pet = col1.text_input("Nome do Pet").upper()
            raca = col2.selectbox("Raça", RACAS)
            nasc = st.date_input("Data de Nascimento", format="DD/MM/YYYY")
            if st.form_submit_button("Cadastrar Pet"):
                c.execute("INSERT INTO pets (nome, raca, nascimento, tutor_id) VALUES (?,?,?,?)", 
                          (nome_pet, raca, str(nasc), tutor_id[0]))
                conn.commit()
                st.success(f"{nome_pet} cadastrado!")

# --- TELA: ATENDIMENTO (PRONTUÁRIO) ---
elif menu == "Atendimento":
    st.header("📝 Prontuário Médico")
    pets = c.execute("SELECT pets.id, pets.nome, tutores.nome FROM pets JOIN tutores ON pets.tutor_id = tutores.id").fetchall()
    
    if not pets:
        st.info("Nenhum pet cadastrado.")
    else:
        pet_sel = st.selectbox("Selecionar Paciente", pets, format_func=lambda x: f"{x[1]} (Tutor: {x[2]})")
        
        col1, col2 = st.columns(2)
        anamnese = col1.text_area("Anamnese / Sintomas", height=200)
        conduta = col2.text_area("Conduta / Prescrição", height=200)
        valor = st.number_input("Valor da Consulta (R$)", min_value=0.0)

        if st.button("💾 Finalizar Atendimento"):
            hoje = datetime.now().strftime("%d/%m/%Y")
            # Salva no Prontuário
            c.execute("INSERT INTO prontuario (pet_id, data, anamnese, conduta, valor) VALUES (?,?,?,?,?)",
                      (pet_sel[0], hoje, anamnese, conduta, valor))
            # Lança no Financeiro automaticamente
            c.execute("INSERT INTO financeiro (data, descricao, valor, tipo) VALUES (?,?,?,?)",
                      (hoje, f"Consulta: {pet_sel[1]}", valor, "Receita"))
            conn.commit()
            st.success("Tudo salvo e financeiro atualizado!")

# --- TELA: FINANCEIRO ---
elif menu == "Financeiro":
    st.header("💰 Controle de Caixa")
    resumo = c.execute("SELECT SUM(valor) FROM financeiro").fetchone()[0]
    st.metric("Faturamento Total", f"R$ {resumo if resumo else 0:.2f}")
    
    dados = c.execute("SELECT data, descricao, valor FROM financeiro ORDER BY id DESC").fetchall()
    if dados:
        df = pd.DataFrame(dados, columns=["Data", "Descrição", "Valor"])
        st.dataframe(df, use_container_width=True)

# --- TELA: INÍCIO ---
elif menu == "Início":
    st.title("Bem-vindo ao Ribeira Vet Pro")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tutores", c.execute("SELECT COUNT(*) FROM tutores").fetchone()[0])
    c2.metric("Pacientes", c.execute("SELECT COUNT(*) FROM pets").fetchone()[0])
    c3.metric("Consultas", c.execute("SELECT COUNT(*) FROM prontuario").fetchone()[0])
