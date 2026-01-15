import streamlit as st
import pandas as pd
from datetime import datetime

# --- INICIALIZAÇÃO (Mantendo o que já temos) ---
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'clientes' not in st.session_state: st.session_state['clientes'] = []

# --- 2. SESSÃO: CADASTRO DE PETS (ATUALIZADA) ---
if menu == "🐾 Pets":
    st.subheader("🐾 Ficha Técnica do Animal")
    
    if not st.session_state['clientes']:
        st.warning("⚠️ Atenção: Cadastre um Tutor primeiro para poder vincular o Pet.")
    else:
        with st.form("form_pet_detalhado", clear_on_submit=True):
            # Geração automática do código do pet
            id_pet = f"P{len(st.session_state['pets']) + 1:03d}"
            st.info(f"Código do Paciente: **{id_pet}**")
            
            # Vinculação com Tutor existente
            lista_tutores = {f"{c['id']} - {c['nome']}": c['id'] for c in st.session_state['clientes']}
            tutor_vinculo = st.selectbox("Proprietário (Tutor)*", list(lista_tutores.keys()))
            
            nome_pet = st.text_input("Nome do Pet*")
            
            col1, col2, col3 = st.columns(3)
            raca = col1.text_input("Raça")
            sexo = col2.selectbox("Sexo", ["Macho", "Fêmea", "Não informado"])
            idade = col3.text_input("Idade (Ex: 2 anos e 3 meses)")
            
            c1, c2 = st.columns(2)
            castrado = c1.radio("O animal é castrado?", ["Sim", "Não", "Não informado"], horizontal=True)
            vacinado = c2.selectbox("Status de Vacinação", ["Em dia", "Atrasado", "Nunca vacinado"])
            
            historico_vacinas = st.text_area("Vacinas já administradas (Histórico)")
            
            # Botão de Salvar
            salvar_pet = st.form_submit_button("✅ CADASTRAR PACIENTE")
            
            if salvar_pet:
                if nome_pet:
                    st.session_state['pets'].append({
                        "id": id_pet,
                        "tutor_id": lista_tutores[tutor_vinculo],
                        "nome": nome_pet.upper(),
                        "raca": raca,
                        "sexo": sexo,
                        "idade": idade,
                        "castrado": castrado,
                        "vacinado": vacinado,
                        "historico_vacinas": historico_vacinas
                    })
                    st.success(f"Paciente {nome_pet} cadastrado com sucesso!")
                else:
                    st.error("O nome do Pet é obrigatório.")

    # Tabela de Pacientes para conferência
    if st.session_state['pets']:
        st.write("### Pacientes Cadastrados")
        df_pets = pd.DataFrame(st.session_state['pets'])
        # Mostra apenas as colunas principais na tabela para não poluir
        st.table(df_pets[['id', 'nome', 'raca', 'sexo', 'vacinado']])
