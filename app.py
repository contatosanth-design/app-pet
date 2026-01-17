# 3. MÓDULO 1: TUTORES (COMPLETO)
if menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    
    # Mantém a busca que o senhor aprovou
    busca = st.text_input("🔍 Buscar por Nome:")
    if busca:
        res = [c for c in st.session_state['clientes'] if busca.upper() in c['NOME']]
        if res: st.table(pd.DataFrame(res))
    
    with st.form("f_tutor_completo"):
        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo *")
        zap = c2.text_input("Telefone")
        
        c3, c4 = st.columns([1, 1])
        cpf = c3.text_input("CPF")
        email = c4.text_input("E-mail") # Campo recuperado
        
        end = st.text_input("Endereço Completo") # Campo recuperado
        
        if st.form_submit_button("💾 Salvar"):
            if nome:
                # Salvando todos os parâmetros novamente
                novo = {
                    "NOME": nome.upper(), 
                    "CPF": cpf, 
                    "TEL": zap, 
                    "ENDEREÇO": end, 
                    "E-MAIL": email
                }
                st.session_state['clientes'].append(novo)
                st.session_state['clientes'] = sorted(st.session_state['clientes'], key=lambda x: x['NOME'])
                st.rerun()

    if st.session_state['clientes']:
        st.write("📋 **Lista de Clientes Cadastrados**")
        st.table(pd.DataFrame(st.session_state['clientes']))
