class Game:
    def __init__(self, amount=1):
        self.amount = amount
        self.index = 0
        self.questions = ["Qual é a capital da França?"]
        self.answers = [["Londres", "Paris", "Berlim", "Roma"]]
    
    def get_question()
        return self.questions[self.index]

    def get_answer(index)
        return self.answers[self.index][index]

    def next()
        if(self.index < self.amount - 1)
            self.index += 1
