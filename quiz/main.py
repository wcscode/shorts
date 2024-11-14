import flet as ft
import threading
import time
import flet.canvas as cv
import math

# Função para destacar a resposta correta
def highlight_correct_answer(correct_button):
    time.sleep(3)  # Aguarda 3 segundos
    correct_button.bgcolor = ft.colors.GREEN  # Muda a cor de fundo para verde
    correct_button.update()

def main(page: ft.Page):
    # Configura a janela da aplicação
    page.title = "Quiz"    
    page.padding = 20
    page.window.width = 40 * 9  # Define a largura da janela
    page.window.height = 40 * 19.5  # Define a altura da janela
    page.window_resizable = False  # Impede o redimensionamento da janela
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

    countdown = countdown_canvas(page)

    question_container = ft.Container(content=question, margin=ft.margin.only(bottom=40))
    buttons_columns = ft.Column(controls = [button1, button2, button3, button4])
    button_container = ft.Container(content=buttons_columns, margin=ft.margin.only(bottom=40))
    countdown_container = ft.Container(content=countdown, width=page.window.width, height=100, bgcolor="red")
    
    # Layout com a pergunta e os botões de resposta
    page.add(
        question_container,
        button_container,
        countdown_container
    )

    # Inicia a thread para destacar a resposta correta
    threading.Thread(target=highlight_correct_answer, args=(button2,), daemon=True).start()

def countdown_canvas(page):
    stroke_paint = ft.Paint(stroke_width=10, style=ft.PaintingStyle.STROKE, color="white")
    fill_paint = ft.Paint(style=ft.PaintingStyle.FILL, color="green")    
    center_x = (page.window.width - 50) / 2
    cp = cv.Canvas(
        [
            #cv.Circle(center_x, 100 / 2, 50, stroke_paint),            
            cv.Arc(center_x, 95, 50, 40, 0, math.pi, paint=stroke_paint),
        ],
        width=float("inf"),
        height=1250,
        expand=True,
    )
    return cp

# Função para exibir o pop-up com o resultado
def show_popup(e, result):
    msg = "Resposta correta!" if result == "correta" else "Resposta incorreta!"
    ft.dialog.MessageDialog(title="Resultado", content=ft.Text(msg)).show()

# Executa o aplicativo
ft.app(target=main)