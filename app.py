import streamlit as st
import uuid
import json
from datetime import datetime, date
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ribeira Vet Pro v7.0", layout="wide", page_icon="🐾")

# --- INICIALIZAÇÃO COMPLETA DO ESTADO ---
chaves_sistema = [
    'tutores', 'pets', 'records', 'estoque_servicos', 
    'financeiro', 'exames', 'procedimentos', 'rascunho'
]
for chave in chaves_sistema:
    if chave not in st.session_state:
        st.session_state[chave] = []

# --- FUNÇÕES DE APOIO ---
def calcular_idade(nasc_str):
    try:
        # Tenta converter a string de data salva
        nasc = datetime.strptime(nasc_str, "%Y-%m-%d").date()
        hoje = date.today()
        idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
        return f"{idade} anos"
    except:
        return "Idade não registrada"

# --- SIDEBAR COMPLETA ---
with st.sidebar:
    st.markdown("## 🐾 Ribeira Vet Pro")
    menu = st.radio("Navegação", [
        "Tutores", "Pacientes", "Prontuário", 
        "Exames & Procedimentos", "Financeiro", 
        "Estoque & Serviços", "Rascunho", "Dados & Backup"
    ])
    st.divider()
    st.info("💡 **Dica de Voz:** Clique no campo e use **Win + H**")
    st.success("Sistema v7.0 Estável 🟢")

# --- 1. TUTORES (Com Endereço Completo) ---
if menu == "Tutores":
    st.header("👤 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome = col1.text_input("NOME COMPLETO *").upper()
        cpf = col2.text_input("CPF *")
        zap = col1.text_input("WhatsApp (com DDD) *")
        mail = col2.text_input("E-mail para Recibo")
        endereco = st.text_input("ENDEREÇO COMPLETO") # Parâmetro recuperado
        
        if st.form_submit_button("SALVAR TUTOR"):
            if nome and zap:
                novo_tutor = {
                    "id": str(uuid.uuid4()), "nome": nome, "cpf": cpf, 
                    "zap": zap, "mail": mail, "endereco": endereco
                }
                st.session_state.tutores.append(novo_tutor)
                st.success(f"Tutor {nome} cadastrado com sucesso!")
            else:
                st.error("Campos Nome e WhatsApp são obrigatórios.")

# --- 2. PACIENTES ---
elif menu == "Pacientes":
    st.header("🐶 Cadastro de Pacientes")
    if not st.session_state.tutores:
        st.warning("⚠️ Cadastre um tutor antes de adicionar um pet.")
    else:
        with st.form("f_pet", clear_on_submit=True):
            t_map = {t['id']: t['nome'] for t in st.session_state.tutores}
            t_id = st.selectbox("Responsável", options=list(t_map.keys()), format_func=lambda x: t_map[x])
            
            c1, c2 = st.columns(2)
            nome_p = c1.text_input("Nome do Pet *").upper()
            raca = c2.text_input("Raça").upper()
            
            # Data de Nascimento com formato BR visual
            nasc = st.date_input("Data de Nascimento (Aniversário)", format="DD/MM/YYYY")
            
            if st.form_submit_button("CADASTRAR PACIENTE"):
                if nome_p:
                    st.session_state.pets.append({
                        "id": str(uuid.uuid4()), "t_id": t_id, 
                        "nome": nome_p, "raca": raca, "nasc": str(nasc)
                    })
                    st.success(f"Paciente {nome_p} registrado!")
                else:
                    st.error("O nome do pet é obrigatório.")

# --- 3. PRONTUÁRIO (Com Verificação de Erro 'KeyError') ---
elif menu == "Prontuário":
    st.header("📝 Atendimento Médico")
    if not st.session_state.pets:
        st.info("Nenhum paciente cadastrado para atendimento.")
    else:
        p_id = st.selectbox("Selecionar Paciente", options=[p['id'] for p in st.session_state.pets], 
                            format_func=lambda x: next(p['nome'] for p in st.session_state.pets if p['id'] == x))
        
        # Busca segura do pet e tutor
        pet = next(p for p in st.session_state.pets if p['id'] == p_id)
        tutor = next(t for t in st.session_state.tutores if t['id'] == pet['t_id'])
        
        # Card de informações usando .get() para evitar KeyError
        idade = calcular_idade(pet.get('nasc', ''))
        st.markdown(f"""
        <div style="background-color: #f0f4f8; padding: 15px; border-radius: 10px; border-left: 5px solid #2b6cb0;">
            <b>PACIENTE:</b> {pet['nome']} ({pet['raca']}) | <b>IDADE:</b> {idade}<br>
            <b>TUTOR:</b> {tutor['nome']} | <b>ZAP:</b> {tutor['zap']}<br>
            <b>ENDEREÇO:</b> {tutor.get('endereco', 'Não informado')}
        </div>
        """, unsafe_allow_html=True)

        anamnese = st.text_area("Anamnese / Sintomas (Dite aqui)", height=150)
        conduta = st.text_area("Conduta / Medicamentos", height=150)
        valor_atendimento = st.number_input("Valor da Consulta R$", min_value=0.0)
        
        if st.button("💾 FINALIZAR ATENDIMENTO"):
            # Salva no histórico
            st.session_state.records.append({
                "p_id": p_id, "data": date.today().strftime("%d/%m/%Y"), 
                "anamnese": anamnese, "conduta": conduta, "valor": valor_atendimento
            })
            # Lança no financeiro automaticamente
            st.session_state.financeiro.append({
                "data": str(date.today()), "item": f"Consulta: {pet['nome']}", 
                "valor": valor_atendimento, "tipo": "Receita"
            })
            st.success("Prontuário gravado e financeiro atualizado!")

# --- 4. EXAMES & PROCEDIMENTOS ---
elif menu == "Exames & Procedimentos":
    st.header("🔬 Exames e Procedimentos")
    tab1, tab2 = st.tabs(["Cadastrar Exame", "Registrar Procedimento"])
    with tab1:
        ex_nome = st.text_input("Nome do Exame")
        ex_res = st.text_area("Resultado/Observação")
        if st.button("Salvar Exame"):
            st.session_state.exames.append({"nome": ex_nome, "obs": ex_res, "data": str(date.today())})
            st.success("Exame protocolado.")
    with tab2:
        proc_nome = st.text_input("Procedimento (ex: Limpeza de Tártaro)")
        if st.button("Salvar Procedimento"):
            st.session_state.procedimentos.append({"nome": proc_nome, "data": str(date.today())})
            st.success("Procedimento registrado.")

# --- 5. FINANCEIRO ---
elif menu == "Financeiro":
    st.header("💰 Controle Financeiro")
    if st.session_state.financeiro:
        df_f = pd.DataFrame(st.session_state.financeiro)
        st.metric("Faturamento Total", f"R$ {df_f['valor'].sum():.2f}")
        st.table(df_f)
    else:
        st.info("Nenhuma movimentação financeira.")

# --- 6. ESTOQUE & SERVIÇOS ---
elif menu == "Estoque & Serviços":
    st.header("📦 Cadastro de Produtos e Serviços")
    with st.form("f_estoque"):
        item = st.text_input("Nome do Produto ou Serviço").upper()
        preco = st.number_input("Preço R$", min_value=0.0)
        if st.form_submit_button("ADICIONAR"):
            st.session_state.estoque_servicos.append({"item": item, "preco": preco})
    st.table(pd.DataFrame(st.session_state.estoque_servicos))

# --- 7. RASCUNHO ---
elif menu == "Rascunho":
    st.header("📓 Bloco de Notas (Rascunhos Rápidos)")
    st.session_state.rascunho = st.text_area("Escreva aqui suas notas...", value=st.session_state.get('rascunho', ""), height=300)

# --- 8. DADOS & BACKUP ---
elif menu == "Dados & Backup":
    st.header("💾 Gerenciar Dados do Computador")
    
    # Prepara o arquivo para baixar no PC
    dados_completos = {k: st.session_state[k] for k in chaves_sistema}
    json_data = json.dumps(dados_completos, indent=4)
    
    st.download_button(
        label="📥 BAIXAR TUDO E SALVAR NO PC",
        data=json_data,
        file_name=f"ribeira_vet_backup_{date.today()}.json",
        mime="application/json"
    )
    
    if st.button("🚨 LIMPAR TUDO (RECOMENDADO PARA ATUALIZAR VERSÃO)"):
        st.session_state.clear()
        st.rerun()
