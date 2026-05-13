import tkinter as tk

from leap import explain_year, next_leap_years, parse_positive_year


def set_result(text):
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, text)
    result_text.config(state="disabled")


def check_one_year():
    try:
        year = parse_positive_year(year_entry.get())
        set_result(explain_year(year))
    except ValueError as error:
        set_result(f"Ошибка ввода: {error}")


def check_multiple_years():
    parts = year_entry.get().split(",")
    results = []

    for part in parts:
        try:
            year = parse_positive_year(part)
            results.append(explain_year(year))
        except ValueError as error:
            results.append(f"Ошибка для значения '{part.strip()}': {error}")

    set_result("\n".join(results))


def show_next_years():
    try:
        year = parse_positive_year(year_entry.get())
        years = next_leap_years(year)
        set_result(f"Следующие {len(years)} високосных годов после {year}: {', '.join(map(str, years))}")
    except ValueError as error:
        set_result(f"Ошибка ввода: {error}")


def run_demo_checks():
    years = [2000, 1900, 2024, 2023]
    results = ["Демонстрационные проверки:"]

    for year in years:
        results.append(explain_year(year))

    set_result("\n".join(results))


def clear_input():
    year_entry.delete(0, tk.END)
    set_result("")


window = tk.Tk()
window.title("Проверка високосного года")
window.geometry("650x430")

title_label = tk.Label(window, text="Проверка високосного года", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

hint_label = tk.Label(
    window,
    text="Введите один год или несколько годов через запятую:",
    font=("Arial", 11)
)
hint_label.pack()

year_entry = tk.Entry(window, width=45, font=("Arial", 12))
year_entry.pack(pady=8)

buttons_frame = tk.Frame(window)
buttons_frame.pack(pady=8)

tk.Button(buttons_frame, text="Проверить один год", command=check_one_year, width=24).grid(row=0, column=0, padx=5, pady=5)
tk.Button(buttons_frame, text="Проверить несколько годов", command=check_multiple_years, width=24).grid(row=0, column=1, padx=5, pady=5)
tk.Button(buttons_frame, text="Показать следующие 5", command=show_next_years, width=24).grid(row=1, column=0, padx=5, pady=5)
tk.Button(buttons_frame, text="Демо-проверки", command=run_demo_checks, width=24).grid(row=1, column=1, padx=5, pady=5)
tk.Button(buttons_frame, text="Очистить", command=clear_input, width=24).grid(row=2, column=0, columnspan=2, pady=5)

result_text = tk.Text(window, height=8, width=72, wrap="word", font=("Arial", 10))
result_text.pack(pady=10)
result_text.config(state="disabled")

window.mainloop()
