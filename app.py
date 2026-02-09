import streamlit as st
import uuid
from datetime import datetime, date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ribeira Vet Pro AI", layout="wide", page_icon="🐾")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'tutores' not in st.session_state: st.session_state.tutores = []
if 'pets' not in st.session_state: st.session_state.pets = []
if 'records' not in st.session_state: st.session_state.records = []

# --- FUNÇÕES AUXILIARES ---
def calcular_idade(nascimento):
    today = date.today()
    return today.year - nascimento.year - ((today.month, today.day) < (nascimento.month, nascimento.day))

# --- SIDEBAR PROFISSIONAL ---
with st.sidebar:
    st.markdown("# 🐾 Ribeira Vet")
    menu = st.radio("Navegação", ["Tutores", "Pacientes", "Prontuário", "Dados"])
    st.markdown("---")
    st.success("IA Conectada 🟢")

# --- TELAS ---

if menu == "Tutores":
    st.title("👤 Cadastro de Tutores")
    with st.container():
        with st.form("form_tutor", clear_on_submit=True):
            col1, col2 = st.columns(2)
            nome = col1.text_input("NOME DO TUTOR *").upper()
            cpf = col2.text_input("CPF *")
            
            col3, col4 = st.columns(2)
            tel = col3.text_input("WhatsApp / Telefone")
            email = col4.text_input("E-mail")
            
            endereco = st.text_input("Endereço Completo")
            
            if st.form_submit_button("SALVAR TUTOR"):
                if nome and cpf:
                    st.session_state.tutores.append({
                        "id": str(uuid.uuid4()), "nome": nome, "cpf": cpf, 
                        "tel": tel, "email": email, "endereco": endereco
                    })
                    st.balloons()
                    st.success(f"Tutor {nome} cadastrado!")
                else:
                    st.error("Por favor, preencha os campos obrigatórios (*)")

elif menu == "Pacientes":
    st.title("🐶 Cadastro de Pacientes")
    if not st.session_state.tutores:
        st.warning("⚠️ Cadastre um tutor primeiro para vincular o pet.")
    else:
        with st.form("form_pet", clear_on_submit=True):
            # Recuperamos o parâmetro de vínculo com o tutor
            tutor_map = {t['id']: t['nome'] for t in st.session_state.tutores}
            tutor_id = st.selectbox("Responsável pelo Pet", options=list(tutor_map.keys()), format_func=lambda x: tutor_map[x])
            
            col1, col2 = st.columns(2)
            nome_pet = col1.text_input("Nome do Pet *").upper()
            raca = col2.text_input("Raça").upper()
            
            # Recuperamos os parâmetros de tempo
            col3, col4 = st.columns(2)
            nascimento = col3.date_input("Data de Nascimento", value=date(2020, 1, 1))
            vacinacao = col4.date_input("Data da Última Vacina (V10/Raiva)")
            
            if st.form_submit_button("CADASTRAR PACIENTE"):
                if nome_pet:
                    st.session_state.pets.append({
                        "id": str(uuid.uuid4()), "nome": nome_pet, "raca": raca, 
                        "tutor_id": tutor_id, "nascimento": nascimento, "vacina": vacinacao
                    })
                    st.success(f"Paciente {nome_pet} adicionado ao sistema!")
                else:
                    st.error("O nome do pet é obrigatório.")

elif menu == "Prontuário":
    st.title("📝 Atendimento Médico")
    if not st.session_state.pets:
        st.info("Aguardando pacientes cadastrados...")
    else:
        pet_id = st.selectbox("Selecione o Paciente para Iniciar", 
                             options=[p['id'] for p in st.session_state.pets],
                             format_func=lambda x: next(p['nome'] for p in st.session_state.pets if p['id'] == x))
        
        pet = next(p for p in st.session_state.pets if p['id'] == pet_id)
        tutor = next(t for t in st.session_state.tutores if t['id'] == pet['tutor_id'])
        
        # --- RESUMO DO PACIENTE (Parâmetros de Idade e Vacina) ---
        hoje = date.today()
        proxima_vacina = pet['vacina'].replace(year=pet['vacina'].year + 1)
        status_vacina = "🔴 ATRASADA" if hoje > proxima_vacina else "🟢 EM DIA"
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Idade", f"{calcular_idade(pet['nascimento'])} anos")
        col_b.metric("Revacina em", proxima_vacina.strftime('%d/%m/%Y'), delta=status_vacina, delta_color="inverse")
        col_c.write(f"**Tutor:** {tutor['nome']}\n\n**Contato:** {tutor['tel']}")

        st.markdown("---")
        
        # --- GRAVAÇÃO REAL ---
        sintomas = st.text_area("Anamnese e Sintomas (O que o pet tem?)", height=150)
        conduta = st.text_area("Conduta e Prescrição (O que foi feito?)", height=150)
        
        if st.button("💾 GRAVAR NO HISTÓRICO"):
            if sintomas or conduta:
                st.session_state.records.append({
                    "pet_id": pet_id,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "sintomas": sintomas,
                    "conduta": conduta
                })
                st.success("Prontuário atualizado!")
            else:
                st.warning("Preencha algo para salvar.")

        # --- HISTÓRICO ABAIXO ---
        st.subheader("📚 Histórico de Consultas")
        for r in reversed([res for res in st.session_state.records if res['pet_id'] == pet_id]):
            with st.expander(f"Consulta em {r['data']}"):
                st.write(f"**Sintomas:** {r['sintomas']}")
                st.write(f"**Conduta:** {r['conduta']}")
