import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as test_client:
        yield test_client


def test_web_get_index_page_returns_200(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Проверка високосного года" in html
    assert "Режим проверки:" in html
    assert "Год или список годов:" in html
    assert "Выполнить проверку" in html


def test_web_post_one_year_returns_result(client):
    response = client.post(
        "/",
        data={
            "mode": "one",
            "year": "2000",
        },
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "2000 - високосный год, потому что он делится на 400." in html


def test_web_post_multiple_years_returns_results(client):
    response = client.post(
        "/",
        data={
            "mode": "multiple",
            "year": "2000, 1900, 2024, 2023",
        },
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "2000 - високосный год, потому что он делится на 400." in html
    assert "1900 - не високосный год, потому что он делится на 100, но не делится на 400." in html
    assert "2024 - високосный год, потому что он делится на 4 и не делится на 100." in html
    assert "2023 - не високосный год, потому что он не делится на 4." in html


def test_web_post_multiple_years_with_invalid_value_returns_error(client):
    response = client.post(
        "/",
        data={
            "mode": "multiple",
            "year": "2000, abc, 2024",
        },
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "2000 - високосный год, потому что он делится на 400." in html
    assert "2024 - високосный год, потому что он делится на 4 и не делится на 100." in html
    assert "Ошибка для значения" in html
    assert "abc" in html
    assert "год должен быть положительным целым числом." in html


def test_web_post_next_years_returns_next_five_leap_years(client):
    response = client.post(
        "/",
        data={
            "mode": "next",
            "year": "2023",
        },
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Следующие 5 високосных годов после 2023: 2024, 2028, 2032, 2036, 2040" in html


def test_web_post_demo_returns_demo_checks(client):
    response = client.post(
        "/",
        data={
            "mode": "demo",
            "year": "",
        },
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Демонстрационные проверки:" in html
    assert "2000 - високосный год, потому что он делится на 400." in html
    assert "1900 - не високосный год, потому что он делится на 100, но не делится на 400." in html
    assert "2024 - високосный год, потому что он делится на 4 и не делится на 100." in html
    assert "2023 - не високосный год, потому что он не делится на 4." in html


def test_web_post_invalid_input_returns_error(client):
    response = client.post(
        "/",
        data={
            "mode": "one",
            "year": "abc",
        },
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Ошибка ввода: год должен быть положительным целым числом." in html
