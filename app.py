import streamlit as st

st.set_page_config(page_title="PetControl Profissional", page_icon="🐾")

st.title("🐾 Sistema PetControl v2.0")
st.markdown("---")

tab1, tab2 = st.tabs(["👤 Clientes", "🐶 Pets"])

with tab1:
    with tab1:
        st.header("👤 Cadastrar Cliente")
        with st.form("form_cliente"):
            nome_dono = st.text_input("Nome do Dono")
            cpf = st.text_input("CPF (apenas números)")
            email = st.text_input("E-mail")
            whatsapp = st.text_input("WhatsApp (com DDD)")
            
            # Parte de Endereço
            col1, col2 = st.columns([1, 3])
            with col1:
                cep = st.text_input("CEP")
            with col2:
                endereco = st.text_input("Endereço Completo (Rua, Número, Bairro)")
            
            submit_cliente = st.form_submit_button("Salvar Cliente")
            
            if submit_cliente:
                if nome_dono and whatsapp:
                    # Aqui você pode adicionar a lógica para salvar no banco de dados
                    st.success(f"✅ Cliente {nome_dono} cadastrado com sucesso!")
                    st.balloons()
                else:
                    st.error("⚠️ Por favor, preencha pelo menos Nome e WhatsApp.")

with tab2:
    st.header("Cadastrar Pet")
    nome_pet = st.text_input("Nome do Animal")
    especie = st.selectbox("Espécie", ["Cão", "Gato", "Outros"])
    if st.button("Salvar Pet"):
        st.balloons()
        st.success(f"Pet {nome_pet} cadastrado!")
