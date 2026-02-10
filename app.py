import streamlit as st
import uuid
import json
from datetime import datetime, date
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ribeira Vet Pro v7.0", layout="wide", page_icon="🐾")

# --- INICIALIZAÇÃO DO ESTADO ---
chaves_sistema = ['tutores', 'pets', 'records', 'estoque', 'financeiro']
for chave in chaves_sistema:
    if chave not in st.session_state:
        st.session_state[chave] = []

# --- LISTA DE RAÇAS COMUNS (Versão 2.0 Recuperada) ---
RACAS_COMUNS = [
    "SRD (Vira-lata)", "Shih Tzu", "Poodle", "Pinscher", "Golden Retriever", 
    "Bulldog Francês", "Yorkshire", "Lhasa Apso", "Pit Bull", "Beagle",
    "Persa", "Siamês", "Maine Coon", "Angorá", "Bengal", "Outra"
]

# --- FUNÇÕES DE APOIO ---
def calcular_idade_seguro(nasc_str):
    if not nasc_str: return "N/D"
    try:
        nasc = datetime.strptime(nasc_str, "%Y-%m-%d").date()
        hoje = date.today()
        return f"{hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))} anos"
    except: return "N/D"

# --- SIDEBAR ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("Navegação", ["Tutores", "Pacientes", "Prontuário", "Financeiro", "Dados"])
    st.divider()
    st.success("Ditado de Voz Ativo (Win + H) 🟢")

# --- 1. TUTORES (Com Endereço Completo) ---
if menu == "Tutores":
    st.header("👤 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        c1, c2 = st.columns(2)
        nome = c1.text_input("NOME COMPLETO *").upper()
        cpf = c2.text_input("CPF *")
        zap = c1.text_input("WhatsApp (DDD + Número) *")
        end = st.text_input("ENDEREÇO COMPLETO")
        if st.form_submit_button("SALVAR TUTOR"):
            if nome and zap:
                st.session_state.tutores.append({"id": str(uuid.uuid4()), "nome": nome, "zap": zap, "end": end})
                st.success("Tutor cadastrado!")

# --- 2. PACIENTES (Diferenciação por Raça e Idade) ---
elif menu == "Pacientes":
    st.header("🐶 Cadastro de Pacientes")
    if not st.session_state.tutores:
        st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet", clear_on_submit=True):
            t_map = {t['id']: t['nome'] for t in st.session_state.tutores}
            t_id = st.selectbox("Responsável", options=list(t_map.keys()), format_func=lambda x: t_map[x])
            
            c1, c2 = st.columns(2)
            nome_p = c1.text_input("NOME DO PET *").upper()
            raca = c2.selectbox("RAÇA", options=RACAS_COMUNS)
            
            if raca == "Outra":
                raca_especifica = st.text_input("Especifique a Raça").upper()
                raca = raca_especifica if raca_especifica else "OUTRA"

            nasc = st.date_input("DATA DE NASCIMENTO", format="DD/MM/YYYY")
            
            if st.form_submit_button("CADASTRAR PET"):
                if nome_p:
                    st.session_state.pets.append({
                        "id": str(uuid.uuid4()), "t_id": t_id, 
                        "nome": nome_p, "raca": raca, "nasc": str(nasc)
                    })
                    st.success(f"{nome_p} ({raca}) cadastrado!")

# --- 3. PRONTUÁRIO (Seleção Inteligente) ---
elif menu == "Prontuário":
    st.header("📝 Atendimento Médico")
    if not st.session_state.pets:
        st.info("Nenhum pet cadastrado.")
    else:
        # Aqui resolvemos o problema de nomes iguais: mostramos Nome + Raça + Idade no seletor
        def formatar_pet_seletor(p_id):
            p = next(pet for pet in st.session_state.pets if pet['id'] == p_id)
            idade = calcular_idade_seguro(p['nasc'])
            return f"{p['nome']} - {p['raca']} ({idade})"

        pet_id = st.selectbox("SELECIONE O PACIENTE", 
                             options=[p['id'] for p in st.session_state.pets],
                             format_func=formatar_pet_seletor)
        
        pet = next(p for p in st.session_state.pets if p['id'] == pet_id)
        tutor = next(t for t in st.session_state.tutores if t['id'] == pet['t_id'])

        st.info(f"📋 **Paciente:** {pet['nome']} | **Tutor:** {tutor['nome']} | **Endereço:** {tutor.get('end', 'N/D')}")

        with st.form("f_consulta"):
            anamnese = st.text_area("Sintomas (Win + H para ditar)")
            conduta = st.text_area("Conduta e Receituário")
            valor = st.number_input("Valor da Consulta R$", min_value=0.0)
            if st.form_submit_button("SALVAR ATENDIMENTO"):
                st.session_state.records.append({
                    "p_id": pet_id, "data": date.today().strftime("%d/%m/%Y"), 
                    "anamnese": anamnese, "conduta": conduta
                })
                st.session_state.financeiro.append({"data": str(date.today()), "item": f"Consulta: {pet['nome']}", "valor": valor})
                st.success("Gravado!")

# --- 4. DADOS E BACKUP ---
elif menu == "Dados":
    st.header("💾 Salvar no Computador")
    dados_completos = {k: st.session_state[k] for k in chaves_sistema}
    st.download_button("📥 BAIXAR BACKUP COMPLETO", 
                      data=json.dumps(dados_completos, indent=4), 
                      file_name=f"vet_backup_{date.today()}.json")
    
    if st.button("🚨 LIMPAR TUDO (PARA NOVA VERSÃO)"):
        st.session_state.clear()
        st.rerun()
