import socket
import threading

import pytest
from playwright.sync_api import expect
from werkzeug.serving import make_server

from app import app as flask_app


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="session")
def live_server_url():
    flask_app.config["TESTING"] = True
    port = get_free_port()
    server = make_server("127.0.0.1", port, flask_app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://127.0.0.1:{port}"

    server.shutdown()
    thread.join(timeout=5)


def submit_form(page, mode, year):
    page.select_option("#mode", mode)
    page.fill("#year", year)
    page.get_by_role("button", name="Выполнить проверку").click()


@pytest.mark.e2e
def test_e2e_index_page_shows_form(page, live_server_url):
    page.goto(live_server_url)

    expect(page).to_have_title("Проверка високосного года")
    expect(page.get_by_role("heading", name="Проверка високосного года")).to_be_visible()
    expect(page.locator("#mode")).to_be_visible()
    expect(page.locator("#year")).to_be_visible()
    expect(page.get_by_role("button", name="Выполнить проверку")).to_be_visible()


@pytest.mark.e2e
def test_e2e_check_single_year(page, live_server_url):
    page.goto(live_server_url)
    submit_form(page, "one", "2000")

    expect(page.locator(".result")).to_contain_text(
        "2000 - високосный год, потому что он делится на 400."
    )


@pytest.mark.e2e
def test_e2e_check_multiple_years_with_invalid_value(page, live_server_url):
    page.goto(live_server_url)
    submit_form(page, "multiple", "2000, 1900, abc")

    result = page.locator(".result")
    expect(result).to_contain_text("2000 - високосный год, потому что он делится на 400.")
    expect(result).to_contain_text(
        "1900 - не високосный год, потому что он делится на 100, но не делится на 400."
    )
    expect(result).to_contain_text(
        "Ошибка для значения 'abc': год должен быть положительным целым числом."
    )


@pytest.mark.e2e
def test_e2e_show_next_five_leap_years(page, live_server_url):
    page.goto(live_server_url)
    submit_form(page, "next", "2023")

    expect(page.locator(".result")).to_contain_text(
        "Следующие 5 високосных годов после 2023: 2024, 2028, 2032, 2036, 2040"
    )


@pytest.mark.e2e
def test_e2e_invalid_input(page, live_server_url):
    page.goto(live_server_url)
    submit_form(page, "one", "abc")

    expect(page.locator(".result")).to_contain_text(
        "Ошибка ввода: год должен быть положительным целым числом."
    )
