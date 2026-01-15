import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Configuração da Página
st.set_page_config(page_title="Ribeira Vet Pro", layout="wide")

# --- DESIGN E ESTILO ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3d59; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #2e7bcf; color: white; border-radius: 5px; width: 100%; }
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
if 'clientes' not in st.session_state: st.session_state['clientes'] = {}
if 'pets' not in st.session_state: st.session_state['pets'] = []
if 'historico' not in st.session_state: st.session_state['historico'] = []

# --- MENU LATERAL ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/contatosanth-design/app-pet/main/Squash_pet%20(1).png", use_container_width=True)
    st.markdown("<h2 style='text-align: center;'>Ribeira Vet Pro</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MENU", ["🏠 Início & Excel", "🎉 Aniversariantes", "👤 Cadastro Tutor", "🐶 Cadastro Pet", "🩺 Prontuário IA"])

# --- 🏠 PÁGINA: INÍCIO E EXPORTAÇÃO EXCEL ---
if menu == "🏠 Início & Excel":
    st.title("📊 Painel de Controle e Arquivos")
    
    # Métricas rápidas
    c1, c2 = st.columns(2)
    c1.metric("Total de Tutores", len(st.session_state['clientes']))
    c2.metric("Total de Pacientes", len(st.session_state['pets']))
    
    st.divider()
    st.subheader("📁 Exportar Banco de Dados (Excel)")
    
    if st.session_state['historico']:
        df = pd.DataFrame(st.session_state['historico'])
        # Formatação da data para o Excel (Padrão BR)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Consultas')
        
        st.download_button(
            label="📥 Baixar Planilha de Atendimentos",
            data=output.getvalue(),
            file_name=f"historico_consultas_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.dataframe(df) # Exibe a prévia da planilha
    else:
        st.info("Nenhum atendimento realizado para gerar planilha.")

# --- 🎉 PÁGINA: ANIVERSARIANTES ---
elif menu == "🎉 Aniversariantes":
    st.title("🎂 Aniversariantes do Dia")
    hoje = datetime.now().strftime("%d/%m")
    encontrou = False
    for p in st.session_state['pets']:
        if p['nascimento'].strftime("%d/%m") == hoje:
            encontrou = True
            tutor = st.session_state['clientes'].get(p['cod_tutor'], {})
            st.success(f"🐾 **{p['nome']}** faz anos hoje! (Tutor: {tutor.get('nome')})")
    if not encontrou: st.info("Sem aniversários hoje.")

# --- 👤 PÁGINA: CADASTRO TUTOR ---
elif menu == "👤 Cadastro Tutor":
    st.title("👤 Cadastro de Proprietário")
    with st.form("f_tutor"):
        id_t = f"T-{len(st.session_state['clientes'])+1:04d}"
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome Completo")
        cpf = c2.text_input("CPF")
        zap = c1.text_input("WhatsApp")
        email = c2.text_input("E-mail")
        end = st.text_area("Endereço Completo")
        if st.form_submit_button("Salvar Tutor"):
            st.session_state['clientes'][id_t] = {"nome": nome, "zap": zap, "email": email, "cpf": cpf, "end": end}
            st.success("Tutor cadastrado!")

# --- 🐶 PÁGINA: CADASTRO PET ---
elif menu == "🐶 Cadastro Pet":
    st.title("🐶 Cadastro de Paciente")
    if not st.session_state['clientes']: st.warning("Cadastre o tutor primeiro.")
    else:
        with st.form("f_pet"):
            tutores = [f"{k} - {v['nome']}" for k, v in st.session_state['clientes'].items()]
            tutor_sel = st.selectbox("Proprietário", tutores)
            nome_p = st.text_input("Nome do Animal")
            # Data de Nascimento com calendário BR
            nasc = st.date_input("Data de Nascimento", format="DD/MM/YYYY")
            raca = st.text_input("Raça")
            if st.form_submit_button("Salvar Pet"):
                st.session_state['pets'].append({
                    "nome": nome_p, "nascimento": nasc, "raca": raca, 
                    "cod_tutor": tutor_sel.split(" - ")[0], "tutor_nome": tutor_sel.split(" - ")[1]
                })
                st.success("Pet cadastrado!")

# --- 🩺 PÁGINA: PRONTUÁRIO COM TRANSCRIÇÃO ---
elif menu == "🩺 Prontuário IA":
    st.title("🩺 Atendimento com Transcrição de Voz")
    st.info("🎤 **Dica do Doutor:** Clique no campo e use 'Windows + H' para transcrever a conversa automaticamente.")
    
    if not st.session_state['pets']: st.info("Cadastre um pet primeiro.")
    else:
        with st.form("f_atend_ia"):
            pet_sel = st.selectbox("Selecione o Paciente", [p['nome'] for p in st.session_state['pets']])
            c1, c2 = st.columns(2)
            peso = c1.text_input("Peso (kg)")
            temp = c2.text_input("Temperatura (°C)")
            
            st.subheader("📝 Evolução Clínica (Transcrição)")
            # Campo onde a IA de voz do sistema vai escrever
            anamnese = st.text_area("Relato do Tutor e Diagnóstico", height=200, help="Use o ditado do seu teclado aqui.")
            
            if st.form_submit_button("💾 Finalizar e Arquivar"):
                # Captura dados do pet para o histórico
                pet_data = next(item for item in st.session_state['pets'] if item["nome"] == pet_sel)
                
                atendimento = {
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Tutor": pet_data['tutor_nome'],
                    "Paciente": pet_sel,
                    "Peso": peso,
                    "Temp": temp,
                    "Transcricao_Consulta": anamnese
                }
                st.session_state['historico'].append(atendimento)
                st.success("Atendimento arquivado na planilha!")
