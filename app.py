import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

st.set_page_config(page_title="Ribeira Vet Pro v7.0", layout="wide")

# 1. Banco de Dados e Itens
if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [
        {"Item": "Vacina V10 (Importada)", "Preco": 120.00},
        {"Item": "Vacina Antirrábica", "Preco": 60.00},
        {"Item": "Consulta Clínica", "Preco": 150.00},
        {"Item": "Hemograma Completo", "Preco": 95.00},
        {"Item": "Castração Macho", "Preco": 350.00},
        {"Item": "Simparic 10-20kg", "Preco": 88.00}
    ]

for key in ['clientes', 'pets', 'historico']:
    if key not in st.session_state: st.session_state[key] = []

# 2. Menu Lateral
with st.sidebar:
    st.title("Ribeira Vet Pro")
    st.info("Versão 7.0 - Estável")
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "💰 Financeiro"])

# --- TUTORES ---
if menu == "👤 Tutores":
    st.subheader("📝 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        nome = st.text_input("Nome do Cliente*")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        zap = c2.text_input("WhatsApp (Ex: 22985020463)*")
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({"id": f"T{len(st.session_state['clientes'])+1:03d}", "nome": nome.upper(), "cpf": cpf, "zap": zap, "end": end})
                st.success("Tutor cadastrado!")

# --- PETS (IDADE DINÂMICA E RAÇAS) ---
elif menu == "🐾 Pets":
    st.subheader("🐾 Ficha do Paciente")
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor primeiro.")
    else:
        t_lista = {f"{c['id']} - {c['nome']}": c['nome'] for c in st.session_state['clientes']}
        t_sel = st.selectbox("Proprietário*", list(t_lista.keys()))
        nome_p = st.text_input("Nome do Pet*")
        
        c1, c2, c3 = st.columns(3)
        especie = c1.selectbox("Espécie", ["Cão", "Gato", "Outro"])
        raca = c2.selectbox("Raça", ["SRD", "Pinscher", "Poodle", "Shih Tzu", "Pitbull", "Spitz Alemão", "Buldogue", "Outra"])
        sexo = c3.selectbox("Sexo", ["Macho", "Fêmea"])
        
        nasc = st.date_input("Data de Nascimento", value=date(2020, 1, 1), format="DD/MM/YYYY")
        hoje = date.today()
        idade_real = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
        st.info(f"Idade Calculada: {idade_real} anos")
        
        if st.button("✅ Salvar Ficha do Pet"):
            if nome_p:
                st.session_state['pets'].append({"nome": nome_p.upper(), "raca": raca, "idade": idade_real, "tutor": t_lista[t_sel]})
                st.success("Paciente registrado!")

# --- PRONTUÁRIO IA ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento Clínico")
    st.markdown("> **DICA:** Clique na caixa de texto e use **Win+H** para ditar.")
    if not st.session_state['pets']: st.info("Cadastre um pet.")
    else:
        p_sel = st.selectbox("Selecione o Paciente", [p['nome'] for p in st.session_state['pets']])
        relato = st.text_area("Relato da Consulta (Clique aqui antes de falar)", height=300)
        if st.button("💾 Salvar Atendimento"):
            st.session_state['historico'].append({"Data": date.today().strftime("%d/%m/%Y"), "Pet": p_sel, "Relato": relato})
            st.success("Histórico atualizado!")

# --- FINANCEIRO ---
elif menu == "💰 Financeiro":
    st.subheader("💰 Fechamento de Conta")
    if st.session_state['clientes']:
        t_nome = st.selectbox("Tutor para Cobrança", [c['nome'] for c in st.session_state['clientes']])
        itens_sel = st.multiselect("Procedimentos realizados", [i['Item'] for i in st.session_state['estoque']])
        
        if itens_sel:
            st.write("### 📄 Detalhamento do Recibo")
            total = 0
            for nome_item in itens_sel:
                preco = next(item['Preco'] for item in st.session_state['estoque'] if item['Item'] == nome_item)
                st.write(f"✅ **{nome_item}**: R$ {preco:.2f}")
                total += preco
            st.divider()
            st.markdown(f"## **VALOR TOTAL: R$ {total:.2f}**")
