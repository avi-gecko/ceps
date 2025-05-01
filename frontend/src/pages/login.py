import flet as ft

def get_login_view(page: ft.Page) -> ft.View:
    login = ft.TextField(label="Логин", width=300)
    password = ft.TextField(label="Пароль", password=True, can_reveal_password=True, width=300)

    def on_login_click(e):
        # здесь можно проверить логин/пароль
        page.go("/home")

    login_button = ft.ElevatedButton("Войти", on_click=on_login_click)

    return ft.View(
        route="/",
        controls=[
            ft.AppBar(title=ft.Text("Авторизация")),
            ft.Column(
                [login, password, login_button],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ]
    )
