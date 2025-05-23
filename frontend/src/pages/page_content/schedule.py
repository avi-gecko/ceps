import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

def schedule(page: ft.Page) -> ft.Row:
    """
    Renders a Gantt chart and resource consumption epures per task using Matplotlib.
    One epure bar per task period, displayed as filled columns under the Gantt chart.
    Embeds in Flet via MatplotlibChart.
    """
    # Mock data: tasks with start/end month indices
    tasks = [
        ("Excavation", 1, 2),
        ("Foundation", 3, 4),
        ("Framing", 5, 7),
        ("Roofing", 8, 9),
        ("Finishing", 10, 12),
    ]
    # Mock resource consumption by month
    resources = {
        "Water":  [50, 60, 55, 70, 65, 80, 75, 60, 55, 50, 45, 40],
        "Cement": [20, 25, 30, 40, 35, 45, 50, 30, 25, 20, 15, 10],
    }
    # Months for x-axis
    month_start_dates = [datetime.date(2025, m, 1) for m in range(1, 13)]
    month_end_dates = month_start_dates[1:] + [datetime.date(2026, 1, 1)]

    # Create figure: 1 Gantt row + one epure plot per resource
    nrows = 1 + len(resources)
    fig, axs = plt.subplots(nrows, 1, figsize=(12, 3 * nrows), sharex=True)

    # Gantt chart on first axis
    ax_gantt = axs[0]
    for i, (name, start, end) in enumerate(tasks):
        d0 = month_start_dates[start-1]
        d1 = month_end_dates[end-1]
        ax_gantt.barh(i, (d1 - d0).days, left=d0, height=0.6, color='skyblue', edgecolor='black')
    ax_gantt.set_yticks(range(len(tasks)))
    ax_gantt.set_yticklabels([t[0] for t in tasks])
    ax_gantt.invert_yaxis()
    ax_gantt.set_title('Gantt Chart of Tasks')
    ax_gantt.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    # Epure diagrams per resource: vertical bars under Gantt
    for idx, (res, vals) in enumerate(resources.items(), start=1):
        ax = axs[idx]
        # for each task, sum consumption over period
        periods = []
        consumptions = []
        for _, start, end in tasks:
            periods.append((month_start_dates[start-1], month_end_dates[end-1]))
            consumptions.append(sum(vals[start-1:end]))
        # plot filled bar from zero upwards, spanning task period
        max_c = max(consumptions)
        for (d0, d1), c in zip(periods, consumptions):
            ax.bar(d0, c, width=(d1 - d0).days, align='edge', color='green', edgecolor='black')
        unit = 'm³' if res == 'Water' else 't'
        ax.set_ylabel(f'{res} ({unit})')
        ax.set_ylim(0, max_c * 1.1)
        ax.set_title(f'Resource Consumption Epure')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    fig.tight_layout()

    # Embed in Flet
    chart = MatplotlibChart(fig, expand=True)

    # Print button: save chart image
    def on_print(e):
        fig.savefig("test.png")
    print_btn = ft.ElevatedButton(
        text='Печать', icon=ft.Icons.PRINT,
        on_click=on_print
    )
    header = ft.Text(
        "Недельно-суточный график",
        theme_style=ft.TextThemeStyle.HEADLINE_LARGE,
    )
    # Return Row
    return ft.Row([
        ft.Column([header, chart], expand=True, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
        ft.VerticalDivider(width=1),
        ft.Column([print_btn], alignment=ft.MainAxisAlignment.START)
    ], expand=True, spacing=20)