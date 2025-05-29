import flet as ft

needs_machines: list[dict] = []
machines =[
  {
    "machine_id": 0,
    "machine_name": "Кран",
    "count": 5
  },
    {
        "machine_id": 2,
        "machine_name": "Бетонномешалка",
        "count": 3
    }
]
work_scope = [
  {
    "id_work_scope": 0,
    "work_name": "Замешать глины",
    "work_unit": "м3",
    "work_scope": 0
  },
  {
    "id_work_scope": 0,
    "work_name": "Навалить кирпичей",
    "work_unit": "кг",
    "work_scope": 0
  }
]
def statement(page: ft.Page) -> ft.Control:

    def refresh_table():
        rows = []
        for entry in needs_machines:
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



    def refresh_having_machines():
        def move_to_needs_machines(entry: dict):
            txt_number = ft.TextField(value="0", text_align="right", width=100)

            def minus_click(e):
                txt_number.value = str(int(txt_number.value) - 1)
                page.update()

            def plus_click(e):
                txt_number.value = str(int(txt_number.value) + 1)
                page.update()

            needs_machines_entry.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(entry.get("machine_id", "Без названия"))),
                        ft.DataCell(ft.Text(entry.get("machine_name", ""))),
                        ft.DataCell(ft.Row([ft.IconButton(ft.Icons.REMOVE, on_click=minus_click), txt_number, ft.IconButton(ft.Icons.ADD, on_click=plus_click)])),
                    ]
                )
            )
            page.update()
        rows = []
        for entry in machines:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(entry.get("machine_id", "Без названия"))),
                    ft.DataCell(ft.Text(entry.get("machine_name", ""))),
                    ft.DataCell(ft.Text(entry.get("count", ""))),
                ],
                on_select_changed=lambda e, entry=entry: move_to_needs_machines(entry),
            )
            rows.append(row)
        having_machines.rows = rows
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
                "date": date_input.value,
                "created_by": created_by_input.value,
            }
            having_machines.append(new_entry)
            page.close(dlg)
            page.update()
            refresh_table()
        refresh_having_machines()


        dlg = ft.AlertDialog(
            title=ft.Text("Добавить ведомость"),
            content=ft.Row(
                [
                    ft.Column(
                        [needs_machines_entry, work_scope_entry],
                        spacing=10,
                        width=500,
                        height=250,
                    ),
                    ft.Column(
                        [having_machines],
                        spacing=10,
                        width=500,
                        height=250,
                    ),
                ],
                expand=True
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
        ft.DataColumn(ft.Text("№ п/п")),
        ft.DataColumn(ft.Text("Дата создания")),
        ft.DataColumn(ft.Text("Кем создано")),
    ]
    table = ft.DataTable(
        columns=columns, border=ft.border.all(1, ft.Colors.OUTLINE), expand=True
    )

    having_machines_columns = [
        ft.DataColumn(ft.Text("№ п/п")),
        ft.DataColumn(ft.Text("Название машины")),
        ft.DataColumn(ft.Text("Количество")),
    ]
    having_machines = ft.DataTable(
        columns=having_machines_columns, border=ft.border.all(1, ft.Colors.OUTLINE), expand=True
    )

    needs_machines_columns = [
        ft.DataColumn(ft.Text("№ п/п")),
        ft.DataColumn(ft.Text("Название работы")),
        ft.DataColumn(ft.Text("Название машины")),
        ft.DataColumn(ft.Text("Количество")),
    ]
    needs_machines_entry = ft.DataTable(
        columns=needs_machines_columns, border=ft.border.all(1, ft.Colors.OUTLINE), expand=True
    )

    work_scope_columns = [
        ft.DataColumn(ft.Text("№ п/п")),
        ft.DataColumn(ft.Text("Название работы")),
    ]
    work_scope_entry = ft.DataTable(
        columns=work_scope_columns, border=ft.border.all(1, ft.Colors.OUTLINE), expand=True
    )

    add_btn = ft.ElevatedButton(
        text="Добавить запись", icon=ft.Icons.ADD, on_click=add_entry
    )
    header = ft.Text(
        "Ведомости потребности в строительных машинах и технологической оснастке",
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
