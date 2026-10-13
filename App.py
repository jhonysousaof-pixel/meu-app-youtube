import streamlit as st
import yt_dlp
import requests
import urllib.parse
from google import genai

# 1. Configurações visuais iniciais do aplicativo
st.set_page_config(page_title="Modelador YT", page_icon="🚀", layout="wide")
st.title("🎬 Modelador de Conteúdo do YouTube")

# 2. Gerenciamento seguro da chave de API do Gemini
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Insira sua Gemini API Key:", type="password")

url_video = st.text_input("Cole a URL do vídeo do YouTube aqui:")

# 3. Execução principal ao clicar no botão
if st.button("Analisar e Modelar Vídeo") and url_video:
    if not api_key:
        st.error("Por favor, insira sua chave de API do Gemini para continuar.")
    else:
        with st.spinner("Buscando dados do YouTube..."):
            try:
                # Extração dos dados do vídeo usando yt-dlp
                ydl_opts = {}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_video, download=False)
                    titulo_orig = info.get('title', 'Não encontrado')
                    desc_orig = info.get('description', 'Não encontrada')
                    tags_orig = info.get('tags', [])
                    thumb_orig = info.get('thumbnail', '')

                # Criação das abas estruturadas na tela
                tab1, tab2 = st.tabs(["📊 Dados Originais", "✨ Versão IA"])

                with tab1:
                    st.subheader("Título Original")
                    st.code(titulo_orig)
                    if thumb_orig: 
                        st.image(thumb_orig, width=400)
                    st.subheader("Tags Encontradas")
                    if tags_orig: 
                        st.code(", ".join(tags_orig))
                    else: 
                        st.warning("Nenhuma tag oculta encontrada neste vídeo específico.")

                with tab2:
                    # Conexão com o modelo oficial e obrigatório da Google
                    client = genai.Client(api_key=api_key)
                    prompt = f"Baseado no título '{titulo_orig}' e descrição '{desc_orig}', crie 3 novos títulos chamativos, uma descrição nova com SEO e um prompt em inglês de 1 parágrafo corrido para gerar uma capa conceitual no formato [TITULOS], [DESCRICAO], [PROMPT_CAPA]."
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                    
                    st.subheader("💡 Sugestões da IA")
                    st.write(response.text)
                    
                    st.subheader("🖼️ Nova Capa Sugerida")
                    
                    # Gera um link de imagem limpo e seguro usando formatação do Python
                    titulo_codificado = urllib.parse.quote(titulo_orig)
                    url_img = f"https://pollinations.ai{titulo_codificado}?width=1280&height=720&nologo=true"
                    
                    # Exibe o botão de clique grande e limpo para abrir a imagem
                    st.markdown(f"### [🖼️ CLIQUE AQUI PARA ABRIR E SALVAR SUA NOVA CAPA]({url_img})")
                    st.caption("Clique no link azul acima para abrir a imagem gerada em alta resolução e fazer o download direto no seu celular.")

            except Exception as e:
                st.error(f"Erro ao processar: {e}")
                
