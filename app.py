import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- BANCO DE DADOS (Persistência) ---
if 'clientes' not in st.session_state: st.session_state['clientes'] = {}
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'historico' not in st.session_state: st.session_state['historico'] = []

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", use_container_width=True)
    st.title("Ribeira Vet Pro")
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["Início & Excel", "Cadastro Tutor", "Cadastro Pet", "Prontuário IA"])

# --- 🏠 PÁGINA: INÍCIO & EXCEL ---
if menu == "Início & Excel":
    st.title("📊 Painel de Controle")
    col1, col2 = st.columns(2)
    col1.metric("Tutores", len(st.session_state['clientes']))
    col2.metric("Pacientes", len(st.session_state['pets']))
    
    st.divider()
    if st.session_state['historico']:
        st.subheader("📁 Arquivo de Consultas")
        df_excel = pd.DataFrame(st.session_state['historico'])
        
        # Gerador de Excel em memória
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_excel.to_excel(writer, index=False, sheet_name='Atendimentos')
        
        st.download_button(
            label="📥 Baixar Planilha de Consultas",
            data=buffer.getvalue(),
            file_name=f"consultas_ribeira_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
            mime="application/vnd.ms-excel"
        )
        st.dataframe(df_excel)
    else:
        st.info("Nenhum atendimento realizado ainda.")

# --- 👤 PÁGINA: CADASTRO TUTOR ---
elif menu == "Cadastro Tutor":
    st.title("👤 Cadastro de Proprietário")
    with st.form("tutor_form", clear_on_submit=True):
        nome = st.text_input("Nome Completo")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        zap = c2.text_input("WhatsApp (DDD)")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço Completo") # Endereço restaurado
        if st.form_submit_button("Salvar Cadastro"):
            if nome and zap:
                id_t = f"T-{len(st.session_state['clientes'])+1:03d}"
                st.session_state['clientes'][id_t] = {"nome": nome, "cpf": cpf, "zap": zap, "email": email, "end": end}
                st.success(f"Tutor {nome} cadastrado!")
            else: st.error("Nome e WhatsApp são obrigatórios.")

# --- 🐶 PÁGINA: CADASTRO PET ---
elif menu == "Cadastro Pet":
    st.title("🐶 Cadastro de Paciente")
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("pet_form", clear_on_submit=True):
            lista_t = [f"{k} | {v['nome']}" for k, v in st.session_state['clientes'].items()]
            tutor_ref = st.selectbox("Proprietário", lista_t)
            nome_p = st.text_input("Nome do Animal")
            # Data Brasileira
            nasc = st.date_input("Data de Nascimento", format="DD/MM/YYYY")
            raca = st.text_input("Raça")
            if st.form_submit_button("Registrar Pet"):
                st.session_state['pets'].append({
                    "nome": nome_p, "nasc": nasc.strftime("%d/%m/%Y"), 
                    "raca": raca, "tutor": tutor_ref.split(" | ")[1]
                })
                st.success(f"Pet {nome_p} cadastrado!")

# --- 🩺 PÁGINA: PRONTUÁRIO IA ---
elif menu == "Prontuário IA":
    st.title("🩺 Atendimento Clínico")
    st.info("🎤 Use 'Windows + H' no teclado para ditar a consulta.")
    if not st.session_state['pets']:
        st.info("Cadastre um pet primeiro.")
    else:
        with st.form("atend_form"):
            paciente = st.selectbox("Selecionar Paciente", [p['nome'] for p in st.session_state['pets']])
            c1, c2 = st.columns(2)
            peso = c1.text_input("Peso (kg)")
            temp = c2.text_input("Temperatura (°C)")
            texto_ia = st.text_area("Transcrição da Conversa / Diagnóstico", height=200)
            if st.form_submit_button("💾 Salvar Atendimento"):
                pet_info = next(p for p in st.session_state['pets'] if p['nome'] == paciente)
                st.session_state['historico'].append({
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Tutor": pet_info['tutor'],
                    "Paciente": paciente,
                    "Peso": peso,
                    "Temp": temp,
                    "Conteudo": texto_ia
                })
                st.success("Consulta arquivada para o Excel!")
