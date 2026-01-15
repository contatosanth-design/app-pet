import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN PROFISSIONAL (Correção de Contraste) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59 !important; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold; }
    .header-box { background: white; padding: 20px; border-radius: 10px; border-left: 6px solid #2e7bcf; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton>button { background-color: #2e7bcf; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA DO BANCO ---
for key in ['clientes', 'pets', 'historico', 'estoque']:
    if key not in st.session_state: st.session_state[key] = []

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/620/620851.png", width=100)
    st.title("Ribeira Vet Pro")
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Cadastro de Tutores", "🐾 Cadastro de Pets", "🩺 Prontuário IA"])

# --- CABEÇALHO ---
st.markdown(f"<div class='header-box'><h1 style='color:#1e3d59; margin:0;'>Ribeira Vet Pro</h1><p style='margin:0;'>Sistema de Gestão Veterinária • {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- 1. CADASTRO DE TUTORES (TODOS OS PARÂMETROS RESTAURADOS) ---
if menu == "👤 Cadastro de Tutores":
    st.subheader("📝 Ficha Cadastral do Proprietário")
    with st.form("form_tutor_completo", clear_on_submit=True):
        proximo_id = f"T{len(st.session_state['clientes']) + 1:03d}"
        st.info(f"Código Gerado: **{proximo_id}**")
        
        nome = st.text_input("Nome Completo")
        col1, col2 = st.columns(2)
        cpf = col1.text_input("CPF (Somente números)")
        tel = col2.text_input("WhatsApp / Telefone")
        
        email = st.text_input("E-mail para contato")
        endereco = st.text_area("Endereço Completo (Rua, Número, Bairro, Cidade)")
        
        if st.form_submit_button("✅ SALVAR TUTOR"):
            if nome and tel:
                st.session_state['clientes'].append({
                    "id": proximo_id, "nome": nome, "cpf": cpf, 
                    "tel": tel, "email": email, "endereco": endereco
                })
                st.success(f"Tutor {nome} cadastrado com sucesso!")
            else:
                st.error("Campos Nome e Telefone são obrigatórios!")

# --- 2. CADASTRO DE PETS (COM VÍNCULO DE CÓDIGO) ---
elif menu == "🐾 Cadastro de Pets":
    st.subheader("🐶 Registro de Pacientes")
    if not st.session_state['clientes']:
        st.warning("⚠️ Cadastre um tutor antes de registrar um pet.")
    else:
        with st.form("form_pet_vinculo"):
            proximo_id_p = f"P{len(st.session_state['pets']) + 1:03d}"
            st.info(f"Código do Paciente: **{proximo_id_p}**")
            
            opcoes_tutores = {f"{c['id']} - {c['nome']}": c['id'] for c in st.session_state['clientes']}
            tutor_ref = st.selectbox("Selecione o Proprietário Responsável", list(opcoes_tutores.keys()))
            
            nome_pet = st.text_input("Nome do Animal")
            nascimento = st.date_input("Data de Nascimento", format="DD/MM/YYYY")
            raca = st.text_input("Raça / Espécie")
            
            if st.form_submit_button("✅ REGISTRAR PET"):
                st.session_state['pets'].append({
                    "id": proximo_id_p, "nome": nome_pet, "tutor_id": opcoes_tutores[tutor_ref],
                    "tutor_nome": tutor_ref.split(" - ")[1], "nasc": nascimento.strftime("%d/%m/%Y"), "raca": raca
                })
                st.success(f"O pet {nome_pet} foi vinculado ao tutor {tutor_ref}!")

# --- 3. PRONTUÁRIO IA (ARQUIVAMENTO DE RESUMO) ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento com Transcrição")
    if not st.session_state['pets']:
        st.info("Cadastre um pet primeiro para iniciar o atendimento.")
    else:
        with st.form("form_consulta_ia"):
            opcoes_pets = {f"Cód: {p['id']} | Nome: {p['nome']} (Tutor: {p['tutor_id']})": p for p in st.session_state['pets']}
            pet_atendimento = st.selectbox("Identifique o Paciente", list(opcoes_pets.keys()))
            
            st.info("🎤 Dica: Use 'Windows + H' no campo abaixo para transcrever sua voz.")
            resumo = st.text_area("Resumo da Consulta / Diagnóstico / Prescrição", height=250)
            
            if st.form_submit_button("💾 ARQUIVAR NO HISTÓRICO"):
                dados_paciente = opcoes_pets[pet_atendimento]
                st.session_state['historico'].append({
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Cód_Pet": dados_paciente['id'], "Paciente": dados_paciente['nome'],
                    "Cód_Tutor": dados_paciente['tutor_id'], "Tutor": dados_paciente['tutor_nome'],
                    "Relato_IA": resumo
                })
                st.success("Atendimento arquivado! Os dados já estão disponíveis no Dashboard.")

# --- 4. DASHBOARD (HISTÓRICO E EXPORTAÇÃO) ---
elif menu == "🏠 Dashboard":
    st.subheader("📊 Central de Dados e Pesquisa")
    col1, col2 = st.columns(2)
    col1.metric("Tutores Registrados", len(st.session_state['clientes']))
    col2.metric("Pacientes no Sistema", len(st.session_state['pets']))
    
    st.divider()
    if st.session_state['historico']:
        df = pd.DataFrame(st.session_state['historico'])
        st.write("### Histórico Completo de Atendimentos")
        st.dataframe(df, use_container_width=True)
        # Download simples para evitar erro de módulo
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Baixar Arquivo para Pesquisa (Excel/CSV)", data=csv, file_name="ribeira_vet_dados.csv")
    else:
        st.info("Realize um atendimento no Prontuário IA para gerar o arquivo de histórico.")
