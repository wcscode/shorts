class Game:
    def __init__(self, amount=1):
        self.amount = amount
        self.index = 0
        self.questions = ["Qual é a capital da França?"]        
        self.answers = [["Londres", "Paris", "Berlim", "Roma"]]
        self.corrects_answers = [0, 1]
        self.corrects_answers[self.index] = 1 
    
    def get_question(self):
        return self.questions[self.index]

    def get_answer(self, index):
        return self.answers[self.index][index]
    
    def get_correct_answer_index(self):
        return self.corrects_answers[self.index]

    def get_question_and_answers_text(self):
        return f'{self.get_question()}, {[self.get_answer(i) for i in range(0, 4)]}' 

    def get_correct_answer_text(self):
        return self.get_answer(self.get_correct_answer_index())

    def next(self):
        if(self.index < self.amount - 1):
            self.index += 1
