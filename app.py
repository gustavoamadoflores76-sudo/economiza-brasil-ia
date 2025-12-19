import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# CONFIGURAÇÃO DE SEGURANÇA
try:
    genai.configure(api_key=st.secrets["GEMINI_CHAVE"])
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Erro na chave: {e}")

st.title("🛒 Economiza Brasil: Comparador")

produto = st.text_input("O que você busca? (Ex: Feijão)")
cidade = st.text_input("Sua cidade? (Ex: Corumbá)")

def buscar_precos(item, local):
    # Damos mais tempo e tentamos uma busca mais simples
    with st.spinner('Aguarde... A IA está lendo os encartes online...'):
        try:
            resultados = ""
            with DDGS() as ddgs:
                # Busca simplificada para não travar
                query = f"preço {item} hoje {local} Atacadão Assaí"
                search_results = list(ddgs.text(query, max_results=3))
                for r in search_results:
                    resultados += f"\n{r['body']}"
            
            if not resultados:
                return "Não encontrei preços online agora. Tente pesquisar um produto mais comum."

            prompt = f"Com base nesses dados: {resultados}. Qual o preço do {item} em {local}? Responda de forma curta."
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"A IA está sobrecarregada. Tente clicar novamente em 5 segundos! (Erro: {e})"

if st.button("🔍 COMPARAR AGORA"):
    if produto and cidade:
        resultado = buscar_precos(produto, cidade)
        st.info(resultado)
    else:
        st.warning("Preencha os dois campos.")
