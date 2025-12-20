import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# CONFIGURAÇÃO DA IA (Usando sua chave salva)
genai.configure(api_key=st.secrets["GEMINI_CHAVE"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Economiza Brasil", page_icon="🛒")
st.title("🛒 Economiza Brasil")

# BARRA ÚNICA COMO VOCÊ PEDIU
produto = st.text_input("Digite o produto (Ex: Banana, Arroz, Ração):")

def buscar_precos_real(item):
    with st.spinner(f'Vasculhando ofertas de {item}...'):
        try:
            dados_encontrados = ""
            # BUSCA AMPLIADA NOS MERCADOS QUE VOCÊ ESPECIFICOU
            with DDGS() as ddgs:
                # Pesquisamos nos sites oficiais e em encartes atuais
                query = f"{item} preço hoje Atacadão Assaí Fort Pão de Açúcar"
                busca = list(ddgs.text(query, max_results=5))
                for r in busca:
                    dados_encontrados += f"\nInfo: {r['body']}"
            
            if not dados_encontrados:
                return "Não encontrei preços para este produto nos sites agora. Tente ser mais específico (ex: Banana Nanica)."

            prompt = f"""
            Analise estes dados reais: {dados_encontrados}
            Qual o preço médio ou oferta encontrada para '{item}' no Atacadão, Assaí, Fort ou Pão de Açúcar?
            Responda APENAS os valores e os nomes dos mercados. Seja curto.
            """
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro ao acessar os mercados: {e}"

if st.button("ENCONTRAR PREÇO"):
    if produto:
        resultado = buscar_precos_real(produto)
        st.info(resultado)
    else:
        st.warning("Por favor, digite uma palavra.")
