class Game:
    def __init__(self, amount=1):
        self.amount = amount
        self.index = 0
        self.questions = ["Qual é a capital da França?"]
        self.answers = [["Londres", "Paris", "Berlim", "Roma"]]
    
    def get_question(self):
        return self.questions[self.index]

    def get_answer(self, index):
        return self.answers[self.index][index]

    def next(self):
        if(self.index < self.amount - 1):
            self.index += 1
