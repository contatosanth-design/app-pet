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

# 3. MÓDULO 1: TUTORES (A-Z)
if menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")
    nomes_ordenados = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    escolha = st.selectbox("⚡ Selecionar ou Criar Novo:", ["--- Novo Cadastro ---"] + nomes_ordenados)
    
    with st.form("f_tutor_v9"):
        if escolha == "--- Novo Cadastro ---":
            v_nome, v_tel, v_cpf, v_email, v_end = "", "", "", "", ""
        else:
            dados = next(c for c in st.session_state['clientes'] if c['NOME'] == escolha)
            v_nome, v_tel, v_cpf, v_email, v_end = dados['NOME'], dados['TEL'], dados['CPF'], dados['E-MAIL'], dados['ENDEREÇO']

        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo *", value=v_nome).upper()
        zap = c2.text_input("Telefone", value=v_tel)
        c3, c4 = st.columns([1, 1])
        cpf = c3.text_input("CPF", value=v_cpf)
        email = c4.text_input("E-mail", value=v_email)
        end = st.text_input("Endereço Completo", value=v_end)
        
        if st.form_submit_button("💾 Salvar Cadastro"):
            if nome and escolha == "--- Novo Cadastro ---":
                st.session_state['clientes'].append({"NOME": nome, "CPF": cpf, "TEL": zap, "ENDEREÇO": end, "E-MAIL": email})
                st.rerun()

# 4. MÓDULO 2: PETS (FILTRO POR TUTOR)
elif menu == "🐾 Pets":
    st.subheader("🐾 Pacientes por Tutor")
    tutores_disp = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    
    if not tutores_disp:
        st.warning("⚠️ Cadastre um Tutor primeiro!")
    else:
        tutor_sel = st.selectbox("Selecione o Tutor para ver os animais:", tutores_disp)
        
        # Filtra animais do tutor selecionado
        pets_do_tutor = [p for p in st.session_state['pets'] if p.get('TUTOR') == tutor_sel]
        
        if pets_do_tutor:
            st.write(f"✅ **Animais de {tutor_sel}:**")
            st.table(pd.DataFrame(pets_do_tutor)[["PET", "ESP", "RAÇA", "NASC"]])
        else:
            st.info(f"O tutor {tutor_sel} ainda não tem animais cadastrados.")

        with st.expander("➕ Cadastrar Novo Animal para este Tutor"):
            with st.form("f_novo_pet"):
                n_pet = st.text_input("Nome do Pet *").upper()
                nasc = st.text_input("Nascimento", value=datetime.now().strftime('%d/%m/%Y'))
                esp = st.selectbox("Espécie", ["Cão", "Gato", "Outro"])
                rac = st.text_input("Raça").upper()
                if st.form_submit_button("💾 Salvar Pet"):
                    if n_pet:
                        st.session_state['pets'].append({"PET": n_pet, "TUTOR": tutor_sel, "ESP": esp, "RAÇA": rac, "NASC": nasc})
                        st.rerun()

# 5. MÓDULO 3: PRONTUÁRIO (COM HISTÓRICO NA TELA)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento e Histórico")
    opcoes_pets = sorted([f"{p['PET']} (Tutor: {p.get('TUTOR', 'N/D')})" for p in st.session_state['pets']])
    
    paciente_sel = st.selectbox("Buscar Paciente *", ["--- Selecione ---"] + opcoes_pets)
    
    if paciente_sel != "--- Selecione ---":
        # MOSTRAR HISTÓRICO ANTES DO NOVO ATENDIMENTO
        hist_filtrado = [h for h in st.session_state['historico'] if h['PACIENTE'] == paciente_sel]
        if hist_filtrado:
            with st.expander(f"📜 Ver Histórico de {paciente_sel}", expanded=False):
                st.table(pd.DataFrame(hist_filtrado)[["DATA", "PESO", "TEMP", "RELATO"]])

        # FORMULÁRIO DE NOVO ATENDIMENTO
        with st.form("f_atend_v9"):
            st.write(f"📝 **Novo Atendimento: {paciente_sel}**")
            c1, c2 = st.columns(2)
            peso = c1.text_input("Peso (kg)")
            temp = c2.text_input("Temperatura (°C)")
            anamnese = st.text_area("🎙️ Anamnese (Win+H):", height=200, key="txt_v9")
            
            if st.form_submit_button("💾 Salvar Atendimento"):
                if anamnese:
                    st.session_state['historico'].append({
                        "DATA": datetime.now().strftime('%d/%m/%Y %H:%M'),
                        "PACIENTE": paciente_sel, "PESO": peso, "TEMP": temp, "RELATO": anamnese
                    })
                    st.success("Salvo!")
                    st.rerun()

# 6. FINANCEIRO E 7. BACKUP (Mantidos como solicitado)
elif menu == "💰 Financeiro":
    st.subheader("💰 Financeiro")
    servico = st.text_input("Serviço")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")
    if st.button("➕ Adicionar"):
        st.session_state['carrinho'].append({"Item": servico.upper(), "Preco": valor})
    if st.session_state['carrinho']:
        df = pd.DataFrame(st.session_state['carrinho'])
        st.table(df.assign(Preco=df['Preco'].map("R$ {:.2f}".format)))
        if st.button("🏁 Fechar"): st.session_state['carrinho'] = []; st.rerun()

elif menu == "💾 Backup":
    st.subheader("💾 Exportar")
    if st.session_state['clientes']:
        st.download_button("📥 Excel", pd.DataFrame(st.session_state['clientes']).to_csv(index=False).encode('utf-8-sig'), "vet.csv")
