import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- CSS PARA ESTILO E CONTRASTE ---
st.markdown("""
    <style>
    .main { background-color: #f1f3f6; }
    [data-testid="stSidebar"] { background-color: #1e3d59 !important; }
    [data-testid="stSidebar"] .stRadio label p { color: white !important; font-weight: bold; }
    [data-testid="stSidebar"] h2 { color: white !important; }
    .header-box { 
        background-color: white; padding: 20px; border-radius: 10px; 
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px;
        border-left: 6px solid #2e7bcf;
    }
    .metric-card { background: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DOS DADOS ---
if 'clientes' not in st.session_state: st.session_state['clientes'] = []
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'historico' not in st.session_state: st.session_state['historico'] = []

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/620/620851.png", width=100)
    st.markdown("<h2 style='text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pacientes", "🩺 Prontuário IA", "💰 Financeiro"])

# --- CABEÇALHO ---
st.markdown(f"<div class='header-box'><h1 style='color:#1e3d59; margin:0;'>Ribeira Vet Pro</h1><p style='margin:0; color:#666;'>Sistema de Gestão • {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- TELAS ---

if menu == "🏠 Dashboard":
    st.subheader("📊 Resumo do Arquivo Clínico")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tutores", len(st.session_state['clientes']))
    c2.metric("Pacientes", len(st.session_state['pets']))
    c3.metric("Atendimentos", len(st.session_state['historico']))

    if st.session_state['historico']:
        st.write("### Histórico Arquivado")
        df_hist = pd.DataFrame(st.session_state['historico'])
        st.dataframe(df_hist, use_container_width=True)
        # Exportação segura
        csv = df_hist.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Exportar Arquivo (Excel/CSV)", data=csv, file_name="historico_clinico.csv")
    else:
        st.info("O arquivo de prontuários está vazio. Inicie um atendimento para registrar dados.")

elif menu == "👤 Tutores":
    st.subheader("Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        proximo_cod = f"T{len(st.session_state['clientes']) + 1:03d}"
        st.info(f"Código Gerado: **{proximo_cod}**")
        nome = st.text_input("Nome do Cliente")
        zap = st.text_input("WhatsApp")
        if st.form_submit_button("Salvar Tutor"):
            st.session_state['clientes'].append({"id": proximo_cod, "nome": nome, "zap": zap})
            st.success(f"Tutor {nome} (Cod: {proximo_cod}) cadastrado!")

elif menu == "🐾 Pacientes":
    st.subheader("Cadastro de Pacientes")
    if not st.session_state['clientes']: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet", clear_on_submit=True):
            proximo_cod_p = f"P{len(st.session_state['pets']) + 1:03d}"
            st.info(f"Código do Paciente: **{proximo_cod_p}**")
            tutor_opcoes = {f"{c['id']} - {c['nome']}": c['id'] for c in st.session_state['clientes']}
            tutor_sel = st.selectbox("Dono (Código - Nome)", list(tutor_opcoes.keys()))
            nome_p = st.text_input("Nome do Animal")
            raca = st.text_input("Raça / Espécie")
            if st.form_submit_button("Salvar Paciente"):
                st.session_state['pets'].append({
                    "id": proximo_cod_p, "nome": nome_p, 
                    "tutor_id": tutor_opcoes[tutor_sel], "raca": raca
                })
                st.success(f"Pet {nome_p} cadastrado com sucesso!")

elif menu == "🩺 Prontuário IA":
    st.subheader("Atendimento Clínico")
    if not st.session_state['pets']: st.info("Cadastre um pet primeiro.")
    else:
        with st.form("f_atend"):
            pet_opcoes = {f"{p['id']} - {p['nome']} (Dono: {p['tutor_id']})": p for p in st.session_state['pets']}
            pet_sel = st.selectbox("Selecione o Paciente", list(pet_opcoes.keys()))
            relato = st.text_area("Resumo do Atendimento (Dite com Win+H)", height=200)
            if st.form_submit_button("Arquivar Prontuário"):
                dados_pet = pet_opcoes[pet_sel]
                st.session_state['historico'].append({
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Cód. Pet": dados_pet['id'],
                    "Paciente": dados_pet['nome'],
                    "Cód. Tutor": dados_pet['tutor_id'],
                    "Resumo Clínico": relato
                })
                st.success("Atendimento arquivado no histórico!")
