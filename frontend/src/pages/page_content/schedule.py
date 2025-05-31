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

# Словарь для русификации дней недели
weekdays_ru = {
    'Mon': 'Пн', 'Tue': 'Вт', 'Wed': 'Ср', 'Thu': 'Чт',
    'Fri': 'Пт', 'Sat': 'Сб', 'Sun': 'Вс'
}

# Форматтер, который возвращает русские сокращения месяцев
class RussianDateFormatter(mdates.DateFormatter):
    def __call__(self, x, pos=None):
        result = super().__call__(x, pos)
        return months_ru.get(result, result)

# Форматтер для дней недели
class RussianWeekdayFormatter(mdates.DateFormatter):
    def __call__(self, x, pos=None):
        result = super().__call__(x, pos)
        return weekdays_ru.get(result, result)

def build_chart_figure(page: ft.Page) -> plt.Figure:
    """Строит фигуру matplotlib на основе текущих фильтров"""
    # Извлекаем даты из session_state
    start_date = page.session_state['start_date']
    end_date = page.session_state['end_date']
    
    # Преобразуем даты, если они в формате datetime
    if isinstance(start_date, datetime.datetime):
        start_date = start_date.date()
    if isinstance(end_date, datetime.datetime):
        end_date = end_date.date()
    
    # --- 1. Исходные данные по задачам с доп. полями ---
    tasks = [
        ("Подготовка территории", 1, 1, "м²", 5, 2),
        ("Рытьё котлована", 2, 3, "м³", 8, 3),
        ("Заливка фундамента", 3, 5, "м³", 10, 4),
        ("Укладка кирпичей (этаж 1)", 4, 4, "м³", 12, 5),
        ("Укладка кирпичей (этаж 2)", 5, 5, "м³", 12, 5),
        ("Укладка кирпичей (этаж 3)", 6, 6, "м³", 12, 5),
        ("Монтаж перекрытий", 5, 7, "м³", 7, 3),
        ("Установка оконных блоков", 7, 8, "м³", 6, 2),
        ("Кровельные работы", 8, 9, "м²", 7, 3),
        ("Фасадные работы", 9, 10, "м²", 9, 4),
        ("Внутренняя отделка", 10, 11, "м²", 15, 6),
        ("Благоустройство территории", 11, 12, "м²", 4, 1),
        ("Сдача объекта", 12, 12, "ед.", 1, 0)
    ]

    resources = {
        "Вода": [random.randint(50, 200) for _ in range(12)],
        "Цемент": [random.randint(100, 500) for _ in range(12)],
    }

    # Список дат: 1-е число каждого месяца 2025 и «следующий» месяц
    month_start_dates = [datetime.date(2025, m, 1) for m in range(1, 13)]
    month_end_dates   = month_start_dates[1:] + [datetime.date(2026, 1, 1)]

    # --- 2. Фильтрация задач по выбранному диапазону ---
    filtered_tasks = []
    for task in tasks:
        name, start_m, end_m, unit, workers, machines = task
        task_start = datetime.date(2025, start_m, 1)
        # Вычисляем фактическую дату окончания (последний день месяца)
        if end_m == 12:
            task_end = datetime.date(2025, 12, 31)
        else:
            task_end = datetime.date(2025, end_m + 1, 1) - datetime.timedelta(days=1)
        
        # Проверяем пересечение с выбранным диапазоном
        if not (task_end < start_date or task_start > end_date):
            filtered_tasks.append((name, start_m, end_m, unit, workers, machines))

    num_tasks = len(filtered_tasks)
    num_resources = len(resources)

    # --- 3. Подготовка данных для таблицы (только отфильтрованные задачи) ---
    col_headers = [
        "№", "Наименование работ", "Ед.", "Раб.", "Мех.", "Дн.", "Начало", "Конец"
    ]
    num_row = [str(i + 1) for i in range(len(col_headers))]

    table_data = []
    for idx, (name, start_m, end_m, unit, workers, machines) in enumerate(filtered_tasks, start=1):
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
            d0.strftime("%d.%m.%y"),
            end_real.strftime("%d.%m.%y"),
        ]
        table_data.append(row)

    # --- 4. Построение фигуры с GridSpec ---
    total_rows = 1 + num_resources
    fig = plt.figure(figsize=(20, 3 * (1 + num_resources)))
    gs = GridSpec(
        nrows=total_rows,
        ncols=2,
        width_ratios=[1.3, 3],
        height_ratios=[num_tasks + 2] + [1] * num_resources,
        wspace=0.05,
        hspace=0.3,
        figure=fig
    )

    # === 4.1 Ось для таблицы ===
    ax_table = fig.add_subplot(gs[0, 0])
    ax_table.axis("off")

    full_table = [col_headers] + [num_row] + table_data
    table = plt.table(
        cellText=full_table,
        cellLoc='center',
        loc='center',
        bbox=[0, 0, 1, 1]
    )
    table.auto_set_column_width(col=list(range(len(col_headers))))
    total_table_rows = 2 + num_tasks
    row_height = 1.0 / total_table_rows
    
    for (row, col), cell in table.get_celld().items():
        cell.set_height(row_height)
        cell.set_linewidth(0.5)
        cell.set_edgecolor('gray')
        if row == 0:
            cell.set_text_props(weight='bold')
        if row >= 2:
            cell.set_text_props(wrap=True)

    # === 4.2 Ось для диаграммы Ганта ===
    ax_gantt = fig.add_subplot(gs[0, 1])
    # Устанавливаем диапазон оси X по выбранным датам
    ax_gantt.set_xlim(start_date, end_date)

    for i, (name, start_m, end_m, *_ ) in enumerate(filtered_tasks):
        d0 = month_start_dates[start_m - 1]
        d1 = month_end_dates[end_m - 1]
        ax_gantt.barh(
            y=i + 2,
            width=(d1 - d0).days,
            left=d0,
            height=0.6,
            color="skyblue",
            edgecolor="black"
        )

    ax_gantt.set_yticks([])
    ax_gantt.set_ylim(-0.5, num_tasks + 1 + 0.5)
    ax_gantt.invert_yaxis()

    # === 4.3 Улучшенное форматирование оси дат ===
    date_range = (end_date - start_date).days
    
    if date_range <= 7:  # Неделя - показывать дни с днями недели
        ax_gantt.xaxis.set_major_locator(mdates.DayLocator())
        ax_gantt.xaxis.set_major_formatter(RussianWeekdayFormatter("%a\n%d"))
        ax_gantt.tick_params(axis='x', which='major', labelsize=8)
        
    elif date_range <= 30:  # Месяц - показывать дни
        ax_gantt.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        ax_gantt.xaxis.set_major_formatter(mdates.DateFormatter("%d"))
        ax_gantt.xaxis.set_minor_locator(mdates.DayLocator())
        ax_gantt.tick_params(axis='x', which='major', labelsize=8)
        
    elif date_range <= 90:  # Квартал - показывать недели
        ax_gantt.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        ax_gantt.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        ax_gantt.tick_params(axis='x', which='major', labelsize=8)
        
    else:  # Более 3 месяцев - показывать месяцы
        ax_gantt.xaxis.set_major_locator(mdates.MonthLocator())
        ax_gantt.xaxis.set_major_formatter(RussianDateFormatter("%b"))
        ax_gantt.tick_params(axis='x', which='major', labelsize=8)

    # Автоматический поворот дат для экономии места
    plt.setp(ax_gantt.get_xticklabels(), rotation=30, ha='right')

    # === 4.4 Пустые оси слева для эпюр ===
    for i in range(1, total_rows):
        ax_empty = fig.add_subplot(gs[i, 0])
        ax_empty.axis("off")

    # === 4.5 Эпюры ресурсов (только для отфильтрованных задач) ===
    for idx_res, (res, vals) in enumerate(resources.items(), start=1):
        ax = fig.add_subplot(gs[idx_res, 1], sharex=ax_gantt)
        for name, start_m, end_m, *_, in filtered_tasks:
            d0 = month_start_dates[start_m - 1]
            d1 = month_end_dates[end_m - 1]
            consumption = sum(vals[start_m - 1 : end_m])
            ax.bar(
                x=d0,
                height=consumption,
                width=(d1 - d0).days,
                align="edge",
                color="lightgreen",
                edgecolor="black"
            )
        unit_res = "м³" if res == "Вода" else "кг"
        ax.set_ylabel(f"{res} ({unit_res})", fontsize=10)
        
        # Скрываем подписи дат для всех, кроме последнего графика
        if idx_res < num_resources:
            ax.tick_params(axis='x', labelbottom=False)
        else:
            # Применяем тот же форматтер дат, что и для Ганта
            if date_range <= 7:
                ax.xaxis.set_major_formatter(RussianWeekdayFormatter("%a\n%d"))
            elif date_range <= 30:
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%d"))
            elif date_range <= 90:
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
            else:
                ax.xaxis.set_major_formatter(RussianDateFormatter("%b"))
            
            # Поворот дат для последнего графика
            plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return fig

import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import random
from matplotlib.gridspec import GridSpec


def schedule(page: ft.Page) -> ft.Row:
    """Создает интерфейс графика с элементами управления"""
    # Инициализация дат фильтра в session_state
    if not hasattr(page, 'session_state'):
        page.session_state = {}
    if 'start_date' not in page.session_state:
        page.session_state['start_date'] = datetime.date(2025, 1, 1)
    if 'end_date' not in page.session_state:
        page.session_state['end_date'] = datetime.date(2025, 12, 31)
    
    # Создаем элементы управления
    start_field = ft.TextField(
        label="Начальная дата",
        value=page.session_state['start_date'].strftime("%d.%m.%Y"),
        read_only=True,
        width=150
    )
    end_field = ft.TextField(
        label="Конечная дата",
        value=page.session_state['end_date'].strftime("%d.%m.%Y"),
        read_only=True,
        width=150
    )
    
    # Создаем контейнер для графика
    chart_container = ft.Container(expand=True)
    
    # Функция для обновления графика
    def update_chart():
        fig = build_chart_figure(page)
        chart_container.content = MatplotlibChart(fig, expand=True)
        start_field.value = page.session_state['start_date'].strftime("%d.%m.%Y")
        end_field.value = page.session_state['end_date'].strftime("%d.%m.%Y")
        page.update()
    
    # DatePicker
    dp_start = ft.DatePicker(
        first_date=datetime.datetime(2025, 1, 1),
        last_date=datetime.datetime(2025, 12, 31),
        value=datetime.datetime.combine(page.session_state['start_date'], datetime.time())
    )
    dp_end = ft.DatePicker(
        first_date=datetime.datetime(2025, 1, 1),
        last_date=datetime.datetime(2025, 12, 31),
        value=datetime.datetime.combine(page.session_state['end_date'], datetime.time())
    )
    
    page.overlay.extend([dp_start, dp_end])
    
    # Функция обновления даты
    def update_date(field, picker, field_control):
        selected_date = picker.value
        if isinstance(selected_date, datetime.datetime):
            selected_date = selected_date.date()
        page.session_state[field] = selected_date
        update_chart()
    
    # Установка обработчиков
    dp_start.on_change = lambda e: update_date('start_date', dp_start, start_field)
    dp_end.on_change = lambda e: update_date('end_date', dp_end, end_field)
    
    # Сброс фильтров
    def reset_filters(e):
        page.session_state['start_date'] = datetime.date(2025, 1, 1)
        page.session_state['end_date'] = datetime.date(2025, 12, 31)
        # Обновляем значения DatePicker
        dp_start.value = datetime.datetime.combine(page.session_state['start_date'], datetime.time())
        dp_end.value = datetime.datetime.combine(page.session_state['end_date'], datetime.time())
        update_chart()
    
    # Кнопка печати
    def on_print(e):
        fig = build_chart_figure(page)
        fig.savefig("график.png")
        page.snack_bar = ft.SnackBar(ft.Text("График сохранен как график.png"))
        page.snack_bar.open = True
        page.update()
    
    # Собираем панель управления
    controls = ft.Row([
        # Поля выбора дат
        ft.Row([
            start_field,
            ft.ElevatedButton(
                "Выбрать",
                on_click=lambda e: page.open(dp_start),
                icon=ft.Icons.CALENDAR_MONTH
            ),
            end_field,
            ft.ElevatedButton(
                "Выбрать",
                on_click=lambda e: page.open(dp_end),
                icon=ft.Icons.CALENDAR_MONTH
            ),
            ft.ElevatedButton(
                "Сбросить фильтры",
                on_click=reset_filters,
                icon=ft.Icons.CLEAR
            ),
        ], spacing=10),
        
        # Кнопка печати справа
        ft.ElevatedButton(
            text="Печать", 
            icon=ft.Icons.PRINT, 
            on_click=on_print
        )
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    # Заголовок
    header = ft.Text(
        "Недельно-суточный график",
        theme_style=ft.TextThemeStyle.HEADLINE_LARGE,
    )

    right_column = ft.Column(
        [
            header,
            controls,
            chart_container,
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    # Первоначальное построение графика
    update_chart()

    return ft.Row([right_column], expand=True, spacing=20)