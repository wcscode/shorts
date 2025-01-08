import flet as ft
import time 
from screen_recorder import ScreenRecorder
from audio import Audio
from compiler import Compiler
from game import Game
from game_animation import GameAnimation
from timeline import Timeline

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
    style_button = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=ft.padding.symmetric(vertical=25), color="white", text_style=ft.TextStyle(size=40))
    
    game = Game()

    # Pergunta e alternativas
    question = ft.Text(game.get_question(), text_align=ft.TextAlign.CENTER, size=40, weight=ft.FontWeight.BOLD)    

    button1 = ft.ElevatedButton(game.get_answer(0), width=page.width, style=style_button)
    button2 = ft.ElevatedButton(game.get_answer(1), width=page.width, style=style_button)
    button3 = ft.ElevatedButton(game.get_answer(2), width=page.width, style=style_button)
    button4 = ft.ElevatedButton(game.get_answer(3), width=page.width, style=style_button)   
    
    buttons = [button1, button2, button3, button4]

    progress_bar = ft.ProgressBar(height=10,color="amber", value=0)   

    question_container = ft.Container(content=question, width=page.width, margin=ft.margin.only(bottom=40))
    buttons_columns = ft.Column(controls=buttons)
    button_container = ft.Container(content=buttons_columns, margin=ft.margin.only(bottom=40))
    progress_bar_container = ft.Container(content=progress_bar)
    
    quiz_container = ft.Container(content=ft.Column(controls=[
        question_container, button_container, progress_bar_container
    ]),rotate=-1.5708, padding=ft.padding.symmetric(horizontal=horizontal_padding))

    splash_screen_text = ft.Text("Daily Quiz", text_align=ft.TextAlign.CENTER, size=60, weight=ft.FontWeight.BOLD)
    splash_screen_container = ft.Container(content=splash_screen_text,rotate=-1.5708)

    game_animation = GameAnimation(ft)

    #Contador
    #game_animation.contador(page, question)

    animation_duration = 1000
    animation_reverse_duration = 100

    main_container = game_animation.set_splash_screen_animation(
        splash_screen_container, 
        animation_duration, 
        animation_reverse_duration)   

    def change_content():
        main_container.content = splash_screen_container if main_container.content == quiz_container else quiz_container
        main_container.update()  

    page.add(ft.Container(content=main_container))       

    audio = Audio()   

    audio_duration_1 = audio.create(game.get_question_and_answers_text(), "audio_file_1")    
    audio_duration_2 = audio.create(game.get_correct_answer_text(), "audio_file_2")

    geometry = (tuple(map(int, (page.window.top, page.window.left, page.window.width, page.window.height))))
    
    timeline = Timeline()
    timeline.start()

    recorder = ScreenRecorder(geometry)    
    recorder.start_recording()

    timeline.wait("INIT_SPLASH_SCREEN", 2)
    change_content()    

    timeline.wait("INIT_READ_QUESTION", 1)
    timeline.wait("READ_QUESTION", audio_duration_1) 
    game_animation.progress_bar_update(page, progress_bar)
     
    game_animation.highlight_correct_answer(buttons, game.get_correct_answer_index())
    timeline.register("INIT_READ_ANSWER")
    timeline.wait("READ_ANSWER", audio_duration_2) 

    timeline.wait("RETURN_SPLASH_SCREEN", 2)  
    change_content()
    
    timeline.wait("END_RECORD", 1)  
    recorder.stop_recording()  
    
    compiler = Compiler()
   
    compiler.add_video(recorder.get_file_name())    
    compiler.add_audio(audio.get_files_names()[0], timeline.recovery("INIT_READ_QUESTION")) 
    compiler.add_audio(audio.get_files_names()[0], timeline.recovery("INIT_READ_ANSWER")) 
    compiler.add_background_music("./assets/audios/free-stile.mp3")
    
    page.window.destroy() 

# Executa o aplicativo
ft.app(target=main)