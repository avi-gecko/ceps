import flet as ft
from pages.content import get_dashboard_content, get_profile_content

def get_home_view(page: ft.Page) -> ft.View:
    content_area = ft.Container(content=get_dashboard_content(), expand=True)

    def show_dashboard(e):
        content_area.content = get_dashboard_content()
        page.update()

    def show_profile(e):
        content_area.content = get_profile_content()
        page.update()

    nav_bar = ft.Row([
        ft.ElevatedButton("Главная", on_click=show_dashboard),
        ft.ElevatedButton("Профиль", on_click=show_profile),
        ft.IconButton(icon=ft.icons.LOGOUT, on_click=lambda _: page.go("/")),
    ], alignment=ft.MainAxisAlignment.CENTER)

    return ft.View(
        route="/home",
        controls=[
            ft.AppBar(title=ft.Text("Главная")),
            nav_bar,
            content_area
        ]
    )
