import streamlit as st
import uuid
import json
from datetime import datetime, date
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ribeira Vet Pro v7.0", layout="wide", page_icon="🐾")

# --- INICIALIZAÇÃO DO ESTADO ---
chaves = ['tutores', 'pets', 'records', 'estoque', 'financeiro', 'exames', 'procedimentos']
for chave in chaves:
    if chave not in st.session_state:
        st.session_state[chave] = []

# --- FUNÇÕES AUXILIARES ---
def calcular_idade(nasc_str):
    try:
        nasc = datetime.strptime(nasc_str, "%Y-%m-%d").date()
        return f"{date.today().year - nasc.year} anos"
    except: return "N/A"

# --- SIDEBAR EVOLUÍDA ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("Navegação", [
        "Tutores", "Pacientes", "Prontuário", 
        "Exames & Procedimentos", "Financeiro", 
        "Estoque & Serviços", "Rascunho", "Dados & Backup"
    ])
    st.divider()
    st.success("Ditado de Voz Ativo (Win + H) 🟢")

# --- 1. TUTORES ---
if menu == "Tutores":
    st.header("👤 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        c1, c2 = st.columns(2)
        nome = c1.text_input("NOME COMPLETO *").upper()
        cpf = c2.text_input("CPF *")
        zap = c1.text_input("WhatsApp *")
        mail = c2.text_input("E-mail")
        if st.form_submit_button("SALVAR"):
            st.session_state.tutores.append({"id": str(uuid.uuid4()), "nome": nome, "cpf": cpf, "zap": zap, "mail": mail})
            st.success("Tutor salvo!")

# --- 2. PACIENTES ---
elif menu == "Pacientes":
    st.header("🐶 Cadastro de Pacientes")
    if not st.session_state.tutores: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            t_map = {t['id']: t['nome'] for t in st.session_state.tutores}
            t_id = st.selectbox("Responsável", options=list(t_map.keys()), format_func=lambda x: t_map[x])
            c1, c2 = st.columns(2)
            nome_p = c1.text_input("Nome do Pet").upper()
            raca = c2.text_input("Raça").upper()
            nasc = st.date_input("Data de Nascimento", format="DD/MM/YYYY")
            if st.form_submit_button("CADASTRAR"):
                st.session_state.pets.append({"id": str(uuid.uuid4()), "t_id": t_id, "nome": nome_p, "raca": raca, "nasc": str(nasc)})
                st.success("Pet cadastrado!")

# --- 3. PRONTUÁRIO (Com foco para Voz) ---
elif menu == "Prontuário":
    st.header("📝 Atendimento (Dite com Win + H)")
    if not st.session_state.pets: st.info("Sem pacientes.")
    else:
        p_id = st.selectbox("Pet", options=[p['id'] for p in st.session_state.pets], format_func=lambda x: next(p['nome'] for p in st.session_state.pets if p['id'] == x))
        pet = next(p for p in st.session_state.pets if p['id'] == p_id)
        
        st.subheader(f"🐾 Atendendo: {pet['nome']} ({calcular_idade(pet['nasc'])})")
        
        anamnese = st.text_area("Anamnese / Sintomas (Clique aqui antes de Win+H)", height=150)
        conduta = st.text_area("Conduta / Prescrição", height=150)
        valor = st.number_input("Valor da Consulta R$", min_value=0.0)
        
        if st.button("💾 GRAVAR PRONTUÁRIO"):
            st.session_state.records.append({"p_id": p_id, "data": date.today().strftime("%d/%m/%Y"), "anamnese": anamnese, "conduta": conduta, "valor": valor})
            st.session_state.financeiro.append({"data": str(date.today()), "desc": f"Consulta: {pet['nome']}", "valor": valor, "tipo": "Receita"})
            st.success("Gravado e enviado ao Financeiro!")

# --- 4. EXAMES & PROCEDIMENTOS ---
elif menu == "Exames & Procedimentos":
    st.header("🔬 Exames e Procedimentos")
    tab1, tab2 = st.tabs(["Solicitar Exame", "Registrar Procedimento"])
    with tab1:
        exame = st.text_input("Nome do Exame")
        laboratorio = st.text_input("Laboratório")
        if st.button("Protocolar Exame"):
            st.session_state.exames.append({"item": exame, "lab": laboratorio, "status": "Solicitado"})
    with tab2:
        proc = st.text_input("Procedimento Realizado (ex: Castração)")
        if st.button("Registrar Procedimento"):
            st.session_state.procedimentos.append({"proc": proc, "data": str(date.today())})

# --- 5. FINANCEIRO ---
elif menu == "Financeiro":
    st.header("💰 Gestão Financeira")
    df_fin = pd.DataFrame(st.session_state.financeiro)
    if not df_fin.empty:
        st.metric("Receita Total", f"R$ {df_fin[df_fin['tipo']=='Receita']['valor'].sum():.2f}")
        st.table(df_fin)
    else: st.info("Nenhuma movimentação.")

# --- 6. ESTOQUE & SERVIÇOS ---
elif menu == "Estoque & Serviços":
    st.header("📦 Produtos e Serviços")
    with st.form("f_estoque"):
        item = st.text_input("Produto/Serviço").upper()
        preco = st.number_input("Preço de Venda R$", min_value=0.0)
        if st.form_submit_button("CADASTRAR"):
            st.session_state.estoque.append({"item": item, "preco": preco})
    st.table(st.session_state.estoque)

# --- 7. RASCUNHO ---
elif menu == "Rascunho":
    st.header("📓 Bloco de Notas Rápido")
    notas = st.text_area("Notas temporárias...", height=400)
    st.info("As notas ficam salvas apenas nesta sessão.")

# --- 8. DADOS & BACKUP ---
elif menu == "Dados & Backup":
    st.header("💾 Backup")
    data_export = {k: st.session_state[k] for k in chaves}
    st.download_button("📥 BAIXAR TUDO (SAVE NO PC)", data=json.dumps(data_export, indent=4), file_name=f"vet_backup_{date.today()}.json")
