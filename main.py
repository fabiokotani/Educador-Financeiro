# Importar o Flask
from flask import Flask, request, jsonify

# A lógica do chatbot precisa ser encapsulada em uma função
def get_chatbot_response(user_message, conversation_history):
  # A configuração do genai e do modelo já deve ter sido feita
  # model = genai.GenerativeModel("gemini-2.5-flash")

  # Adiciona a mensagem do usuário ao histórico da conversa
  # Note que 'historico' deve ser mantido para cada sessão de chat.
  # Em uma aplicação web real, isso seria gerenciado por sessão de usuário.
  conversation_history += f"\nUsuário: {user_message}"

  # Gera a resposta do modelo
  response = model.generate_content(conversation_history)
  chatbot_response = response.text

  # Adiciona a resposta do chatbot ao histórico
  conversation_history += f"\nEducador Financeiro: {chatbot_response}"

  return chatbot_response, conversation_history

app = Flask(__name__)

# Rota principal para o chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_data = request.get_json()
    user_message = user_data.get('message')
    current_history = user_data.get('history', historico) # Use o 'historico' inicial se não houver um fornecido

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    response, updated_history = get_chatbot_response(user_message, current_history)

    return jsonify({
        'response': response,
        'history': updated_history
    })

# Você não precisa rodar o app aqui no Colab, pois ele será rodado no Cloud Run.
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

%%writefile requirements.txt
Flask
google-generativeai
python-dotenv # Se ainda for usar, embora o Colab Secrets seja melhor

%%writefile Dockerfile
# Use a imagem base oficial do Python
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da sua aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que o Flask vai ouvir
EXPOSE 8080

# Comando para rodar a aplicação usando Gunicorn
# Gunicorn é um servidor WSGI para aplicações Python
# Substitua 'main:app' pelo nome do seu arquivo Python e o nome da sua instância Flask
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

