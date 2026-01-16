import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Ribeira Vet Pro v7.0", layout="wide")

# BANCO DE DADOS (MEMÓRIA)
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

# MENU LATERAL - Define a variável 'menu' para evitar o NameError
with st.sidebar:
    st.title("Ribeira Vet Pro")
    st.info("Versão 7.0 - Estável")
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "💰 Financeiro"])

# =========================================================
# MÓDULO 0: DASHBOARD (A NOVA CARA DO APP)
# =========================================================
if menu == "🏠 Dashboard":
    st.title("🏥 Bem-vindo ao Ribeira Vet Pro")
    st.write(f"Hoje é dia: **{date.today().strftime('%d/%m/%Y')}**")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Tutores", len(st.session_state['clientes']))
    col2.metric("🐾 Pacientes", len(st.session_state['pets']))
    col3.metric("🩺 Atendimentos", len(st.session_state['historico']))
    
    st.divider()
    
    st.subheader("⚡ Atalhos Rápidos")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("➕ Novo Tutor", use_container_width=True):
            st.info("Clique em '👤 Tutores' no menu lateral")
    with c2:
        if st.button("🐾 Cadastrar Pet", use_container_width=True):
            st.info("Clique em '🐾 Pets' no menu lateral")
    with c3:
        if st.button("💰 Gerar Recibo", use_container_width=True):
            st.info("Clique em '💰 Financeiro' no menu lateral")

    if st.session_state['historico']:
        st.subheader("📅 Últimos Atendimentos")
        st.table(pd.DataFrame(st.session_state['historico']).tail(5))
    else:
        st.info("Nenhum atendimento hoje. A lista aparecerá aqui após usar o Prontuário.")

# =========================================================
# MÓDULO 1: TUTORES
# =========================================================
elif menu == "👤 Tutores":
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
                st.success("Tutor cadastrado!")

# =========================================================
# MÓDULO 2: PETS
# =========================================================
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
            
            nasc = st.date_input("Data de Nascimento", value=date(2020, 1, 1), format="DD/MM/YYYY")
            hoje = date.today()
            idade_real = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
            st.info(f"O paciente tem {idade_real} anos.")
            
            if st.form_submit_button("✅ Salvar Pet"):
                st.session_state['pets'].append({"nome": nome_p.upper(), "raca": raca, "idade": idade_real, "tutor": t_lista[t_sel]})
                st.success("Pet salvo!")

# =========================================================
# MÓDULO 3: PRONTUÁRIO IA
# =========================================================
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento Clínico")
    st.info("💡 Clique no campo 'Relato' e use Win+H para ditar.")
    if st.session_state['pets']:
        p_sel = st.selectbox("Paciente", [p['nome'] for p in st.session_state['pets']])
        relato = st.text_area("Relato da Consulta (Clique aqui e fale)", height=300)
        if st.button("💾 Salvar Atendimento"):
            st.session_state['historico'].append({"Data": date.today().strftime("%d/%m/%Y"), "Pet": p_sel, "Relato": relato})
            st.success("Prontuário salvo!")
    else: st.info("Cadastre um pet.")

# =========================================================
# MÓDULO 4: FINANCEIRO
# =========================================================
elif menu == "💰 Financeiro":
    st.subheader("💰 Fechamento de Conta")
    if st.session_state['clientes']:
        t_nome = st.selectbox("Tutor", [c['nome'] for c in st.session_state['clientes']])
        itens_sel = st.multiselect("Procedimentos", [i['Item'] for i in st.session_state['estoque']])
        if itens_sel:
            total = 0
            for nome_item in itens_sel:
                preco = next(item['Preco'] for item in st.session_state['estoque'] if item['Item'] == nome_item)
                st.write(f"🔹 {nome_item}: **R$ {preco:.2f}**")
                total += preco
            st.divider()
            st.markdown(f"## **TOTAL: R$ {total:.2f}**")
