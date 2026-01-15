import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# 1. Configuração de Estabilidade
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# 2. Banco de Dados e Carga Automática de Medicamentos/Vacinas
if 'estoque' not in st.session_state or len(st.session_state['estoque']) <= 3:
    st.session_state['estoque'] = [
        {"Item": "Vacina V10 (Importada)", "Preco": 120.00},
        {"Item": "Vacina Antirrábica", "Preco": 60.00},
        {"Item": "Vacina Gripe (KC)", "Preco": 95.00},
        {"Item": "Apoquel 5.4mg (Unid)", "Preco": 12.00},
        {"Item": "Simparic 10-20kg", "Preco": 85.00},
        {"Item": "Drontal Plus (Cão)", "Preco": 35.00},
        {"Item": "Meloxivet 1mg", "Preco": 45.00},
        {"Item": "Gaviz V 10mg", "Preco": 52.00},
        {"Item": "Consulta Clínica", "Preco": 150.00},
        {"Item": "Hemograma Completo", "Preco": 90.00}
    ]

for key in ['clientes', 'pets', 'historico']:
    if key not in st.session_state: st.session_state[key] = []

# 3. Menu Lateral (Proteção contra tela em branco)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=70)
    st.title("Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "💰 Financeiro"])

# --- SESSÃO 1: TUTORES (COM E-MAIL E ENDEREÇO COMPLETO) ---
if menu == "👤 Tutores":
    st.subheader("📝 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        id_t = f"T{len(st.session_state['clientes']) + 1:03d}"
        nome = st.text_input("Nome do Cliente*")
        c1, c2 = st.columns(2)
        zap = c1.text_input("WhatsApp (Ex: 22985020463)*")
        email = c2.text_input("E-mail para Contato")
        endereco = st.text_area("Endereço Completo (Rua, Nº, Bairro)")
        
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({
                    "id": id_t, "nome": nome.upper(), "zap": zap, 
                    "email": email, "endereco": endereco
                })
                st.success(f"Tutor {nome} cadastrado com sucesso!")

# --- SESSÃO 2: PETS (COM DATA E CÁLCULO DE ANOS) ---
elif menu == "🐾 Pets":
    st.subheader("🐾 Ficha do Paciente")
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor antes de registrar o pet.")
    else:
        with st.form("f_pet"):
            t_lista = {f"{c['id']} - {c['nome']}": c for c in st.session_state['clientes']}
            t_sel = st.selectbox("Proprietário", list(t_lista.keys()))
            nome_p = st.text_input("Nome do Animal*")
            
            c1, c2 = st.columns(2)
            data_nasc = c1.date_input("Data de Nascimento", value=date(2022, 1, 1))
            
            # Cálculo Automático de Idade
            hoje = date.today()
            idade_anos = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
            c2.info(f"Idade Detectada: {idade_anos} anos")
            
            raca = st.selectbox("Raça", ["SRD", "Spitz Alemão", "Poodle", "Shih Tzu", "Bulldog", "Outra"])
            sexo = st.radio("Sexo", ["Macho", "Fêmea"], horizontal=True)
            
            if st.form_submit_button("✅ Finalizar Cadastro"):
                st.session_state['pets'].append({
                    "id": f"P{len(st.session_state['pets'])+1:03d}", "nome": nome_p.upper(),
                    "idade": f"{idade_anos} anos", "tutor": t_lista[t_sel]['nome'],
                    "raca": raca, "sexo": sexo
                })
                st.success(f"Pet {nome_p} registrado!")

# --- SESSÃO 3: PRONTUÁRIO (ESTATÍSTICAS) ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Prontuário de Atendimento")
    if not st.session_state['pets']:
        st.info("Nenhum pet cadastrado.")
    else:
        with st.form("f_clin"):
            p_lista = {p['nome']: p for p in st.session_state['pets']}
            pet_atend = st.selectbox("Selecione o Paciente", list(p_lista.keys()))
            
            col1, col2, col3 = st.columns(3)
            peso = col1.text_input("Peso (kg)")
            temp = col2.text_input("Temp (°C)")
            f_card = col3.text_input("F. Cardíaca")
            
            relato = st.text_area("Relato Clínico / Anamnese", height=150)
            
            if st.form_submit_button("💾 Salvar Consulta"):
                st.session_state['historico'].append({
                    "Data": date.today().strftime("%d/%m/%Y"),
                    "Pet": pet_atend, "Peso": peso, "Relato": relato
                })
                st.success("Consulta arquivada!")

# --- SESSÃO 4: FINANCEIRO (LISTA DE MEDICAMENTOS) ---
elif menu == "💰 Financeiro":
    st.subheader("💰 Fechamento e Recibo")
    if not st.session_state['clientes']:
        st.error("Cadastre um tutor para cobrar.")
    else:
        with st.form("f_pag"):
            t_lista = {c['nome']: c for c in st.session_state['clientes']}
            t_nome = st.selectbox("Tutor para Cobrança", list(t_lista.keys()))
            servicos = st.multiselect("Itens (Medicamentos/Vacinas)", [i['Item'] for i in st.session_state['estoque']])
            
            if st.form_submit_button("📄 Gerar Recibo WhatsApp"):
                t_info = t_lista[t_nome]
                valor_total = sum([i['Preco'] for i in st.session_state['estoque'] if i['Item'] in servicos])
                texto = f"Olá {t_nome}, recibo da Ribeira Vet: {', '.join(servicos)}. Total: R$ {valor_total:.2f}"
                st.markdown(f"[📲 Enviar WhatsApp](https://wa.me/{t_info['zap']}?text={urllib.parse.quote(texto)})")

# --- DASHBOARD ---
elif menu == "🏠 Dashboard":
    st.title("📊 Painel de Controle")
    c1, c2 = st.columns(2)
    c1.metric("Tutores", len(st.session_state['clientes']))
    c2.metric("Pacientes", len(st.session_state['pets']))
    if st.session_state['historico']:
        st.write("### Histórico Recente")
        st.table(pd.DataFrame(st.session_state['historico']))
