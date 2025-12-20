import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# CONFIGURAÇÃO DA IA
genai.configure(api_key=st.secrets["GEMINI_CHAVE"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Economiza Brasil", page_icon="🛒")
st.title("🛒 Economiza Brasil")

# BARRA ÚNICA: UMA PALAVRA SÓ
produto = st.text_input("Qual produto você quer comparar?")

def buscar_precos(item):
    with st.spinner(f'Procurando {item} nos mercados...'):
        try:
            dados_brutos = ""
            # SITES REAIS DOS MERCADOS QUE VOCÊ MANDOU
            sites = [
                "atacadao.com.br",
                "fortatacadista.com.br",
                "assai.com.br",
                "paodeacucar.com"
            ]
            
            with DDGS() as ddgs:
                for s in sites:
                    # Força a IA a entrar no site do mercado
                    query = f"site:{s} {item} preço"
                    busca = list(ddgs.text(query, max_results=2))
                    for r in busca:
                        dados_brutos += f"\nMercado: {s} - Info: {r['body']}"
            
            if not dados_brutos:
                return "Não encontrei o produto nesses mercados hoje."

            prompt = f"Com base nestes dados: {dados_brutos}. Qual o preço mais barato para '{item}'? Responda o nome do mercado e o valor."
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro na busca: {e}"

if st.button("BUSCAR AGORA"):
    if produto:
        resultado = buscar_precos(produto)
        st.success(resultado)
