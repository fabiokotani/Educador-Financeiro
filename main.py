import streamlit as st
from groq import Groq
import os

# 1. Configuração da Página
st.set_page_config(page_title="Educador Financeiro IA", page_icon="💰")
st.title("💰 Educador Financeiro IA (via Groq)")

# 2. Configuração da API Groq
# No Cloud Run ou Streamlit Cloud, você usará o nome da variável de sua escolha
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("Por favor, configure a variável de ambiente GROQ_API_KEY.")
    st.stop()

client = Groq(api_key=api_key)

# 3. Inicialização do Histórico
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou seu consultor financeiro turbinado pela Groq. Como posso ajudar?"}
    ]

# Exibição das Mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Lógica de Interação
if prompt := st.chat_input("Ex: Como economizar 20% do salário?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando na velocidade da luz..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "Você é um especialista em educação financeira simples e ético."
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="llama3-70b-8192",
                )
                
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"Erro na Groq: {e}")