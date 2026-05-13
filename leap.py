def is_leap_year(year):
    """Проверяет, является ли год високосным."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def explain_year(year):
    """Возвращает объяснение, почему год високосный или не високосный."""
    if year % 400 == 0:
        return f"{year} - високосный год, потому что он делится на 400."
    if year % 100 == 0:
        return f"{year} - не високосный год, потому что он делится на 100, но не делится на 400."
    if year % 4 == 0:
        return f"{year} - високосный год, потому что он делится на 4 и не делится на 100."
    return f"{year} - не високосный год, потому что он не делится на 4."


def parse_positive_year(value):
    """Преобразует пользовательский ввод в положительное целое число."""
    value = "".join(value.strip().split())

    if not value:
        raise ValueError("ввод пустой.")

    if not value.isdigit():
        raise ValueError("год должен быть положительным целым числом.")

    year = int(value)

    if year <= 0:
        raise ValueError("год должен быть больше 0.")

    return year


def check_single_year():
    """Запрашивает один год и выводит результат проверки."""
    user_input = input("Введите год: ")

    try:
        year = parse_positive_year(user_input)
        print(explain_year(year))
    except ValueError as error:
        print(f"Ошибка ввода: {error}")


def check_multiple_years():
    """Запрашивает несколько годов через запятую и проверяет каждый."""
    user_input = input("Введите годы через запятую: ")
    parts = user_input.split(",")

    for part in parts:
        try:
            year = parse_positive_year(part)
            print(explain_year(year))
        except ValueError as error:
            print(f"Ошибка для значения '{part.strip()}': {error}")


def next_leap_years(start_year, count=5):
    """Возвращает следующие count високосных годов после указанного года."""
    if count <= 0:
        return []

    leap_years = []
    current_year = start_year + 1

    while len(leap_years) < count:
        if is_leap_year(current_year):
            leap_years.append(current_year)
        current_year += 1

    return leap_years


def show_next_leap_years():
    """Запрашивает год и выводит следующие 5 високосных годов."""
    user_input = input("Введите начальный год: ")

    try:
        year = parse_positive_year(user_input)
        years = next_leap_years(year)
        print(f"Следующие {len(years)} високосных годов после {year}: {', '.join(map(str, years))}")
    except ValueError as error:
        print(f"Ошибка ввода: {error}")


def run_demo_checks():
    """Выводит демонстрационные проверки для важных граничных случаев."""
    print("Демонстрационные проверки:")

    for year in [2000, 1900, 2024, 2023]:
        print(explain_year(year))

    print()


def show_menu():
    """Выводит главное меню приложения."""
    print("Проверка високосного года")
    print("1. Проверить один год")
    print("2. Проверить несколько годов")
    print("3. Показать следующие 5 високосных годов")
    print("4. Запустить демонстрационные проверки")
    print("5. Выход")


def main():
    """Запускает консольное приложение."""
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            check_single_year()
        elif choice == "2":
            check_multiple_years()
        elif choice == "3":
            show_next_leap_years()
        elif choice == "4":
            run_demo_checks()
        elif choice == "5":
            print("Работа завершена.")
            break
        else:
            print("Неизвестный пункт меню. Выберите 1, 2, 3, 4 или 5.")

        print()


if __name__ == "__main__":
    main()
