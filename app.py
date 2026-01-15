import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Banco de Dados de Preços
if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [
        {"Item": "Vacina V10 (Importada)", "Preco": 120.00},
        {"Item": "Vacina Antirrábica", "Preco": 60.00},
        {"Item": "Consulta Clínica", "Preco": 150.00},
        {"Item": "Hemograma Completo", "Preco": 95.00},
        {"Item": "Castração Macho", "Preco": 350.00}
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
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({"id": f"T{len(st.session_state['clientes'])+1:03d}", "nome": nome.upper(), "cpf": cpf, "zap": zap, "end": end})
                st.success("Tutor salvo!")

# --- PETS (IDADE DINÂMICA E RAÇAS) ---
elif menu == "🐾 Pets":
    st.subheader("🐾 Ficha do Paciente")
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            t_lista = {f"{c['id']} - {c['nome']}": c['nome'] for c in st.session_state['clientes']}
            t_sel = st.selectbox("Proprietário*", list(t_lista.keys()))
            nome_p = st.text_input("Nome do Pet*")
            
            c1, c2, c3 = st.columns(3)
            especie = c1.selectbox("Espécie", ["Cão", "Gato", "Outro"])
            raca = c2.selectbox("Raça", ["SRD", "Pinscher", "Poodle", "Shih Tzu", "Pitbull", "Outra"])
            sexo = c3.selectbox("Sexo", ["Macho", "Fêmea"])
            
            # Cálculo de Idade Automático na Mudança da Data
            nasc = st.date_input("Data de Nascimento", value=date(2020, 1, 1), format="DD/MM/YYYY")
            hoje = date.today()
            anos = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
            st.info(f"O paciente tem {anos} anos.")
            
            if st.form_submit_button("✅ Salvar Pet"):
                st.session_state['pets'].append({"nome": nome_p.upper(), "raca": raca, "idade": anos, "tutor": t_lista[t_sel]})
                st.success("Pet cadastrado!")

# --- PRONTUÁRIO (VOZ) ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento (Use Win+H para ditar)")
    if not st.session_state['pets']: st.info("Cadastre um pet.")
    else:
        with st.form("f_ia"):
            p_sel = st.selectbox("Paciente", [p['nome'] for p in st.session_state['pets']])
            relato = st.text_area("Relato da Consulta (Clique aqui e fale)", height=200)
            if st.form_submit_button("💾 Salvar Histórico"):
                st.session_state['historico'].append({"Data": date.today().strftime("%d/%m/%Y"), "Pet": p_sel, "Relato": relato})
                st.success("Salvo!")

# --- FINANCEIRO (RECIBO VISÍVEL) ---
elif menu == "💰 Financeiro":
    st.subheader("💰 Fechamento de Conta")
    if st.session_state['clientes']:
        t_nome = st.selectbox("Tutor", [c['nome'] for c in st.session_state['clientes']])
        itens_sel = st.multiselect("Procedimentos", [i['Item'] for i in st.session_state['estoque']])
        
        if itens_sel:
            st.write("### 📄 Detalhamento do Recibo")
            total = 0
            for nome_item in itens_sel:
                preco = next(item['Preco'] for item in st.session_state['estoque'] if item['Item'] == nome_item)
                st.write(f"🔹 {nome_item}: **R$ {preco:.2f}**")
                total += preco
            st.divider()
            st.markdown(f"## **VALOR TOTAL: R$ {total:.2f}**")

elif menu == "🏠 Dashboard":
    st.metric("Pacientes", len(st.session_state['pets']))
    if st.session_state['historico']: st.table(pd.DataFrame(st.session_state['historico']))
