import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- CSS PROFISSIONAL ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59 !important; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold !important; }
    .header-box { background: white; padding: 20px; border-radius: 10px; border-left: 6px solid #2e7bcf; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO BANCO ---
for key in ['clientes', 'pets', 'historico', 'estoque', 'vendas']:
    if key not in st.session_state: st.session_state[key] = []

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=80)
    st.title("Ribeira Vet Pro")
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "📦 Produtos", "💰 Financeiro & Recibo"])

# --- CABEÇALHO ---
st.markdown(f"<div class='header-box'><h1 style='color:#1e3d59; margin:0;'>Ribeira Vet Pro</h1><p style='margin:0;'>Gestão e Cobrança • {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- 1. CADASTRO DE TUTORES (COM E-MAIL E WHATSAPP) ---
if menu == "👤 Tutores":
    st.subheader("📝 Ficha do Proprietário")
    with st.form("f_tutor", clear_on_submit=True):
        id_t = f"T{len(st.session_state['clientes']) + 1:03d}"
        nome = st.text_input("Nome Completo")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        zap = c2.text_input("WhatsApp (Ex: 22985020463)")
        email = st.text_input("E-mail para envio de recibo")
        end = st.text_area("Endereço")
        if st.form_submit_button("Salvar Tutor"):
            st.session_state['clientes'].append({"id": id_t, "nome": nome, "cpf": cpf, "zap": zap, "email": email, "end": end})
            st.success("Tutor cadastrado!")

# --- 2. CADASTRO DE PETS (CONFORME REQUISITADO) ---
elif menu == "🐾 Pets":
    st.subheader("🐶 Ficha do Animal")
    if not st.session_state['clientes']: st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            t_lista = {f"{c['id']} - {c['nome']}": c for c in st.session_state['clientes']}
            tutor_ref = st.selectbox("Proprietário", list(t_lista.keys()))
            c1, c2 = st.columns(2)
            nome_p = c1.text_input("Nome do Pet")
            raca = c2.selectbox("Raça", ["SRD", "Spitz Alemão", "Poodle", "Shih Tzu", "Outra"])
            sexo = st.selectbox("Sexo", ["Macho", "Fêmea"])
            castrado = st.radio("Castrado?", ["Sim", "Não"], horizontal=True)
            if st.form_submit_button("Cadastrar Pet"):
                st.session_state['pets'].append({"id": f"P{len(st.session_state['pets']) + 1:03d}", "nome": nome_p, "tutor": t_lista[tutor_ref]})
                st.success("Pet cadastrado!")

# --- 3. PRONTUÁRIO IA (COM BOTÃO DE COBRANÇA) ---
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento Clínico")
    if not st.session_state['pets']: st.info("Cadastre um pet.")
    else:
        with st.form("f_ia"):
            p_lista = {f"{p['id']} - {p['nome']}": p for p in st.session_state['pets']}
            pet_sel = st.selectbox("Selecione o Paciente", list(p_lista.keys()))
            relato = st.text_area("Resumo Clínico (Use Win+H para ditar)", height=200)
            if st.form_submit_button("💾 Salvar e IR PARA COBRANÇA"):
                st.session_state['historico'].append({"Data": datetime.now().strftime("%d/%m/%Y"), "Pet": p_lista[pet_sel]['nome'], "Resumo": relato})
                st.success("Prontuário salvo! Use o menu 'Financeiro' para fechar a conta.")

# --- 4. GESTÃO DE PRODUTOS (CORREÇÃO DE ZEROS) ---
elif menu == "📦 Produtos":
    st.subheader("📦 Catálogo de Preços")
    with st.form("f_prod", clear_on_submit=True):
        item = st.text_input("Nome do Produto/Vacina/Serviço")
        preco = st.number_input("Preço (R$)", min_value=0.0, format="%.2f", step=0.50)
        if st.form_submit_button("Adicionar"):
            st.session_state['estoque'].append({"Item": item, "Preco": preco})
            st.success("Item adicionado!")
    
    if st.session_state['estoque']:
        df_est = pd.DataFrame(st.session_state['estoque'])
        # Formatação para exibir apenas 2 casas decimais na tabela
        df_est['Preco'] = df_est['Preco'].map('R$ {:.2f}'.format)
        st.table(df_est)

# --- 5. FINANCEIRO E RECIBO (NOVO MÓDULO) ---
elif menu == "💰 Financeiro & Recibo":
    st.subheader("💰 Fechamento de Conta e Emissão de Recibo")
    if not st.session_state['clientes'] or not st.session_state['estoque']:
        st.error("Cadastre tutores e produtos primeiro.")
    else:
        t_dados = {c['nome']: c for c in st.session_state['clientes']}
        tutor_nome = st.selectbox("Selecione o Tutor para Cobrança", list(t_dados.keys()))
        tutor_info = t_dados[tutor_nome]
        
        itens_sel = st.multiselect("Procedimentos e Medicamentos", [i['Item'] for i in st.session_state['estoque']])
        desc = st.number_input("Desconto (R$)", min_value=0.0, format="%.2f")
        pagamento = st.selectbox("Forma de Pagamento", ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"])
        
        if st.form_submit_button("📄 GERAR RECIBO"):
            lista_precos = [i['Preco'] for i in st.session_state['estoque'] if i['Item'] in itens_sel]
            subtotal = sum(lista_precos)
            total = subtotal - desc
            
            # Montagem do Recibo para exibição
            st.markdown(f"""
            ---
            ### RECIBO - Ribeira Vet Pro
            **Cliente:** {tutor_nome} | **WhatsApp:** {tutor_info['zap']}
            **Itens:** {', '.join(itens_sel)}
            **Subtotal:** R$ {subtotal:.2f} | **Desconto:** R$ {desc:.2f}
            ## TOTAL A PAGAR: R$ {total:.2f}
            **Forma de Pagamento:** {pagamento}
            ---
            """)
            
            # Botão WhatsApp Automático
            texto_zap = f"Olá {tutor_nome}, segue seu recibo da Ribeira Vet Pro:\nItens: {', '.join(itens_sel)}\nTotal: R$ {total:.2f}\nPagamento: {pagamento}"
            link_zap = f"https://wa.me/{tutor_info['zap']}?text={urllib.parse.quote(texto_zap)}"
            st.markdown(f'[📲 Enviar Recibo por WhatsApp]( {link_zap} )')
