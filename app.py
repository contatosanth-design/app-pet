import streamlit as st
import pandas as pd
from datetime import datetime, date

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59 !important; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold !important; }
    .header-box { background: white; padding: 20px; border-radius: 10px; border-left: 6px solid #2e7bcf; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE DADOS ---
for key in ['clientes', 'pets', 'historico', 'estoque']:
    if key not in st.session_state: st.session_state[key] = []

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=80)
    st.title("Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "💰 Financeiro"])

# --- FUNÇÃO CALCULAR IDADE ---
def calcular_idade(nasc):
    hoje = date.today()
    anos = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
    return f"{anos} anos"

# --- 1. SESSÃO: TUTORES (MANTIDA) ---
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        id_t = f"T{len(st.session_state['clientes']) + 1:03d}"
        nome = st.text_input("Nome do Cliente*")
        zap = st.text_input("WhatsApp*")
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({"id": id_t, "nome": nome.upper(), "zap": zap})
                st.success("Tutor salvo!")

# --- 2. SESSÃO: PETS (COM CÁLCULO DE IDADE) ---
elif menu == "🐾 Pets":
    st.subheader("🐾 Ficha do Paciente")
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet", clear_on_submit=True):
            id_p = f"P{len(st.session_state['pets']) + 1:03d}"
            t_lista = {f"{c['id']} - {c['nome']}": c['id'] for c in st.session_state['clientes']}
            tutor_ref = st.selectbox("Proprietário*", list(t_lista.keys()))
            nome_p = st.text_input("Nome do Pet*")
            
            c1, c2 = st.columns(2)
            nascimento = c1.date_input("Data de Nascimento", value=date(2020, 1, 1))
            raca = c2.selectbox("Raça", ["SRD", "Spitz Alemão", "Poodle", "Shih Tzu", "Outra"])
            
            # Exibe a idade calculada na hora
            idade_calc = calcular_idade(nascimento)
            st.write(f"**Idade Calculada:** {idade_calc}")
            
            sexo = st.selectbox("Sexo", ["Macho", "Fêmea"])
            castrado = st.radio("Castrado?", ["Sim", "Não"], horizontal=True)
            
            if st.form_submit_button("✅ SALVAR PET"):
                st.session_state['pets'].append({
                    "id": id_p, "tutor": t_lista[tutor_ref], "nome": nome_p.upper(), 
                    "idade": idade_calc, "raca": raca, "sexo": sexo, "castrado": castrado
                })
                st.success(f"Pet {nome_p} salvo com {idade_calc}!")

# --- 3. SESSÃO: PRONTUÁRIO (PREENCHIDO COM PARÂMETROS) ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento Clínico")
    if not st.session_state['pets']:
        st.info("Cadastre um pet para iniciar o prontuário.")
    else:
        with st.form("f_prontuario"):
            p_lista = {f"{p['id']} - {p['nome']}": p for p in st.session_state['pets']}
            pet_sel = st.selectbox("Paciente", list(p_lista.keys()))
            
            st.markdown("### 📋 Parâmetros Vitais")
            c1, c2, c3 = st.columns(3)
            peso = c1.text_input("Peso (kg)")
            temp = c2.text_input("Temperatura (°C)")
            fc = c3.text_input("Freq. Cardíaca (bpm)")
            
            st.markdown("### 📝 Avaliação e Conduta")
            relato = st.text_area("Relato da Consulta (Win+H)", height=200)
            prescricao = st.text_area("Prescrição / Tratamento")
            
            if st.form_submit_button("💾 SALVAR ATENDIMENTO"):
                st.session_state['historico'].append({
                    "Data": date.today().strftime("%d/%m/%Y"),
                    "Pet": p_lista[pet_sel]['nome'],
                    "Peso": peso, "Temp": temp, "Relato": relato
                })
                st.success("Histórico clínico atualizado!")

# --- 4. DASHBOARD ---
elif menu == "🏠 Dashboard":
    st.subheader("📊 Painel Geral")
    st.write(f"Tutores: {len(st.session_state['clientes'])} | Pacientes: {len(st.session_state['pets'])}")
    if st.session_state['historico']:
        st.write("### Últimos Atendimentos")
        st.table(pd.DataFrame(st.session_state['historico']))
