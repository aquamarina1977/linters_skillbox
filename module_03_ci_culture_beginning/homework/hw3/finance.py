from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    try:
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:])

        expense = storage.setdefault(year, {}).setdefault(month, {}).get(day, 0)
        storage[year][month][day] = expense + number
        return "Expense added successfully!"
    except ValueError:
        return 'Internal Server Error', 500


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    if year in storage:
        total = 0
        for month in storage[year]:
            for day in storage[year][month]:
                total += storage[year][month][day]
        return f"Total expenses in {year}: {total}"
    else:
        return f"No expenses found for {year}"


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    if year in storage and month in storage[year]:
        total = 0
        for day in storage[year][month]:
            total += storage[year][month][day]
        return f"Total expenses in {year}/{month}: {total}"
    else:
        return f"No expenses found for {year}/{month}"

if __name__ == '__main__':
    app.run(debug=True)