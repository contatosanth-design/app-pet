import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN E LOGOTIPO ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 5px; }
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO BANCO DE DADOS ---
for key in ['clientes', 'pets', 'historico', 'estoque', 'financeiro']:
    if key not in st.session_state: st.session_state[key] = {} if key == 'clientes' else []

# --- MENU LATERAL ---
with st.sidebar:
    # Logotipo conforme combinado
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", width=200)
    st.markdown("<h2 style='text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("NAVEGAÇÃO", [
        "📊 Dashboard & Excel", 
        "👤 Tutores", 
        "🐶 Pets", 
        "🩺 Prontuário IA",
        "💊 Estoque e Serviços",
        "💰 Cobrança / Checkout",
        "🎉 Aniversariantes"
    ])

# --- 📊 DASHBOARD & EXCEL ---
if menu == "📊 Dashboard & Excel":
    st.title("Painel Administrativo")
    if st.session_state['historico']:
        df = pd.DataFrame(st.session_state['historico'])
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        st.download_button("📥 Baixar Planilha de Atendimentos", data=buffer.getvalue(), file_name="atendimentos_ribeira.xlsx")
        st.dataframe(df)
    else: st.info("Nenhum atendimento arquivado para gerar planilha.")

# --- 👤 CADASTRO DE TUTORES (COMPLETO) ---
elif menu == "👤 Tutores":
    st.title("Cadastro de Proprietário")
    with st.form("f_tutor"):
        id_t = f"T-{len(st.session_state['clientes'])+1:03d}"
        nome = st.text_input("Nome Completo")
        c1, c2 = st.columns(2)
        cpf, zap = c1.text_input("CPF"), c2.text_input("WhatsApp")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço")
        if st.form_submit_button("Salvar"):
            st.session_state['clientes'][id_t] = {"nome": nome, "cpf": cpf, "zap": zap, "email": email, "end": end}
            st.success("Tutor cadastrado!")

# --- 🐶 CADASTRO DE PETS (COM DATA BR) ---
elif menu == "🐶 Pets":
    st.title("Cadastro de Pacientes")
    if not st.session_state['clientes']: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            tutores = [f"{k} | {v['nome']}" for k, v in st.session_state['clientes'].items()]
            tutor_sel = st.selectbox("Proprietário", tutores)
            nome_p = st.text_input("Nome do Animal")
            nasc = st.date_input("Data de Nascimento", format="DD/MM/YYYY")
            if st.form_submit_button("Registrar Pet"):
                st.session_state['pets'].append({"nome": nome_p, "nascimento": nasc, "tutor": tutor_sel.split(" | ")[1]})
                st.success("Pet registrado!")

# --- 🩺 PRONTUÁRIO IA (TRANSCRIÇÃO) ---
elif menu == "🩺 Prontuário IA":
    st.title("Consulta (Ditado por Voz)")
    st.info("🎤 Use 'Windows + H' para transcrever o atendimento.")
    if not st.session_state['pets']: st.info("Cadastre um pet primeiro.")
    else:
        with st.form("f_ia"):
            pet = st.selectbox("Paciente", [p['nome'] for p in st.session_state['pets']])
            anamnese = st.text_area("Relato Clínico (IA)", height=200)
            if st.form_submit_button("Arquivar Consulta"):
                st.session_state['historico'].append({"Data": datetime.now().strftime("%d/%m/%Y"), "Paciente": pet, "Relato": anamnese})
                st.success("Consulta arquivada!")

# --- 💊 ESTOQUE E SERVIÇOS ---
elif menu == "💊 Estoque e Serviços":
    st.title("Tabela de Preços")
    with st.form("f_est"):
        item = st.text_input("Nome do Produto/Serviço")
        valor = st.number_input("Preço (R$)", min_value=0.0)
        if st.form_submit_button("Adicionar"):
            st.session_state['estoque'].append({"Item": item, "Preco": valor})
            st.success("Item adicionado!")
    st.table(st.session_state['estoque'])

# --- 💰 COBRANÇA / CHECKOUT (NOVO!) ---
elif menu == "💰 Cobrança / Checkout":
    st.title("Fechamento de Atendimento")
    if not st.session_state['estoque']: st.info("Cadastre produtos no estoque primeiro.")
    else:
        with st.form("f_fin"):
            tutor_nomes = [v['nome'] for v in st.session_state['clientes'].values()]
            tutor = st.selectbox("Responsável pelo Pagamento", tutor_nomes)
            selecionados = st.multiselect("Procedimentos/Produtos", [i['Item'] for i in st.session_state['estoque']])
            if st.form_submit_button("Gerar Conta Final"):
                total = sum(i['Preco'] for i in st.session_state['estoque'] if i['Item'] in selecionados)
                st.write(f"### Valor Total para {tutor}: R$ {total:.2f}")
                st.session_state['financeiro'].append({"Tutor": tutor, "Total": total, "Data": datetime.now()})

# --- 🎉 ANIVERSARIANTES ---
elif menu == "🎉 Aniversariantes":
    st.title("🎂 Aniversariantes")
    hoje = datetime.now().strftime("%d/%m")
    for p in st.session_state['pets']:
        if p['nascimento'].strftime("%d/%m") == hoje:
            st.success(f"🐾 Parabéns para o(a) **{p['nome']}**!")
