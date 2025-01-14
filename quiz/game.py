import sqlite3
from datetime import datetime
import random
import html
import json

class Game:
    def __init__(self, amount=1):
        self.amount = amount
        self.index = 0
        self.questions = self.load_questions_from_db()  # Carregar perguntas do banco de dados
        
        # Se não houver perguntas, levanta uma exceção para indicar que o banco de dados está vazio
        if not self.questions:
            raise ValueError("Nenhuma pergunta encontrada no banco de dados.")
        
        #self.question = self.questions[self.index]       
    
    def load_questions_from_db(self):
        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()
        
        # Recupera todas as perguntas armazenadas
        cursor.execute("SELECT id, question, incorrect_answers, correct_answer FROM quiz WHERE compilation_date IS NULL")
        rows = cursor.fetchall()
        
        # Converte os resultados para um formato utilizável
        questions = []
        for row in rows:
            id, question, incorrect_answers_str, correct_answer = row
            
            question = self.decode_html_entities(question)
            incorrect_answers_str = self.decode_html_entities(incorrect_answers_str)  # Converte as respostas de volta para uma lista
            correct_answer = self.decode_html_entities(correct_answer)
            answers = json.loads(incorrect_answers_str)
           
            # Adiciona a resposta correta à lista de respostas (caso não esteja)
            if correct_answer not in answers:
                answers.append(correct_answer)

            # Embaralha as respostas para que a posição da resposta correta varie
            random.shuffle(answers)
            
            questions.append({
                "id": id,
                "question": question,
                "answers": answers[:],
                "correct_answer": correct_answer
            })
        
        conn.close()
        return questions
    
    def decode_html_entities(self, value):
        previous = value
        while True:
            current = html.unescape(previous)
            if current == previous:  # Se nenhuma mudança ocorrer, finalize
                break
            previous = current
        return current

    def mark_migration_date(self, id):
        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()
        
        # Atualiza a data de migração para a data e hora atual
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE quiz SET compilation_date = ? WHERE id = ?", (current_time, id))
        
        conn.commit()
        conn.close()


    def get_questions(self):
        return self.questions

    def get_question(self):
        return self.questions[self.index]   
    
    def get_question_and_answers_text(self):
        return f'{self.questions[self.index]["question"]}, {", ".join(self.questions[self.index]["answers"])}' 

    def get_correct_answer_text(self):
        return self.questions[self.index]["correct_answer"]
    
    def next(self):
        if self.index < self.amount - 1:
            self.index += 1
