import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Banco de Dados de Preços
if 'estoque' not in st.session_state or len(st.session_state['estoque']) < 5:
    st.session_state['estoque'] = [
        {"Item": "Vacina V10 (Importada)", "Preco": 120.00},
        {"Item": "Vacina Antirrábica", "Preco": 60.00},
        {"Item": "Consulta Clínica", "Preco": 150.00},
        {"Item": "Hemograma Completo", "Preco": 95.00},
        {"Item": "Simparic 10-20kg", "Preco": 88.00},
        {"Item": "Castração Macho", "Preco": 350.00},
        {"Item": "Limpeza de Tártaro", "Preco": 280.00}
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
        nome = st.text_input("Nome do Cliente*")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        zap = c2.text_input("WhatsApp*")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({"id": f"T{len(st.session_state['clientes'])+1:03d}", "nome": nome.upper(), "cpf": cpf, "zap": zap, "email": email, "end": end})
                st.success("Tutor salvo!")

# --- PETS (PARÂMETROS COMPLETOS) ---
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
            raca = c2.text_input("Raça")
            sexo = c3.selectbox("Sexo", ["Macho", "Fêmea"])
            c4, c5 = st.columns(2)
            porte = c4.selectbox("Porte", ["Mini", "Pequeno", "Médio", "Grande"])
            castrado = c5.radio("Castrado?", ["Sim", "Não"], horizontal=True)
            nasc = st.date_input("Data de Nascimento", value=date(2022, 1, 1), format="DD/MM/YYYY")
            hoje = date.today()
            anos = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
            st.info(f"Idade: {anos} anos")
            if st.form_submit_button("✅ Salvar Pet"):
                st.session_state['pets'].append({"nome": nome_p.upper(), "especie": especie, "raca": raca, "sexo": sexo, "idade": anos, "tutor": t_lista[t_sel], "castrado": castrado})
                st.success("Pet cadastrado!")

# --- PRONTUÁRIO ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento (Win+H para ditar)")
    if not st.session_state['pets']: st.info("Cadastre um pet.")
    else:
        with st.form("f_ia"):
            p_sel = st.selectbox("Paciente", [p['nome'] for p in st.session_state['pets']])
            relato = st.text_area("Relato da Consulta", height=200)
            if st.form_submit_button("💾 Salvar Histórico"):
                st.session_state['historico'].append({"Data": date.today().strftime("%d/%m/%Y"), "Pet": p_sel, "Relato": relato})
                st.success("Salvo!")

# --- FINANCEIRO (ESTILO RECIBO LISTADO) ---
elif menu == "💰 Financeiro":
    st.subheader("💰 Fechamento de Recibo")
    if not st.session_state['clientes']: st.error("Cadastre um tutor.")
    else:
        t_lista = {c['nome']: c for c in st.session_state['clientes']}
        t_nome = st.selectbox("Tutor para Cobrança", list(t_lista.keys()))
        itens_sel = st.multiselect("Selecione os Procedimentos", [i['Item'] for i in st.session_state['estoque']])
        
        if itens_sel:
            st.write("---")
            st.write("### 📄 Itens do Recibo")
            total = 0
            resumo_msg = ""
            for nome_item in itens_sel:
                # Busca o preço de cada item selecionado
                preco = next(item['Preco'] for item in st.session_state['estoque'] if item['Item'] == nome_item)
                st.write(f"✅ {nome_item} : **R$ {preco:.2f}**")
                total += preco
                resumo_msg += f"- {nome_item}: R$ {preco:.2f}\n"
            
            st.write("---")
            st.markdown(f"## **TOTAL: R$ {total:.2f}**")
            
            if st.button("📲 Enviar Recibo por WhatsApp"):
                t_zap = t_lista[t_nome]['zap']
                msg_final = f"Olá {t_nome}, segue seu recibo da Ribeira Vet:\n\n{resumo_msg}\n*Total: R$ {total:.2f}*"
                link = f"https://wa.me/{t_zap}?text={urllib.parse.quote(msg_final)}"
                st.markdown(f"#### [Clique aqui para enviar o WhatsApp]({link})")
        else:
            st.info("Selecione um ou mais procedimentos acima para gerar o recibo.")

elif menu == "🏠 Dashboard":
    st.metric("Pacientes", len(st.session_state['pets']))
    if st.session_state['historico']: st.table(pd.DataFrame(st.session_state['historico']))
