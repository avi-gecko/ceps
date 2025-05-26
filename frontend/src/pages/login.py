import flet as ft
import requests
import json


def get_login_view(page: ft.Page) -> ft.View:
    page.title = "Авторизация"
    login = ft.TextField(label="Логин", width=300)
    password = ft.TextField(
        label="Пароль", password=True, can_reveal_password=True, width=300
    )
    error_text = ft.Text(value="", color="red")
    logo = ft.Image("mgsu.png", height=250)

    def on_login_click(e):
        repos_resp = requests.post(
            "http://ceps-backend_dev-1:8081/auth",
            json={"username": login.value, "password": password.value},
        )
        if repos_resp.status_code == 200:
            page.client_storage.set("access_token", repos_resp.json()["access_token"])
            page.go("/home")
        else:
            error_text.value = "Неверный логин или пароль"
            page.go("/")

        page.update()

    login_button = ft.ElevatedButton("Войти", on_click=on_login_click)

    def on_key_down(e: ft.KeyboardEvent):
        if e.key == "Enter":
            on_login_click(e)

    page.on_keyboard_event = on_key_down

    return ft.View(
        route="/",
        controls=[
            ft.Column(
                [logo, login, password, login_button, error_text],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.SPACE_AROUND,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
