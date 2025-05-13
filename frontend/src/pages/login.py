import flet as ft

def get_login_view(page: ft.Page) -> ft.View:
    page.title = "Авторизация"
    login = ft.TextField(label="Логин", width=300)
    password = ft.TextField(label="Пароль", password=True, can_reveal_password=True, width=300)

    def on_login_click(e):
        # здесь можно проверить логин/пароль
        page.go("/home")

    login_button = ft.ElevatedButton("Войти", on_click=on_login_click)

    logo = ft.Image("mgsu.png", height=250)

    return ft.View(
        route="/",
        controls=[
            ft.Column(
                [logo, login, password, login_button],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.SPACE_AROUND,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
