import flet as ft
import threading
import time 
from recorder import Recorder
from game import Game
#from record import record_screen

# Função para destacar a resposta correta
def highlight_correct_answer(correct_button):
    #time.sleep(3)  # Aguarda 3 segundos
    correct_button.bgcolor = ft.Colors.GREEN  # Muda a cor de fundo para verde
    correct_button.update()

def main(page: ft.Page):
    # Configura a janela da aplicação
    page.title = "Quiz"    
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window.frameless = True
    page.window.top = 0
    page.window.left = 0
    page.window.height = 720  # Define a altura da janela
    page.window.width = 1280  # Define a largura da janela       
    page.window.resizable = False  # Impede o redimensionamento da janela
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    horizontal_padding = 20 + ((page.window.width - page.window.height) / 2)
    print(horizontal_padding)
    style_button = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=ft.padding.symmetric(vertical=25), color="white", text_style=ft.TextStyle(size=20))
    
    game = Game()

    # Pergunta e alternativas
    question = ft.Text(game.get_question(), text_align=ft.TextAlign.CENTER, size=20, weight=ft.FontWeight.BOLD)    

    button1 = ft.ElevatedButton(game.get_answer(0), width=page.width, style=style_button)
    button2 = ft.ElevatedButton(game.get_answer(1), width=page.width, style=style_button)
    button3 = ft.ElevatedButton(game.get_answer(2), width=page.width, style=style_button)
    button4 = ft.ElevatedButton(game.get_answer(3), width=page.width, style=style_button)   

    progress_bar = ft.ProgressBar(height=10,color="amber")   

    question_container = ft.Container(content=question, width=page.width, margin=ft.margin.only(bottom=40))
    buttons_columns = ft.Column(controls = [button1, button2, button3, button4])
    button_container = ft.Container(content=buttons_columns, margin=ft.margin.only(bottom=40))
    progress_bar_container = ft.Container(content=progress_bar)
    
    quiz_container = ft.Container(content=ft.Column(controls=[
        question_container, button_container, progress_bar_container
    ]),rotate=-1.5708, padding=ft.padding.symmetric(horizontal=horizontal_padding))

    transition_text = ft.Text("Daily Quiz", text_align=ft.TextAlign.CENTER, size=40, weight=ft.FontWeight.BOLD)
    transition_container = ft.Container(content=transition_text,rotate=-1.5708)

    main_container = set_animation(transition_container)

    def change_content():
        main_container.content = transition_container if main_container.content == quiz_container else quiz_container
        main_container.update()
  
    # Layout com a pergunta e os botões de resposta
    page.add(ft.Container(content=main_container))
   

    def close_window(e):        
        page.window.destroy()
    
    page.window.on_event = close_window

    geometry = (tuple(map(int, (page.window.left, page.window.top, page.window.width, page.window.height))))
    
    recorder = Recorder(geometry)

    recorder.start_recording()

    time.sleep(1)    
    change_content()

    progress_bar_update(page, progress_bar)
    highlight_correct_answer(button2)

    time.sleep(2)
    change_content()
    
    time.sleep(2)
    recorder.stop_recording()    


  
def set_animation(initial_container):
    return ft.AnimatedSwitcher(
        initial_container,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=1000,
        reverse_duration=100,
        switch_in_curve=ft.AnimationCurve.EASE_IN_OUT_CIRC,
        switch_out_curve=ft.AnimationCurve.EASE_IN_OUT_CIRC,        
    )

def progress_bar_update(page, progress_bar):
    for i in range(0, 101):
        progress_bar.value = i * 0.01
        time.sleep(0.05)
        page.update()

# Função para exibir o pop-up com o resultado
def show_popup(e, result):
    msg = "Resposta correta!" if result == "correta" else "Resposta incorreta!"
    ft.dialog.MessageDialog(title="Resultado", content=ft.Text(msg)).show()

# Executa o aplicativo
ft.app(target=main)