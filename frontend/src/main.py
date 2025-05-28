import flet as ft
from pages.login import get_login_view
from pages.home import get_home_view
import requests


def main(page: ft.Page):
    page.title = "АCУ"
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(e):
        page.views.clear()
        access_token = page.client_storage.get("access_token")

        if access_token is not None:
            repos_resp = requests.post(
                "http://ceps-backend_dev-1:8081/is_auth",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if repos_resp.status_code != 200:
                page.go("/")
            else:
                page.go("/home")
        else:
            page.go("/")

        if page.route == "/":
            page.views.append(get_login_view(page))
        elif page.route == "/home":
            page.views.append(get_home_view(page))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)


ft.app(main)
