from flask import Flask, render_template, request

from leap import explain_year, next_leap_years, parse_positive_year

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    mode = "one"

    if request.method == "POST":
        mode = request.form.get("mode", "one")
        user_input = request.form.get("year", "")

        if mode == "one":
            try:
                year = parse_positive_year(user_input)
                result = explain_year(year)
            except ValueError as error:
                result = f"Ошибка ввода: {error}"

        elif mode == "multiple":
            parts = user_input.split(",")
            results = []

            for part in parts:
                try:
                    year = parse_positive_year(part)
                    results.append(explain_year(year))
                except ValueError as error:
                    results.append(f"Ошибка для значения '{part.strip()}': {error}")

            result = "\n".join(results)

        elif mode == "next":
            try:
                year = parse_positive_year(user_input)
                years = next_leap_years(year)
                result = f"Следующие {len(years)} високосных годов после {year}: {', '.join(map(str, years))}"
            except ValueError as error:
                result = f"Ошибка ввода: {error}"

        elif mode == "demo":
            years = [2000, 1900, 2024, 2023]
            result = "Демонстрационные проверки:\n" + "\n".join(explain_year(year) for year in years)

    return render_template("index.html", result=result, mode=mode)


if __name__ == "__main__":
    app.run(debug=True)
