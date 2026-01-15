import streamlit as st
import pandas as pd
from datetime import date
from fpdf import FPDF
import os
import urllib.parse

st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# ================== PASTAS ==================
os.makedirs("data", exist_ok=True)
os.makedirs("recibos", exist_ok=True)

# ================== FUNÇÕES ==================
def salvar_excel(nome, dados):
    pd.DataFrame(dados).to_excel(f"data/{nome}.xlsx", index=False)

def carregar_excel(nome):
    caminho = f"data/{nome}.xlsx"
    if os.path.exists(caminho):
        return pd.read_excel(caminho).to_dict(orient="records")
    return []

def gerar_recibo(tutor, pet, itens, total):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "RIBEIRA VET PRO", ln=True)
    pdf.cell(0, 10, f"Tutor: {tutor}", ln=True)
    pdf.cell(0, 10, f"Paciente: {pet}", ln=True)
    pdf.cell(0, 10, f"Data: {date.today().strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(5)

    for i in itens:
        pdf.cell(0, 10, f"- {i['Item']}  R$ {i['Preco']:.2f}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, f"TOTAL: R$ {total:.2f}", ln=True)

    nome = f"recibos/recibo_{tutor}_{date.today()}.pdf".replace(" ", "_")
    pdf.output(nome)
    return nome

# ================== DADOS ==================
if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [
        {"Item": "Consulta Clínica", "Preco": 150.0},
        {"Item": "Vacina V10", "Preco": 120.0},
        {"Item": "Vacina Antirrábica", "Preco": 60.0},
        {"Item": "Hemograma", "Preco": 95.0},
        {"Item": "Castração", "Preco": 350.0}
    ]

st.session_state['clientes'] = carregar_excel("clientes")
st.session_state['pets'] = carregar_excel("pets")
st.session_state['historico'] = carregar_excel("historico")
st.session_state['financeiro'] = carregar_excel("financeiro")

# ================== MENU ==================
menu = st.sidebar.radio("MENU", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário", "💰 Financeiro"])

# ================== TUTORES ==================
if menu == "👤 Tutores":
    st.subheader("Cadastro de Tutores")
    nome = st.text_input("Nome*")
    zap = st.text_input("WhatsApp* (somente números)")
    if st.button("Salvar"):
        st.session_state['clientes'].append({"Nome": nome, "WhatsApp": zap})
        salvar_excel("clientes", st.session_state['clientes'])
        st.success("Tutor salvo!")

# ================== PETS ==================
elif menu == "🐾 Pets":
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor primeiro.")
    else:
        tutor = st.selectbox("Tutor", [c['Nome'] for c in st.session_state['clientes']])
        nome = st.text_input("Nome do Pet")
        nasc = st.date_input("Nascimento")
        idade = date.today().year - nasc.year
        if st.button("Salvar Pet"):
            st.session_state['pets'].append({"Pet": nome, "Tutor": tutor, "Idade": idade})
            salvar_excel("pets", st.session_state['pets'])
            st.success("Pet salvo!")

# ================== PRONTUÁRIO ==================
elif menu == "🩺 Prontuário":
    if not st.session_state['pets']:
        st.info("Cadastre um pet.")
    else:
        pet = st.selectbox("Paciente", [p['Pet'] for p in st.session_state['pets']])
        texto = st.text_area("Relato (você pode ditar)")
        if st.button("Salvar Prontuário"):
            st.session_state['historico'].append({
                "Data": date.today().strftime("%d/%m/%Y"),
                "Pet": pet,
                "Relato": texto
            })
            salvar_excel("historico", st.session_state['historico'])
            st.success("Prontuário salvo!")

# ================== FINANCEIRO ==================
elif menu == "💰 Financeiro":
    tutor = st.selectbox("Tutor", [c['Nome'] for c in st.session_state['clientes']])
    pet = st.selectbox("Pet", [p['Pet'] for p in st.session_state['pets']])
    itens_nomes = st.multiselect("Serviços", [i['Item'] for i in st.session_state['estoque']])

    if itens_nomes:
        itens = []
        total = 0
        for n in itens_nomes:
            i = next(x for x in st.session_state['estoque'] if x['Item'] == n)
            itens.append(i)
            total += i['Preco']

        if st.button("Gerar Recibo"):
            pdf = gerar_recibo(tutor, pet, itens, total)
            st.session_state['financeiro'].append({
                "Data": date.today().strftime("%d/%m/%Y"),
                "Tutor": tutor,
                "Pet": pet,
                "Total": total
            })
            salvar_excel("financeiro", st.session_state['financeiro'])

            zap = next(c['WhatsApp'] for c in st.session_state['clientes'] if c['Nome'] == tutor)
            msg = f"Olá {tutor}, segue o recibo do atendimento do {pet}. Total R$ {total:.2f}"
            link = f"https://wa.me/55{zap}?text={urllib.parse.quote(msg)}"

            st.success("Recibo gerado!")
            st.markdown(f"[📲 Enviar pelo WhatsApp]({link})")

# ================== DASHBOARD ==================
else:
    st.metric("Tutores", len(st.session_state['clientes']))
    st.metric("Pets", len(st.session_state['pets']))
    st.metric("Atendimentos", len(st.session_state['historico']))
