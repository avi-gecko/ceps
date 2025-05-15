import flet as ft

entries: list[dict] = []


def act(page: ft.Page) -> ft.Control:

    def refresh_table():
        rows = []
        for entry in entries:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(entry.get("title", "Без названия"))),
                    ft.DataCell(ft.Text(entry.get("date", ""))),
                    ft.DataCell(ft.Text(entry.get("created_by", ""))),
                ],
                on_select_changed=lambda e, entry=entry: open_entry(entry),
            )
            rows.append(row)
        table.rows = rows
        page.update()

    def open_entry(entry: dict):
        dlg = ft.AlertDialog(
            title=ft.Text(entry.get("title", "Без названия")),
            content=ft.Column(
                [
                    ft.Text(f"Описание: {entry.get('description', '')}"),
                    ft.Text(f"Дата создания: {entry.get('date', '')}"),
                    ft.Text(f"Кем создано: {entry.get('created_by', '')}"),
                ],
                width=500,
                height=250,
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
        def save_entry(ev: ft.ControlEvent):
            new_entry = {
                "title": title_input.value,
                "description": desc_input.value,
            }
            entries.append(new_entry)
            page.close(dlg)
            page.update()
            refresh_table()

        title_input = ft.TextField(label="Номер")
        desc_input = ft.TextField(label="Описание", multiline=True)
        
        dlg = ft.AlertDialog(
            title=ft.Text("Добавить запись"),
            content=ft.Column(
                [title_input, desc_input],
                spacing=10,
                width=500,
                height=250,
            ),
            actions=[
                ft.TextButton(text="Сохранить", on_click=save_entry),
                ft.TextButton(text="Отмена", on_click=lambda ev: page.close(dlg)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg)
        page.update()

    columns = [
        ft.DataColumn(ft.Text("Номер")),
        ft.DataColumn(ft.Text("Дата создания")),
        ft.DataColumn(ft.Text("Кем создано")),
    ]

    table = ft.DataTable(
        columns=columns, border=ft.border.all(1, ft.Colors.OUTLINE), expand=True
    )

    add_btn = ft.ElevatedButton(
        text="Добавить запись", icon=ft.Icons.ADD, on_click=add_entry
    )
    header = ft.Text(
        "Акты о приёмке выполненных работ КС-2",
        theme_style=ft.TextThemeStyle.HEADLINE_LARGE,
    )

    refresh_table()

    return ft.Row(
        [
            ft.Column(
                [header, table],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            ft.VerticalDivider(width=1),
            ft.Column([add_btn], alignment=ft.MainAxisAlignment.START),
        ],
        expand=True,
    )
