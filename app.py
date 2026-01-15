import streamlit as st
import pandas as pd
from datetime import datetime, date

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- CSS PROFISSIONAL ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59 !important; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold !important; }
    .header-box { background: white; padding: 20px; border-radius: 10px; border-left: 6px solid #2e7bcf; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if 'clientes' not in st.session_state: st.session_state['clientes'] = []
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'historico' not in st.session_state: st.session_state['historico'] = []
if 'estoque' not in st.session_state: st.session_state['estoque'] = []

# --- LISTA DE RAÇAS PRÉ-CADASTRADAS ---
RACA_LISTA = ["SRD (Vira-lata)", "Spitz Alemão", "Poodle", "Shih Tzu", "Yorkshire", "Bulldog Francês", "Golden Retriever", "Pinscher", "Persa (Gato)", "Siamês (Gato)", "Outra"]

# --- FUNÇÃO CALCULAR IDADE ---
def calcular_idade(nasc):
    hoje = date.today()
    anos = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
    return f"{anos} anos" if anos > 0 else "Filhote"

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=80)
    st.title("Ribeira Vet Pro")
    st.divider()
    menu = st.radio("MENU", ["🏠 Dashboard", "👤 Tutores", "🐾 Cadastro de Pets", "🩺 Prontuário IA", "📦 Produtos", "💰 Financeiro"])

# --- CABEÇALHO ---
st.markdown(f"<div class='header-box'><h1 style='color:#1e3d59; margin:0;'>Ribeira Vet Pro</h1><p style='margin:0;'>Identificação Clínica • {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- CADASTRO DE PETS (VERSÃO DETALHADA) ---
if menu == "🐾 Cadastro de Pets":
    st.subheader("🐶 Ficha Técnica do Animal")
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor antes de registrar o pet.")
    else:
        with st.form("f_pet_detalhado", clear_on_submit=True):
            id_p = f"P{len(st.session_state['pets']) + 1:03d}"
            st.info(f"Cód. Paciente: **{id_p}**")
            
            # Vínculo com Tutor
            t_lista = {f"{c['id']} - {c['nome']}": c['id'] for c in st.session_state['clientes']}
            tutor_ref = st.selectbox("Proprietário Responsável", list(t_lista.keys()))
            
            col1, col2, col3 = st.columns(3)
            nome_p = col1.text_input("Nome do Animal*")
            nasc_p = col2.date_input("Data de Nascimento", value=date(2020,1,1), format="DD/MM/YYYY")
            sexo_p = col3.selectbox("Sexo", ["Macho", "Fêmea"])
            
            col4, col5, col6 = st.columns(3)
            raca_p = col4.selectbox("Raça/Espécie", RACA_LISTA)
            pelo_p = col5.text_input("Cor do Pêlo")
            castrado = col6.selectbox("Animal Castrado?", ["Não", "Sim"])
            
            col7, col8 = st.columns(2)
            chip_p = col7.text_input("Número do Microchip (se houver)")
            foto_p = col8.file_uploader("Carregar Foto do Pet", type=['png', 'jpg', 'jpeg'])
            
            if st.form_submit_button("✅ SALVAR FICHA DO ANIMAL"):
                if nome_p:
                    idade_texto = calcular_idade(nasc_p)
                    st.session_state['pets'].append({
                        "id": id_p, "nome": nome_p, "tutor_id": t_lista[tutor_ref],
                        "idade": idade_texto, "sexo": sexo_p, "raca": raca_p,
                        "pelo": pelo_p, "castrado": castrado, "chip": chip_p
                    })
                    st.success(f"Ficha de {nome_p} ({idade_texto}) arquivada com sucesso!")
                else:
                    st.error("O nome do animal é obrigatório.")

# --- DEMAIS MÓDULOS (Mantidos conforme solicitado) ---
elif menu == "👤 Tutores":
    st.subheader("📝 Cadastro de Tutores")
    with st.form("f_tutor"):
        nome = st.text_input("Nome Completo")
        c1, c2 = st.columns(2); cpf = c1.text_input("CPF"); zap = c2.text_input("WhatsApp")
        email = st.text_input("E-mail"); end = st.text_area("Endereço")
        if st.form_submit_button("Salvar"):
            st.session_state['clientes'].append({"id": f"T{len(st.session_state['clientes']) + 1:03d}", "nome": nome, "cpf": cpf, "zap": zap, "end": end})
            st.success("Tutor cadastrado!")

elif menu == "📦 Produtos":
    st.subheader("📦 Catálogo")
    with st.form("f_prod"):
        item = st.text_input("Nome"); preco = st.number_input("Preço", format="%.2f")
        if st.form_submit_button("Adicionar"):
            st.session_state['estoque'].append({"Item": item, "Preco": round(preco, 2)})
            st.success("Adicionado!")
    st.table(st.session_state['estoque'])

elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento")
    if not st.session_state['pets']: st.info("Cadastre um pet.")
    else:
        with st.form("f_ia"):
            p_lista = {f"{p['id']} - {p['nome']}": p for p in st.session_state['pets']}
            pet_sel = st.selectbox("Paciente", list(p_lista.keys()))
            relato = st.text_area("Resumo Clínico (Dite Win+H)", height=200)
            if st.form_submit_button("Arquivar"):
                st.session_state['historico'].append({"Data": datetime.now().strftime("%d/%m/%Y"), "Pet": p_lista[pet_sel]['nome'], "Resumo": relato})
                st.success("Salvo!")

elif menu == "🏠 Dashboard":
    st.subheader("📊 Pesquisa Geral")
    if st.session_state['historico']:
        st.dataframe(pd.DataFrame(st.session_state['historico']), use_container_width=True)
