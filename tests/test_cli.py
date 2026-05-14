import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEAP_SCRIPT = PROJECT_ROOT / "leap.py"


def run_cli_with_input(user_input):
    completed_process = subprocess.run(
        [sys.executable, str(LEAP_SCRIPT)],
        input=user_input,
        text=True,
        capture_output=True,
        check=False,
        timeout=5,
    )

    return completed_process


def test_cli_check_single_leap_year():
    result = run_cli_with_input("1\n2000\n5\n")

    assert result.returncode == 0
    assert "Проверка високосного года" in result.stdout
    assert "2000 - високосный год, потому что он делится на 400." in result.stdout
    assert "Работа завершена." in result.stdout


def test_cli_check_multiple_years_with_invalid_value():
    result = run_cli_with_input("2\n2000, 1900, abc\n5\n")

    assert result.returncode == 0
    assert "2000 - високосный год, потому что он делится на 400." in result.stdout
    assert "1900 - не високосный год, потому что он делится на 100, но не делится на 400." in result.stdout
    assert "Ошибка для значения 'abc': год должен быть положительным целым числом." in result.stdout
    assert "Работа завершена." in result.stdout


def test_cli_show_next_five_leap_years():
    result = run_cli_with_input("3\n2023\n5\n")

    assert result.returncode == 0
    assert "Следующие 5 високосных годов после 2023: 2024, 2028, 2032, 2036, 2040" in result.stdout
    assert "Работа завершена." in result.stdout


def test_cli_run_demo_checks():
    result = run_cli_with_input("4\n5\n")

    assert result.returncode == 0
    assert "Демонстрационные проверки:" in result.stdout
    assert "2000 - високосный год, потому что он делится на 400." in result.stdout
    assert "1900 - не високосный год, потому что он делится на 100, но не делится на 400." in result.stdout
    assert "2024 - високосный год, потому что он делится на 4 и не делится на 100." in result.stdout
    assert "2023 - не високосный год, потому что он не делится на 4." in result.stdout


def test_cli_unknown_menu_option():
    result = run_cli_with_input("9\n5\n")

    assert result.returncode == 0
    assert "Неизвестный пункт меню. Выберите 1, 2, 3, 4 или 5." in result.stdout
    assert "Работа завершена." in result.stdout


def test_cli_exit():
    result = run_cli_with_input("5\n")

    assert result.returncode == 0
    assert "Работа завершена." in result.stdout
