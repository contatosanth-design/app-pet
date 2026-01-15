import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN PROFISSIONAL ---
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

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=100)
    st.title("Ribeira Vet Pro")
    st.divider()
    menu = st.radio("MENU", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "📦 Produtos & Preços", "💰 Financeiro"])

# --- CABEÇALHO ---
st.markdown(f"<div class='header-box'><h1 style='color:#1e3d59; margin:0;'>Ribeira Vet Pro</h1><p style='margin:0; color:#666;'>Gestão de Clínica e Estoque • {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- CADASTRO DE PRODUTOS E EDIÇÃO DE PREÇOS ---
if menu == "📦 Produtos & Preços":
    st.subheader("📦 Gestão de Produtos e Serviços")
    
    # Parte 1: Novo Cadastro
    with st.expander("➕ Cadastrar Novo Item", expanded=True):
        with st.form("f_novo_prod", clear_on_submit=True):
            item_n = st.text_input("Nome do Produto/Serviço")
            preco_n = st.number_input("Preço de Venda (R$)", min_value=0.0, step=0.50, format="%.2f")
            if st.form_submit_button("Salvar Novo Item"):
                if item_n:
                    st.session_state['estoque'].append({"Item": item_n, "Preco": round(preco_n, 2)})
                    st.success(f"{item_n} cadastrado!")
                    st.rerun()

    # Parte 2: Edição de Valores
    if st.session_state['estoque']:
        st.divider()
        st.subheader("✏️ Alterar Valores Cadastrados")
        for i, prod in enumerate(st.session_state['estoque']):
            c1, c2, c3 = st.columns([3, 2, 1])
            c1.write(f"**{prod['Item']}**")
            novo_p = c2.number_input(f"Valor (R$)", value=float(prod['Preco']), key=f"p_{i}", step=0.50, format="%.2f")
            if c3.button("Atualizar", key=f"btn_{i}"):
                st.session_state['estoque'][i]['Preco'] = round(novo_p, 2)
                st.success(f"Preço de {prod['Item']} atualizado!")
                st.rerun()

# --- CADASTRO DE TUTORES (COMPLETO) ---
elif menu == "👤 Tutores":
    st.subheader("📝 Ficha do Tutor")
    with st.form("f_tutor"):
        st.info(f"Cód: T{len(st.session_state['clientes']) + 1:03d}")
        nome = st.text_input("Nome Completo")
        c1, c2 = st.columns(2)
        cpf, zap = c1.text_input("CPF"), c2.text_input("WhatsApp")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço")
        if st.form_submit_button("Salvar"):
            st.session_state['clientes'].append({"id": f"T{len(st.session_state['clientes']) + 1:03d}", "nome": nome, "cpf": cpf, "zap": zap, "end": end})
            st.success("Tutor salvo!")

# --- CADASTRO DE PETS ---
elif menu == "🐾 Pets":
    st.subheader("🐶 Ficha do Animal")
    if not st.session_state['clientes']: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            t_lista = {f"{c['id']} - {c['nome']}": c['id'] for c in st.session_state['clientes']}
            tutor_ref = st.selectbox("Proprietário", list(t_lista.keys()))
            nome_p = st.text_input("Nome do Pet")
            nasc = st.date_input("Nascimento", format="DD/MM/YYYY")
            if st.form_submit_button("Cadastrar Pet"):
                st.session_state['pets'].append({"id": f"P{len(st.session_state['pets']) + 1:03d}", "nome": nome_p, "tutor_id": t_lista[tutor_ref]})
                st.success("Pet cadastrado!")

# --- PRONTUÁRIO IA ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento Clínico")
    if not st.session_state['pets']: st.info("Cadastre um pet.")
    else:
        with st.form("f_ia"):
            p_lista = {f"{p['id']} - {p['nome']}": p for p in st.session_state['pets']}
            pet_sel = st.selectbox("Paciente", list(p_lista.keys()))
            anamnese = st.text_area("Relato da Consulta (Dite com Win+H)", height=200)
            if st.form_submit_button("Arquivar"):
                d = p_lista[pet_sel]
                st.session_state['historico'].append({"Data": datetime.now().strftime("%d/%m/%Y"), "Paciente": d['nome'], "Resumo": anamnese})
                st.success("Arquivado!")

# --- FINANCEIRO ---
elif menu == "💰 Financeiro":
    st.subheader("💰 Fechamento")
    if not st.session_state['estoque']: st.warning("Cadastre produtos primeiro.")
    else:
        with st.form("f_fin"):
            tutor_f = st.selectbox("Tutor", [c['nome'] for c in st.session_state['clientes']])
            itens_sel = st.multiselect("Itens", [i['Item'] for i in st.session_state['estoque']])
            if st.form_submit_button("Calcular"):
                total = sum(i['Preco'] for i in st.session_state['estoque'] if i['Item'] in itens_sel)
                st.markdown(f"### Total: R$ {total:.2f}")

# --- DASHBOARD ---
elif menu == "🏠 Dashboard":
    st.subheader("📊 Histórico de Pesquisa")
    if st.session_state['historico']:
        df = pd.DataFrame(st.session_state['historico'])
        st.dataframe(df, use_container_width=True)
