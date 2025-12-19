import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# 1. Configuração Segura: A IA pega a chave do 'cofre' do site
try:
    genai.configure(api_key=st.secrets["GEMINI_CHAVE"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("Aguardando configuração da chave secreta...")

st.title("🛒 Economiza Brasil: Comparador Nacional")

# 2. Interface para o cliente
produto = st.text_input("O que você quer comprar? (Ex: Arroz 5kg)")
cidade = st.text_input("Qual sua cidade e estado? (Ex: Corumbá - MS)")

def buscar_promocoes(item, local):
    with st.spinner(f'IA vasculhando Atacadão, Assaí e Fort em {local}...'):
        try:
            with DDGS() as ddgs:
                # Busca focada nos sites dos grandes mercados brasileiros
                query = f"preço {item} hoje site oficial {local} Atacadão Assaí Fort Pão de Açúcar"
                busca = list(ddgs.text(query, max_results=5))
                texto_busca = "\n".join([b['body'] for b in busca])
            
            # A IA analisa os dados e decide quem está mais barato
            prompt = f"Analise estes dados de mercado para {item} em {local}: {texto_busca}. Diga qual mercado está mais barato e dê dicas de economia."
            return model.generate_content(prompt).text
        except:
            return "Erro ao buscar. Tente clicar novamente!"

if st.button("🔍 COMPARAR PREÇOS AGORA"):
    if produto and cidade:
        resultado = buscar_promocoes(produto, cidade)
        st.success(resultado)
    else:
        st.warning("Preencha o produto e a cidade.")
