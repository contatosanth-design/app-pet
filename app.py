import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# 1. Configuração de Página e Identidade
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# 2. Banco de Dados em Memória (Estoque e Listas)
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

# 3. Menu Lateral de Navegação
with st.sidebar:
    st.title("Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "💰 Financeiro"])

# --- SESSÃO 1: TUTORES (DADOS COMPLETOS) ---
if menu == "👤 Tutores":
    st.subheader("📝 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        nome = st.text_input("Nome do Cliente*")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        zap = c2.text_input("WhatsApp (Somente Números)*")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({
                    "id": f"T{len(st.session_state['clientes'])+1:03d}", 
                    "nome": nome.upper(), "cpf": cpf, "zap": zap, 
                    "email": email, "end": end
                })
                st.success("Tutor cadastrado com sucesso!")

# --- SESSÃO 2: PETS (FICHA TÉCNICA DETALHADA) ---
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
            raca = c2.text_input("Raça")
            sexo = c3.selectbox("Sexo", ["Macho", "Fêmea"])
            
            c4, c5 = st.columns(2)
            porte = c4.selectbox("Porte", ["Mini", "Pequeno", "Médio", "Grande", "Gigante"])
            castrado = c5.radio("Castrado?", ["Sim", "Não"], horizontal=True)
            
            nasc = st.date_input("Data de Nascimento", value=date(2022, 1, 1), format="DD/MM/YYYY")
            hoje = date.today()
            anos = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
            st.info(f"O paciente tem {anos} anos.")
            
            if st.form_submit_button("✅ Salvar Pet"):
                if nome_p:
                    st.session_state['pets'].append({
                        "nome": nome_p.upper(), "especie": especie, "raca": raca, 
                        "sexo": sexo, "idade": f"{anos} anos", "tutor": t_lista[t_sel], 
                        "castrado": castrado
                    })
                    st.success("Paciente registrado!")

# --- SESSÃO 3: PRONTUÁRIO (TRANSCRIÇÃO DE VOZ) ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento Clínico")
    st.info("💡 Clique no campo de texto e use Win+H para ditar o atendimento.")
    if not st.session_state['pets']:
        st.info("Nenhum pet cadastrado.")
    else:
        with st.form("f_pront"):
            p_sel = st.selectbox("Selecione o Paciente", [p['nome'] for p in st.session_state['pets']])
            c1, c2 = st.columns(2)
            peso = c1.text_input("Peso (kg)")
            temp = c2.text_input("Temperatura (°C)")
            relato = st.text_area("Evolução Clínica / Anamnese", height=250)
            if st.form_submit_button("💾 Salvar Consulta"):
                st.session_state['historico'].append({
                    "Data": date.today().strftime("%d/%m/%Y"), 
                    "Pet": p_sel, "Peso": peso, "Relato": relato
                })
                st.success("Prontuário arquivado!")

# --- SESSÃO 4: FINANCEIRO (RECIBO EM LISTA) ---
elif menu == "💰 Financeiro":
    st.subheader("💰 Fechamento de Conta")
    if not st.session_state['clientes']:
        st.error("Nenhum cliente cadastrado.")
    else:
        t_lista = {c['nome']: c for c in st.session_state['clientes']}
        t_nome = st.selectbox("Selecione o Tutor", list(t_lista.keys()))
        itens_sel = st.multiselect("Procedimentos e Medicamentos", [i['Item'] for i in st.session_state['estoque']])
        
        if itens_sel:
            st.markdown("### 📄 Detalhamento do Recibo")
            total = 0
            resumo_texto = ""
            for nome_item in itens_sel:
                preco = next(item['Preco'] for item in st.session_state['estoque'] if item['Item'] == nome_item)
                st.write(f"🔹 {nome_item}: **R$ {preco:.2f}**")
                total += preco
                resumo_texto += f"- {nome_item}: R$ {preco:.2f}\n"
            
            st.divider()
            st.markdown(f"## **VALOR TOTAL: R$ {total:.2f}**")
            
            if st.button("📲 Gerar Recibo WhatsApp"):
                zap = t_lista[t_nome]['zap']
                msg = f"Olá {t_nome}, recibo da Ribeira Vet:\n\n{resumo_texto}\n*Total Final: R$ {total:.2f}*"
                link = f"https://wa.me/{zap}?text={urllib.parse.quote(msg)}"
                st.markdown(f"#### [Clique aqui para enviar o Recibo]({link})")

# --- DASHBOARD ---
elif menu == "🏠 Dashboard":
    st.title("📊 Painel de Controle")
    c1, c2 = st.columns(2)
    c1.metric("Tutores Cadastrados", len(st.session_state['clientes']))
    c2.metric("Pacientes Ativos", len(st.session_state['pets']))
    if st.session_state['historico']:
        st.write("### Histórico Recente")
        st.table(pd.DataFrame(st.session_state['historico']))
