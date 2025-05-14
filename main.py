import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders.csv_loader import CSVLoader
from typing import List
import json

load_dotenv()
# Configuração inicial
app_title = os.getenv("APP_TITLE")
sidebar_logo = os.getenv("SIDEBAR_LOGO")
main_body_logo = os.getenv("MAIN_BODY_LOGO")
app_footer = os.getenv("APP_FOOTER")
app_footer_link = os.getenv("APP_FOOTER_LINK")
app_footer_copy = os.getenv("APP_FOOTER_COPYRIGHT")
app_footer_copy_link = os.getenv("APP_FOOTER_COPYRIGHT_LINK")
msg_prompt = os.getenv("MSG_PROMPT")
st.set_page_config(page_title=app_title,page_icon=":material/robot_2:", layout="wide")
st.title("🤖 "+ app_title)
st.logo(image=sidebar_logo, size="medium", link=None, icon_image=sidebar_logo)

# Método de autenticação
def autenticar_usuario():
        with st.sidebar.expander("🔑 Credenciais", expanded=True):
            st.sidebar.markdown("### 🔒 Autenticação")
            usuario = st.sidebar.text_input("Usuário", key="usuario")
            senha = st.sidebar.text_input("Senha", type="password", key="senha")
            botao_login = st.sidebar.button("Entrar")
            
            if botao_login:
                if usuario == os.getenv("APP_USER") and senha == os.getenv("APP_PASSWORD"):
                    st.session_state.autenticado = True
                    st.sidebar.success("✅ Autenticado com sucesso!")
                else:
                    st.sidebar.error("❌ Usuário ou senha incorretos.")

            if "autenticado" not in st.session_state:
                st.session_state.autenticado = False

            if not st.session_state.autenticado:
                st.stop()

# Chamar o método de autenticação
autenticar_usuario()

# Ocultar sidebar de autenticação após login
if st.session_state.autenticado:
    st.sidebar.empty()

# Sidebar para credenciais

st.sidebar.header("🔐 Configurações")
api_key = os.getenv("GROQ_API_KEY")
if api_key:
    st.sidebar.markdown("**Chave da API Groq:**")
    st.sidebar.text_input("Chave da API Groq", value=api_key, type="password", disabled=True)
else:
    api_key = st.sidebar.text_input("Chave da API Groq", type="password")
    st.sidebar.markdown("**Dica:** Você pode encontrar sua chave de API Groq [aqui](https://console.groq.com/).")
startDate = st.sidebar.date_input("Data de início", value=None)
endDate = st.sidebar.date_input("Data de fim", value=None)
os.environ['GROQ_API_KEY'] = api_key

if "pergunta" not in st.session_state:
    st.session_state.pergunta = ""

# Sugestões de perguntas como no GPT
st.markdown("### 💬 Sugestões de perguntas")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Fonte de dados disponíveis"):
        st.session_state.pergunta = "Quais são as fontes de dados disponiveis?"
with col2:
    if st.button("Periodo de dados disponíveis"):
        st.session_state.pergunta = "Quais são os periodos de dados disponíveis?"
with col3:
    if st.button("Quantidade de gravações por operador"):
        st.session_state.pergunta = "Quantas chamadas por operador foram atendidas nos ultimos 5 dias?"
with col4:
    if st.button("Quantidade de gravações por skill"):
        st.session_state.pergunta = "Separe o volume de interações por Skill no mês corrente?"

# Campo de pergunta
st.markdown("### ✍️ Qual sua pergunta?")
st.markdown("**Exemplo:** Quantas chamadas foram atendidas no mês passado?")
pergunta = st.text_input("Digite sua pergunta:", 
                         value=st.session_state.pergunta, 
                         key="input_pergunta")

# --- FUNÇÕES AUXILIARES ---

chat = ChatGroq(model='llama-3.3-70b-versatile')

def resposta_bot(mensagens, documento,startDate, endDate):
    mensagem_system = msg_prompt
    st.session_state.mensagem_system = mensagem_system   
    if not mensagem_system:
        st.error("❌ Mensagem de sistema não encontrada. Verifique a variável de ambiente MSG_PROMPT.")
        return None
    else:
        mensagens_modelo = [('system', mensagem_system)]
        mensagens_modelo += mensagens
        template = ChatPromptTemplate.from_messages(mensagens_modelo)
        chain = template | chat
        return chain.invoke({'informacoes': documento, 'startDate' : startDate,'endDate' : endDate }).content

def carrega_csv():
    caminho = os.getenv("CSV_PATH")
    if not caminho:
        st.error("❌ Caminho do CSV não encontrado. Verifique a variável de ambiente CSV_PATH.")
        return None
    loader = CSVLoader(caminho,autodetect_encoding=True,encoding='utf-8', csv_args={'delimiter': ';'})
    lista_documentos = loader.load()
    # Convert the loaded data to a list of dictionaries
    json_list = []
    for page in lista_documentos:
        json_list.append(page.page_content) #or page.page_content if you want the content as well
    # Convert the list of dictionaries to JSON
    json_data = json.dumps(json_list, indent=4)
    return json_data


# Execução principal
if pergunta:
    st.markdown("### 🤖 Resposta do " + app_title)
    documento = carrega_csv()  
    if not documento:
        st.error("❌ Não foi possível carregar o CSV.")
        st.stop()
    else:
        if startDate and endDate:
            st.session_state.startDate = startDate
            st.session_state.endDate = endDate
            st.session_state.pergunta = pergunta
            mostrar_sql = st.toggle("👁️ Mostrar documento")
            if mostrar_sql:       
                st.write(f"Dados utilizados: {documento}")
            # Gerar resposta do bot
            resposta = resposta_bot([('user', pergunta)], documento, startDate = startDate, endDate = endDate)
            st.write(resposta)
        else:
            st.error("❌ Por favor, selecione as datas de início e fim.")
            st.stop()

st.markdown(f"""
    <style>
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            text-align: center;
           
            padding: 10px;
        }}
    </style>
    <div class="footer">
        <p>{app_footer} | <a href="{app_footer_link}">{app_footer_copy}</a> | <a href="{app_footer_copy_link}">Copyright</a></p>
    </div>
""", unsafe_allow_html=True)