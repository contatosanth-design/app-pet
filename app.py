import streamlit as st
import uuid
from datetime import datetime, date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ribeira Vet Pro AI", layout="wide")

# --- ESTADO DO SISTEMA ---
if 'tutores' not in st.session_state: st.session_state.tutores = []
if 'pets' not in st.session_state: st.session_state.pets = []
if 'records' not in st.session_state: st.session_state.records = []

# --- FUNÇÕES AUXILIARES ---
def calcular_idade(nascimento):
    today = date.today()
    return today.year - nascimento.year - ((today.month, today.day) < (nascimento.month, nascimento.day))

# --- SIDEBAR ---
with st.sidebar:
    st.title("🐾 Ribeira Vet")
    menu = st.radio("Menu", ["Tutores", "Pacientes", "Prontuário", "Dados"])
    st.info("IA Conectada 🟢")

# --- TELAS ---

if menu == "Tutores":
    st.header("👤 Cadastro de Tutores")
    with st.form("form_tutor"):
        nome = st.text_input("Nome do Tutor").upper()
        cpf = st.text_input("CPF")
        if st.form_submit_button("SALVAR TUTOR"):
            st.session_state.tutores.append({"id": str(uuid.uuid4()), "nome": nome, "cpf": cpf})
            st.success("Tutor cadastrado!")

elif menu == "Pacientes":
    st.header("🐶 Cadastro de Pacientes")
    if not st.session_state.tutores:
        st.warning("Cadastre um tutor primeiro!")
    else:
        with st.form("form_pet"):
            tutor_id = st.selectbox("Responsável", 
                                   options=[t['id'] for t in st.session_state.tutores],
                                   format_func=lambda x: next(t['nome'] for t in st.session_state.tutores if t['id'] == x))
            
            col1, col2 = st.columns(2)
            nome_pet = col1.text_input("Nome do Pet").upper()
            raca = col2.text_input("Raça").upper()
            
            col3, col4 = st.columns(2)
            nascimento = col3.date_input("Data de Nascimento", min_value=date(2000, 1, 1))
            ultima_vacina = col4.date_input("Data da Última Vacina")
            
            if st.form_submit_button("CADASTRAR PACIENTE"):
                st.session_state.pets.append({
                    "id": str(uuid.uuid4()), 
                    "nome": nome_pet, 
                    "raca": raca, 
                    "tutor_id": tutor_id,
                    "nascimento": nascimento,
                    "ultima_vacina": ultima_vacina
                })
                st.success(f"{nome_pet} cadastrado com sucesso!")

elif menu == "Prontuário":
    st.header("📝 Atendimento e Histórico")
    if not st.session_state.pets:
        st.warning("Nenhum paciente cadastrado.")
    else:
        # Seleção do Pet
        pet_id = st.selectbox("Escolha o Paciente", 
                             options=[p['id'] for p in st.session_state.pets],
                             format_func=lambda x: next(p['nome'] for p in st.session_state.pets if p['id'] == x))
        
        pet = next(p for p in st.session_state.pets if p['id'] == pet_id)
        
        # --- CARD DE INFORMAÇÕES DO PET ---
        idade = calcular_idade(pet['nascimento'])
        st.markdown(f"""
        <div style="background-color: #eef2ff; padding: 20px; border-radius: 15px; border-left: 5px solid #2563eb;">
            <h4>🐾 {pet['nome']} ({pet['raca']})</h4>
            <p><b>Idade:</b> {idade} anos | <b>Nascimento:</b> {pet['nascimento'].strftime('%d/%m/%Y')}</p>
            <p><b>📅 Próxima Revacina:</b> {pet['ultima_vacina'].replace(year=pet['ultima_vacina'].year + 1).strftime('%d/%m/%Y')}</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # --- GRAVAÇÃO DE CONSULTA ---
        st.subheader("Nova Consulta")
        sintomas = st.text_area("Anamnese / Sintomas")
        conduta = st.text_area("Conduta / Tratamento")
        
        if st.button("💾 FINALIZAR E SALVAR CONSULTA"):
            novo_registro = {
                "pet_id": pet_id,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "sintomas": sintomas,
                "conduta": conduta
            }
            st.session_state.records.append(novo_registro)
            st.success("Consulta gravada com sucesso!")

        # --- HISTÓRICO ---
        st.subheader("📚 Histórico do Paciente")
        historico = [r for r in st.session_state.records if r['pet_id'] == pet_id]
        if not historico:
            st.write("Nenhum registro anterior.")
        for rec in reversed(historico):
            with st.expander(f"Consulta em {rec['data']}"):
                st.write(f"**Sintomas:** {rec['sintomas']}")
                st.write(f"**Conduta:** {rec['conduta']}")

elif menu == "Dados":
    st.header("💾 Gerenciamento de Dados")
    st.write("Total de Tutores:", len(st.session_state.tutores))
    st.write("Total de Pets:", len(st.session_state.pets))
    if st.button("Limpar Tudo"):
        st.session_state.clear()
        st.rerun()
