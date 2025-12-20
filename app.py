import streamlit as st
import google.generativeai as genai

# SUA CHAVE INSERIDA DIRETAMENTE PARA NÃO DAR ERRO
genai.configure(api_key="AIzaSyAdG9iKuv0pnzi0ptQk40f1HDcmlAbnCJY")

# USANDO O MODELO FLASH (O MESMO DO SEU PRINT DO STUDIO)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Economiza Brasil", page_icon="🛒")
st.title("🛒 Economiza Brasil: Versão Google AI")

# BARRA DE PESQUISA ÚNICA
produto = st.text_input("Qual produto você quer comparar hoje?")

if st.button("BUSCAR PREÇOS AGORA"):
    if produto:
        with st.spinner(f'Consultando Atacadão, Assaí e Fort para achar {produto}...'):
            try:
                # O comando que faz a mágica acontecer
                prompt = f"Busque o preço atual do produto '{produto}' nos sites do Atacadão, Assaí e Fort Atacadista no Brasil. Liste as marcas (como Tio João, Camil, etc) e os preços de cada um. Responda em formato de lista organizada."
                response = model.generate_content(prompt)
                
                st.success("### Resultados encontrados:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Houve um problema técnico: {e}")
    else:
        st.warning("Por favor, digite o nome de um produto.")
