import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Banco de Dados de Medicamentos e Vacinas
if 'estoque' not in st.session_state or len(st.session_state['estoque']) < 5:
    st.session_state['estoque'] = [
        {"Item": "Vacina V10 (Importada)", "Preco": 120.00},
        {"Item": "Vacina Antirrábica", "Preco": 60.00},
        {"Item": "Consulta Clínica", "Preco": 150.00},
        {"Item": "Hemograma Completo", "Preco": 95.00},
        {"Item": "Simparic 10-20kg", "Preco": 88.00},
        {"Item": "Castração Macho", "Preco": 350.00},
        {"Item": "Limpeza de Tártaro", "Preco": 280.00},
        {"Item": "Apoquel 5.4mg (Unid)", "Preco": 15.00},
        {"Item": "Vermífugo Drontal", "Preco": 40.00}
    ]

for key in ['clientes', 'pets', 'historico']:
    if key not in st.session_state: st.session_state[key] = []

with st.sidebar:
    st.title("Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "💰 Financeiro"])

# --- CADASTRO DE TUTOR (CPF, E-MAIL, ENDEREÇO) ---
if menu == "👤 Tutores":
    st.subheader("📝 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        nome = st.text_input("Nome do Cliente*")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        zap = c2.text_input("WhatsApp (Ex: 22985020463)*")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({"id": f"T{len(st.session_state['clientes'])+1:03d}", "nome": nome.upper(), "cpf": cpf, "zap": zap, "email": email, "end": end})
                st.success("Tutor salvo!")

# --- CADASTRO DE PET (TODOS OS PARÂMETROS + DATA BR) ---
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            t_lista = {f"{c['id']} - {c['nome']}": c['nome'] for c in st.session_state['clientes']}
            t_sel = st.selectbox("Proprietário*", list(t_lista.keys()))
            nome_p = st.text_input("Nome do Pet*")
            
            c1, c2, c3 = st.columns(3)
            especie = c1.selectbox("Espécie", ["Cão", "Gato", "Outro"])
            raca = c2.text_input("Raça (Ex: Poodle, SRD)")
            sexo = c3.selectbox("Sexo", ["Macho", "Fêmea"])
            
            c4, c5, c6 = st.columns(3)
            porte = c4.selectbox("Porte", ["Mini", "Pequeno", "Médio", "Grande", "Gigante"])
            pelagem = c5.text_input("Cor/Pelagem")
            castrado = c6.radio("Castrado?", ["Sim", "Não"], horizontal=True)
            
            nasc = st.date_input("Data de Nascimento", value=date(2022, 1, 1), format="DD/MM/YYYY")
            hoje = date.today()
            anos = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
            st.info(f"O pet tem {anos} anos.")
            
            if st.form_submit_button("✅ Salvar Pet"):
                if nome_p:
                    st.session_state['pets'].append({"id": f"P{len(st.session_state['pets'])+1:03d}", "nome": nome_p.upper(), "especie": especie, "raca": raca, "sexo": sexo, "idade": f"{anos} anos", "tutor": t_lista[t_sel], "castrado": castrado})
                    st.success("Ficha do Pet cadastrada!")

# --- PRONTUÁRIO (TRANSCRIÇÃO DE VOZ) ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento Clínico (Use Win+H para ditar)")
    if not st.session_state['pets']: st.info("Cadastre um pet.")
    else:
        with st.form("f_ia"):
            p_lista = {p['nome']: p for p in st.session_state['pets']}
            p_sel = st.selectbox("Paciente", list(p_lista.keys()))
            c1, c2 = st.columns(2)
            peso = c1.text_input("Peso (kg)")
            temp = c2.text_input("Temperatura (°C)")
            relato = st.text_area("Relato da Consulta (Clique aqui e fale)", height=200)
            if st.form_submit_button("💾 Salvar Histórico"):
                st.session_state['historico'].append({"Data": date.today().strftime("%d/%m/%Y"), "Pet": p_sel, "Peso": peso, "Relato": relato})
                st.success("Histórico salvo!")

# --- FINANCEIRO (SOMA AUTOMÁTICA E RECIBO) ---
elif menu == "💰 Financeiro":
    st.subheader("💰 Fechamento e Soma de Recibo")
    if not st.session_state['clientes']: st.error("Cadastre um tutor.")
    else:
        t_lista = {c['nome']: c for c in st.session_state['clientes']}
        t_nome = st.selectbox("Tutor para Cobrança", list(t_lista.keys()))
        itens_sel = st.multiselect("Procedimentos e Medicamentos", [i['Item'] for i in st.session_state['estoque']])
        valor_bruto = sum([i['Preco'] for i in st.session_state['estoque'] if i['Item'] in itens_sel])
        st.write(f"### Total a Pagar: R$ {valor_bruto:.2f}")
        if st.button("📲 Gerar e Enviar Recibo WhatsApp"):
            t_zap = t_lista[t_nome]['zap']
            msg = f"Olá {t_nome}, recibo Ribeira Vet: {', '.join(itens_sel)}. Total: R$ {valor_bruto:.2f}."
            link = f"https://wa.me/{t_zap}?text={urllib.parse.quote(msg)}"
            st.markdown(f"#### [Clique aqui para enviar]({link})")

elif menu == "🏠 Dashboard":
    st.metric("Total de Pacientes", len(st.session_state['pets']))
    if st.session_state['historico']: st.table(pd.DataFrame(st.session_state['historico']))
