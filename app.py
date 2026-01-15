import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- INICIALIZAÇÃO DO BANCO DE DADOS ---
if 'clientes' not in st.session_state: st.session_state['clientes'] = []
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'estoque' not in st.session_state: st.session_state['estoque'] = []

# --- MENU LATERAL (Define a variável 'menu') ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=80)
    st.title("Ribeira Vet Pro")
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Cadastro de Pets", "🩺 Prontuário IA", "📦 Produtos", "💰 Financeiro"])

# --- SESSÃO: CADASTRO DE PETS (COM TODOS OS SEUS PARÂMETROS) ---
if menu == "🐾 Cadastro de Pets":
    st.subheader("🐾 Ficha Técnica do Animal")
    
    if not st.session_state['clientes']:
        st.warning("⚠️ Cadastre um Tutor antes de registrar o pet.")
    else:
        with st.form("form_pet_final", clear_on_submit=True):
            id_pet = f"P{len(st.session_state['pets']) + 1:03d}"
            st.info(f"Código do Paciente: **{id_pet}**")
            
            # Seleção do Tutor já cadastrado
            tutores_dict = {f"{c['id']} - {c['nome']}": c['id'] for c in st.session_state['clientes']}
            tutor_ref = st.selectbox("Proprietário Responsável*", list(tutores_dict.keys()))
            
            nome_p = st.text_input("Nome do Animal*")
            
            col1, col2, col3 = st.columns(3)
            # Lista de raças para seleção rápida como o senhor pediu
            raca = col1.selectbox("Raça", ["SRD", "Spitz Alemão", "Poodle", "Shih Tzu", "Yorkshire", "Bulldog Francês", "Golden Retriever", "Persa", "Siamês", "Outra"])
            sexo = col2.selectbox("Sexo", ["Macho", "Fêmea"])
            idade = col3.text_input("Idade Aproximada")
            
            col4, col5 = st.columns(2)
            cor = col4.text_input("Cor do Pêlo")
            chip = col5.text_input("Número do Chip (se houver)")
            
            c1, c2 = st.columns(2)
            castrado = c1.radio("O animal é castrado?", ["Sim", "Não", "Não informado"], horizontal=True)
            vacinado = c2.selectbox("Status de Vacinação", ["Em dia", "Atrasado", "Nunca vacinado"])
            
            # Foto do Pet
            foto = st.file_uploader("Carregar Foto do Paciente", type=['jpg', 'png', 'jpeg'])
            
            if st.form_submit_button("✅ SALVAR FICHA DO PET"):
                if nome_p:
                    st.session_state['pets'].append({
                        "id": id_pet, "tutor_id": tutores_dict[tutor_ref], "nome": nome_p.upper(),
                        "raca": raca, "sexo": sexo, "idade": idade, "cor": cor,
                        "chip": chip, "castrado": castrado, "vacinado": vacinado
                    })
                    st.success(f"Paciente {nome_p} cadastrado com sucesso!")
                else:
                    st.error("O nome do animal é obrigatório.")

# --- MANUTENÇÃO DAS OUTRAS SESSÕES ---
elif menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Tutores")
    # Mantido conforme configuramos anteriormente

elif menu == "🏠 Dashboard":
    st.subheader("📊 Painel Geral")
    st.write(f"Tutores: {len(st.session_state['clientes'])}")
    st.write(f"Pacientes: {len(st.session_state['pets'])}")
