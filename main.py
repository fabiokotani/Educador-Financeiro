import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# CORREÇÃO: Usando modelo existente
model = genai.GenerativeModel("gemini-1.5-flash") 

app = Flask(__name__)

# Configuração do System Instruction (o que estava solto antes)
SYSTEM_PROMPT = """
  Você é um especialista em educação financeira e finanças pessoais.
  Seu objetivo é ajudar pessoas com dúvidas ou problemas financeiros.
  Diretrizes: Análise sem julgamentos, conselhos personalizados e linguagem simples.
"""

def get_chatbot_response(user_message, conversation_history):
    # Inclui o prompt de sistema se o histórico estiver vazio
    full_prompt = f"{SYSTEM_PROMPT}\n{conversation_history}\nUsuário: {user_message}"
    
    response = model.generate_content(full_prompt)
    chatbot_response = response.text
    
    updated_history = conversation_history + f"\nUsuário: {user_message}\nEducador Financeiro: {chatbot_response}"
    return chatbot_response, updated_history

@app.route('/chat', methods=['POST'])
def chat():
    user_data = request.get_json()
    if not user_data:
        return jsonify({'error': 'Corpo da requisição vazio'}), 400
        
    user_message = user_data.get('message')
    current_history = user_data.get('history', "")

    if not user_message:
        return jsonify({'error': 'Nenhuma mensagem enviada'}), 400

    try:
        response, updated_history = get_chatbot_response(user_message, current_history)
        return jsonify({
            'response': response,
            'history': updated_history
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)








