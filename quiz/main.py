import flet as ft
import threading
import time 

# Função para destacar a resposta correta
def highlight_correct_answer(correct_button):
    #time.sleep(3)  # Aguarda 3 segundos
    correct_button.bgcolor = ft.colors.GREEN  # Muda a cor de fundo para verde
    correct_button.update()

def main(page: ft.Page):
    # Configura a janela da aplicação
    page.title = "Quiz"    
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window.width = 40 * 9  # Define a largura da janela
    page.window.height = 40 * 19.5  # Define a altura da janela
    page.window.resizable = False  # Impede o redimensionamento da janela
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER    

    style_button = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=ft.padding.symmetric(vertical=25), color="white", text_style=ft.TextStyle(size=16))
    
    # Pergunta e alternativas
    question = ft.Text("Qual é a capital da França?", text_align=ft.TextAlign.CENTER, size=16, weight=ft.FontWeight.BOLD)    

    button1 = ft.ElevatedButton("Londres", width=page.width, style=style_button)
    button2 = ft.ElevatedButton("Paris", width=page.width, style=style_button)
    button3 = ft.ElevatedButton("Berlim", width=page.width, style=style_button)
    button4 = ft.ElevatedButton("Roma", width=page.width, style=style_button)   

    progress_bar = ft.ProgressBar(height=10,color="amber")   

    question_container = ft.Container(content=question, width=page.width, margin=ft.margin.only(bottom=40))
    buttons_columns = ft.Column(controls = [button1, button2, button3, button4])
    button_container = ft.Container(content=buttons_columns, margin=ft.margin.only(bottom=40))
    progress_bar_container = ft.Container(content=progress_bar)
    
    quiz_container = ft.Container(content=ft.Column(controls=[
        question_container, button_container, progress_bar_container
    ]))

    transition_text = ft.Text("Daily Quiz", text_align=ft.TextAlign.CENTER, size=16, weight=ft.FontWeight.BOLD)
    transition_container = ft.Container(content=transition_text)

    main_container = set_animation(transition_container)

    def animate():
        main_container.content = transition_container if main_container.content == quiz_container else quiz_container
        main_container.update()
    # Layout com a pergunta e os botões de resposta
    page.add(main_container)

    time.sleep(1)
    animate()

    progress_bar_update(page, progress_bar)
    highlight_correct_answer(button2)

    time.sleep(1)
    animate()

    # Inicia a thread para destacar a resposta correta
   # threading.Thread(target=highlight_correct_answer, args=(button2,), daemon=True).start()

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