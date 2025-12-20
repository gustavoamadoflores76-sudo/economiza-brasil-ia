import streamlit as st
import google.generativeai as genai

# Configuração com a sua chave que já está salva no Streamlit
genai.configure(api_key=st.secrets["GEMINI_CHAVE"])

# Aqui usamos o modelo Flash, que é o que você viu no Studio
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🛒 Economiza Brasil: Versão Google AI")

# Barra única para o produto
produto = st.text_input("O que você quer comparar hoje?")

if st.button("BUSCAR PREÇOS EM TEMPO REAL"):
    if produto:
        with st.spinner(f'Usando a inteligência do Google para buscar {produto}...'):
            try:
                # O comando abaixo pede para a IA buscar na web como se fosse você no Google
                prompt = f"Procure o preço de {produto} nos sites do Atacadão, Assaí, Fort Atacadista e Pão de Açúcar hoje. Liste o nome do mercado e o valor encontrado."
                response = model.generate_content(prompt)
                
                st.success("### Resultados encontrados:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Houve um erro na conexão: {e}")
    else:
        st.warning("Por favor, digite o nome de um produto.")
