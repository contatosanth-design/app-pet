import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Storypet | Clínica Veterinária", layout="centered")

st.title("🐾 Storypet – Ficha Veterinária com PDF")
st.write("Preencha os dados abaixo para gerar a ficha em PDF.")

with st.form("ficha_pet"):
    nome_tutor = st.text_input("Nome do Tutor")
    telefone = st.text_input("Telefone / WhatsApp")
    nome_pet = st.text_input("Nome do Pet")
    especie = st.selectbox("Espécie", ["Cão", "Gato", "Outro"])
    idade = st.text_input("Idade do Pet")
    observacoes = st.text_area("Observações Clínicas")

    gerar = st.form_submit_button("📄 Gerar PDF")

if gerar:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "FICHA VETERINÁRIA", ln=True)

    pdf.set_font("Arial", size=12)_
