
Arquivo Dockerfile para o Flask
Crie um arquivo chamado Dockerfile no mesmo diretório:
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]

Arquivo requirements.txt
Liste as dependências do Flask e do banco de dados:
flask
psycopg2-binary

Arquivo app.py
Um exemplo básico de aplicação Flask conectada ao banco de dados:
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/')
def home():
    try:
        conn = psycopg2.connect(
            dbname="mydatabase",
            user="user",
            password="password",
            host="db"
        )
        return jsonify({"message": "Conexão com o banco de dados bem-sucedida!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

Como executar

Certifique-se de que o Docker e o Docker Compose estão instalados.
No diretório onde estão os arquivos, execute:docker-compose up --build


Acesse a API Flask em http://localhost:5000.

Esse setup é simples e pode ser expandido conforme necessário.