import streamlit as st
import uuid
import json
from datetime import datetime, date
import pandas as pd

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Ribeira Vet Pro AI v7.0", layout="wide", page_icon="🐾")

# --- INICIALIZAÇÃO DO ESTADO ---
for key in ['tutores', 'pets', 'records', 'medicamentos']:
    if key not in st.session_state:
        st.session_state[key] = []

# Banco de dados de vacinas padrão
VACINAS_PADRAO = ["V10", "V8", "Raiva", "Gripe", "Giárdia", "Leishmaniose"]

# --- FUNÇÕES CORE ---
def calcular_idade(nascimento):
    if isinstance(nascimento, str):
        nascimento = datetime.strptime(nascimento, "%Y-%m-%d").date()
    today = date.today()
    return today.year - nascimento.year - ((today.month, today.day) < (nascimento.month, nascimento.day))

def format_date_br(d):
    return d.strftime("%d/%m/%Y")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/194/194279.png", width=80)
    st.title("Ribeira Vet Pro")
    menu = st.radio("Menu Principal", ["Tutores", "Pacientes", "Prontuário", "Estoque/Vacinas", "Dados & Backup"])
    st.divider()
    st.success("IA Gemini Ativa 🟢")

# --- 1. TUTORES (Com parâmetros de contato para Recibo) ---
if menu == "Tutores":
    st.header("👤 Gestão de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome = col1.text_input("NOME COMPLETO *").upper()
        cpf = col2.text_input("CPF *")
        tel = col1.text_input("WhatsApp (com DDD) *")
        email = col2.text_input("E-mail")
        end = st.text_input("Endereço")
        if st.form_submit_button("CADASTRAR TUTOR"):
            if nome and tel:
                st.session_state.tutores.append({"id": str(uuid.uuid4()), "nome": nome, "cpf": cpf, "tel": tel, "email": email, "end": end})
                st.success("Tutor salvo!")
            else: st.error("Nome e WhatsApp são obrigatórios.")

# --- 2. PACIENTES (Data BR e Idade) ---
elif menu == "Pacientes":
    st.header("🐶 Cadastro de Pacientes")
    if not st.session_state.tutores: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            t_map = {t['id']: t['nome'] for t in st.session_state.tutores}
            t_id = st.selectbox("Tutor Responsável", options=list(t_map.keys()), format_func=lambda x: t_map[x])
            c1, c2 = st.columns(2)
            nome_p = c1.text_input("Nome do Pet").upper()
            raca = c2.text_input("Raça").upper()
            # Calendário padrão BR (o widget exibe conforme o browser, mas salvamos formatado)
            nasc = st.date_input("Data de Nascimento", format="DD/MM/YYYY")
            if st.form_submit_button("SALVAR PET"):
                st.session_state.pets.append({"id": str(uuid.uuid4()), "tutor_id": t_id, "nome": nome_p, "raca": raca, "nasc": str(nasc)})
                st.success(f"{nome_p} cadastrado!")

# --- 3. PRONTUÁRIO (Gravação Funcional e Recibo) ---
elif menu == "Prontuário":
    st.header("📝 Atendimento Médico")
    if not st.session_state.pets: st.info("Sem pets cadastrados.")
    else:
        p_id = st.selectbox("Selecionar Paciente", options=[p['id'] for p in st.session_state.pets], 
                            format_func=lambda x: next(p['nome'] for p in st.session_state.pets if p['id'] == x))
        pet = next(p for p in st.session_state.pets if p['id'] == p_id)
        tutor = next(t for t in st.session_state.tutores if t['id'] == pet['tutor_id'])
        
        st.info(f"🐾 **{pet['nome']}** | {calcular_idade(pet['nasc'])} anos | Tutor: {tutor['nome']}")
        
        with st.container():
            sint = st.text_area("Sintomas/Anamnese")
            cond = st.text_area("Conduta/Medicamentos")
            valor = st.number_input("Valor da Consulta (R$)", min_value=0.0)
            
            if st.button("💾 FINALIZAR E GRAVAR ATENDIMENTO"):
                rec = {"id": str(uuid.uuid4()), "pet_id": p_id, "data": datetime.now().strftime("%d/%m/%Y"), "sint": sint, "cond": cond, "valor": valor}
                st.session_state.records.append(rec)
                st.success("Gravado com sucesso!")

        st.subheader("🧾 Gerar Recibo")
        if st.button("Gerar Link WhatsApp"):
            msg = f"Olá {tutor['nome']}, recibo de {pet['nome']}: {valor}. Conduta: {cond}"
            url = f"https://wa.me/{tutor['tel']}?text={msg.replace(' ', '%20')}"
            st.markdown(f"[Clique aqui para enviar no WhatsApp]({url})")

# --- 4. ESTOQUE E VACINAS ---
elif menu == "Estoque/Vacinas":
    st.header("💉 Medicamentos e Vacinas")
    with st.form("f_med"):
        tipo = st.selectbox("Tipo", ["Vacina", "Medicamento"])
        nome_m = st.text_input("Nome").upper()
        qtd = st.number_input("Quantidade em Estoque", min_value=0)
        if st.form_submit_button("ADICIONAR"):
            st.session_state.medicamentos.append({"nome": nome_m, "tipo": tipo, "qtd": qtd})

    st.table(pd.DataFrame(st.session_state.medicamentos))

# --- 5. DADOS & BACKUP (Salvar no PC) ---
elif menu == "Dados & Backup":
    st.header("💾 Gerenciamento de Dados")
    
    # Mostrar estatísticas para não ficar em branco
    c1, c2, c3 = st.columns(3)
    c1.metric("Tutores", len(st.session_state.tutores))
    c2.metric("Pets", len(st.session_state.pets))
    c3.metric("Atendimentos", len(st.session_state.records))

    # Botão para baixar JSON (Salvar no Computador)
    full_data = {
        "tutores": st.session_state.tutores,
        "pets": st.session_state.pets,
        "records": st.session_state.records,
        "medicamentos": st.session_state.medicamentos
    }
    
    json_string = json.dumps(full_data, indent=4)
    st.download_button(
        label="📥 SALVAR BACKUP NO COMPUTADOR (JSON)",
        data=json_string,
        file_name=f"backup_ribeira_vet_{date.today()}.json",
        mime="application/json"
    )
    
    if st.button("🗑️ LIMPAR TUDO (CUIDADO)"):
        st.session_state.clear()
        st.rerun()
