import streamlit as st
import yt_dlp
from google import genai

# Configuração da página do site (Versão Clássica que está perfeita)
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
                    
                    # Nova instrução cirúrgica para clonar a capa e alterar apenas a pessoa
                    prompt_texto = f"""
                    Baseado nas informações deste vídeo do YouTube:
                    Título: {titulo_original}
                    Descrição: {descricao_original}
                    Link da capa original: {thumbnail_original}
                    
                    Faça o seguinte:
                    1. Crie 3 opções de títulos altamente chamativos (focados em clickbait saudável e retenção).
                    2. Reescreva a descrição inteira otimizando para o SEO do YouTube, incluindo parágrafos explicativos e sugestões de marcações de tempo estruturadas.
                    3. Escreva um prompt muito detalhado e completo EM INGLÊS para um gerador de imagens clonar esta capa original baseada no link fornecido.
                    
                    REGRAS OBRIGATÓRIAS PARA O PROMPT DA CAPA (ITEM 3):
                    - Não crie uma capa do zero ou aleatória. Faça engenharia reversa.
                    - Ordene que o gerador mantenha exatamente o mesmo cenário de fundo, a mesma disposição dos elementos, o mesmo esquema de cores e as MESMAS LETRAS E TEXTOS escritos no mesmo lugar.
                    - SE HOUVER UMA PESSOA NA CAPA ORIGINAL: Ordene que substitua a imagem dessa pessoa por outra pessoa diferente, mas mantendo a mesma pose e expressão.
                    - SE NÃO HOUVER NENHUMA PESSOA NA CAPA ORIGINAL: Ordene que adicione uma pessoa estrategicamente no layout para diferenciar, mantendo todo o resto do fundo e textos idênticos.
                    - Mude apenas para melhorar a tonalidade, nitidez e qualidade geral (4k, professional lighting).
                    
                    Responda estritamente separando os blocos com: [TITULOS], [DESCRICAO], [PROMPT_CAPA].
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt_texto
                    )
                    
                    resultado_ia = response.text
                    
                    # Separando as respostas da IA de forma limpa
                    try:
                        titulos_novos = resultado_ia.split("[TITULOS]").split("[DESCRICAO]").strip()
                        desc_nova = resultado_ia.split("[DESCRICAO]").split("[PROMPT_CAPA]").strip()
                        prompt_capa = resultado_ia.split("[PROMPT_CAPA]").strip()
                    except:
                        titulos_novos = "Veja o bloco completo abaixo."
                        desc_nova = resultado_ia
                        prompt_capa = f"A replica of the YouTube thumbnail layout for {titulo_original}, exact same background, same text typography, same words written. Swap the person's face/image for a different individual keeping the exact same pose and placement. High quality, 4k, professional lighting."

                    st.subheader("🔥 3 Novas Opções de Títulos")
                    st.code(titulos_novos, language="")

                    st.subheader("📝 Nova Descrição Otimizada (SEO)")
                    st.text_area("", value=desc_nova, height=250)
                    
                    # Prompt em inglês aberto e focado em clonar/modificar a pessoa
                    st.subheader("📋 Prompt Completo da Capa (Em Inglês)")
                    st.info("Copie o texto da caixa abaixo. Ele instrui qualquer IA a copiar o fundo e os textos da capa antiga, alterando apenas a pessoa:")
                    st.code(prompt_capa, language="")

            except Exception as e:
                st.error(f"Ocorreu um erro ao processar o link. Verifique se a URL está correta. Detalhes: {e}")
                    
