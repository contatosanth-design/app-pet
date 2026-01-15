import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- CSS PARA CORES E CONTRASTE ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59 !important; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold !important; }
    .header-box { background: white; padding: 20px; border-radius: 10px; border-left: 6px solid #2e7bcf; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO BANCO ---
for key in ['clientes', 'pets', 'historico', 'estoque']:
    if key not in st.session_state: st.session_state[key] = []

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=80)
    st.title("Ribeira Vet Pro")
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "📦 Produtos", "💰 Financeiro & Recibo"])

# --- CABEÇALHO ---
st.markdown(f"<div class='header-box'><h1 style='color:#1e3d59; margin:0;'>Ribeira Vet Pro</h1><p style='margin:0;'>Sistema Estabilizado • {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- 1. TUTORES (COM WHATSAPP E E-MAIL) ---
if menu == "👤 Tutores":
    st.subheader("📝 Cadastro de Tutor")
    with st.form("f_tutor", clear_on_submit=True):
        id_t = f"T{len(st.session_state['clientes']) + 1:03d}"
        nome = st.text_input("Nome Completo")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        zap = c2.text_input("WhatsApp (Ex: 5522985020463)")
        email = st.text_input("E-mail")
        end = st.text_area("Endereço")
        if st.form_submit_button("Salvar Tutor"):
            st.session_state['clientes'].append({"id": id_t, "nome": nome, "cpf": cpf, "zap": zap, "email": email, "end": end})
            st.success(f"Tutor {nome} salvo!")

# --- 2. PETS (COM TODOS OS PARÂMETROS) ---
elif menu == "🐾 Pets":
    st.subheader("🐶 Cadastro de Pet")
    if not st.session_state['clientes']: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            t_lista = {f"{c['id']} - {c['nome']}": c for c in st.session_state['clientes']}
            t_sel = st.selectbox("Proprietário", list(t_lista.keys()))
            nome_p = st.text_input("Nome do Pet")
            c1, c2 = st.columns(2)
            raca = c1.selectbox("Raça", ["SRD", "Spitz Alemão", "Poodle", "Shih Tzu", "Outra"])
            sexo = c2.selectbox("Sexo", ["Macho", "Fêmea"])
            if st.form_submit_button("Salvar Pet"):
                st.session_state['pets'].append({"id": f"P{len(st.session_state['pets']) + 1:03d}", "nome": nome_p, "tutor": t_lista[t_sel]})
                st.success(f"Pet {nome_p} cadastrado!")

# --- 3. PRONTUÁRIO IA ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento Clínico")
    if not st.session_state['pets']: st.info("Cadastre um pet.")
    else:
        with st.form("f_ia"):
            p_lista = {f"{p['id']} - {p['nome']}": p for p in st.session_state['pets']}
            pet_sel = st.selectbox("Paciente", list(p_lista.keys()))
            transcricao = st.text_area("Relato da Consulta (Win+H)", height=200)
            if st.form_submit_button("💾 SALVAR E IR PARA COBRANÇA"):
                st.session_state['historico'].append({"Data": datetime.now().strftime("%d/%m/%Y"), "Pet": p_lista[pet_sel]['nome'], "Resumo": transcricao})
                st.success("Prontuário salvo! Agora clique em 'Financeiro & Recibo' no menu lateral.")

# --- 4. PRODUTOS (CORREÇÃO DE ZEROS) ---
elif menu == "📦 Produtos":
    st.subheader("📦 Gestão de Itens")
    with st.form("f_prod", clear_on_submit=True):
        item = st.text_input("Nome do Item")
        preco = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
        if st.form_submit_button("Adicionar"):
            st.session_state['estoque'].append({"Item": item, "Preco": preco})
            st.success("Item adicionado!")
    
    if st.session_state['estoque']:
        df_prod = pd.DataFrame(st.session_state['estoque'])
        df_prod['Preco'] = df_prod['Preco'].map('R$ {:.2f}'.format)
        st.table(df_prod)

# --- 5. FINANCEIRO E RECIBO (CORREÇÃO DO ERRO) ---
elif menu == "💰 Financeiro & Recibo":
    st.subheader("💰 Cobrança e Emissão de Recibo")
    if not st.session_state['clientes'] or not st.session_state['estoque']:
        st.error("Cadastre tutores e produtos antes de cobrar.")
    else:
        with st.form("f_cobranca"):
            t_dados = {c['nome']: c for c in st.session_state['clientes']}
            tutor_nome = st.selectbox("Tutor para Cobrança", list(t_dados.keys()))
            
            itens_sel = st.multiselect("Procedimentos/Produtos", [i['Item'] for i in st.session_state['estoque']])
            desc = st.number_input("Desconto (R$)", min_value=0.0, format="%.2f")
            pagamento = st.selectbox("Forma de Pagamento", ["Pix", "Cartão", "Dinheiro"])
            
            gerar = st.form_submit_button("📄 GERAR RECIBO")

        if gerar:
            tutor_info = t_dados[tutor_nome]
            lista_precos = [i['Preco'] for i in st.session_state['estoque'] if i['Item'] in itens_sel]
            subtotal = sum(lista_precos)
            total = subtotal - desc
            
            st.markdown(f"""
            ---
            ### 📄 RECIBO DE ATENDIMENTO
            **Cliente:** {tutor_nome} | **WhatsApp:** {tutor_info['zap']}
            **Serviços:** {', '.join(itens_sel)}
            **Subtotal:** R$ {subtotal:.2f} | **Desconto:** R$ {desc:.2f}
            ## TOTAL: R$ {total:.2f} ({pagamento})
            ---
            """)
            
            # Link para WhatsApp
            msg = f"Olá {tutor_nome}, recibo Ribeira Vet:\nItens: {', '.join(itens_sel)}\nTotal: R$ {total:.2f}"
            st.markdown(f"[📲 Enviar Recibo via WhatsApp](https://wa.me/{tutor_info['zap']}?text={urllib.parse.quote(msg)})")

elif menu == "🏠 Dashboard":
    if st.session_state['historico']:
        st.write("### Histórico de Atendimentos")
        st.table(pd.DataFrame(st.session_state['historico']))
