import streamlit as st

st.set_page_config(page_title="PetControl Profissional", layout="wide")

st.title("🐾 Sistema PetControl v4.0")

# Banco de dados na memória com contadores para códigos crescentes
if 'clientes' not in st.session_state:
    st.session_state['clientes'] = {}
if 'pets' not in st.session_state:
    st.session_state['pets'] = []
if 'proximo_cod_cliente' not in st.session_state:
    st.session_state['proximo_cod_cliente'] = 1
if 'proximo_cod_pet' not in st.session_state:
    st.session_state['proximo_cod_pet'] = 1

tab1, tab2, tab3 = st.tabs(["👤 Clientes", "🐶 Pets", "📋 Relatório Geral"])

with tab1:
    st.header("Cadastrar Cliente")
    with st.form("form_cliente"):
        # Código numérico de 4 dígitos (0001, 0002...)
        cod_cliente_formatado = f"{st.session_state['proximo_cod_cliente']:04d}"
        st.info(f"Código do Novo Cliente: {cod_cliente_formatado}")
        
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF")
        email = st.text_input("E-mail")
        whatsapp = st.text_input("WhatsApp")
        cep = st.text_input("CEP")
        endereco = st.text_area("Endereço Completo")
        
        if st.form_submit_button("Salvar Cliente"):
            if nome:
                st.session_state['clientes'][cod_cliente_formatado] = nome
                st.session_state['proximo_cod_cliente'] += 1
                st.success(f"✅ Cliente {nome} salvo com o código {cod_cliente_formatado}!")
                st.balloons()
            else:
                st.error("O nome é obrigatório!")

with tab2:
    st.header("Cadastrar Pet")
    if not st.session_state['clientes']:
        st.warning("⚠️ Cadastre um cliente primeiro.")
    else:
        with st.form("form_pet"):
            cod_pet_formatado = f"{st.session_state['proximo_cod_pet']:04d}"
            st.info(f"Código do Pet: {cod_pet_formatado}")
            
            opcoes_clientes = [f"{id} - {nome}" for id, nome in st.session_state['clientes'].items()]
            dono_selecionado = st.selectbox("Quem é o Dono?", opcoes_clientes)
            
            nome_pet = st.text_input("Nome do Pet")
            raca = st.text_input("Raça")
            
            # Opção de Idade em Anos ou Meses
            col_id1, col_id2 = st.columns([1, 1])
            with col_id1:
                valor_idade = st.number_input("Idade (Número)", min_value=0)
            with col_id2:
                unidade_idade = st.selectbox("Tempo", ["Ano(s)", "Mês(es)"])
            
            # Campo de Foto
            foto = st.file_uploader("Clique abaixo para enviar a foto do Pet", type=['png', 'jpg', 'jpeg'])
            
            if st.form_submit_button("Salvar Pet"):
                if nome_pet:
                    st.session_state['pets'].append({
                        "id": cod_pet_formatado,
                        "dono": dono_selecionado,
                        "nome": nome_pet,
                        "raca": raca,
                        "idade": f"{valor_idade} {unidade_idade}",
                        "foto": foto
                    })
                    st.session_state['proximo_cod_pet'] += 1
                    st.success(f"✅ Pet {nome_pet} salvo com código {cod_pet_formatado}!")
                else:
                    st.error("O nome do pet é obrigatório!")

with tab3:
    st.header("Relatório de Associação")
    if st.session_state['pets']:
        for p in st.session_state['pets']:
            with st.expander(f"🐶 {p['nome']} (Cód: {p['id']}) | Dono: {p['dono']}"):
                st.write(f"**Raça:** {p['raca']}")
                st.write(f"**Idade:** {p['idade']}")
                if p['foto']:
                    st.image(p['foto'], width=300, caption=f"Foto de {p['nome']}")
    else:
        st.write("Nenhum registro encontrado.")
