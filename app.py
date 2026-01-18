import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicialização de banco de dados
for k in ['clientes', 'pets', 'carrinho', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [
        {"Item": "CONSULTA CLÍNICA", "Preco": 150.0},
        {"Item": "VACINA V10", "Preco": 120.0},
        {"Item": "VACINA ANTIRRÁBICA", "Preco": 60.0}
    ]

# 2. MENU LATERAL
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    menu = st.radio("NAVEGAÇÃO", ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"])

# 3. MÓDULO 1: TUTORES
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    busca = st.text_input("🔍 Buscar por Nome:")
    if busca:
        res = [c for c in st.session_state['clientes'] if busca.upper() in c['NOME']]
        if res: st.table(pd.DataFrame(res))
    
    with st.form("f_tutor"):
        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo *")
        zap = c2.text_input("Telefone")
        c3, c4 = st.columns([1, 1])
        cpf = c3.text_input("CPF")
        email = c4.text_input("E-mail")
        end = st.text_input("Endereço Completo")
        
        if st.form_submit_button("💾 Salvar"):
            if nome:
                novo = {"NOME": nome.upper(), "CPF": cpf, "TEL": zap, "ENDEREÇO": end, "E-MAIL": email}
                st.session_state['clientes'].append(novo)
                st.session_state['clientes'] = sorted(st.session_state['clientes'], key=lambda x: x['NOME'])
                st.rerun()

    if st.session_state['clientes']:
        st.write("📋 **Lista de Tutores**")
        st.table(pd.DataFrame(st.session_state['clientes']))

# 4. MÓDULO 2: PETS
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    
    # Lista de tutores para vincular ao pet
    lista_tutores = ["--- Selecione o Tutor ---"]
    if st.session_state['clientes']:
        lista_tutores.extend([c['NOME'] for c in st.session_state['clientes']])

    esp = st.selectbox("Selecione a Espécie", ["Cão", "Gato", "Outro"])
    lista_racas = ["SRD", "Poodle", "Shih Tzu", "Yorkshire", "Siamês", "Persa", "Outra..."]

    with st.form("f_pet"):
        tutor_vinculo = st.selectbox("Tutor (Dono) *", lista_tutores)
        c1, c2 = st.columns([2, 1])
        n_pet = c1.text_input("Nome do Pet *")
        data_nasc = c2.text_input("Nascimento (DD/MM/AAAA)", value=datetime.now().strftime('%d/%m/%Y'))
        
        rac_sel = st.selectbox("Raça", lista_racas)
        rac_nova = st.text_input("Se 'Outra', digite aqui:")

        if st.form_submit_button("💾 Salvar Pet"):
            if n_pet and tutor_vinculo != "--- Selecione o Tutor ---":
                r_final = rac_nova.upper() if rac_sel == "Outra..." else rac_sel
                st.session_state['pets'].append({
                    "PET": n_pet.upper(), "TUTOR": tutor_vinculo, 
                    "ESPÉCIE": esp, "RAÇA": r_final, "NASCIMENTO": data_nasc
                })
                st.success(f"Paciente {n_pet} cadastrado!")
                st.rerun()

    if st.session_state['pets']:
        st.table(pd.DataFrame(st.session_state['pets']))

# 5. MÓDULO 3: PRONTUÁRIO (BUSCA AUTOMÁTICA CORRIGIDA)
elif menu == "📋 Prontuário":
    st.subheader("📋 Atendimento Clínico")
    
    opcoes_busca = ["--- Escolha o Paciente ---"]
    if st.session_state['pets']:
        # Aqui o sistema busca AUTOMATICAMENTE o Pet e o Tutor cadastrados
        opcoes_busca.extend([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])

    with st.form("f_pronto"):
        pet_selecionado = st.selectbox("Buscar Paciente *", opcoes_busca)
        c1, c2 = st.columns(2)
        peso = c1.text_input("Peso (kg)")
        temp = c2.text_input("Temp (°C)")
        
        st.write("🎙️ **Anamnese** (Win + H para ditar)")
        anamnese = st.text_area("Relato e Exame Clínico:", height=200)
        
        if st.form_submit_button("💾 Salvar Atendimento"):
            if pet_selecionado != "--- Escolha o Paciente ---" and anamnese:
                st.session_state['historico'].append({
                    "DATA": datetime.now().strftime('%d/%m/%Y %H:%M'),
                    "PACIENTE": pet_selecionado, "PESO": peso, "TEMP": temp, "RELATO": anamnese
                })
                # Lança no financeiro
                st.session_state['carrinho'].append({"Item": f"CONSULTA: {pet_selecionado}", "Preco": 150.0})
                st.success("Prontuário salvo e consulta lançada no financeiro!")
                st.rerun()

    if st.session_state['historico']:
        st.divider()
        st.write("📂 **Histórico Recente**")
        st.table(pd.DataFrame(st.session_state['historico']))

# 6. MÓDULO 4: FINANCEIRO
elif menu == "💰 Financeiro":
    st.subheader("💰 Caixa e Orçamentos")
    if st.session_state['carrinho']:
        df_c = pd.DataFrame(st.session_state['carrinho'])
        st.table(df_c)
        total = df_c['Preco'].sum()
        st.write(f"### TOTAL: R$ {total:.2f}")
        if st.button("🏁 Fechar Caixa"):
            st.session_state['carrinho'] = []
            st.success("Venda finalizada!")
            st.rerun()
    else:
        st.info("Nenhum lançamento pendente.")

# 7. MÓDULO 5: BACKUP
elif menu == "💾 Backup":
    st.subheader("💾 Backup para Drive Externo")
    col1, col2 = st.columns(2)
    if st.session_state['clientes']:
        col1.download_button("📥 Excel Clientes", pd.DataFrame(st.session_state['clientes']).to_csv(index=False).encode('utf-8-sig'), "clientes.csv")
    if st.session_state['pets']:
        col2.download_button("📥 Excel Pets", pd.DataFrame(st.session_state['pets']).to_csv(index=False).encode('utf-8-sig'), "pets.csv")
