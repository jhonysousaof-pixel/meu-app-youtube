import streamlit as st
import yt_dlp
from google import genai

# Configuração da página do site (Versão Clássica que você aprovou)
st.set_page_config(page_title="Modelador de Conteúdo YT", page_icon="🚀", layout="wide")

st.title("🎬 Modelador e Validador de Conteúdo do YouTube")
st.caption("Cole o link de um vídeo de referência para extrair dados e criar uma versão totalmente nova com IA.")

# Puxa a chave de forma segura direto das configurações do Streamlit
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Insira sua Gemini API Key:", type="password")

url_video = st.text_input("Cole a URL do vídeo do YouTube aqui:")

if st.button("Analisar e Modelar Vídeo") and url_video:
    if not api_key:
        st.error("Por favor, insira sua chave de API do Gemini para continuar.")
    else:
        with st.spinner("Buscando dados do YouTube e gerando novas ideias..."):
            try:
                # 1. Extraindo dados do YouTube usando yt-dlp
                ydl_opts = {}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_video, download=False)
                    
                    titulo_original = info.get('title', 'Não encontrado')
                    descricao_original = info.get('description', 'Não encontrada')
                    tags_originais = info.get('tags', [])
                    thumbnail_original = info.get('thumbnail', '')

                # Criando as abas clássicas idênticas
                tab1, tab2 = st.tabs(["📊 Dados Originais Extraídos", "✨ Versão Modelada por IA"])

                with tab1:
                    st.subheader("Título Original")
                    st.code(titulo_original, language="")
                    
                    if thumbnail_original:
                        st.subheader("Capa Original")
                        st.image(thumbnail_original, width=400)

                    st.subheader("Tags Encontradas")
                    if tags_originais:
                        texto_tags = ", ".join(tags_originais)
                        st.code(texto_tags, language="")
                    else:
                        st.warning("Nenhuma tag oculta encontrada neste vídeo específico.")

                with tab2:
                    # 2. Conectando à API do Gemini para recriar o conteúdo (Modelo Oficial 3.8)
                    client = genai.Client(api_key=api_key)
                    
                    prompt_texto = f"""
                    Baseado nas informações deste vídeo do YouTube:
                    Título: {titulo_original}
                    Descrição: {descricao_original}
                    
                    Faça o seguinte:
                    1. Crie 3 opções de títulos altamente chamativos (focados em clickbait saudável e retenção).
                    2. Reescreva a descrição inteira otimizando para o SEO do YouTube, incluindo parágrafos explicativos e sugestões de marcações de tempo estruturadas.
                    3. Escreva um prompt muito detalhado e completo EM INGLÊS com mais de 30 palavras para um gerador de imagens criar uma capa/thumbnail conceitual semelhante e moderna sobre este tema.
                    
                    Responda estritamente separando os blocos com: [TITULOS], [DESCRICAO], [PROMPT_CAPA].
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt_texto
                    )
                    
                    resultado_ia = response.text
                    
                    # Separando as respostas da IA de forma limpa
                    try:
                        titulos_novos = resultado_ia.split("[TITULOS]")[1].split("[DESCRICAO]")[0].strip()
                        desc_nova = resultado_ia.split("[DESCRICAO]")[1].split("[PROMPT_CAPA]")[0].strip()
                        prompt_capa = resultado_ia.split("[PROMPT_CAPA]")[1].strip()
                    except:
                        # Caso a IA mude a formatação, exibe o texto corrido para não quebrar
                        titulos_novos = "Veja o bloco completo abaixo."
                        desc_nova = resultado_ia
                        prompt_capa = f"A vibrant and eye-catching YouTube thumbnail background about {titulo_original}, gaming style, hyper-detailed, 4k."

                    st.subheader("🔥 3 Novas Opções de Títulos")
                    st.code(titulos_novos, language="")

                    st.subheader("📝 Nova Descrição Otimizada (SEO)")
                    st.text_area("", value=desc_nova, height=250)
                    
                    # A MUDANÇA: Agora o prompt em inglês sai inteiro e livre de cortes, sem links com erro
                    st.subheader("📋 Prompt Completo da Capa (Em Inglês)")
                    st.info("Copie o texto da caixa abaixo e cole no ChatGPT, Leonardo AI ou qualquer outra IA para gerar sua imagem:")
                    st.code(prompt_capa, language="")

            except Exception as e:
                st.error(f"Ocorreu um erro ao processar o link. Verifique se a URL está correta. Detalhes: {e}")
                
