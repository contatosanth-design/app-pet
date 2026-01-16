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
# MÓDULO 4: FINANCEIRO (LIMPO E SEM ENGAVETAMENTO)
# =========================================================
elif menu == "💰 Financeiro":
    st.subheader("💰 Orçamento Rápido")

    if 'gaveta_aberta' not in st.session_state: st.session_state['gaveta_aberta'] = False
    if 'carrinho' not in st.session_state: st.session_state['carrinho'] = []

    # 1. ESCOLHA DE PRODUTOS (GAVETA)
    with st.expander("🔍 CLIQUE PARA VER A TABELA DE PREÇOS", expanded=st.session_state['gaveta_aberta']):
        st.write("Selecione o item para adicionar ao caderno:")
        for idx, produto in enumerate(st.session_state['estoque']):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"**{produto['Item']}**")
            c2.write(f"R$ {produto['Preco']:.2f}")
            if c3.button("➕", key=f"add_item_{idx}"):
                st.session_state['carrinho'].append({"Item": produto['Item'], "Preco": produto['Preco']})
                st.session_state['gaveta_aberta'] = False 
                st.rerun()

    # Botão simples para reabrir a lista sem poluir a tela
    if not st.session_state['gaveta_aberta']:
        st.button("🔍 Adicionar Itens", on_click=lambda: st.session_state.update({"gaveta_aberta": True}))

    st.divider()

    # 2. O ORÇAMENTO (VISUAL DE CADERNO ORGANIZADO)
    if st.session_state['clientes']:
        t_lista = {c['nome']: c for c in st.session_state['clientes']}
        t_nome = st.selectbox("Cliente", list(t_lista.keys()))
        
        if st.session_state['carrinho']:
            st.write("### 📝 Caderno de Orçamentos")
            
            # Criamos uma tabela organizada para evitar o engavetamento
            total_geral = 0
            
            # Cabeçalho Fixo
            st.markdown("---")
            col_cab1, col_cab2, col_cab3 = st.columns([4, 2, 1])
            col_cab1.write("**DESCRIÇÃO**")
            col_cab2.write("**VALOR**")
            col_cab3.write("**X**")
            st.markdown("---")

            # Linhas do Orçamento (Simulando o Excel)
            for i, item in enumerate(st.session_state['carrinho']):
                c_desc, c_val, c_del = st.columns([4, 2, 1])
                c_desc.write(f"{i+1:02d}. {item['Item']}")
                c_val.write(f"R$ {item['Preco']:.2f}")
                if c_del.button("❌", key=f"del_fin_{i}"):
                    st.session_state['carrinho'].pop(i)
                    st.rerun()
                total_geral += item['Preco']
            
            st.divider()
            st.markdown(f"## **TOTAL: R$ {total_geral:.2f}**")

            # Botões de Ação Final
            b1, b2 = st.columns(2)
            if b1.button("🗑️ Limpar Nota"):
                st.session_state['carrinho'] = []
                st.rerun()
            if b2.button("📲 WhatsApp"):
                zap = t_lista[t_nome]['zap']
                resumo = "\n".join([f"- {it['Item']}: R$ {it['Preco']:.2f}" for it in st.session_state['carrinho']])
                msg = f"Orçamento Ribeira Vet para {t_nome}:\n\n{resumo}\n\n*Total: R$ {total_geral:.2f}*"
                link = f"https://wa.me/{zap}?text={urllib.parse.quote(msg)}"
                st.markdown(f"#### [👉 Enviar pelo WhatsApp]({link})")
        else:
            st.info("O orçamento está vazio. Use o botão acima para adicionar produtos.")
