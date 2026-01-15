import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN PROFISSIONAL ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 5px; width: 100%; }
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1e3d59 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA DO BANCO DE DADOS ---
if 'clientes' not in st.session_state: st.session_state['clientes'] = {}
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'vacinas' not in st.session_state: st.session_state['vacinas'] = []
if 'historico' not in st.session_state: st.session_state['historico'] = []

# --- MENU LATERAL ATUALIZADO ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", use_container_width=True)
    st.markdown("<h1 style='text-align: center; font-size: 20px;'>Ribeira Vet Pro</h1>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MENU DE NAVEGAÇÃO", [
        "🏠 Início & Excel", 
        "👤 Cadastro de Tutores", 
        "🐶 Cadastro de Pets", 
        "🩺 Prontuário IA",
        "💉 Controle de Vacinas",
        "🎉 Aniversariantes"
    ])

# --- 🏠 INÍCIO & EXCEL ---
if menu == "🏠 Início & Excel":
    st.title("📊 Painel de Controle")
    if st.session_state['historico']:
        df = pd.DataFrame(st.session_state['historico'])
        st.subheader("📁 Exportar Histórico de Consultas")
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Consultas')
        st.download_button("📥 Baixar Planilha Excel (.xlsx)", data=output.getvalue(), 
                           file_name=f"atendimentos_{datetime.now().strftime('%d_%m_%Y')}.xlsx")
        st.dataframe(df)
    else:
        st.info("Nenhum atendimento arquivado até o momento.")

# --- 👤 CADASTRO DE TUTORES (CORRIGIDO) ---
elif menu == "👤 Cadastro de Tutores":
    st.title("👤 Registro de Proprietário")
    with st.form("form_tutor_novo"):
        id_t = f"T-{len(st.session_state['clientes'])+1:04d}"
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome Completo")
        cpf = col2.text_input("CPF")
        zap = col1.text_input("WhatsApp (com DDD)")
        email = col2.text_input("E-mail")
        endereco = st.text_area("Endereço Completo")
        if st.form_submit_button("✅ Salvar Cadastro"):
            if nome and zap:
                st.session_state['clientes'][id_t] = {
                    "nome": nome, "cpf": cpf, "zap": zap, "email": email, "end": endereco
                }
                st.success(f"Tutor {nome} cadastrado com sucesso!")
            else:
                st.error("Por favor, preencha o Nome e o WhatsApp.")

# --- 🐶 CADASTRO DE PETS (COM DATA BR) ---
elif menu == "🐶 Cadastro de Pets":
    st.title("🐶 Registro de Paciente")
    if not st.session_state['clientes']:
        st.warning("⚠️ Cadastre um tutor antes de registrar um animal.")
    else:
        with st.form("form_pet_novo"):
            tutores = [f"{k} - {v['nome']}" for k, v in st.session_state['clientes'].items()]
            tutor_sel = st.selectbox("Selecione o Proprietário", tutores)
            col1, col2 = st.columns(2)
            nome_p = col1.text_input("Nome do Animal")
            raca = col2.text_input("Raça")
            nascimento = st.date_input("Data de Nascimento", format="DD/MM/YYYY")
            if st.form_submit_button("✅ Registrar Pet"):
                st.session_state['pets'].append({
                    "nome": nome_p, "nascimento": nascimento, "raca": raca,
                    "cod_tutor": tutor_sel.split(" - ")[0],
                    "tutor_nome": tutor_sel.split(" - ")[1]
                })
                st.success(f"O paciente {nome_p} foi registrado!")

# --- 🩺 PRONTUÁRIO IA ---
elif menu == "🩺 Prontuário IA":
    st.title("🩺 Atendimento com Transcrição")
    st.info("🎤 **Atalho:** Clique no campo e aperte 'Windows + H' para ditar.")
    if not st.session_state['pets']:
        st.info("Cadastre um pet primeiro.")
    else:
        with st.form("form_consulta"):
            pet_sel = st.selectbox("Paciente", [p['nome'] for p in st.session_state['pets']])
            c1, c2 = st.columns(2)
            peso = c1.text_input("Peso (kg)")
            temp = c2.text_input("Temp (°C)")
            anamnese = st.text_area("Transcrição da Consulta / Diagnóstico", height=200)
            if st.form_submit_button("💾 Finalizar e Arquivar"):
                pet_data = next(p for p in st.session_state['pets'] if p['nome'] == pet_sel)
                st.session_state['historico'].append({
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Tutor": pet_data['tutor_nome'],
                    "Paciente": pet_sel,
                    "Peso": peso, "Temp": temp,
                    "Relato_IA": anamnese
                })
                st.success("Consulta arquivada na planilha de pesquisa!")

# --- 💉 CONTROLE DE VACINAS & 🎂 ANIVERSARIANTES ---
# (Lógica simplificada para evitar erros de carregamento)
elif menu == "💉 Controle de Vacinas":
    st.title("💉 Próximas Vacinas")
    st.info("Funcionalidade em carregamento...")

elif menu == "🎉 Aniversariantes":
    st.title("🎂 Parabéns do Dia")
    hoje = datetime.now().strftime("%d/%m")
    for p in st.session_state['pets']:
        if p['nascimento'].strftime("%d/%m") == hoje:
            st.success(f"🎈 Hoje é aniversário de **{p['nome']}**!")
