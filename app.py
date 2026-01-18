import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

# 2. MENU
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"])

# 3. MÓDULO 1: TUTORES (COM ORDEM ALFABÉTICA)
if menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    
    # Organiza a lista de nomes em ordem alfabética para a busca
    nomes_ordenados = sorted([c['NOME'] for c in st.session_state['clientes']])
    escolha = st.selectbox("⚡ Selecionar Tutor ou Criar Novo:", ["--- Novo Cadastro ---"] + nomes_ordenados)
    
    with st.form("f_tutor_v74", clear_on_submit=True):
        if escolha == "--- Novo Cadastro ---":
            v_nome, v_tel, v_cpf, v_email, v_end = "", "", "", "", ""
        else:
            dados = next(c for c in st.session_state['clientes'] if c['NOME'] == escolha)
            v_nome, v_tel, v_cpf, v_email, v_end = dados['NOME'], dados['TEL'], dados['CPF'], dados['E-MAIL'], dados['ENDEREÇO']

        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo *", value=v_nome).upper()
        zap = c2.text_input("Telefone/WhatsApp", value=v_tel)
        c3, c4 = st.columns([1, 1])
        cpf = c3.text_input("CPF", value=v_cpf)
        email = c4.text_input("E-mail", value=v_email)
        end = st.text_input("Endereço Completo", value=v_end)
        
        if st.form_submit_button("💾 Salvar Cadastro"):
            if nome and escolha == "--- Novo Cadastro ---":
                st.session_state['clientes'].append({"NOME": nome, "CPF": cpf, "TEL": zap, "ENDEREÇO": end, "E-MAIL": email})
                st.success(f"Tutor {nome} cadastrado!")
                st.rerun()

    if st.session_state['clientes']:
        st.write("---")
        # Exibe a tabela também em ordem alfabética
        df_clientes = pd.DataFrame(st.session_state['clientes']).sort_values(by="NOME")
        st.table(df_clientes)

# 4. MÓDULO 2: PETS (ORDEM ALFABÉTICA NO SELETOR)
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    # Puxa tutores em ordem alfabética para o vínculo
    tutores_disp = sorted([c['NOME'] for c in st.session_state['clientes']])
    
    if not tutores_disp:
        st.warning("⚠️ Cadastre um Tutor primeiro!")
    else:
        with st.form("f_pet_v74"):
            tutor_sel = st.selectbox("Tutor Responsável *", tutores_disp)
            c1, c2 = st.columns([2, 1])
            n_pet = c1.text_input("Nome do Pet *").upper()
            nasc = c2.text_input("Nascimento", value=datetime.now().strftime('%d/%m/%Y'))
            esp = st.selectbox("Espécie", ["Cão", "Gato", "Outro"])
            rac = st.text_input("Raça")
            if st.form_submit_button("💾 Salvar Pet"):
                if n_pet:
                    st.session_state['pets'].append({"PET": n_pet, "TUTOR": tutor_sel, "ESP": esp, "RAÇA": rac.upper(), "NASC": nasc})
                    st.rerun()
    if st.session_state['pets']:
        st.table(pd.DataFrame(st.session_state['pets']).sort_values(by="PET"))

# --- AJUSTE NO PRONTUÁRIO (PARA NÃO LANÇAR VALOR AUTOMÁTICO) ---
# No botão de salvar do Prontuário, removi a linha que somava 150.00 direto.

# 6. MÓDULO 4: FINANCEIRO (O SENHOR DECIDE O VALOR)
elif menu == "💰 Financeiro":
    st.subheader("💰 Gestão de Caixa e Orçamentos")
    
    # Parte 1: Lançar novo item manualmente
    with st.form("f_caixa"):
        st.write("💵 **Adicionar Item ao Carrinho**")
        c1, c2 = st.columns([3, 1])
        servico = c1.text_input("Descrição do Serviço (Ex: Consulta, Revisão, Vacina)")
        valor = c2.number_input("Valor (R$)", min_value=0.0, step=10.0, format="%.2f")
        
        if st.form_submit_button("➕ Adicionar ao Carrinho"):
            if servico:
                st.session_state['carrinho'].append({"Item": servico.upper(), "Preco": valor})
                st.rerun()

    # Parte 2: Exibição do Carrinho com casas decimais corrigidas
    if st.session_state['carrinho']:
        st.write("---")
        st.write("🛒 **Itens do Atendimento Atual:**")
        df_caixa = pd.DataFrame(st.session_state['carrinho'])
        
        # Formata para aparecer R$ 150,00 em vez de 150.0
        df_caixa["Preco"] = df_caixa["Preco"].map("R$ {:.2f}".format)
        st.table(df_caixa)
        
        total = sum(item['Preco'] for item in st.session_state['carrinho'])
        st.metric("Total a Cobrar", f"R$ {total:.2f}")
        
        if st.button("🏁 Finalizar e Limpar Carrinho"):
            st.session_state['carrinho'] = []
            st.success("Caixa fechado!")
            st.rerun()
    else:
        st.info("O carrinho está vazio. Adicione um serviço acima.")
