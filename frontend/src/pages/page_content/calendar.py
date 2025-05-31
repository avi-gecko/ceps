import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import random
from matplotlib.gridspec import GridSpec

# Словарь для русификации сокращённых названий месяцев
months_ru = {
    'Jan': 'Янв', 'Feb': 'Фев', 'Mar': 'Мар', 'Apr': 'Апр',
    'May': 'Май', 'Jun': 'Июн', 'Jul': 'Июл', 'Aug': 'Авг',
    'Sep': 'Сен', 'Oct': 'Окт', 'Nov': 'Ноя', 'Dec': 'Дек'
}

# Форматтер, который возвращает русские сокращения месяцев
class RussianDateFormatter(mdates.DateFormatter):
    def __call__(self, x, pos=None):
        result = super().__call__(x, pos)
        return months_ru.get(result, result)

def calendar(page: ft.Page) -> ft.Row:
    """
    Рисует комбинированную фигуру:
    - Слева (в gs[0,0]): «таблица» (текстовые ячейки), у которой
        1. первая строка — заголовок (col_headers),
        2. вторая строка — нумерация колонок (1,2,3,…,8),
        3. далее — строки с данными (каждая выровнена по высоте с Gantt-баром).
    - Справа (в gs[0,1]):
        1. первые две «строки» оставляются пустыми (y = 0 и y = 1),
        2. с третьей строки (y = 2 и далее) рисуются настоящие полосы Ганта (соответствуют задачам).
    Ниже (в gs[1..,1]) — эпюры потребления ресурсов.
    """

    # --- 1. Исходные данные по задачам с доп. полями ---
    # Каждая запись: (название, месяц_старта, месяц_окончания, ед.изм., кол-во рабочих, кол-во механизмов)
    tasks = [
        ("Подготовка территории",    1,  2, "м²", 5, 2),
        ("Рытьё котлована",          3,  4, "м³", 8, 3),
        ("Заливка фундамента",       5,  7, "м³", 10, 4),
        ("Укладка кирпичей",         8,  9, "м³", 12, 5),
        ("Установка оконных блоков",11, 12, "м³", 6,  2),
    ]
    resources = {
        "Вода":   [random.randint(10, 100) for _ in range(12)],
        "Цемент": [random.randint(10, 100) for _ in range(12)],
    }

    # Список дат: 1-е число каждого месяца 2025 и «следующий» месяц
    month_start_dates = [datetime.date(2025, m, 1) for m in range(1, 13)]
    month_end_dates   = month_start_dates[1:] + [datetime.date(2026, 1, 1)]

    num_tasks = len(tasks)
    num_resources = len(resources)

    # --- 2. Подготовка данных для таблицы ---
    # Сокращённые заголовки (первая строка таблицы)
    col_headers = [
        "№", "Наименование работ", "Ед.", "Раб.", "Мех.", "Дн.", "Начало", "Конец"
    ]
    # Вторая строка — просто цифры колонок 1..8
    num_row = [str(i + 1) for i in range(len(col_headers))]

    # Третья и далее — реальные строки данных
    table_data = []
    for idx, (name, start_m, end_m, unit, workers, machines) in enumerate(tasks, start=1):
        d0 = month_start_dates[start_m - 1]
        d1 = month_end_dates[end_m - 1]
        duration_days = (d1 - d0).days
        end_real = d1 - datetime.timedelta(days=1)
        row = [
            str(idx),
            name,
            unit,
            str(workers),
            str(machines),
            f"{duration_days}",
            d0.strftime("%d.%m.%y"),   # Сокращённый формат даты
            end_real.strftime("%d.%m.%y"),
        ]
        table_data.append(row)

    # --- 3. Построение фигуры с GridSpec ---
    # Одна «строка» (row 0) для таблицы и Ганта, затем по одной строке под каждый ресурс
    total_rows = 1 + num_resources

    fig = plt.figure(figsize=(20, 3 * (1 + num_resources)))
    gs = GridSpec(
        nrows=total_rows,
        ncols=2,
        width_ratios=[1.3, 3],              # доля ширины: таблица vs графики
        height_ratios=[num_tasks + 2] + [1] * num_resources,
        # ↑↑ height_ratios[0] = num_tasks + 2, т.к. у нас две «пустых» строки вверху Ганта
        wspace=0.05,
        hspace=0.3,
        figure=fig
    )

    # === 3.1 Ось для таблицы (в gs[0,0]) ===
    ax_table = fig.add_subplot(gs[0, 0])
    ax_table.axis("off")

    # Объединяем: первая строка = col_headers, вторая = num_row, далее = data
    full_table = [col_headers] + [num_row] + table_data
    table = plt.table(
        cellText=full_table,
        cellLoc='center',
        loc='center',
        bbox=[0, 0, 1, 1]   # занимает весь axes[0,0]
    )

    # ВОССТАНАВЛИВАЕМ автоматическое задание ширины колонок:
    table.auto_set_column_width(col=list(range(len(col_headers))))

    # Всего теперь (1 + 1 + num_tasks) строк в таблице
    total_table_rows = 2 + num_tasks

    # Настраиваем шрифты и размеры строк
    table.auto_set_font_size(False)
    table.set_fontsize(9)

    # Желательно, чтобы каждая строка таблицы имела высоту 1/(total_table_rows)
    row_height = 1.0 / total_table_rows
    for (row, col), cell in table.get_celld().items():
        # row = 0..(total_table_rows-1), col = 0..(len(col_headers)-1)
        cell.set_height(row_height)
        cell.set_linewidth(0.5)
        cell.set_edgecolor('gray')
        # Для header (row == 0) — делаем текст жирным:
        if row == 0:
            cell.set_text_props(weight='bold')
        # Для data-строк (row >= 2) — включаем перенос текста:
        if row >= 2:
            cell.set_text_props(wrap=True)

    # === 3.2 Ось для диаграммы Ганта (в gs[0,1]) ===
    ax_gantt = fig.add_subplot(gs[0, 1])

    # Рисуем две «пустые» строки (y = 0 и y = 1), а сами задачи — по y = 2..(num_tasks+1)
    for i, (name, start_m, end_m, *_ ) in enumerate(tasks):
        d0 = month_start_dates[start_m - 1]
        d1 = month_end_dates[end_m - 1]
        ax_gantt.barh(
            y=i + 2,                 # сдвиг «на две» строки вверх
            width=(d1 - d0).days,
            left=d0,
            height=0.6,              # чуть уже, чтобы между рядами была щель
            color="skyblue",
            edgecolor="black"
        )

    ax_gantt.set_yticks([])  # Убираем метки на оси Y
    ax_gantt.set_yticklabels([])  # Убираем подписи задач
    ax_gantt.set_ylabel("")  # Убираем заголовок оси Y

    # Ограничиваем видимую область по y так, чтобы «0» и «1» оставались пустыми
    ax_gantt.set_ylim(-0.5, num_tasks + 1 + 0.5)
    ax_gantt.invert_yaxis()  # первая задача сверху

    ax_gantt.xaxis.set_major_formatter(RussianDateFormatter("%b"))

    # === 3.3 «Пустые» оси слева для эпюр (gs[1..,0]) ===
    for i in range(1, total_rows):
        ax_empty = fig.add_subplot(gs[i, 0])
        ax_empty.axis("off")

    # === 3.4 Эпюры ресурсов (в gs[1.., 1]) ===
    for idx_res, (res, vals) in enumerate(resources.items(), start=1):
        ax = fig.add_subplot(gs[idx_res, 1], sharex=ax_gantt)
        periods = []
        consumptions = []
        for (_, start_m, end_m, *_) in tasks:
            d0 = month_start_dates[start_m - 1]
            d1 = month_end_dates[end_m - 1]
            periods.append((d0, d1))
            consumptions.append(sum(vals[start_m - 1 : end_m]))
        for (d0, d1), c in zip(periods, consumptions):
            ax.bar(
                x=d0,
                height=c,
                width=(d1 - d0).days,
                align="edge",
                color="lightgreen",
                edgecolor="black"
            )
        unit_res = "м³" if res == "Вода" else "кг"
        ax.set_ylabel(f"{res} ({unit_res})", fontsize=10)
        ax.xaxis.set_major_formatter(RussianDateFormatter("%b"))

    # --- 4. Финальные штрихи ---

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # учитываем заголовок

    # --- 5. Встраивание в Flet ---
    chart = MatplotlibChart(fig, expand=True)

    def on_print(e):
        fig.savefig("test.png")

    print_btn = ft.ElevatedButton(text="Печать", icon=ft.Icons.PRINT, on_click=on_print)
    header = ft.Text(
        "Календарный график",
        theme_style=ft.TextThemeStyle.HEADLINE_LARGE,
    )

    right_column = ft.Column(
        [
            header,
            chart,
            ft.Row([print_btn], alignment=ft.MainAxisAlignment.END),
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    return ft.Row([right_column], expand=True, spacing=20)
