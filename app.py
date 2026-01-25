import streamlit as st
from datetime import datetime
import urllib.parse
import ast

# 1. CONFIGURAÇÃO MOBILE
st.set_page_config(page_title="Ribeira Vet Pro", layout="centered")

for k in ['clientes', 'pets', 'historico', 'caixa', 'carrinho']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"

# --- 2. MENU LATERAL ---
with st.sidebar:
    st.title("🐾 Ribeira Vet")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💰 Financeiro", "💾 Backup"]
    escolha = st.radio("MENU", opcoes, index=opcoes.index(st.session_state.aba_atual))
    if escolha != st.session_state.aba_atual:
        st.session_state.aba_atual = escolha
        st.rerun()

# --- 3. MÓDULO TUTORES ---
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Cadastro de Tutores")
    nomes = sorted(list(set([c['NOME'] for c in st.session_state['clientes']])))
    t_sel = st.selectbox("Buscar Cliente:", ["--- Novo ---"] + nomes)
    v_nome, v_cpf, v_tel, v_email, v_end = ("", "", "", "", "")
    if t_sel != "--- Novo ---":
        c = next(i for i in st.session_state['clientes'] if i['NOME'] == t_sel)
        v_nome, v_cpf, v_tel, v_email, v_end = c.get('NOME',''), c.get('CPF',''), c.get('TEL',''), c.get('EMAIL',''), c.get('END','')

    with st.form("f_tutor_v105"):
        f_nome = st.text_input("Nome Completo *", value=v_nome).upper()
        f_cpf = st.text_input("CPF", value=v_cpf)
        f_tel = st.text_input("WhatsApp", value=v_tel)
        f_email = st.text_input("E-mail", value=v_email)
        f_end = st.text_area("Endereço", value=v_end)
        if st.form_submit_button("💾 SALVAR TUTOR", use_container_width=True):
            if f_nome:
                d = {"NOME": f_nome, "CPF": f_cpf, "TEL": f_tel, "EMAIL": f_email, "END": f_end}
                if t_sel == "--- Novo ---": st.session_state['clientes'].append(d)
                else:
                    for i, cli in enumerate(st.session_state['clientes']):
                        if cli['NOME'] == t_sel: st.session_state['clientes'][i] = d
                st.success("Tutor Salvo!")
                st.rerun()

# --- 4. MÓDULO PETS (CORRIGIDO) ---
elif st.session_state.aba_atual == "🐾 Pets":
    st.subheader("🐾 Cadastro de Animais")
    # Puxa a lista de tutores salvos
    lista_tutores = sorted([c['NOME'] for c in st.session_state['clientes']])
    
    if not lista_tutores:
        st.warning("⚠️ Cadastre um Tutor primeiro na aba '👤 Tutores'.")
    else:
        tutor_f = st.selectbox("Selecione o Dono:", ["--- Selecione ---"] + lista_tutores)
        
        if tutor_f != "--- Selecione ---":
            # Mostra pets já cadastrados para este tutor
            meus_pets = [p for p in st.session_state['pets'] if p['TUTOR'] == tutor_f]
            for p in meus_pets:
                st.info(f"🐕 **{p['PET']}** ({p['RAÇA']})")
                if st.button(f"🩺 Atender {p['PET']}", key=p['PET'], use_container_width=True):
                    st.session_state.pet_foco = f"{p['PET']} (Tutor: {tutor_f})"
                    st.session_state.aba_atual = "📋 Prontuário"
                    st.rerun()
            
            with st.expander("➕ Cadastrar Novo Pet para este Tutor"):
                with st.form("f_pet_v105"):
                    n_p = st.text_input("Nome do Pet").upper()
                    r_p = st.text_input("Raça").upper()
                    i_p = st.text_input("Idade/Nascimento")
                    if st.form_submit_button("💾 SALVAR PET", use_container_width=True):
                        if n_p:
                            st.session_state['pets'].append({"PET": n_p, "RAÇA": r_p, "TUTOR": tutor_f, "IDADE": i_p})
                            st.success(f"{n_p} cadastrado!")
                            st.rerun()

# --- 7. MÓDULO BACKUP ---
elif st.session_state.aba_atual == "💾 Backup":
    st.subheader("💾 Backup e Restauração")
    dados = {'clientes': st.session_state.clientes, 'pets': st.session_state.pets, 'historico': st.session_state.historico, 'caixa': st.session_state.caixa}
    st.download_button("📥 BAIXAR BACKUP", str(dados), file_name="backup_vet.txt", use_container_width=True)
    st.divider()
    arquivo = st.file_uploader("Restaurar do arquivo:", type="txt")
    if arquivo and st.button("🔄 RESTAURAR TUDO", use_container_width=True):
        d_rec = ast.literal_eval(arquivo.read().decode("utf-8"))
        st.session_state.clientes = d_rec.get('clientes', [])
        st.session_state.pets = d_rec.get('pets', [])
        st.session_state.historico = d_rec.get('historico', [])
        st.session_state.caixa = d_rec.get('caixa', [])
        st.success("✅ Dados recuperados!")
