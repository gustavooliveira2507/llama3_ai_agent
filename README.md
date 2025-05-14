# llama3_ai_agent
Application made in python that uses langchain and groq to communicate with llama 3 and execute tasks through Rag model
You need to obtain a token from Groq through the website: https://console.groq.com/
Application made using streamlit, documentation available at https://docs.streamlit.io/
To run the project, run the command "streamlit run main.py"

#Variaveis de ambiente a serem configuradas no arquivo .env, com uma sugestão de prompt
APP_VERSION="1.0.0"
APP_DESCRIPTION="Sistema de gravação de chamadas "
APP_FOOTER="Sistema de gravação de chamadas"
APP_FOOTER_LINK=""
APP_FOOTER_LINK_TEXT=""
APP_FOOTER_COPYRIGHT="Copyright © 2025"
APP_FOOTER_COPYRIGHT_LINK="" 
GROQ_API_KEY=
APP_USER="admin"
APP_PASSWORD="admin"
APP_TITLE=""
SIDEBAR_LOGO=""
MAIN_BODY_LOGO=""
CSV_PATH=""
MSG_PROMPT= "Você é um assistente amigável chamado Llama 3 Bot.
  Você utiliza as seguintes informações para formular as suas respostas: {informacoes}
  filtre os dados entre as datas {startDate} e {endDate} usando a coluna Date.
  Segue uma breve descrição do que cada coluna contida nos dados acima representam
  Coluna A contém o nome da fonte de dados,
  coluna B é a chave unica da chamada para aquela fonte de dados,
  coluna Date é a data e hora que a chamada foi atendida, 
  Evitar respostas longas e complexas.
  Você deve responder de forma clara e objetiva, utilizando uma linguagem simples e direta."
