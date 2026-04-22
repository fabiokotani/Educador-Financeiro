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
