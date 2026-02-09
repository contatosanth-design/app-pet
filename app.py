import streamlit as st
import uuid
import json
from datetime import datetime, date
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ribeira Vet Pro v7.0", layout="wide", page_icon="🐾")

# --- INICIALIZAÇÃO DO ESTADO (Garante que as chaves existam) ---
if 'tutores' not in st.session_state: st.session_state.tutores = []
if 'pets' not in st.session_state: st.session_state.pets = []
if 'records' not in st.session_state: st.session_state.records = []
if 'estoque' not in st.session_state: st.session_state.estoque = []

# --- FUNÇÕES AUXILIARES ---
def calcular_idade(nasc_str):
    try:
        nasc = datetime.strptime(nasc_str, "%Y-%m-%d").date()
        today = date.today()
        return today.year - nasc.year - ((today.month, today.day) < (nasc.month, nasc.day))
    except: return "N/A"

# --- SIDEBAR ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("Menu Principal", ["Tutores", "Pacientes", "Prontuário", "Estoque & Vacinas", "Dados & Backup"])
    st.divider()
    st.success("IA Gemini Ativa 🟢")

# --- 1. TUTORES ---
if menu == "Tutores":
    st.header("👤 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome = col1.text_input("NOME COMPLETO *").upper()
        cpf = col2.text_input("CPF *")
        whatsapp = col1.text_input("WhatsApp (ex: 11999999999) *")
        email = col2.text_input("E-mail para Recibo")
        endereco = st.text_input("Endereço")
        if st.form_submit_button("SALVAR TUTOR"):
            if nome and whatsapp:
                st.session_state.tutores.append({
                    "id": str(uuid.uuid4()), "nome": nome, "cpf": cpf, 
                    "whatsapp": whatsapp, "email": email, "endereco": endereco
                })
                st.success("Tutor cadastrado!")
            else: st.error("Nome e WhatsApp são obrigatórios.")

# --- 2. PACIENTES ---
elif menu == "Pacientes":
    st.header("🐶 Cadastro de Pacientes")
    if not st.session_state.tutores:
        st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet", clear_on_submit=True):
            t_map = {t['id']: t['nome'] for t in st.session_state.tutores}
            tutor_id = st.selectbox("Responsável", options=list(t_map.keys()), format_func=lambda x: t_map[x])
            c1, c2 = st.columns(2)
            nome_p = c1.text_input("Nome do Pet").upper()
            raca = c2.text_input("Raça").upper()
            nasc = st.date_input("Data de Nascimento (Aniversário)", format="DD/MM/YYYY")
            if st.form_submit_button("CADASTRAR PACIENTE"):
                st.session_state.pets.append({
                    "id": str(uuid.uuid4()), "tutor_id": tutor_id, 
                    "nome": nome_p, "raca": raca, "nasc": str(nasc)
                })
                st.success(f"Paciente {nome_p} cadastrado!")

# --- 3. PRONTUÁRIO ---
elif menu == "Prontuário":
    st.header("📝 Atendimento Médico")
    if not st.session_state.pets:
        st.info("Nenhum paciente cadastrado.")
    else:
        pet_id = st.selectbox("Selecionar Paciente", options=[p['id'] for p in st.session_state.pets], 
                            format_func=lambda x: next(p['nome'] for p in st.session_state.pets if p['id'] == x))
        
        pet = next(p for p in st.session_state.pets if p['id'] == pet_id)
        tutor = next(t for t in st.session_state.tutores if t['id'] == pet['tutor_id'])
        
        # Exibição segura de dados
        idade = calcular_idade(pet.get('nasc', str(date.today())))
        st.info(f"🐾 **{pet['nome']}** | {idade} anos | Tutor: {tutor['nome']}")

        with st.form("atendimento"):
            anamnese = st.text_area("Anamnese / Sintomas")
            tratamento = st.text_area("Conduta / Medicamentos Prescritos")
            valor = st.number_input("Valor da Consulta (R$)", min_value=0.0)
            if st.form_submit_button("💾 FINALIZAR E GRAVAR"):
                st.session_state.records.append({
                    "id": str(uuid.uuid4()), "pet_id": pet_id, 
                    "data": datetime.now().strftime("%d/%m/%Y"), 
                    "anamnese": anamnese, "tratamento": tratamento, "valor": valor
                })
                st.success("Atendimento gravado!")

        # --- RECIBOS ---
        st.subheader("🧾 Enviar Recibo")
        col_w, col_e = st.columns(2)
        
        # WhatsApp
        msg = f"Olá {tutor['nome']}, recibo de {pet['nome']}. Valor: R$ {valor:.2f}. Conduta: {tratamento}"
        wa_link = f"https://wa.me/{tutor['whatsapp']}?text={msg.replace(' ', '%20')}"
        col_w.markdown(f"[📲 Enviar via WhatsApp]({wa_link})")
        
        # E-mail (Link mailto)
        mail_link = f"mailto:{tutor['email']}?subject=Recibo%20Veterinario&body={msg.replace(' ', '%20')}"
        col_e.markdown(f"[📧 Enviar via E-mail]({mail_link})")

# --- 4. ESTOQUE & VACINAS ---
elif menu == "Estoque & Vacinas":
    st.header("💉 Gestão de Medicamentos e Vacinas")
    with st.form("f_estoque"):
        c1, c2 = st.columns(2)
        item = c1.text_input("Nome do Item (Vacina/Remédio)").upper()
        qtd = c2.number_input("Qtd em Estoque", min_value=0)
        if st.form_submit_button("ADICIONAR AO ESTOQUE"):
            st.session_state.estoque.append({"item": item, "qtd": qtd})
    st.table(st.session_state.estoque)

# --- 5. DADOS & BACKUP ---
elif menu == "Dados & Backup":
    st.header("💾 Backup do Sistema")
    
    # Dashboard rápido
    c1, c2, c3 = st.columns(3)
    c1.metric("Tutores", len(st.session_state.tutores))
    c2.metric("Pets", len(st.session_state.pets))
    c3.metric("Consultas", len(st.session_state.records))

    # Download de Backup (Salvar no Computador)
    data_final = {
        "tutores": st.session_state.tutores,
        "pets": st.session_state.pets,
        "records": st.session_state.records,
        "estoque": st.session_state.estoque
    }
    
    st.download_button(
        label="📥 BAIXAR BACKUP COMPLETO (.JSON)",
        data=json.dumps(data_final, indent=4),
        file_name=f"backup_vet_{date.today()}.json",
        mime="application/json"
    )

    if st.button("🚨 APAGAR TUDO"):
        st.session_state.clear()
        st.rerun()
