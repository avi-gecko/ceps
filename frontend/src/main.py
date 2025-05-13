import flet as ft
from pages.login import get_login_view
from pages.home import get_home_view

def main(page: ft.Page):
    page.title = "АCУ"
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(get_login_view(page))
        elif page.route == "/home":
            page.views.append(get_home_view(page))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(main)
