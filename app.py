import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO INICIAL (Cura o NameError)
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

for k in ['clientes', 'pets', 'carrinho']:
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

# 3. MÓDULO 1: TUTORES (CAMPOS RECUPERADOS)
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    busca = st.text_input("🔍 Buscar por Nome:")
    if busca:
        res = [c for c in st.session_state['clientes'] if busca.upper() in c['NOME']]
        if res: st.table(pd.DataFrame(res))
    
    with st.form("f_tutor_definitivo"):
        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo *")
        zap = c2.text_input("Telefone")
        
        c3, c4 = st.columns([1, 1])
        cpf = c3.text_input("CPF")
        email = c4.text_input("E-mail") # Recuperado conforme solicitado
        
        end = st.text_input("Endereço Completo") # Recuperado conforme solicitado
        
        if st.form_submit_button("💾 Salvar"):
            if nome:
                novo = {"NOME": nome.upper(), "CPF": cpf, "TEL": zap, "ENDEREÇO": end, "E-MAIL": email}
                st.session_state['clientes'].append(novo)
                st.session_state['clientes'] = sorted(st.session_state['clientes'], key=lambda x: x['NOME'])
                st.rerun()

    if st.session_state['clientes']:
        st.write("📋 **Lista Geral**")
        st.table(pd.DataFrame(st.session_state['clientes']))

# 4. MÓDULO 2: PETS (CORREÇÃO DE RAÇAS E ANIVERSÁRIO)
elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    
    # 1. Escolha da Espécie (Fora do form para atualizar as raças na hora)
    esp = st.selectbox("Selecione a Espécie", ["Cão", "Gato", "Outro"])
    
    # 2. Definição automática das listas baseada na espécie
    if esp == "Cão":
        lista_racas = ["SRD", "Poodle", "Pinscher", "Shih Tzu", "Yorkshire", "Golden Retriever", "Bulldog", "Outra..."]
    elif esp == "Gato":
        lista_racas = ["SRD", "Siamês", "Persa", "Angorá", "Maine Coon", "Bengal", "Outra..."]
    else:
        lista_racas = ["Outra..."]

    # 3. Formulário de Cadastro
    with st.form("f_pet_v19", clear_on_submit=True):
        c1, c2 = st.columns([2, 1])
        n_pet = c1.text_input("Nome do Pet *")
        
        # Campo de Aniversário para arquivo e contato futuro
        data_nasc = c2.date_input("Data de Nascimento", value=datetime.now())
        
        # Seletor de Raça dinâmico
        rac_sel = st.selectbox("Raça", lista_racas)
        
        # Campo extra que só aparece se escolher "Outra..."
        rac_nova = st.text_input("Se escolheu 'Outra', digite a raça aqui:")

        if st.form_submit_button("💾 Salvar Pet"):
            if n_pet:
                # Lógica para salvar a raça correta
                r_final = rac_nova.upper() if rac_sel == "Outra..." else rac_sel
                
                novo_pet = {
                    "PET": n_pet.upper(), 
                    "ESPÉCIE": esp, 
                    "RAÇA": r_final, 
                    "NASCIMENTO": data_nasc.strftime('%d/%m/%Y')
                }
                st.session_state['pets'].append(novo_pet)
                st.success(f"Paciente {n_pet} cadastrado!")
                st.rerun()

    # Mostra a tabela atualizada com as novas colunas
    if st.session_state['pets']:
        st.table(pd.DataFrame(st.session_state['pets']))
# 5. MÓDULO 6: BACKUP (DRIVE EXTERNO)
elif menu == "💾 Backup":
    st.subheader("💾 Exportar para Drive Externo")
    if st.session_state['clientes']:
        df_c = pd.DataFrame(st.session_state['clientes'])
        st.download_button("📥 Baixar Clientes (Excel)", df_c.to_csv(index=False).encode('utf-8-sig'), "clientes_vet.csv")
    if st.session_state['pets']:
        df_p = pd.DataFrame(st.session_state['pets'])
        st.download_button("📥 Baixar Pets (Excel)", df_p.to_csv(index=False).encode('utf-8-sig'), "pets_vet.csv")

# 6. MÓDULOS RESTANTES (PRONTUÁRIO E FINANCEIRO)
else:
    st.subheader("📋 Prontuário / 💰 Financeiro")
    st.info("Utilize as opções acima para registrar atendimentos ou orçamentos.")
