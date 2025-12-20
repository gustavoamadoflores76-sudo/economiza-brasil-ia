import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# CONFIGURAÇÃO
genai.configure(api_key=st.secrets["GEMINI_CHAVE"])
model = genai.GenerativeModel('gemini-pro')

st.title("🛒 Economiza Brasil: Ofertas do Dia")

produto = st.text_input("Qual alimento ou bebida você procura?")

def buscar_ofertas_abertas(item):
    with st.spinner('Vasculhando encartes e folhetos digitais...'):
        try:
            dados = ""
            with DDGS() as ddgs:
                # Mudamos a busca para focar em OFERTAS e ENCARTES (mais fácil de ler)
                query = f"preço {item} encarte oferta Atacadão Assaí Fort Pão de Açúcar"
                busca = list(ddgs.text(query, max_results=6))
                for r in busca:
                    dados += f"\n{r['body']}"
            
            if not dados:
                return "Não encontrei folhetos online para este produto agora."

            prompt = f"Analise estes encartes: {dados}. Qual o preço de '{item}'? Liste os mercados e valores encontrados."
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro ao acessar ofertas: {e}"

if st.button("🔍 VASCULHAR ENCARTES"):
    if produto:
        st.info(buscar_ofertas_abertas(produto))
