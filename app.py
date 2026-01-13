import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN PROFISSIONAL ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59; color: white; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 5px; width: 100%; }
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1e3d59 !important; }
    .stTextArea textarea { font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
for key in ['clientes', 'pets', 'estoque', 'vendas', 'historico']:
    if key not in st.session_state: st.session_state[key] = {} if key == 'clientes' else []

if 'proximo_cod_cliente' not in st.session_state: st.session_state['proximo_cod_cliente'] = 1
if 'proximo_cod_pet' not in st.session_state: st.session_state['proximo_cod_pet'] = 1

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", use_container_width=True)
    st.markdown("<h2 style='text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("NAVEGAÇÃO", [
        "📊 Dashboard", "👤 Tutores", "🐶 Animais", 
        "🩺 Novo Atendimento", "📋 Histórico Clínico",
        "💊 Estoque/Serviços", "💰 Faturamento"
    ])

# --- 🩺 NOVO ATENDIMENTO (COM TRANSCRIÇÃO VET) ---
if menu == "🩺 Novo Atendimento":
    st.title("🩺 Consulta em Andamento")
    if not st.session_state['pets']:
        st.warning("Cadastre um animal primeiro.")
    else:
        with st.form("atendimento_v6"):
            pacientes = [f"{p['id']} - {p['nome']} (Tutor: {p['dono']})" for p in st.session_state['pets']]
            paciente_atual = st.selectbox("Selecione o Paciente", pacientes)
            
            st.markdown("#### 🌡️ Parâmetros Clínicos")
            c1, c2, c3, c4 = st.columns(4)
            peso = c1.text_input("Peso (kg)")
            temp = c2.text_input("Temp (°C)")
            freq_c = c3.text_input("Freq. Cardíaca")
            freq_r = c4.text_input("Freq. Resp.")
            
            st.markdown("#### 🗣️ Anamnese e Diagnóstico")
            st.info("💡 Dica: Você pode usar o atalho 'Windows + H' (no PC) para ditar as respostas do tutor diretamente nos campos abaixo.")
            
            queixa = st.text_area("Queixa Principal e Histórico (O que o tutor relatou)")
            exame_fisico = st.text_area("Achados do Exame Físico / Diagnóstico")
            prescricao = st.text_area("Receituário / Conduta / Medicamentos Aplicados")
            
            st.markdown("#### 📅 Próximos Passos")
            col_ret, col_vac = st.columns(2)
            retorno = col_ret.date_input("Agendar Retorno")
            vacinas_pendentes = col_vac.text_input("Vacinas para o Retorno")
            
            exames_anexo = st.file_uploader("Anexar Exames Laboratoriais (PDF/JPG)", accept_multiple_files=True)

            if st.form_submit_button("✅ Finalizar Atendimento e Gerar Registro"):
                atend_data = {
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "paciente": paciente_atual,
                    "anamnese": queixa,
                    "diagnostico": exame_fisico,
                    "prescricao": prescricao,
                    "retorno": str(retorno)
                }
                st.session_state['historico'].append(atend_data)
                st.success("Prontuário salvo com sucesso!")

# --- 📋 HISTÓRICO CLÍNICO ---
elif menu == "📋 Histórico Clínico":
    st.title("📚 Linha do Tempo de Atendimentos")
    if not st.session_state['historico']:
        st.info("Ainda não há atendimentos registrados.")
    else:
        for at in reversed(st.session_state['historico']):
            with st.expander(f"📅 {at['data']} - {at['paciente']}"):
                st.write(f"**Anamnese:** {at['anamnese']}")
                st.write(f"**Diagnóstico:** {at['diagnostico']}")
                st.write(f"**Prescrição:** {at['prescricao']}")
                st.warning(f"🔔 Retorno agendado para: {at['retorno']}")

# --- 👤 TUTORES (CAMPOS COMPLETOS) ---
elif menu == "👤 Tutores":
    st.title("Registro de Tutor")
    with st.form("tutor_full"):
        cod = f"T-{st.session_state['proximo_cod_cliente']:04d}"
        c1, c2 = st.columns(2)
        n = c1.text_input("Nome Completo")
        cpf = c2.text_input("CPF")
        zap = c1.text_input("WhatsApp")
        mail = c2.text_input("E-mail")
        end = st.text_area("Endereço")
        if st.form_submit_button("Salvar"):
            st.session_state['clientes'][cod] = {"nome": n, "cpf": cpf, "zap": zap, "email": mail, "end": end}
            st.session_state['proximo_cod_cliente'] += 1
            st.success("Tutor cadastrado!")

# --- (As outras abas de Animais, Estoque e Faturamento permanecem com a lógica anterior) ---
