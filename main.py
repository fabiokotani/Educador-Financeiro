
import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
import os

# 1. Configuração da Página
st.set_page_config(page_title="Educador Financeiro IA", page_icon="💰")
st.title("💰 Educador Financeiro IA")

# 2. Configuração Vertex AI (Nativa do Google Cloud)
# O Cloud Run já identifica o projeto automaticamente
project_id = "gen-lang-client-0523474741" 
vertexai.init(project=project_id, location="us-central1")

# Inicializa o modelo sem prefixos problemáticos
model = GenerativeModel("gemini-1.5-flash")

# 3. Inicialização do Histórico do Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou seu consultor financeiro. Como posso ajudar seu bolso hoje?"}
    ]

# 4. Exibição das Mensagens do Histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Lógica de Interação
if prompt := st.chat_input("Ex: Como começar a investir com 100 reais?"):
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera resposta com o Gemini
    with st.chat_message("assistant"):
        with st.spinner("Analisando finanças..."):
            try:
                # Instrução de sistema embutida na chamada
                system_instruction = (
                    "Você é um especialista em educação financeira. "
                    "Responda de forma simples, ética e sem julgamentos."
                )
                full_prompt = f"{system_instruction}\n\nUsuário: {prompt}"
                
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                
                # Salva resposta no histórico
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro ao contatar a IA: {e}")







