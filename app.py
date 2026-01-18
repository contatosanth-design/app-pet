import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO (ESTABILIDADE TOTAL)
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
    
    with st.form("f_tutor_v95"):
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

# 4. MÓDULO 2: PETS (A RAÇA VOLTOU E ESTÁ TRAVADA)
elif menu == "🐾 Pets":
    st.subheader("🐾 Pacientes e Raças")
    tutores_disp = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    
    if not tutores_disp:
        st.warning("⚠️ Cadastre um Tutor primeiro!")
    else:
        tutor_sel = st.selectbox("Selecione o Tutor:", tutores_disp)
        
        # Mostra os animais já existentes deste tutor
        pets_do_tutor = [p for p in st.session_state['pets'] if p.get('TUTOR') == tutor_sel]
        if pets_do_tutor:
            st.write(f"✅ **Pacientes de {tutor_sel}:**")
            st.table(pd.DataFrame(pets_do_tutor)[["PET", "ESP", "RAÇA", "NASC"]])

        # Formulário para novo pet COM CAMPO DE RAÇA EXPLÍCITO
        with st.expander("➕ Adicionar Novo Animal para este Tutor", expanded=True):
            with st.form("f_pet_v95"):
                c1, c2 = st.columns(2)
                n_pet = c1.text_input("Nome do Pet *").upper()
                nasc = c2.text_input("Nascimento", value=datetime.now().strftime('%d/%m/%Y'))
                
                c3, c4 = st.columns(2)
                esp = c3.selectbox("Espécie", ["Cão", "Gato", "Outro"])
                rac = c4.text_input("Raça (Ex: Bulldog, SRD) *").upper() # AQUI ESTÁ A RAÇA!
                
                if st.form_submit_button("💾 Salvar Animal"):
                    if n_pet and rac:
                        st.session_state['pets'].append({
                            "PET": n_pet, "TUTOR": tutor_sel, 
                            "ESP": esp, "RAÇA": rac, "NASC": nasc
                        })
                        st.success(f"{n_pet} cadastrado com sucesso!")
                        st.rerun()

# 5. MÓDULO 3: PRONTUÁRIO (COM HISTÓRICO VISÍVEL)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    opcoes_pets = sorted([f"{p['PET']} (Tutor: {p.get('TUTOR', 'N/D')})" for p in st.session_state['pets']])
    paciente_sel = st.selectbox("Buscar Paciente *", ["--- Selecione ---"] + opcoes_pets)
    
    if paciente_sel != "--- Selecione ---":
        # Filtra e mostra o histórico na hora
        hist_filtrado = [h for h in st.session_state['historico'] if h['PACIENTE'] == paciente_sel]
        if hist_filtrado:
            with st.expander("📜 Ver atendimentos anteriores", expanded=False):
                st.table(pd.DataFrame(hist_filtrado)[["DATA", "PESO", "TEMP", "RELATO"]])

        with st.form("f_pronto_v95"):
            c1, c2 = st.columns(2)
            peso = c1.text_input("Peso (kg)")
            temp = c2.text_input("Temperatura (°C)")
            anamnese = st.text_area("🎙️ Descrição do Caso:", height=200, key="caixa_texto")
            if st.form_submit_button("💾 Salvar Atendimento"):
                if anamnese:
                    st.session_state['historico'].append({
                        "DATA": datetime.now().strftime('%d/%m/%Y %H:%M'),
                        "PACIENTE": paciente_sel, "PESO": peso, "TEMP": temp, "RELATO": anamnese
                    })
                    st.rerun()

# 6. FINANCEIRO (R$ 0,00 CORRIGIDO)
elif menu == "💰 Financeiro":
    st.subheader("💰 Financeiro")
    with st.form("f_caixa"):
        serv = st.text_input("Serviço")
        val = st.number_input("Valor", min_value=0.0, format="%.2f")
        if st.form_submit_button("➕ Lançar"):
            st.session_state['carrinho'].append({"Item": serv.upper(), "Preco": val})
            st.rerun()
    if st.session_state['carrinho']:
        df = pd.DataFrame(st.session_state['carrinho'])
        st.table(df.assign(Preco=df['Preco'].map("R$ {:.2f}".format)))
        if st.button("🏁 Finalizar"): st.session_state['carrinho'] = []; st.rerun()

# 7. BACKUP
elif menu == "💾 Backup":
    st.subheader("💾 Backup")
    if st.session_state['clientes']:
        st.download_button("📥 Baixar Tudo", pd.DataFrame(st.session_state['clientes']).to_csv(index=False).encode('utf-8-sig'), "dados.csv")
