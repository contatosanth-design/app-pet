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
# MÓDULO 1: TUTORES (DISTRIBUIÇÃO DE ESPAÇO OTIMIZADA)
# =========================================================
elif menu == "👤 Tutores":
    st.subheader("👤 Gestão de Clientes")

    with st.form("form_tutor_v3", clear_on_submit=True):
        # Primeira Linha: Nome e Telefone (conforme sua imagem)
        c1, c2 = st.columns([3, 1])
        nome = c1.text_input("Nome Completo (Obrigatório) *")
        zap = c2.text_input("Telefone/WhatsApp")
        
        # Segunda Linha: Endereço (espaço total para endereços longos)
        endereco = st.text_input("Endereço Completo (Opcional)")
        
        # Terceira Linha: E-mail (opcional)
        email = st.text_input("E-mail (Opcional)")
        
        if st.form_submit_button("💾 Salvar Cadastro"):
            if nome:
                novo_tutor = {
                    "NOME": nome.upper(),
                    "TEL": zap if zap else "---",
                    "ENDEREÇO": endereco if endereco else "---",
                    "E-MAIL": email if email else "---"
                }
                st.session_state['clientes'].append(novo_tutor)
                # Reorganiza em Ordem Alfabética
                st.session_state['clientes'] = sorted(st.session_state['clientes'], key=lambda x: x['NOME'])
                st.success(f"Tutor {nome.upper()} salvo e organizado!")
                st.rerun()
            else:
                st.error("O Nome é obrigatório para o cadastro.")

    st.divider()
    
    # Lista com numeração automática e visual de grade
    if st.session_state['clientes']:
        st.write("📋 **Lista de Clientes Cadastrados**")
        df_tutores = pd.DataFrame(st.session_state['clientes'])
        
        # Numeração 01, 02... conforme o padrão do orçamento
        df_tutores.index = [f"{i+1:02d}" for i in range(len(df_tutores))]
        
        # Exibe a tabela com as linhas pretas (st.table é mais estável no notebook)
        st.table(df_tutores)

# =========================================================
# MÓDULO 2: PETS (FILTRO DE RAÇAS DINÂMICO)
# =========================================================
elif menu == "🐾 Pets":
    st.subheader("🐾 Gestão de Pacientes")

    # Listas de Raças
    racas_caes = ["SRD (Vira-lata)", "Shih-tzu", "Poodle", "Pinscher", "Golden Retriever", "Bulldog", "Yorkshire", "Dachshund", "Outra"]
    racas_gatos = ["SRD (Vira-lata)", "Persa", "Siamês", "Maine Coon", "Angorá", "Bengal", "Ragdoll", "Munchkin", "Outra"]

    with st.form("form_paciente_finalizado", clear_on_submit=True):
        # Layout inspirado no seu Canva
        c1, c2 = st.columns([3, 1])
        nome_pet = c1.text_input("Nome do Pet (Obrigatório) *")
        especie = c2.selectbox("Espécie", ["Cão", "Gato", "Outro"])
        
        c3, c4 = st.columns([1, 1])
        
        # Lógica de Alternância de Raças
        if especie == "Cão":
            raca = c3.selectbox("Raça do Cão", racas_caes)
        elif especie == "Gato":
            raca = c3.selectbox("Raça do Gato", racas_gatos)
        else:
            raca = c3.text_input("Especifique a Raça/Espécie")
            
        idade = c4.text_input("Idade (Ex: 2 anos)")

        # Puxa os Tutores já cadastrados no Módulo 1
        if st.session_state['clientes']:
            lista_t = [cli['NOME'] for cli in st.session_state['clientes']]
            tutor_p = st.selectbox("Tutor Responsável", lista_t)
        else:
            st.warning("⚠️ Cadastre um Tutor primeiro!")
            tutor_p = "Nenhum"

        # Botão posicionado corretamente dentro do formulário
        if st.form_submit_button("💾 Salvar Cadastro do Pet"):
            if nome_pet:
                novo_pet = {
                    "PET": nome_pet.upper(),
                    "TUTOR": tutor_p,
                    "ESPÉCIE": especie,
                    "RAÇA": raca,
                    "IDADE": idade if idade else "---"
                }
                st.session_state['pets'].append(novo_pet)
                st.success(f"Paciente {nome_pet.upper()} adicionado à lista!")
                st.rerun()
            else:
                st.error("O campo 'Nome do Pet' é obrigatório.")

    st.divider()

    # Exibição em grade estilo "caderno"
    if st.session_state['pets']:
        st.write("📋 **Lista de Pacientes**")
        df_p = pd.DataFrame(st.session_state['pets'])
        df_p.index = [f"{i+1:02d}" for i in range(len(df_p))]
        st.table(df_p)
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
# MÓDULO 4: FINANCEIRO (CABECALHO COMPLETO COM LOGO)
# =========================================================
elif menu == "💰 Financeiro":
    # Cabeçalho com o ícone do cachorrinho médico
    st.markdown("""
        <div style="display: flex; align-items: center; border: 2px solid black; padding: 10px; background-color: white; border-radius: 5px;">
            <div style="font-size: 50px; margin-right: 20px;">🐶⚕️</div>
            <div style="text-align: left;">
                <b style="font-size: 22px; color: #333;">Consultório Veterinário Ribeira</b><br>
                <span style="font-size: 14px; color: #666;">CRVV-RJ 9862 Ricardo Santos</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") 

    if 'carrinho' not in st.session_state: st.session_state['carrinho'] = []

    # 1. Tabela de Preços (Seletor)
    with st.expander("📋 TABELA DE PREÇOS", expanded=st.session_state.get('gaveta_aberta', False)):
        for idx, produto in enumerate(st.session_state['estoque']):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"**{produto['Item']}**")
            c2.write(f"R$ {produto['Preco']:.2f}")
            if c3.button("➕", key=f"add_final_{idx}"):
                st.session_state['carrinho'].append(produto)
                st.session_state['gaveta_aberta'] = False
                st.rerun()

    # 2. Orçamento com Preços Formatados
    if st.session_state['carrinho']:
        st.markdown("### 📝 Orçamento Atual")
        
        df_excluir = pd.DataFrame(st.session_state['carrinho'])
        df_excluir.index = range(1, len(df_excluir) + 1)
        
        # Formatação de Moeda
        df_mostrar = df_excluir.copy()
        df_mostrar['Preco'] = df_mostrar['Preco'].map('R$ {:,.2f}'.format)
        
        # Tabela Estável
        st.table(df_mostrar.rename(columns={'Item': 'DESCRIÇÃO', 'Preco': 'VALOR'})) 

        # Totalizador
        total = sum(item['Preco'] for item in st.session_state['carrinho'])
        st.markdown(f"<div style='text-align: right; border: 2px solid black; padding: 10px; font-size: 20px; background: #f0f2f6;'><b>VALOR TOTAL: R$ {total:.2f}</b></div>", unsafe_allow_html=True)

        st.write("")
        col_rem, col_limp, col_zap = st.columns([2, 1, 1])
        
        with col_rem:
            idx_rem = st.number_input("Remover item nº:", min_value=1, max_value=len(st.session_state['carrinho']), step=1)
            if st.button("❌ Remover Item"):
                st.session_state['carrinho'].pop(int(idx_rem)-1)
                st.rerun()
        
        if col_limp.button("🗑️ Limpar"):
            st.session_state['carrinho'] = []
            st.rerun()
            
        if col_zap.button("📲 WhatsApp"):
            st.success("Link gerado!")            
# =========================================================
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
