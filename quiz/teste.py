import flet as ft
import os

def main(page: ft.Page):
    page.title = "Quiz"    
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window.frameless = True
    page.window.top = 0
    page.window.left = 20
    page.window.height = 854 #720 360  # Define a altura da janela
    page.window.width = 480 #1280 640  # Define a largura da janela       
    page.window.resizable = False  # Impede o redimensionamento da janela
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    horizontal_padding = 20 + ((page.window.width - page.window.height) / 2)   
    style_button = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=ft.padding.symmetric(vertical=25), color="white", text_style=ft.TextStyle(size=40))


    logo = ft.Image(src="assets/images/logo.png", width=300, height=300)
    splash_screen_text = ft.Text("Daily Quiz", text_align=ft.TextAlign.CENTER, size=60, weight=ft.FontWeight.BOLD)    
    #splash_screen_container = ft.Container(content=ft.Column(controls=[logo, splash_screen_text]),rotate=-1.5708)
    splash_screen_container = ft.Container(content=ft.Column(controls=[logo, splash_screen_text],alignment=ft.MainAxisAlignment.CENTER))


    page.add(ft.Container(content=splash_screen_container)) 

ft.app(target=main) 
    