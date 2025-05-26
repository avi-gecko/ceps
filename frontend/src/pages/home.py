import flet as ft
import pages.page_content


def get_home_view(page: ft.Page) -> ft.View:
    content_area = ft.Container(expand=True)

    def set_content(e):
        content = None
        match e.control.selected_index:
            case 0:
                content = pages.page_content.act(page)
            case 1:
                content = pages.page_content.statement(page)
            case 2:
                content = pages.page_content.calendar(page)
            case 3:
                content = pages.page_content.schedule(page)
            case _:
                content = None
        content_area.content = content
        page.update()

    def logout(e):
        page.client_storage.clear()
        page.go("/")

    rail = ft.NavigationRail(
        leading=ft.Image("mgsu.png", height=125),
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.CHECKLIST),
                label="КС-2",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.VIEW_LIST),
                label="Ведомость",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.CALENDAR_MONTH), label="Календарный"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.SCHEDULE), label="Недельно-суточный"
            ),
        ],
        trailing=ft.IconButton(
            icon=ft.Icons.LOGOUT_ROUNDED, tooltip="Выход", on_click=logout
        ),
        on_change=set_content,
        group_alignment=-0.75,
    )

    return ft.View(
        route="/home",
        controls=[
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    content_area,
                ],
                expand=True,
            ),
        ],
        vertical_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bottom_appbar=ft.BottomAppBar(ft.Text("Ильин А.В. ИЦТМС 4-5")),
    )
