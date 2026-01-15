import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN PROFISSIONAL (Menu Azul e Fontes Brancas) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59 !important; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold !important; }
    .header-box { background: white; padding: 20px; border-radius: 10px; border-left: 6px solid #2e7bcf; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 8px; width: 100%; }
    .main { background-color: #f1f3f6; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO BANCO DE DADOS ---
for key in ['clientes', 'pets', 'historico', 'estoque']:
    if key not in st.session_state: st.session_state[key] = []

# --- MENU LATERAL (LOGO E NAVEGAÇÃO) ---
with st.sidebar:
    # Logo Veterinário Estável
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=100)
    st.markdown("<h2 style='text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MENU PRINCIPAL", [
        "🏠 Dashboard & Pesquisa", 
        "👤 Cadastro de Tutores", 
        "🐾 Cadastro de Pets", 
        "🩺 Prontuário IA", 
        "📦 Cadastro de Produtos", 
        "💰 Financeiro & Cobrança"
    ])

# --- CABEÇALHO ---
st.markdown(f"<div class='header-box'><h1 style='color:#1e3d59; margin:0;'>Ribeira Vet Pro</h1><p style='margin:0; color:#666;'>Versão Pro Max • {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- 1. DASHBOARD & PESQUISA ---
if menu == "🏠 Dashboard & Pesquisa":
    st.subheader("📊 Arquivo Geral do Sistema")
    if st.session_state['historico']:
        df = pd.DataFrame(st.session_state['historico'])
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Baixar Planilha para Pesquisa", data=csv, file_name="ribeira_vet_completo.csv")
    else: st.info("Nenhum atendimento arquivado ainda.")

# --- 2. CADASTRO DE TUTORES ---
elif menu == "👤 Cadastro de Tutores":
    st.subheader("📝 Registro de Proprietário")
    with st.form("f_tutor", clear_on_submit=True):
        id_t = f"T{len(st.session_state['clientes']) + 1:03d}"
        st.info(f"Cód. Sistema: {id_t}")
        nome = st.text_input("Nome Completo")
        c1, c2 = st.columns(2)
        cpf, zap = c1.text_input("CPF"), c2.text_input("WhatsApp")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("✅ SALVAR TUTOR"):
            st.session_state['clientes'].append({"id": id_t, "nome": nome, "cpf": cpf, "zap": zap, "email": email, "end": end})
            st.success(f"Tutor {nome} registrado com o código {id_t}!")

# --- 3. CADASTRO DE PETS ---
elif menu == "🐾 Cadastro de Pets":
    st.subheader("🐶 Registro de Pacientes")
    if not st.session_state['clientes']: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet", clear_on_submit=True):
            id_p = f"P{len(st.session_state['pets']) + 1:03d}"
            st.info(f"Cód. Paciente: {id_p}")
            t_lista = {f"{c['id']} - {c['nome']}": c['id'] for c in st.session_state['clientes']}
            tutor_ref = st.selectbox("Selecione o Dono", list(t_lista.keys()))
            nome_p = st.text_input("Nome do Animal")
            nasc = st.date_input("Nascimento", format="DD/MM/YYYY")
            raca = st.text_input("Raça")
            if st.form_submit_button("✅ REGISTRAR PET"):
                st.session_state['pets'].append({"id": id_p, "nome": nome_p, "tutor_id": t_lista[tutor_ref], "nasc": nasc, "raca": raca})
                st.success("Pet cadastrado!")

# --- 4. PRONTUÁRIO IA ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento Clínico (Voz)")
    if not st.session_state['pets']: st.info("Cadastre um pet primeiro.")
    else:
        with st.form("f_ia"):
            p_lista = {f"Cód: {p['id']} - {p['nome']}": p for p in st.session_state['pets']}
            pet_sel = st.selectbox("Paciente", list(p_lista.keys()))
            anamnese = st.text_area("Resumo da Consulta (Use Win+H para ditar)", height=250)
            if st.form_submit_button("💾 ARQUIVAR CONSULTA"):
                dados = p_lista[pet_sel]
                st.session_state['historico'].append({
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Cód_Tutor": dados['tutor_id'], "Cód_Pet": dados['id'],
                    "Paciente": dados['nome'], "Resumo": anamnese
                })
                st.success("Consulta arquivada no histórico!")

# --- 5. CADASTRO DE PRODUTOS ---
elif menu == "📦 Cadastro de Produtos":
    st.subheader("📦 Estoque de Medicamentos, Vacinas e Serviços")
    with st.form("f_prod", clear_on_submit=True):
        item = st.text_input("Nome do Produto ou Serviço")
        preco = st.number_input("Valor de Venda (R$)", min_value=0.0)
        if st.form_submit_button("✅ ADICIONAR AO CATÁLOGO"):
            st.session_state['estoque'].append({"Item": item, "Preco": preco})
            st.success(f"{item} adicionado com sucesso!")
    st.table(st.session_state['estoque'])

# --- 6. FINANCEIRO & COBRANÇA ---
elif menu == "💰 Financeiro & Cobrança":
    st.subheader("💰 Fechamento de Conta")
    if not st.session_state['estoque'] or not st.session_state['clientes']:
        st.warning("É necessário ter Tutores e Produtos cadastrados.")
    else:
        with st.form("f_financeiro"):
            tutor_f = st.selectbox("Responsável pelo Pagamento", [c['nome'] for c in st.session_state['clientes']])
            itens = st.multiselect("Itens utilizados no atendimento", [i['Item'] for i in st.session_state['estoque']])
            if st.form_submit_button("🖩 CALCULAR TOTAL"):
                valor_total = sum(i['Preco'] for i in st.session_state['estoque'] if i['Item'] in itens)
                st.markdown(f"### Valor Total para {tutor_f}: R$ {valor_total:.2f}")
