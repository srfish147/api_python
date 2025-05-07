# Base oficial com Python
FROM python:3.11-slim

# Instala o LibreOffice e dependências do sistema
RUN apt-get update && apt-get install -y \
    libreoffice \
    fonts-dejavu-core \
    fonts-dejavu-extra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pelo uvicorn
EXPOSE 8080

# Comando de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
