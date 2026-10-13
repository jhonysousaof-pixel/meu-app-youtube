import streamlit as st
import yt_dlp
import requests
import urllib.parse

# 1. Configurações visuais iniciais do aplicativo
st.set_page_config(page_title="Modelador YT", page_icon="🚀", layout="wide")
st.title("🎬 Modelador de Conteúdo do YouTube")

url_video = st.text_input("Cole a URL do vídeo do YouTube aqui:")

# 2. Execução principal ao clicar no botão
if st.button("Analisar e Modelar Vídeo") and url_video:
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
                st.subheader("💡 Sugestões da IA")
                
                # Requisição para uma IA de texto alternativa e estável (Llama-3)
                prompt = f"Baseado no título '{titulo_orig}' e descrição '{desc_orig}', crie 3 novos títulos chamativos para o YouTube e uma descrição nova curta com SEO."
                prompt_codificado = urllib.parse.quote(prompt)
                url_texto_ia = f"https://pollinations.ai{prompt_codificado}"
                
                try:
                    resposta_ia = requests.get(url_texto_ia).text
                    st.write(resposta_ia)
                except:
                    st.write(f"1. {titulo_orig} Nova Versão\n2. Como ganhar dinheiro com {titulo_orig}\n3. Segredo revelado: {titulo_orig}")
                    st.write("Nova descrição otimizada gerada com base no tema original.")

                st.subheader("🖼️ Nova Capa Sugerida")
                
                # Gera um link de imagem limpo e seguro
                titulo_url = urllib.parse.quote(titulo_orig)
                url_img = f"https://pollinations.ai{titulo_url}?width=1280&height=720&nologo=true"
                
                # Exibe o botão de clique grande e limpo para abrir a imagem
                st.markdown(f"### [🖼️ CLIQUE AQUI PARA ABRIR E SALVAR SUA NOVA CAPA]({url_img})")
                st.caption("Clique no link azul acima para abrir a imagem gerada em alta resolução e fazer o download direto no seu celular.")

        except Exception as e:
            st.error(f"Erro ao processar: {e}")
            
