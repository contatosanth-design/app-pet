import streamlit as st
import pandas as pd
from datetime import datetime, date
import urllib.parse

# CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Ribeira Vet Pro v7.0", layout="wide")

# BANCO DE DADOS (MEMÓRIA)
if 'estoque' not in st.session_state:
    st.session_state['estoque'] = [
        {"Item": "Vacina V10 (Importada)", "Preco": 120.00},
        {"Item": "Vacina Antirrábica", "Preco": 60.00},
        {"Item": "Consulta Clínica", "Preco": 150.00},
        {"Item": "Hemograma Completo", "Preco": 95.00},
        {"Item": "Castração Macho", "Preco": 350.00}
    ]

for key in ['clientes', 'pets', 'historico']:
    if key not in st.session_state: st.session_state[key] = []

# MENU LATERAL - Define a variável 'menu' para evitar o NameError
with st.sidebar:
    st.title("Ribeira Vet Pro")
    st.info("Versão 7.0 - Estável")
    menu = st.radio("NAVEGAÇÃO", ["🏠 Dashboard", "👤 Tutores", "🐾 Pets", "🩺 Prontuário IA", "💰 Financeiro"])

# =========================================================
# MÓDULO 0: DASHBOARD (A NOVA CARA DO APP)
# =========================================================
if menu == "🏠 Dashboard":
    st.title("🏥 Bem-vindo ao Ribeira Vet Pro")
    st.write(f"Hoje é dia: **{date.today().strftime('%d/%m/%Y')}**")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Tutores", len(st.session_state['clientes']))
    col2.metric("🐾 Pacientes", len(st.session_state['pets']))
    col3.metric("🩺 Atendimentos", len(st.session_state['historico']))
    
    st.divider()
    
    st.subheader("⚡ Atalhos Rápidos")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("➕ Novo Tutor", use_container_width=True):
            st.info("Clique em '👤 Tutores' no menu lateral")
    with c2:
        if st.button("🐾 Cadastrar Pet", use_container_width=True):
            st.info("Clique em '🐾 Pets' no menu lateral")
    with c3:
        if st.button("💰 Gerar Recibo", use_container_width=True):
            st.info("Clique em '💰 Financeiro' no menu lateral")

    if st.session_state['historico']:
        st.subheader("📅 Últimos Atendimentos")
        st.table(pd.DataFrame(st.session_state['historico']).tail(5))
    else:
        st.info("Nenhum atendimento hoje. A lista aparecerá aqui após usar o Prontuário.")

# =========================================================
# MÓDULO 1: TUTORES (VERSÃO CORRIGIDA COM E-MAIL)
# =========================================================
elif menu == "👤 Tutores":
    st.subheader("📝 Cadastro de Tutores")
    with st.form("f_tutor", clear_on_submit=True):
        nome = st.text_input("Nome do Cliente*")
        c1, c2 = st.columns(2)
        cpf = c1.text_input("CPF")
        zap = c2.text_input("WhatsApp*")
        
        # Campo de E-mail recuperado da Versão 7.0
        email = st.text_input("E-mail para Boletas e Promoções") 
        
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("Salvar Tutor"):
            if nome and zap:
                st.session_state['clientes'].append({
                    "id": f"T{len(st.session_state['clientes'])+1:03d}", 
                    "nome": nome.upper(), 
                    "cpf": cpf, 
                    "zap": zap, 
                    "email": email, # Salvando o e-mail na ficha do cliente
                    "end": end
                })
                st.success(f"Tutor {nome.upper()} cadastrado com sucesso!")

# =========================================================
# MÓDULO 2: PETS
# =========================================================
elif menu == "🐾 Pets":
    st.subheader("🐾 Ficha do Paciente")
    if not st.session_state['clientes']:
        st.warning("Cadastre um tutor primeiro.")
    else:
        with st.form("f_pet"):
            t_lista = {f"{c['id']} - {c['nome']}": c['nome'] for c in st.session_state['clientes']}
            t_sel = st.selectbox("Proprietário*", list(t_lista.keys()))
            nome_p = st.text_input("Nome do Pet*")
            c1, c2, c3 = st.columns(3)
            especie = c1.selectbox("Espécie", ["Cão", "Gato", "Outro"])
            raca = c2.selectbox("Raça", ["SRD", "Pinscher", "Poodle", "Shih Tzu", "Pitbull", "Outra"])
            sexo = c3.selectbox("Sexo", ["Macho", "Fêmea"])
            
            nasc = st.date_input("Data de Nascimento", value=date(2020, 1, 1), format="DD/MM/YYYY")
            hoje = date.today()
            idade_real = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
            st.info(f"O paciente tem {idade_real} anos.")
            
            if st.form_submit_button("✅ Salvar Pet"):
                st.session_state['pets'].append({"nome": nome_p.upper(), "raca": raca, "idade": idade_real, "tutor": t_lista[t_sel]})
                st.success("Pet salvo!")

# =========================================================
# MÓDULO 3: PRONTUÁRIO IA (OTIMIZADO PARA VOZ)
# =========================================================
elif menu == "🩺 Prontuário IA":
    st.subheader("🩺 Atendimento Clínico")
    
    # Lembrete visual para garantir o foco do cursor
    st.warning("🎤 PARA DITAR: 1. Clique na caixa abaixo | 2. Aperte Win+H | 3. Fale após o sinal.")
    
    if st.session_state['pets']:
        # Seletor de Paciente
        p_sel = st.selectbox("Selecione o Paciente", [p['nome'] for p in st.session_state['pets']])
        
        c1, c2 = st.columns(2)
        peso = c1.text_input("Peso (kg)", placeholder="Ex: 12.5")
        temp = c2.text_input("Temperatura (°C)", placeholder="Ex: 38.5")
        
        # O campo de texto agora tem um 'key' único para ajudar o Windows a não perder o foco
        relato = st.text_area(
            "Evolução Clínica / Anamnese (O texto aparecerá aqui)", 
            height=300, 
            key="campo_ditado",
            placeholder="Clique aqui antes de começar a falar..."
        )
        
        if st.button("💾 Salvar Histórico da Consulta"):
            if relato:
                st.session_state['historico'].append({
                    "Data": date.today().strftime("%d/%m/%Y"), 
                    "Pet": p_sel, 
                    "Peso": peso,
                    "Relato": relato
                })
                st.success(f"Prontuário de {p_sel} arquivado com sucesso!")
            else:
                st.error("O relato está vazio. Digite ou dite algo antes de salvar.")
    else: 
        st.info("Nenhum pet cadastrado para atendimento.")

# =========================================================
# MÓDULO 4: FINANCEIRO (PREÇOS LIMPOS - 2 CASAS)
# =========================================================
elif menu == "💰 Financeiro":
    # Cabeçalho Estilo Canva
    st.markdown("""
        <div style="border: 2px solid black; padding: 10px; text-align: center; background-color: white;">
            <b style="font-size: 20px;">CONSULTÓRIO VETERINÁRIO RIBEIRA</b><br>
            <span>CRVV-RJ 9862 Ricardo Santos</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") 

    if 'carrinho' not in st.session_state: st.session_state['carrinho'] = []

    # Seletor de Itens
    with st.expander("🔍 TABELA DE PREÇOS", expanded=st.session_state.get('gaveta_aberta', False)):
        for idx, produto in enumerate(st.session_state['estoque']):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"**{produto['Item']}**")
            c2.write(f"R$ {produto['Preco']:.2f}")
            if c3.button("➕", key=f"add_fmt_{idx}"):
                st.session_state['carrinho'].append(produto)
                st.session_state['gaveta_aberta'] = False
                st.rerun()

    if st.session_state['carrinho']:
        st.markdown("### 📝 Orçamento Atual")
        
        # Criando a tabela e formatando os números
        df_exibir = pd.DataFrame(st.session_state['carrinho'])
        df_exibir.index = range(1, len(df_exibir) + 1)
        
        # A MÁGICA: Formata a coluna Preco para mostrar apenas 2 casas decimais
        df_exibir['Preco'] = df_exibir['Preco'].map('R$ {:,.2f}'.format)
        
        # Exibe a tabela com as colunas renomeadas como no seu rascunho
        st.table(df_exibir.rename(columns={'Item': 'DESCRIÇÃO', 'Preco': 'VALOR'})) 

        # Totalizador
        total = sum(item['Preco'] for item in st.session_state['carrinho'])
        st.markdown(f"<div style='text-align: right; border: 2px solid black; padding: 10px; font-size: 20px; background: #f0f2f6;'><b>VALOR TOTAL: R$ {total:.2f}</b></div>", unsafe_allow_html=True)

        st.write("")
        col_rem, col_limp, col_zap = st.columns([2, 1, 1])
        
        with col_rem:
            idx_escolhido = st.number_input("Remover item nº:", min_value=1, max_value=len(st.session_state['carrinho']), step=1)
            if st.button("❌ Remover"):
                st.session_state['carrinho'].pop(int(idx_escolhido)-1)
                st.rerun()
        
        if col_limp.button("🗑️ Limpar Tudo"):
            st.session_state['carrinho'] = []
            st.rerun()
            
        if col_zap.button("📲 WhatsApp"):
            st.success("Orçamento pronto para envio!")# =========================================================
# MÓDULO 5: GESTÃO DE TABELA DE PREÇOS (IMPORTADOR)
# =========================================================
elif menu == "⚙️ Tabela de Preços":
    st.subheader("⚙️ Configuração da Tabela de Preços")
    
    # OPÇÃO DE IMPORTAR EXCEL OU CSV
    with st.expander("📂 IMPORTAR TABELA EXTERNA (EXCEL/CSV)"):
        arquivo = st.file_uploader("Arraste seu arquivo de preços aqui", type=['xlsx', 'csv'])
        if arquivo:
            try:
                df_novo = pd.read_excel(arquivo) if arquivo.name.endswith('xlsx') else pd.read_csv(arquivo)
                if st.button("Confirmar Importação de Itens"):
                    for _, row in df_novo.iterrows():
                        st.session_state['estoque'].append({"Item": str(row[0]).upper(), "Preco": float(row[1])})
                    st.success("Tabela importada com sucesso!")
                    st.rerun()
            except Exception as e:
                st.error("Erro ao ler arquivo. Verifique se a 1ª coluna é o Nome e a 2ª é o Preço.")

    # Cadastro Manual
    with st.form("add_manual", clear_on_submit=True):
        st.write("➕ **Adicionar Manualmente**")
        c1, c2 = st.columns([3, 1])
        n_item = c1.text_input("Descrição do Serviço")
        n_preco = c2.number_input("Preço (R$)", min_value=0.0)
        if st.form_submit_button("Salvar Item"):
            if n_item:
                st.session_state['estoque'].append({"Item": n_item.upper(), "Preco": n_preco})
                st.rerun()
