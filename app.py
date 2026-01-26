import streamlit as st
from datetime import datetime
import urllib.parse
import ast

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="Ribeira Vet Pro", layout="centered")

# Garantia de Memória
for k in ['clientes', 'pets', 'historico']:
    if k not in st.session_state: st.session_state[k] = []

if 'aba_atual' not in st.session_state: st.session_state.aba_atual = "👤 Tutores"

# --- 2. MENU LATERAL ---
with st.sidebar:
    st.title("🐾 Ribeira Vet")
    opcoes = ["👤 Tutores", "🐾 Pets", "📋 Prontuário", "💾 Backup"]
    escolha = st.radio("NAVEGAÇÃO", opcoes, index=opcoes.index(st.session_state.aba_atual))
    st.session_state.aba_atual = escolha

# --- 3. MÓDULO TUTORES ---
if st.session_state.aba_atual == "👤 Tutores":
    st.subheader("👤 Cadastro de Clientes")
    with st.form("f_tutor"):
        f_nome = st.text_input("Nome do Tutor *").upper()
        f_tel = st.text_input("WhatsApp")
        f_email = st.text_input("E-mail")
        f_end = st.text_area("Endereço")
        if st.form_submit_button("💾 SALVAR CLIENTE", use_container_width=True):
            if f_nome:
                st.session_state['clientes'].append({"NOME": f_nome, "TEL": f_tel, "EMAIL": f_email, "END": f_end})
                st.success(f"{f_nome} salvo! Agora vá na aba Pets.")
                st.rerun()

# --- 4. MÓDULO PETS (CORRIGIDO PARA NÃO FICAR EM BRANCO) ---
elif st.session_state.aba_atual == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pacientes")
    
    lista_nomes_tutores = [c['NOME'] for c in st.session_state['clientes']]
    
    if not lista_nomes_tutores:
        st.error("🛑 NENHUM CLIENTE ENCONTRADO!")
        st.info("Para cadastrar um Pet, o senhor precisa primeiro cadastrar o Tutor ou Restaurar o Backup.")
        if st.button("➡️ Ir para Cadastro de Tutor"):
            st.session_state.aba_atual = "👤 Tutores"
            st.rerun()
    else:
        t_f = st.selectbox("Selecione o Tutor:", ["--- Selecione ---"] + lista_nomes_tutores)
        
        if t_f != "--- Selecione ---":
            # Mostra pets já cadastrados
            meus_pets = [p for p in st.session_state['pets'] if p['TUTOR'] == t_f]
            for p in meus_pets:
                st.info(f"🐕 **{p['PET']}** ({p['RAÇA']})")
            
            # Formulário sempre visível após selecionar o tutor
            with st.form("f_novo_pet"):
                st.write(f"➕ Novo Pet para {t_f}")
                n_p = st.text_input("Nome do Pet").upper()
                r_p = st.text_input("Raça").upper()
                d_n = st.text_input("Nascimento (DD/MM/AAAA)")
                if st.form_submit_button("💾 SALVAR PET"):
                    if n_p:
                        st.session_state['pets'].append({"PET": n_p, "RAÇA": r_p, "NASCIMENTO": d_n, "TUTOR": t_f})
                        st.success("Pet cadastrado!")
                        st.rerun()

# --- MÓDULO BACKUP (Obrigatório usar após o erro) ---
elif st.session_state.aba_atual == "💾 Backup":
    st.subheader("💾 Backup e Restauração")
    dados = {'clientes': st.session_state.clientes, 'pets': st.session_state.pets, 'historico': st.session_state.historico}
    st.download_button("📥 BAIXAR BACKUP", str(dados), file_name="backup_vet.txt", use_container_width=True)
    
    st.divider()
    arquivo = st.file_uploader("Restaurar dados que sumiram:", type="txt")
    if arquivo and st.button("🔄 RESTAURAR AGORA"):
        d_rec = ast.literal_eval(arquivo.read().decode("utf-8"))
        st.session_state.clientes = d_rec.get('clientes', [])
        st.session_state.pets = d_rec.get('pets', [])
        st.session_state.historico = d_rec.get('historico', [])
        st.success("✅ Tudo recuperado!")
        st.rerun()
