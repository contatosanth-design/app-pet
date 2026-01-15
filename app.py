import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicialização do Banco de Dados
if 'estoque' not in st.session_state or len(st.session_state['estoque']) < 5:
    st.session_state['estoque'] = [
        {"Item": "Vacina V10 (Importada)", "Preco": 120.00},
        {"Item": "Vacina Antirrábica", "Preco": 60.00},
        {"Item": "Consulta Clínica", "Preco": 150.00},
        {"Item": "Hemograma Completo", "Preco": 95.00},
        {"Item": "Simparic 10-20kg", "Preco": 88.00},
        {"Item": "Castração Macho", "Preco": 350.00},
        {"Item": "Apoquel 5.4mg (Unid)", "Preco": 15.00},
        {"Item": "Vermífugo Drontal", "Preco": 40.00}
    ]

for key in ['clientes', 'pets', 'historico']:
    if key not in st.session_state: st.session_state[key] = []

with st.sidebar:
    st.title("Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "💰 Financeiro"])

# --- TUTORES ---
if menu == "👤 Tutores":
    st.subheader("📝 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        id_t = f"T{len(st.session_state['clientes']) + 1:03d}"
        nome = st.text_input("Nome do Cliente*")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        zap = c2.text_input("WhatsApp (Ex: 22985020463)*")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({"id": id_t, "nome": nome.upper(), "cpf": cpf, "zap": zap, "email": email, "end": end})
                st.success("Tutor cadastrado!")

# --- PETS ---
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            t_lista = {f"{c['id']} - {c['nome']}": c for c in st.session_state['clientes']}
            t_sel = st.selectbox("Proprietário*", list(t_lista.keys()))
            nome_p = st.text_input("Nome do Pet*")
            nasc = st.date_input("Data de Nascimento", value=date(2022, 1, 1), format="DD/MM/YYYY")
            hoje = date.today()
            anos = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
            st.info(f"Idade Calculada: {anos} anos")
            if st.form_submit_button("✅ Salvar Pet"):
                st.session_state['pets'].append({"id": f"P{len(st.session_state['pets'])+1:03d}", "nome": nome_p.upper(), "idade": anos, "tutor": t_lista[t_sel]})
                st.success("Pet cadastrado!")

# --- PRONTUÁRIO ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento (Win+H para ditar)")
    if not st.session_state['pets']: st.info("Cadastre um pet.")
    else:
        with st.form("f_ia"):
            p_lista = {p['nome']: p for p in st.session_state['pets']}
            p_sel = st.selectbox("Paciente", list(p_lista.keys()))
            relato = st.text_area("Relato da Consulta", height=200)
            if st.form_submit_button("💾 Salvar Histórico"):
                st.session_state['historico'].append({"Data": date.today().strftime("%d/%m/%Y"), "Pet": p_sel, "Relato": relato})
                st.success("Salvo!")

# --- FINANCEIRO ---
elif menu == "💰 Financeiro":
    st.subheader("💰 Fechamento e Recibo")
    if not st.session_state['clientes']: st.error("Cadastre um tutor.")
    else:
        t_lista = {c['nome']: c for c in st.session_state['clientes']}
        t_nome = st.selectbox("Tutor", list(t_lista.keys()))
        itens_sel = st.multiselect("Procedimentos", [i['Item'] for i in st.session_state['estoque']])
        valor_bruto = sum([i['Preco'] for i in st.session_state['estoque'] if i['Item'] in itens_sel])
        st.write(f"### Total: R$ {valor_bruto:.2f}")
        if st.button("📲 Gerar Recibo WhatsApp"):
            t_zap = t_lista[t_nome]['zap']
            msg = f"Olá {t_nome}, recibo Ribeira Vet: {', '.join(itens_sel)}. Total: R$ {valor_bruto:.2f}."
            st.markdown(f"#### [Clique aqui para enviar](https://wa.me/{t_zap}?text={urllib.parse.quote(msg)})")

elif menu == "🏠 Dashboard":
    st.metric("Pacientes", len(st.session_state['pets']))
    if st.session_state['historico']: st.table(pd.DataFrame(st.session_state['historico']))
