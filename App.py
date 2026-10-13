import streamlit as st
import yt_dlp
import requests
from google import genai

st.set_page_config(page_title="Modelador YT", page_icon="🚀", layout="wide")
st.title("🎬 Modelador de Conteúdo do YouTube")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Insira sua Gemini API Key:", type="password")

url_video = st.text_input("Cole a URL do vídeo do YouTube aqui:")

if st.button("Analisar e Modelar Vídeo") and url_video:
    if not api_key:
        st.error("Por favor, insira sua chave de API do Gemini para continuar.")
    else:
        with st.spinner("Buscando dados do YouTube..."):
            try:
                ydl_opts = {}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_video, download=False)
                    titulo_orig = info.get('title', 'Não encontrado')
                    desc_orig = info.get('description', 'Não encontrada')
                    tags_orig = info.get('tags', [])
                    thumb_orig = info.get('thumbnail', '')

                tab1, tab2 = st.tabs(["📊 Dados Originais", "✨ Versão IA"])

                with tab1:
                    st.subheader("Título Original")
                    st.code(titulo_orig)
                    if thumb_orig: st.image(thumb_orig, width=400)
                    st.subheader("Tags Encontradas")
                    if tags_orig: st.code(", ".join(tags_orig))
                    else: st.warning("Nenhuma tag encontrada.")

                with tab2:
                    client = genai.Client(api_key=api_key)
                    prompt = f"Baseado no título '{titulo_orig}' e descrição '{desc_orig}', crie 3 novos títulos chamativos, uma descrição nova com SEO e um prompt em inglês para gerar uma capa conceitual no formato [TITULOS], [DESCRICAO], [PROMPT_CAPA]."
                    response = client.models.generate_content(model='gemini-3.8-flash', contents=prompt)
                    
                    st.subheader("💡 Sugestões da IA")
                    st.write(response.text)
                    
                    st.subheader("🖼️ Nova Capa Sugerida")
                    url_img = f"https://pollinations.ai{requests.utils.quote(titulo_orig)}?width=1280&height=720&nologo=true"
                    st.markdown(f"[🖼️ Clique aqui para abrir e salvar sua Nova Capa]({url_img})")
                    st.caption("Clique no link acima para abrir a imagem gerada em alta resolução e fazer o download.")

            except Exception as e:
                st.error(f"Erro ao processar: {e}")
                    
