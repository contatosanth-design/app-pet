import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- CSS PARA CORREÇÃO DE FONTES E CORES ---
st.markdown("""
    <style>
    /* Fundo da tela principal */
    .main { background-color: #f1f3f6; }
    
    /* Menu Lateral Azul Profundo */
    [data-testid="stSidebar"] { 
        background-color: #1e3d59 !important; 
        border-right: 2px solid #2e7bcf; 
    }
    
    /* FORÇAR COR BRANCA NAS FONTES DO MENU */
    [data-testid="stSidebar"] .stRadio label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2 { 
        color: white !important; 
        font-weight: 500 !important;
    }

    /* Estilo dos Botões */
    .stButton>button { 
        background-color: #2e7bcf; 
        color: white !important; 
        border-radius: 8px; 
        font-weight: bold; 
    }

    /* Caixa de Título (Header) */
    .header-box { 
        background-color: white; 
        padding: 25px; 
        border-radius: 12px; 
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08); 
        margin-bottom: 25px;
        border-left: 5px solid #2e7bcf;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
for key in ['clientes', 'pets', 'historico', 'estoque', 'financeiro']:
    if key not in st.session_state: st.session_state[key] = {} if key == 'clientes' else []

# --- BARRA LATERAL ---
with st.sidebar:
    # Logo estável para teste (Coração com Pet)
    st.image("https://cdn-icons-png.flaticon.com/512/194/194279.png", width=120)
    st.markdown("<h2 style='text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    
    # Navegação com ícones
    menu = st.radio("NAVEGAÇÃO", [
        "🏠 Dashboard", 
        "👤 Tutores", 
        "🐾 Pacientes", 
        "🩺 Prontuário IA", 
        "📦 Estoque & Vacinas", 
        "💰 Financeiro", 
        "🎂 Aniversários"
    ])

# --- CABEÇALHO ---
st.markdown(f"""
    <div class='header-box'>
        <h1 style='color: #1e3d59; margin: 0;'>Ribeira Vet Pro</h1>
        <p style='color: #666; margin: 0;'>Sistema de Gestão de Dados Clínica Veterinária • {datetime.now().strftime('%d/%m/%Y')}</p>
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DAS PÁGINAS ---

if menu == "🏠 Dashboard":
    c1, c2 = st.columns(2)
    c1.metric("Tutores Cadastrados", len(st.session_state['clientes']))
    c2.metric("Pacientes Atendidos", len(st.session_state['pets']))
    
    if st.session_state['historico']:
        st.subheader("📊 Relatório de Atendimentos")
        df = pd.DataFrame(st.session_state['historico'])
        st.dataframe(df, use_container_width=True)
        # Exportação Excel
        towrite = io.BytesIO()
        df.to_excel(towrite, index=False, engine='xlsxwriter')
        st.download_button("📥 Baixar Planilha para Pesquisa", data=towrite.getvalue(), file_name="consultas.xlsx")

elif menu == "👤 Tutores":
    st.subheader("Ficha do Proprietário")
    with st.form("f_tutor", clear_on_submit=True):
        nome = st.text_input("Nome Completo")
        c1, c2 = st.columns(2)
        cpf, zap = c1.text_input("CPF"), c2.text_input("WhatsApp")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("Salvar Tutor"):
            st.session_state['clientes'][nome] = {"cpf": cpf, "zap": zap, "email": email, "end": end}
            st.success("Tutor registrado!")

elif menu == "🐾 Pacientes":
    st.subheader("Ficha do Animal")
    if not st.session_state['clientes']: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet", clear_on_submit=True):
            dono = st.selectbox("Proprietário", list(st.session_state['clientes'].keys()))
            nome_p = st.text_input("Nome do Pet")
            nasc = st.date_input("Data de Nascimento", format="DD/MM/YYYY")
            raca = st.text_input("Raça / Espécie")
            if st.form_submit_button("Cadastrar Pet"):
                st.session_state['pets'].append({"nome": nome_p, "nascimento": nasc, "tutor": dono, "raca": raca})
                st.success("Paciente cadastrado!")

elif menu == "🩺 Prontuário IA":
    st.subheader("Atendimento Clínico (Voz)")
    st.info("🎤 **Instrução:** Clique no campo de texto e use 'Windows + H' para ditar a consulta.")
    if not st.session_state['pets']: st.info("Cadastre um pet primeiro.")
    else:
        with st.form("f_atend"):
            pet_sel = st.selectbox("Paciente", [p['nome'] for p in st.session_state['pets']])
            c1, c2 = st.columns(2)
            peso, temp = c1.text_input("Peso (kg)"), c2.text_input("Temp (°C)")
            relato = st.text_area("Transcrição da Consulta e Diagnóstico", height=250)
            if st.form_submit_button("💾 Salvar Atendimento"):
                st.session_state['historico'].append({
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Paciente": pet_sel, "Peso": peso, "Temp": temp, "Diagnostico": relato
                })
                st.success("Prontuário salvo no histórico!")

elif menu == "📦 Estoque & Vacinas":
    st.subheader("Catálogo de Itens e Serviços")
    with st.form("f_est"):
        item = st.text_input("Nome da Vacina/Medicamento/Serviço")
        preco = st.number_input("Valor de Venda (R$)", min_value=0.0)
        if st.form_submit_button("Adicionar"):
            st.session_state['estoque'].append({"Item": item, "Preco": preco})
    st.table(st.session_state['estoque'])

elif menu == "💰 Financeiro":
    st.subheader("Cobrança e Checkout")
    if not st.session_state['estoque']: st.info("Cadastre preços no estoque primeiro.")
    else:
        with st.form("f_cob"):
            tutor = st.selectbox("Tutor Responsável", list(st.session_state['clientes'].keys()) if st.session_state['clientes'] else ["Nenhum"])
            selecionados = st.multiselect("Procedimentos realizados", [i['Item'] for i in st.session_state['estoque']])
            if st.form_submit_button("Calcular Total"):
                total = sum(i['Preco'] for i in st.session_state['estoque'] if i['Item'] in selecionados)
                st.markdown(f"### Valor Final: R$ {total:.2f}")

elif menu == "🎂 Aniversários":
    st.subheader("Próximos Aniversariantes")
    hoje = datetime.now().strftime("%d/%m")
    for p in st.session_state['pets']:
        if p['nascimento'].strftime("%d/%m") == hoje:
            st.success(f"🐾 Hoje é aniversário do(a) **{p['nome']}**!")
