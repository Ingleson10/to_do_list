# Usando a imagem oficial do Python como base
FROM python:3.9-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando os arquivos necessários para dentro do container
COPY requirements.txt /to_do/

# Instalando as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o código da aplicação para dentro do container
COPY . /app/

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
