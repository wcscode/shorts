import requests
import sqlite3
import json
import html
from datetime import datetime

# URL da API
url = "https://opentdb.com/api.php?amount=1&difficulty=easy&type=multiple"

# Fazer a requisição à API
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
else:
    print(f"Erro ao acessar a API: {response.status_code}")
    exit()

# Obter os resultados do JSON
results = data.get("results", [])

# Conectar ao banco de dados SQLite (cria o arquivo se não existir)
conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()

# Criar tabela para armazenar as perguntas (renomeado para compilation_date)
cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    question TEXT UNIQUE,
    correct_answer TEXT,
    incorrect_answers TEXT,
    difficulty TEXT,
    compilation_date TIMESTAMP
)
""")

# Inserir os dados no banco de dados
for result in results:
    category = html.escape(result.get("category"))
    question = html.escape(result.get("question"))
    correct_answer = html.escape(result.get("correct_answer"))
    incorrect_answers = html.escape(json.dumps(result.get("incorrect_answers")))  # Armazena como JSON
    difficulty = html.escape(result.get("difficulty"))

    # Verificar se a pergunta já existe na tabela
    cursor.execute("SELECT 1 FROM quiz WHERE question = ?", (question,))
    exists = cursor.fetchone()

    if not exists:
        # Insere apenas se a pergunta não existir
        cursor.execute("""
        INSERT INTO quiz (category, question, correct_answer, incorrect_answers, difficulty, compilation_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (category, question, correct_answer, incorrect_answers, difficulty, None))
        print(f"Pergunta inserida: {question}")
    else:
        print(f"Pergunta já existe no banco de dados: {question}")

# Salvar as alterações e fechar a conexão
conn.commit()
conn.close()

print("Processo concluído!")
