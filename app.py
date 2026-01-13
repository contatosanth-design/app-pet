import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Veterinário da Ribeira", layout="wide")

# --- CSS PARA DESIGN TÉCNICO E FONTES COMPACTAS ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 13px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .main { background-color: #f0f2f6; }
    .stButton>button { border-radius: 5px; height: 2.5em; background-color: #2e7bcf; color: white; }
    h1 { color: #1e3d59; font-size: 20px !important; margin-bottom: 10px; }
    .stMetric { background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    /* Estilo Planilha */
    .dataframe { font-size: 11px !important; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização do Banco de Dados em Memória
if 'clientes' not in st.session_state: st.session_state['clientes'] = {}
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'proximo_cod_cliente' not in st.session_state: st.session_state['proximo_cod_cliente'] = 1
if 'proximo_cod_pet' not in st.session_state: st.session_state['proximo_cod_pet'] = 1

# --- BARRA LATERAL (LOGOTIPO E MENU) ---
with st.sidebar:
    # Inserindo seu logotipo Squash_pet
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", width=150)
    st.markdown("### 🏥 CONSULTÓRIO DA RIBEIRA")
    st.caption("Gestão Veterinária Profissional")
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["🏠 Início", "👤 Cadastro de Tutores", "🩺 Atendimento / Prontuário", "📋 Banco de Dados (Excel)"])

# --- 🏠 PÁGINA: DASHBOARD ---
if menu == "🏠 Início":
    st.title("📊 Resumo do Consultório")
    col1, col2, col3 = st.columns(3)
    col1.metric("Tutores Cadastrados", len(st.session_state['clientes']))
    col2.metric("Pacientes (Pets)", len(st.session_state['pets']))
    col3.metric("Data de Hoje", datetime.now().strftime("%d/%m/%Y"))

# --- 👤 PÁGINA: CADASTRO DE TUTORES ---
elif menu == "👤 Cadastro de Tutores":
    st.title("📝 Registro de Tutor")
    with st.form("form_tutor"):
        c_id = f"{st.session_state['proximo_cod_cliente']:04d}"
        st.subheader(f"Ficha Nº {c_id}")
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome do Tutor")
        cpf = c2.text_input("CPF / Identidade")
        tel = c1.text_input("WhatsApp / Telefone")
        email = c2.text_input("E-mail para Contato")
        end = st.text_input("Endereço Completo")
        
        if st.form_submit_button("💾 Salvar Registro"):
            if nome and tel:
                st.session_state['clientes'][c_id] = nome
                st.session_state['proximo_cod_cliente'] += 1
                st.success(f"Tutor {nome} cadastrado com sucesso!")
            else: st.error("Nome e Telefone são obrigatórios.")

# --- 🩺 PÁGINA: ATENDIMENTO / PRONTUÁRIO ---
elif menu == "Atendimento / Prontuário":
    st.title("🩺 Ficha de Atendimento Clínico")
    if not st.session_state['clientes']:
        st.warning("⚠️ Cadastre o tutor antes de iniciar o prontuário.")
    else:
        with st.form("form_clinico"):
            p_id = f"{st.session_state['proximo_cod_pet']:04d}"
            
            # Cabeçalho do Atendimento (Inspirado na sua imagem)
            col_h1, col_h2 = st.columns([2, 1])
            opcoes_tutores = [f"{id} - {n}" for id, n in st.session_state['clientes'].items()]
            tutor_ref = col_h1.selectbox("Dono do Animal / Cliente", opcoes_tutores)
            data_atend = col_h2.text_input("Data Entrada", datetime.now().strftime("%d/%m/%Y"))
            
            st.divider()
            
            # Dados do Paciente
            c1, c2, c3 = st.columns(3)
            nome_p = c1.text_input("Nome do Animal")
            especie = c2.selectbox("Espécie", ["Canina", "Felina", "Exóticos", "Outros"])
            raca = c3.text_input("Raça / SRD")
            
            # Análise Clínica (O que você pediu)
            st.markdown("#### 🌡️ Exame Físico e Sinais Vitais")
            v1, v2, v3, v4 = st.columns(4)
            peso = v1.text_input("Peso Atual (kg)")
            temp = v2.text_input("Temperatura (°C)")
            cor = v3.text_input("Cor do Pêlo")
            sexo = v4.selectbox("Sexo", ["Macho", "Fêmea"])
            
            # Idade Personalizada
            v_idade = st.number_input("Idade (Valor)", min_value=0)
            u_idade = st.radio("Unidade", ["Anos", "Meses"], horizontal=True)
            
            # Diagnóstico e Foto
            diag = st.text_area("Anamnese / Aspectos Gerais / Diagnóstico")
            foto = st.file_uploader("📷 Foto do Paciente", type=['jpg', 'jpeg', 'png'])
            
            if st.form_submit_button("✅ Finalizar e Salvar Prontuário"):
                if nome_p:
                    st.session_state['pets'].append({
                        "Cód": p_id, "Tutor": tutor_ref, "Nome": nome_p, "Espécie": especie,
                        "Raça": raca, "Peso": peso, "Temp": temp, "Cor": cor,
                        "Idade": f"{v_idade} {u_idade}", "Diagnóstico": diag, "Foto": foto
                    })
                    st.session_state['proximo_cod_pet'] += 1
                    st.success(f"Atendimento de {nome_p} registrado com sucesso!")
                else: st.error("O nome do animal é obrigatório.")

# --- 📋 PÁGINA: RELATÓRIO (PLANILHA) ---
elif menu == "📋 Banco de Dados (Excel)":
    st.title("📋 Planilha Geral de Atendimentos")
    if not st.session_state['pets']:
        st.info("Nenhum dado registrado para exibição.")
    else:
        # Layout de Tabela Compacta
        st.markdown("---")
        # Cabeçalho
        h_cols = st.columns([1, 1, 2, 2, 1, 1, 1, 3, 1])
        headers = ["FOTO", "CÓD", "PACIENTE", "TUTOR", "RAÇA", "PESO", "TEMP", "DIAGNÓSTICO", "AÇÃO"]
        for i, h in enumerate(headers): h_cols[i].markdown(f"**{h}**")
        
        # Linhas da Planilha
        for p in st.session_state['pets']:
            row = st.columns([1, 1, 2, 2, 1, 1, 1, 3, 1])
            
            # Foto Miniatura
            if p['Foto']: row[0].image(p['Foto'], width=50)
            else: row[0].write("🚫")
            
            row[1].write(p['Cód'])
            row[2].write(p['Nome'])
            row[3].write(p['Tutor'])
            row[4].write(p['Raça'])
            row[5].write(p['Peso'])
            row[6].write(p['Temp'])
            row[7].write(p['Diagnóstico'][:50] + "..." if len(p['Diagnóstico']) > 50 else p['Diagnóstico'])
            row[8].button("🔍", key=p['Cód'])
