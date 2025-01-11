import time
from threading import Thread

class GameAnimation:
    def __init__(self, ft):
        self.ft = ft

    def set_splash_screen_animation(self, initial_container, duration, reverse_duration):
        return self.ft.AnimatedSwitcher(
            initial_container,
            transition=self.ft.AnimatedSwitcherTransition.SCALE,
            duration=duration,
            reverse_duration=reverse_duration,
            switch_in_curve=self.ft.AnimationCurve.EASE_IN_OUT_CIRC,
            switch_out_curve=self.ft.AnimationCurve.EASE_IN_OUT_CIRC,        
        )

    def progress_bar_update(self, page, progress_bar):
        for i in range(0, 101):
            progress_bar.value = i * 0.01
            time.sleep(0.04)
            page.update()

    def highlight_correct_answer(self, buttons, correct_answer): 
        button = [button for button in buttons if correct_answer in button.text][0]   
        button.bgcolor = self.ft.Colors.GREEN  # Muda a cor de fundo para verde
        button.update()

    def contador(self, page, text):
        contador = text
        contador.value = "0"
        # Função para atualizar o contador a cada segundo
        def iniciar_contagem():
            while True:
                contador.value = str(int(contador.value) + 1)
                page.update()
                time.sleep(1)  # Pausa de 1 segundo

        # Inicia a contagem em uma thread separada
        contador_thread = Thread(target=iniciar_contagem, daemon=True)
        contador_thread.start()

        #page.add(contador)