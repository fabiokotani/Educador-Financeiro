import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash") 

current_history = user_data.get('history', 

"""
  Você é um especialista em educação financeira e finanças pessoais.
  Seu objetivo é ajudar pessoas com dúvidas ou problemas financeiros.

  Diretrizes importantes:
  - Faça uma análise da situação ou questão financeira da pessoa, sem emitir julgamentos sobre a pessoa.
  - Procure dar conselhos e orientações personalizadas nas suas respostas.
  - Utilize palavras simples e comuns. Seja didático nas explicações e orientações dadas.
  """)

app = Flask(__name__)

def get_chatbot_response(user_message, conversation_history):
    # Formata a nova entrada
    conversation_history += f"\nUsuário: {user_message}"
    
    # Gera a resposta
    response = model.generate_content(conversation_history)
    chatbot_response = response.text
    
    # Atualiza o histórico
    conversation_history += f"\nEducador Financeiro: {chatbot_response}"
    
    return chatbot_response, conversation_history

@app.route('/chat', methods=['POST'])
def chat():
    user_data = request.get_json()
    if not user_data:
        return jsonify({'error': 'Corpo da requisição vazio'}), 400
        
    user_message = user_data.get('message')
    current_history = user_data.get('history', "") # Começa vazio se não houver

    if not user_message:
        return jsonify({'error': 'Nenhuma mensagem enviada'}), 400

    response, updated_history = get_chatbot_response(user_message, current_history)

    return jsonify({
        'response': response,
        'history': updated_history
    })

if __name__ == '__main__':
    # O Render usa a variável de ambiente PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)









