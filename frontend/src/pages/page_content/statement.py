import flet as ft
import copy

needs_machines: list[dict] = []
machines = [
    {"machine_id": 0, "machine_name": "Кран", "count": 2},
    {"machine_id": 1, "machine_name": "Бетономешалка", "count": 3},
]
work_scope = [
    {
        "id_work_scope": 0,
        "work_name": "Укладка кирпичей",
        "work_unit": "м3",
        "work_scope": 0,
        "work_needs": 1,
    },
    {
        "id_work_scope": 1,
        "work_name": "Заливка фундамента",
        "work_unit": "кг",
        "work_scope": 0,
        "work_needs": 2,
    },
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

    def refresh_work_scope():
        def move_to_needs_machines(entry: dict):
            if (
                len(needs_machines_entry.rows) != 0
                and needs_machines_entry.rows[len(needs_machines_entry.rows) - 1]
                .cells[2]
                .content.value
                == ""
            ):
                return

            def remove_work(entry: ft.ControlEvent):
                try:
                    count_to_return = entry.control.cells[3].content.controls[1].value
                    entry.control.data[2].value += int(count_to_return)
                except:
                    ...
                for index, row in enumerate(needs_machines_entry.rows):
                    if row.data[1] == entry.control.data[1]:
                        del needs_machines_entry.rows[index]
                        break
                for index, row in enumerate(needs_machines_entry.rows):
                    row.cells[0].content.value = index + 1
                page.update()

            needs_machines_entry.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(len(needs_machines_entry.rows) + 1)),
                        ft.DataCell(ft.Text(entry.get("work_name", "Без названия"))),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ],
                    on_long_press=lambda e: remove_work(e),
                    data=[entry["id_work_scope"], len(needs_machines_entry.rows) - 1],
                )
            )
            page.update()

        rows = []
        for index, entry in enumerate(work_scope):
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(index + 1)),
                    ft.DataCell(ft.Text(entry.get("work_name", ""))),
                    ft.DataCell(ft.Text(entry.get("work_needs", ""))),
                ],
                on_select_changed=lambda e, entry=entry: move_to_needs_machines(entry),
            )
            rows.append(row)
        work_scope_entry.rows = rows
        page.update()

    def refresh_having_machines():
        def move_to_needs_machines(count_cell: ft.DataCell, entry: dict):
            if len(needs_machines_entry.rows) == 0:
                return
            if (
                len(needs_machines_entry.rows) != 0
                and needs_machines_entry.rows[len(needs_machines_entry.rows) - 1]
                .cells[2]
                .content.value
                != ""
            ):
                return

            if len(needs_machines_entry.rows) > 1:
                for index, row in enumerate(needs_machines_entry.rows):
                    if index == len(needs_machines_entry.rows) - 1:
                        break
                    if (
                        row.data[0]
                        == needs_machines_entry.rows[
                            len(needs_machines_entry.rows) - 1
                        ].data[0]
                        and row.data[3] == entry["machine_id"]
                    ):
                        return

            count = count_cell.content
            if count.value != 0:
                count.value -= 1
                max_count = (
                    count.value + 1
                )  # Исправлено: исходное значение до уменьшения
                txt_number = ft.TextField(
                    value="1", text_align="center", width=50, read_only=True
                )
            else:
                return

            def minus_click(e):
                current_value = int(txt_number.value)
                if current_value > 1 and count.value < max_count:
                    txt_number.value = str(current_value - 1)
                    count.value += 1
                    page.update()

            def plus_click(e):
                current_value = int(txt_number.value)
                if count.value > 0:
                    txt_number.value = str(current_value + 1)
                    count.value -= 1
                    page.update()

            needs_machines_entry.rows[len(needs_machines_entry.rows) - 1].cells[
                2
            ].content.value = entry.get("machine_name", "")
            needs_machines_entry.rows[len(needs_machines_entry.rows) - 1].cells[
                3
            ].content = ft.Row(
                [
                    ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                    txt_number,
                    ft.IconButton(ft.Icons.ADD, on_click=plus_click),
                ]
            )
            needs_machines_entry.rows[len(needs_machines_entry.rows) - 1].data += [
                count,
                entry["machine_id"],
            ]

            page.update()

        rows = []
        for index, entry in enumerate(machines):
            count_cell = ft.DataCell(ft.Text(entry["count"]))

            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(index + 1)),
                    ft.DataCell(ft.Text(entry.get("machine_name", ""))),
                    count_cell,
                ],
                on_select_changed=lambda e, count_cell=count_cell, entry=entry: move_to_needs_machines(
                    count_cell, entry
                ),
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
        refresh_work_scope()

        dlg = ft.AlertDialog(
            title=ft.Text("Добавить ведомость"),
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Необходимые машины", weight="bold"),
                            needs_machines_container,
                            ft.Text("Объем работ", weight="bold"),
                            work_scope_container,
                        ],
                        expand=True,
                        spacing=10,
                    ),
                    ft.Column(
                        [
                            ft.Text("Имеющиеся машины", weight="bold"),
                            having_machines_container,
                        ],
                        expand=True,
                        spacing=10,
                    ),
                ],
                expand=True,
                spacing=20,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            actions=[
                ft.TextButton("Сохранить", on_click=save_entry),
                ft.TextButton("Отмена", on_click=lambda ev: page.close(dlg)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg)
        page.update()

    def create_fixed_header_container(table: ft.DataTable, height=300, width=None):
        # Создаем отдельный заголовок на основе колонок таблицы
        header = ft.DataTable(
            columns=copy.deepcopy(table.columns),
            heading_row_color=ft.Colors.BLUE_GREY_100,
            heading_row_height=40,
            border=ft.border.only(
                bottom=ft.border.BorderSide(0, ft.Colors.TRANSPARENT)
            ),
            width=table.width,
        )
        for index, column in enumerate(table.columns):
            column.label.value = index + 1
        table.border = ft.border.only(
            top=ft.border.BorderSide(0, ft.Colors.TRANSPARENT)
        )

        # Контейнер для тела с прокруткой
        body_container = ft.Container(
            ft.ListView(
                controls=[table],
                auto_scroll=True,
                expand=True,
            ),
            height=height,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=ft.border_radius.only(bottom_left=5, bottom_right=5),
        )

        # Объединяем заголовок и тело
        return ft.Column(
            [
                ft.Container(
                    header,
                    border=ft.border.all(1, ft.Colors.OUTLINE),
                    border_radius=ft.border_radius.only(top_left=5, top_right=5),
                    bgcolor=ft.Colors.BLUE_GREY_100,
                ),
                body_container,
            ],
            spacing=0,
            width=width,
        )

    columns = [
        ft.DataColumn(ft.Text("№ п/п")),
        ft.DataColumn(ft.Text("Дата создания")),
        ft.DataColumn(ft.Text("Кем создано")),
    ]
    table = ft.DataTable(
        columns=columns, border=ft.border.all(1, ft.Colors.OUTLINE), expand=True
    )

    # Инициализация таблиц с сохранением оригинальных колонок
    having_machines_columns = [
        ft.DataColumn(ft.Text("№ п/п", weight="bold")),
        ft.DataColumn(ft.Text("Название машины", weight="bold")),
        ft.DataColumn(ft.Text("Количество", weight="bold")),
    ]
    having_machines = ft.DataTable(
        columns=having_machines_columns,
        border=ft.border.all(1, ft.Colors.OUTLINE),
        expand=True,
        width=500,
    )

    needs_machines_columns = [
        ft.DataColumn(ft.Text("№ п/п", weight="bold")),
        ft.DataColumn(ft.Text("Название работы", weight="bold")),
        ft.DataColumn(ft.Text("Название машины", weight="bold")),
        ft.DataColumn(ft.Text("Количество", weight="bold")),
    ]
    needs_machines_entry = ft.DataTable(
        columns=needs_machines_columns,
        border=ft.border.all(1, ft.Colors.OUTLINE),
        expand=True,
        width=750,
    )

    work_scope_columns = [
        ft.DataColumn(ft.Text("№ п/п", weight="bold")),
        ft.DataColumn(ft.Text("Название работы", weight="bold")),
        ft.DataColumn(ft.Text("Рекомендуемое значение машин", weight="bold")),
    ]
    work_scope_entry = ft.DataTable(
        columns=work_scope_columns,
        border=ft.border.all(1, ft.Colors.OUTLINE),
        expand=True,
        width=500,
    )

    # Создаем контейнеры с фиксированными заголовками
    having_machines_container = create_fixed_header_container(
        having_machines, height=300, width=500
    )

    needs_machines_container = create_fixed_header_container(
        needs_machines_entry, height=300, width=750
    )

    work_scope_container = create_fixed_header_container(
        work_scope_entry, height=300, width=500
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
