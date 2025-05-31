import flet as ft
import copy

entries: list[dict] = []

entries = [
    {
        "num": "1",
        "work_name": "Земляные работы",
        "unit": "м³",
        "quantity": "150",
        "price_per_unit": "1 500",
        "contract_price": "225 000",
        "total_quantity": "1 200",
        "total_cost": "1 800 000",
        "period_quantity": "300",
        "period_cost": "450 000"
    },
    {
        "num": "2",
        "work_name": "Бетонные работы",
        "unit": "м³",
        "quantity": "80",
        "price_per_unit": "8 000",
        "contract_price": "640 000",
        "total_quantity": "350",
        "total_cost": "2 800 000",
        "period_quantity": "120",
        "period_cost": "960 000"
    },
    {
        "num": "3",
        "work_name": "Арматурные работы",
        "unit": "т",
        "quantity": "15",
        "price_per_unit": "35 000",
        "contract_price": "525 000",
        "total_quantity": "45",
        "total_cost": "1 575 000",
        "period_quantity": "8",
        "period_cost": "280 000"
    },
    {
        "num": "4",
        "work_name": "Монтаж конструкций",
        "unit": "шт",
        "quantity": "25",
        "price_per_unit": "12 000",
        "contract_price": "300 000",
        "total_quantity": "90",
        "total_cost": "1 080 000",
        "period_quantity": "15",
        "period_cost": "180 000"
    },
    {
        "num": "5",
        "work_name": "Кровельные работы",
        "unit": "м²",
        "quantity": "500",
        "price_per_unit": "1 200",
        "contract_price": "600 000",
        "total_quantity": "1 800",
        "total_cost": "2 160 000",
        "period_quantity": "300",
        "period_cost": "360 000"
    }
]


def act(page: ft.Page) -> ft.Control:

    def refresh_table():
        rows = []
        for entry in entries:
            row = ft.DataRow(
            cells=[
                # Порядковый номер
                ft.DataCell(ft.Text(entry["num"])),
                
                # Наименование работ
                ft.DataCell(ft.Text(entry["work_name"])),
                
                # Единица измерения
                ft.DataCell(ft.Text(entry["unit"])),
                
                # Количество
                ft.DataCell(ft.Text(entry["quantity"])),
                
                # Цена за единицу
                ft.DataCell(ft.Text(entry["price_per_unit"])),
                
                # Твердая договорная цена
                ft.DataCell(ft.Text(entry["contract_price"])),
                
                # Количество с начала строительства
                ft.DataCell(ft.Text(entry["total_quantity"])),
                
                # Стоимость с начала строительства
                ft.DataCell(ft.Text(entry["total_cost"])),
                
                # Количество за отчетный период
                ft.DataCell(ft.Text(entry["period_quantity"])),
                
                # Стоимость за отчетный период
                ft.DataCell(ft.Text(entry["period_cost"]))
            ],
                on_select_changed=lambda e, entry=entry: open_entry(entry),
            )
            rows.append(row)
        needs_machines_entry.rows = rows
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

    def create_fixed_header_container(table: ft.DataTable, height=300, width=None):
        # Создаем отдельный заголовок на основе колонок таблицы
        header = ft.DataTable(
            columns=copy.deepcopy(table.columns),
            heading_row_color=ft.Colors.BLUE_GREY_100,
            heading_row_height=60,
            border=ft.border.only(
                bottom=ft.border.BorderSide(0, ft.Colors.TRANSPARENT)
            ),
            expand=True,
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

    def on_print(e): ...

    print_btn = ft.ElevatedButton(text="Печать", icon=ft.Icons.PRINT, on_click=on_print)

    header = ft.Text(
        "Акт о приёмке выполненных работ КС-2",
        theme_style=ft.TextThemeStyle.HEADLINE_LARGE,
    )
    needs_machines_columns = [
        ft.DataColumn(ft.Text("№ п/п", weight="bold")),
        ft.DataColumn(
            ft.Text("Наименование\nукрупненных\nвидов работ и затрат", weight="bold")
        ),
        ft.DataColumn(ft.Text("Единица\nизмерения", weight="bold")),
        ft.DataColumn(ft.Text("Количество", weight="bold")),
        ft.DataColumn(ft.Text("Цена за единицу,\nруб. без НДС", weight="bold")),
        ft.DataColumn(
            ft.Text("Твердая договорная\nцена МГЭ,\nруб. без НДС", weight="bold")
        ),
        ft.DataColumn(ft.Text("Кол-во\nс начала строительства", weight="bold")),
        ft.DataColumn(ft.Text("Стоиомость\nс начала строительства", weight="bold")),
        ft.DataColumn(ft.Text("Кол-во\nза отчетный период", weight="bold")),
        ft.DataColumn(ft.Text("Стоиомость\nза отчетный период", weight="bold")),
    ]
    needs_machines_entry = ft.DataTable(
        columns=needs_machines_columns,
        border=ft.border.all(1, ft.Colors.OUTLINE),
        expand=True,
    )
    table = create_fixed_header_container(needs_machines_entry, height=500)
    refresh_table()

    return ft.Row(
        [
            ft.Column(
                [header, table],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            ft.VerticalDivider(width=1),
            ft.Column([print_btn], alignment=ft.MainAxisAlignment.START),
        ],
        expand=True,
    )
