import streamlit as st
from datetime import datetime

# 1. CONFIGURAÇÃO E MEMÓRIA DO SISTEMA
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# Inicialização de dados para evitar erros de tela
for k in ['clientes', 'pets', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

# Controle de navegação robusto
if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"
if 'tutor_foco' not in st.session_state: st.session_state.tutor_foco = None
if 'pet_foco' not in st.session_state: st.session_state.pet_foco = None

# --- 2. MENU LATERAL ---
with st.sidebar:
    st.title("🐾 Ribeira Vet Pro")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    # Sincroniza o menu com o estado atual do sistema
    index_atual = opcoes.index(st.session_state.aba_atual)
    escolha = st.radio("NAVEGAÇÃO", opcoes, index=index_atual)
    
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- 3. MÓDULO TUTORES (COM CPF) ---
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes (Tutores)")
    
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    t_sel = st.selectbox("Buscar ou Novo:", ["--- Novo ---"] + nomes)

    v_nome, v_cpf, v_tel, v_email, v_end = ("", "", "", "", "")
    if t_sel != "--- Novo ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == t_sel)
        v_nome, v_cpf, v_tel, v_email, v_end = c.get('NOME',''), c.get('CPF',''), c.get('TEL',''), c.get('EMAIL',''), c.get('END','')
        
        if st.button(f"➡️ Ver Animais de {v_nome}"):
            st.session_state.tutor_foco = v_nome
            st.session_state.aba_atual = "🐾 Pets"
            st.rerun()

    with st.form("form_tutor_v85"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        f_cpf = st.text_input("CPF (Para Recibos)", value=v_cpf)
        col1, col2 = st.columns(2)
        f_tel = col1.text_input("WhatsApp / Telefone", value=v_tel)
        f_email = col2.text_input("E-mail (Obrigatório) *", value=v_email).lower()
        f_end = st.text_area("Endereço Completo *", value=v_end)
        
        if st.form_submit_button("💾 Salvar Cliente"):
            if f_nome and f_email:
                dados = {"NOME": f_nome, "CPF": f_cpf, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if t_sel == "--- Novo ---": st.session_state['clientes'].append(dados)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == t_sel: st.session_state['clientes'][i] = dados
                st.rerun()

# --- 4. MÓDULO PETS (RAÇAS PRÉ-DEFINIDAS E IDADE) ---
elif st.session_state.aba_atual == "🐾 Pets":
    st.subheader("🐾 Pacientes e Raças")
    
    # LISTA DE RAÇAS QUE O SENHOR PEDIU
    racas_caes = ["SRD (Cão)", "Poodle", "Pinscher", "Shih Tzu", "Yorkshire", "Golden Retriever", "Border Collie", "Bulldog", "Labrador", "Beagle"]
    racas_gatos = ["SRD (Gato)", "Persa", "Siamês", "Maine Coon", "Angorá", "Bengal"]
    lista_completa = sorted(racas_caes + racas_gatos)
    
    tuts = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    idx_t = (tuts.index(st.session_state.tutor_foco) + 1) if st.session_state.tutor_foco in tuts else 0
    tutor_f = st.selectbox("Selecione o Tutor:", ["--- Selecione ---"] + tuts, index=idx_t)

    if tutor_f != "--- Selecione ---":
        # MOSTRAR PETS JÁ CADASTRADOS (Incluindo a Idade que faltava)
        meus_pets = [p for p in st.session_state['pets'] if p['TUTOR'] == tutor_f]
        for p in meus_pets:
            c1, c2 = st.columns([4, 1])
            # Aqui a idade aparece fixa para o senhor ver
            c1.info(f"🐕 **{p['PET']}** | Raça: **{p['RAÇA']}** | Idade: **{p.get('IDADE', 'N/I')}**")
            
            if c2.button(f"🩺 Atender", key=f"at_{p['PET']}"):
                st.session_state.pet_foco = f"{p['PET']} (Tutor: {tutor_f})"
                st.session_state.aba_atual = "📋 Prontuário"
                st.rerun()
        
        st.divider()
        with st.expander("➕ CADASTRAR NOVO ANIMAL"):
            with st.form("form_pet_v86"):
                col_n, col_r = st.columns(2)
                n_p = col_n.text_input("Nome do Pet *").upper()
                
                # SELETOR DE RAÇAS PRÉ-DEFINIDAS
                r_p = col_r.selectbox("Raça do Animal:", ["Outra"] + lista_completa)
                if r_p == "Outra":
                    r_p = st.text_input("Digite a Raça se não estiver na lista:").upper()
                
                # CAMPO DE IDADE (Texto livre para facilitar: ex: '5 anos' ou '10 meses')
                i_p = st.text_input("Idade ou Data de Nascimento:")
                
                if st.form_submit_button("💾 Salvar Pet no Sistema"):
                    if n_p:
                        st.session_state['pets'].append({
                            "PET": n_p, 
                            "RAÇA": r_p, 
                            "TUTOR": tutor_f, 
                            "IDADE": i_p # Agora a idade é salva de verdade
                        })
                        st.success(f"{n_p} cadastrado com sucesso!")
                        st.rerun()

# --- 5. MÓDULO PRONTUÁRIO ---
elif st.session_state.aba_atual == "📋 Prontuário":
    st.subheader("📋 Prontuário Médico")
    p_lista = sorted([f"{p['PET']} (Tutor: {p['TUTOR']})" for p in st.session_state['pets']])
    idx_p = (p_lista.index(st.session_state.pet_foco) + 1) if st.session_state.pet_foco in p_lista else 0
    paciente = st.selectbox("Paciente em Atendimento:", ["--- Selecione ---"] + p_lista, index=idx_p)

    if paciente != "--- Selecione ---":
        with st.form("form_pront"):
            texto = st.text_area("Anamnese e Conduta:", height=300)
            if st.form_submit_button("💾 Salvar Atendimento"):
                st.session_state['historico'].append({"DATA": datetime.now().strftime("%d/%m/%Y"), "PACIENTE": paciente, "TEXTO": texto})
                st.success("Consulta Finalizada!")
