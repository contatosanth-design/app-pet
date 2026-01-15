import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- ESTILO ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
if 'clientes' not in st.session_state: st.session_state['clientes'] = {}
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'vacinas' not in st.session_state: st.session_state['vacinas'] = []
if 'historico' not in st.session_state: st.session_state['historico'] = []

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", use_container_width=True)
    st.markdown("<h2 style='text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MENU", ["🏠 Início & Excel", "💉 Controle de Vacinas", "🎉 Aniversariantes", "👤 Tutores", "🐶 Pets", "🩺 Prontuário IA"])

# --- 🏠 PÁGINA: INÍCIO & EXCEL ---
if menu == "🏠 Início & Excel":
    st.title("📊 Gestão e Relatórios")
    if st.session_state['historico']:
        df = pd.DataFrame(st.session_state['historico'])
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Atendimentos')
        st.download_button("📥 Baixar Planilha de Atendimentos (Excel)", data=output.getvalue(), 
                           file_name=f"consultas_{datetime.now().strftime('%d_%m_%Y')}.xlsx")
        st.dataframe(df)
    else: st.info("Nenhum atendimento para exportar.")

# --- 💉 PÁGINA: CONTROLE DE VACINAS ---
elif menu == "💉 Controle de Vacinas":
    st.title("💉 Gestão de Vacinação")
    
    with st.expander("Registrar Nova Vacina"):
        with st.form("f_vacina"):
            pet_v = st.selectbox("Paciente", [p['nome'] for p in st.session_state['pets']])
            nome_v = st.text_input("Nome da Vacina (Ex: V10, Raiva)")
            dt_apl = st.date_input("Data de Aplicação", format="DD/MM/YYYY")
            dt_ven = st.date_input("Data de Vencimento/Reforço", format="DD/MM/YYYY")
            if st.form_submit_button("Salvar Vacina"):
                pet_info = next(p for p in st.session_state['pets'] if p['nome'] == pet_v)
                st.session_state['vacinas'].append({
                    "pet": pet_v, "vacina": nome_v, "vencimento": dt_ven, "tutor_id": pet_info['cod_tutor']
                })
                st.success("Vacina registrada!")

    st.subheader("🔔 Próximos Vencimentos (Lembretes)")
    hoje = datetime.now().date()
    proximos = hoje + timedelta(days=7)
    
    for v in st.session_state['vacinas']:
        if hoje <= v['vencimento'] <= proximos:
            tutor = st.session_state['clientes'].get(v['tutor_id'], {})
            col1, col2 = st.columns([3, 1])
            col1.warning(f"⚠️ **{v['pet']}**: {v['vacina']} vence em {v['vencimento'].strftime('%d/%m/%Y')}")
            
            msg = f"Olá {tutor.get('nome')}, aqui é do Consultório da Ribeira. A vacina {v['vacina']} do(a) {v['pet']} vence dia {v['vencimento'].strftime('%d/%m/%Y')}. Vamos agendar o reforço?"
            link = f"https://wa.me/{tutor.get('zap')}?text={msg.replace(' ', '%20')}"
            col2.markdown(f"[📲 Enviar Lembrete]({link})")

# --- 🩺 PÁGINA: PRONTUÁRIO IA ---
elif menu == "🩺 Prontuário IA":
    st.title("🩺 Consulta com Transcrição")
    st.info("🎤 Use 'Windows + H' para transcrever sua conversa com o tutor.")
    if not st.session_state['pets']: st.warning("Cadastre um pet primeiro.")
    else:
        with st.form("f_ia"):
            pet_sel = st.selectbox("Paciente", [p['nome'] for p in st.session_state['pets']])
            c1, c2 = st.columns(2)
            peso, temp = c1.text_input("Peso (kg)"), c2.text_input("Temp (°C)")
            transcricao = st.text_area("Anamnese e Diagnóstico (IA de Voz)", height=250)
            if st.form_submit_button("Arquivar Consulta"):
                p_data = next(p for p in st.session_state['pets'] if p['nome'] == pet_sel)
                st.session_state['historico'].append({
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Tutor": st.session_state['clientes'][p_data['cod_tutor']]['nome'],
                    "Paciente": pet_sel, "Peso": peso, "Temp": temp, "Relato": transcricao
                })
                st.success("Salvo no histórico!")

# --- (As outras abas de Tutores, Pets e Aniversariantes continuam com a mesma lógica estável) ---
