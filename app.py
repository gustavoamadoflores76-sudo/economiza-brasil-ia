import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# Configuração da IA (Pegando a chave que você já salvou nos Secrets)
try:
    genai.configure(api_key=st.secrets["GEMINI_CHAVE"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("Erro ao carregar a chave de IA.")

st.set_page_config(page_title="Economiza Brasil", page_icon="🛒")
st.title("🛒 Economiza Brasil: Comparador Direto")
st.write("Busca inteligente no Atacadão, Assaí, Pão de Açúcar e Fort Atacadista.")

# Apenas uma barra de pesquisa agora, como você pediu
produto = st.text_input("O que você deseja comprar? (Ex: Arroz, Cerveja, Ração, Nutella)")

def buscar_nos_links(item):
    with st.spinner(f'Consultando sites oficiais...'):
        try:
            resultados_texto = ""
            # Definimos os alvos fixos para a IA não se perder
            mercados_alvo = [
                "atacadao.com.br", 
                "assai.com.br", 
                "paodeacucar.com", 
                "fortatacadista.com.br"
            ]
            
            with DDGS() as ddgs:
                # A IA agora busca especificamente DENTRO desses domínios
                for site in mercados_alvo:
                    query = f"site:{site} preço {item} oferta"
                    busca = list(ddgs.text(query, max_results=2))
                    for r in busca:
                        resultados_texto += f"\nNo site {site}: {r['body']}"
            
            if not resultados_texto:
                return "Não encontrei ofertas digitais agora. Tente mudar a marca ou o nome do produto."

            prompt = f"""
            Você é um comparador de preços. Analise estes dados dos sites oficiais:
            {resultados_texto}
            
            Diga qual o menor preço encontrado para '{item}' e em qual desses sites ele está.
            Se houver marcas diferentes, liste-as rapidamente.
            """
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Ocorreu um erro na busca: {e}. Tente novamente."

if st.button("🔍 ENCONTRAR MENOR PREÇO"):
    if produto:
        resultado = buscar_nos_links(produto)
        st.success("### Melhores Opções Encontradas:")
        st.write(resultado)
    else:
        st.warning("Por favor, digite o nome de um alimento ou bebida.")
