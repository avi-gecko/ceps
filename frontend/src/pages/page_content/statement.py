import flet as ft

entries: list[dict] = []


def statement(page: ft.Page) -> ft.Container:

    def refresh_list():
        list_view.controls.clear()
        for entry in entries:
            btn = ft.TextButton(
                text=entry.get("title", "Без названия"), data=entry, on_click=open_entry
            )
            list_view.controls.append(btn)
        page.update()

    def open_entry(e: ft.ControlEvent):
        entry = e.control.data
        dlg = ft.AlertDialog(
            title=ft.Text(entry.get("title", "Без названия")),
            content=ft.Column(
                [
                    ft.Text(f"Описание: {entry.get('description', '')}"),
                    ft.Text(f"Дата: {entry.get('date', '')}"),
                ]
            ),
            actions=[
                ft.TextButton(
                    text="Печать", on_click=lambda e: print_entry(entry, dlg)
                ),
                ft.TextButton(text="Закрыть", on_click=lambda e: page.close(dlg)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg)
        page.update()

    def print_entry(entry: dict, dlg):
        print(f"Печать документа: {entry}")
        page.close(dlg)
        page.update()

    def add_entry(e: ft.ControlEvent):
        title_input = ft.TextField(label="Название")
        desc_input = ft.TextField(label="Описание", multiline=True)
        date_input = ft.TextField(label="Дата")

        def save_entry(ev: ft.ControlEvent):
            # Save new entry
            new_entry = {
                "title": title_input.value,
                "description": desc_input.value,
                "date": date_input.value,
            }
            entries.append(new_entry)
            page.close(dlg)
            refresh_list()

        dlg = ft.AlertDialog(
            title=ft.Text("Добавить запись"),
            content=ft.Column([title_input, desc_input, date_input]),
            actions=[
                ft.TextButton(text="Сохранить", on_click=save_entry),
                ft.TextButton(text="Отмена", on_click=lambda ev: page.close(dlg)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg)
        page.update()

    list_view = ft.ListView(expand=True, spacing=5, padding=10)
    add_btn = ft.ElevatedButton(
        text="Добавить запись", icon=ft.Icons.ADD, on_click=add_entry
    )
    header = ft.Text(
        "Ведомость потребности в строительных машинах и технологической оснастке",
        theme_style=ft.TextThemeStyle.HEADLINE_LARGE,
    )

    container = ft.Container(
        content=ft.Row(
            [
                ft.Column([header, list_view], expand=True),
                ft.VerticalDivider(width=1),
                ft.Column([add_btn], alignment=ft.MainAxisAlignment.START),
            ],
            expand=True,
        ),
        expand=True,
    )

    refresh_list()
    return container
