import streamlit as st
import uuid

st.set_page_config(page_title="PetControl Profissional", layout="wide")

st.title("🐾 Sistema PetControl v3.0")

# Simulando um banco de dados na memória (isso limpa se atualizar a página, 
# mas é ótimo para testar a estrutura)
if 'clientes' not in st.session_state:
    st.session_state['clientes'] = {}
if 'pets' not in st.session_state:
    st.session_state['pets'] = []

tab1, tab2, tab3 = st.tabs(["👤 Clientes", "🐶 Pets", "📋 Relatório Geral"])

with tab1:
    st.header("Cadastrar Cliente")
    with st.form("form_cliente"):
        # Código gerado automaticamente
        cod_cliente = str(uuid.uuid4())[:8].upper()
        st.info(f"Código do Novo Cliente: {cod_cliente}")
        
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF")
        email = st.text_input("E-mail")
        whatsapp = st.text_input("WhatsApp")
        cep = st.text_input("CEP")
        endereco = st.text_area("Endereço Completo")
        
        if st.form_submit_button("Salvar Cliente"):
            if nome:
                st.session_state['clientes'][cod_cliente] = nome
                st.success(f"✅ Cliente {nome} (Cód: {cod_cliente}) salvo!")
                st.balloons()
            else:
                st.error("Nome é obrigatório!")

with tab2:
    st.header("Cadastrar Pet")
    if not st.session_state['clientes']:
        st.warning("⚠️ Cadastre um cliente primeiro para associar ao pet.")
    else:
        with st.form("form_pet"):
            cod_pet = str(uuid.uuid4())[:8].upper()
            st.info(f"Código do Pet: {cod_pet}")
            
            # Associação: Seleciona o cliente pelo nome/código
            opcoes_clientes = [f"{id} - {nome}" for id, nome in st.session_state['clientes'].items()]
            dono_selecionado = st.selectbox("Quem é o Dono?", opcoes_clientes)
            
            nome_pet = st.text_input("Nome do Pet")
            raca = st.text_input("Raça")
            idade = st.number_input("Idade", min_value=0)
            
            # Espaço para foto
            foto = st.file_uploader("Foto do Pet", type=['png', 'jpg', 'jpeg'])
            
            if st.form_submit_button("Salvar Pet"):
                st.session_state['pets'].append({
                    "id": cod_pet,
                    "dono": dono_selecionado,
                    "nome": nome_pet,
                    "raca": raca,
                    "foto": foto
                })
                st.success(f"✅ Pet {nome_pet} associado com sucesso!")

with tab3:
    st.header("Relatório de Associação")
    if st.session_state['pets']:
        for p in st.session_state['pets']:
            with st.expander(f"Pet: {p['nome']} | Dono: {p['dono']}"):
                st.write(f"**Código do Pet:** {p['id']}")
                st.write(f"**Raça:** {p['raca']}")
                if p['foto']:
                    st.image(p['foto'], width=200)
    else:
        st.write("Nenhum pet cadastrado ainda.")
