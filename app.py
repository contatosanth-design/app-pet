import streamlit as st

st.set_page_config(page_title="PetControl Profissional", page_icon="🐾")

st.title("🐾 Sistema PetControl v2.0")
st.markdown("---")

tab1, tab2 = st.tabs(["👤 Clientes", "🐶 Pets"])

with tab1:
    st.header("Cadastrar Cliente")
    nome = st.text_input("Nome do Dono")
    tel = st.text_input("WhatsApp")
    if st.button("Salvar Cliente"):
        st.success(f"Cliente {nome} salvo com sucesso!")

with tab2:
    st.header("Cadastrar Pet")
    nome_pet = st.text_input("Nome do Animal")
    especie = st.selectbox("Espécie", ["Cão", "Gato", "Outros"])
    if st.button("Salvar Pet"):
        st.balloons()
        st.success(f"Pet {nome_pet} cadastrado!")
