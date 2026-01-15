import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN E CONTRASTE ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59 !important; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold !important; }
    .header-box { background: white; padding: 20px; border-radius: 10px; border-left: 6px solid #2e7bcf; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO E CADASTRO AUTOMÁTICO DE PRODUTOS ---
if 'estoque' not in st.session_state or len(st.session_state['estoque']) == 0:
    # Carga automática de 20 itens comuns conforme solicitado
    st.session_state['estoque'] = [
        {"Item": "Vacina V10 (Importada)", "Preco": 120.00}, {"Item": "Vacina Antirrábica", "Preco": 60.00},
        {"Item": "Consulta Geral", "Preco": 150.00}, {"Item": "Hemograma Completo", "Preco": 90.00},
        {"Item": "Simparic 10-20kg", "Preco": 85.00}, {"Item": "Bravecto Cães", "Preco": 190.00},
        {"Item": "Castração Macho (Cão)", "Preco": 350.00}, {"Item": "Limpeza de Tártaro", "Preco": 250.00},
        {"Item": "Meloxicam Injetável", "Preco": 45.00}, {"Item": "Ceftriaxona", "Preco": 55.00},
        {"Item": "Aplicação de Microchip", "Preco": 110.00}, {"Item": "Ultrassom Abdominal", "Preco": 220.00},
        {"Item": "Internação Diária", "Preco": 180.00}, {"Item": "Vacina de Gripe (Pneumodog)", "Preco": 100.00},
        {"Item": "Vacina Giárdia", "Preco": 110.00}, {"Item": "Vermífugo (Drontal)", "Preco": 35.00},
        {"Item": "Curativo Simples", "Preco": 40.00}, {"Item": "Fluidoterapia", "Preco": 75.00},
        {"Item": "Otosys (Ouvido)", "Preco": 65.00}, {"Item": "Corte de Unhas", "Preco": 25.00}
    ]

for key in ['clientes', 'pets', 'historico']:
    if key not in st.session_state: st.session_state[key] = []

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=80)
    st.title("Ribeira Vet Pro")
    st.divider()
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "📦 Produtos & Estoque", "💰 Financeiro & Recibo"])

# --- CABEÇALHO ---
st.markdown(f"<div class='header-box'><h1 style='color:#1e3d59; margin:0;'>Ribeira Vet Pro</h1><p style='margin:0;'>Clínica Veterinária • {datetime.now().strftime('%d/%m/%Y')}</p></div>", unsafe_allow_html=True)

# --- 1. PRONTUÁRIO IA (COM PARÂMETROS CLÍNICOS) ---
if menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento com Parâmetros Clínicos")
    if not st.session_state['pets']: st.info("Cadastre um pet primeiro.")
    else:
        with st.form("f_ia"):
            p_lista = {f"{p['id']} - {p['nome']}": p for p in st.session_state['pets']}
            pet_sel = st.selectbox("Selecione o Paciente", list(p_lista.keys()))
            
            c1, c2, c3 = st.columns(3)
            peso = c1.text_input("Peso (kg)")
            temp = c2.text_input("Temperatura (°C)")
            vacinado = c3.selectbox("Status Vacinal", ["Em dia", "Atrasado", "Não informado"])
            
            vacinas_tomadas = st.text_input("Vacinas já tomadas (Histórico)")
            relato = st.text_area("Transcrição da Consulta (Win+H)", height=150)
            
            if st.form_submit_button("💾 SALVAR E IR PARA COBRANÇA"):
                st.session_state['historico'].append({
                    "Data": datetime.now().strftime("%d/%m/%Y"), 
                    "Pet": p_lista[pet_sel]['nome'], 
                    "Peso": peso, "Temp": temp, "Status_Vac": vacinado,
                    "Historico_Vac": vacinas_tomadas, "Relato": relato
                })
                st.success("Prontuário arquivado! Acesse 'Financeiro' para cobrar.")

# --- 2. PRODUTOS (EDIÇÃO E CARGA AUTOMÁTICA) ---
elif menu == "📦 Produtos & Estoque":
    st.subheader("📦 Catálogo de Produtos e Serviços")
    st.info("💡 20 itens iniciais foram cadastrados automaticamente para facilitar seu trabalho.")
    
    # Exibir e Editar Preços
    for i, prod in enumerate(st.session_state['estoque']):
        c1, c2, c3 = st.columns([3, 2, 1])
        c1.write(f"**{prod['Item']}**")
        novo_p = c2.number_input("Preço R$", value=float(prod['Preco']), key=f"p_{i}", format="%.2f")
        if c3.button("Atualizar", key=f"b_{i}"):
            st.session_state['estoque'][i]['Preco'] = novo_p
            st.success("Preço atualizado!")
            st.rerun()

# --- 3. FINANCEIRO (CORREÇÃO FINAL) ---
elif menu == "💰 Financeiro & Recibo":
    st.subheader("💰 Fechamento de Conta")
    if not st.session_state['clientes']: st.error("Cadastre um tutor primeiro.")
    else:
        with st.form("f_fin"):
            t_dados = {c['nome']: c for c in st.session_state['clientes']}
            tutor_nome = st.selectbox("Tutor", list(t_dados.keys()))
            itens_sel = st.multiselect("Procedimentos/Produtos", [i['Item'] for i in st.session_state['estoque']])
            desc = st.number_input("Desconto (R$)", format="%.2f")
            pagamento = st.selectbox("Modo de Pagamento", ["Pix", "Dinheiro", "Cartão Débito", "Cartão Crédito"])
            
            if st.form_submit_button("📄 GERAR RECIBO"):
                t_info = t_dados[tutor_nome]
                precos = [i['Preco'] for i in st.session_state['estoque'] if i['Item'] in itens_sel]
                total = sum(precos) - desc
                
                st.markdown(f"### RECIBO FINAL - {tutor_nome}")
                st.write(f"**WhatsApp:** {t_info['zap']}")
                st.write(f"**Itens:** {', '.join(itens_sel)}")
                st.subheader(f"VALOR TOTAL: R$ {total:.2f}")
                
                # Link WhatsApp
                msg = f"Olá {tutor_nome}, recibo Ribeira Vet Pro:\nTotal: R$ {total:.2f}\nPagamento: {pagamento}"
                st.markdown(f"[📲 Enviar Recibo via WhatsApp](https://wa.me/{t_info['zap']}?text={urllib.parse.quote(msg)})")

# --- CADASTRO TUTOR E PETS (MANTIDOS) ---
elif menu == "👤 Tutores":
    st.subheader("👤 Cadastro de Tutor")
    with st.form("f_t"):
        nome = st.text_input("Nome")
        zap = st.text_input("WhatsApp (Ex: 5522985020463)")
        if st.form_submit_button("Salvar"):
            st.session_state['clientes'].append({"nome": nome, "zap": zap})
            st.success("Salvo!")

elif menu == "🐾 Pets":
    st.subheader("🐾 Cadastro de Pet")
    with st.form("f_p"):
        nome_p = st.text_input("Nome do Pet")
        if st.form_submit_button("Salvar Pet"):
            st.session_state['pets'].append({"id": "P001", "nome": nome_p})
            st.success("Pet Salvo!")

elif menu == "🏠 Dashboard":
    st.subheader("📊 Histórico Clínico")
    if st.session_state['historico']:
        st.dataframe(pd.DataFrame(st.session_state['historico']), use_container_width=True)
