import time 

class GameAnimation:
    def __init__(self, ft):
        self.ft = ft

    def set_splash_animation(self, initial_container, duration, reverse_duration):
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
            time.sleep(0.05)
            page.update()

    def highlight_correct_answer(self, buttons, correct_answer_index):    
        buttons[correct_answer_index].bgcolor = self.ft.Colors.GREEN  # Muda a cor de fundo para verde
        buttons[correct_answer_index].update()