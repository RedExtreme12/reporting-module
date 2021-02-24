from table_data import TableData

from flask import Flask, render_template, request

app = Flask(__name__)


headings = ('Наименование модели',
            'Дата закупки',
            'Количество единиц автомобилей',
            'Стоимость (одного авто)')

static_data = (
    ('Model X', '21.02.2015', 14, '100000.00$'),
    ('Model S', '22.02.2015', 20, '70000.50$'),
)


models_names = ('Model X', 'Model S', 'Model 3', 'Model Y', 'Roadster 2')


@app.route('/random-data', methods=['POST'])
def random_data_page():
    count_records = int(request.form['count_records'])

    print(count_records)

    random_table_data = TableData(models_names=models_names, headings=headings)
    return render_template('entry.html', headings=headings, data=random_table_data.get_random_data(count_records))


@app.route('/')
def main_page():
    return render_template('entry.html', headings=headings, data=static_data)


if __name__ == '__main__':
    app.run()
