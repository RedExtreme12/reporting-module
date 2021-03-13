import os

from table_data import TableData
from data import headings, models_names, static_data, LINE_SPACING_VALUES

from flask import Flask, render_template, request, send_file
from flask_caching import Cache
from mailmerge import MailMerge
from docx import Document


cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
cache.init_app(app)

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))


FILE_READY_TEMPLATE_NAME = 'template.docx'


@app.route('/change-interval', methods=['GET', 'POST'])
def change_interval():

    uploads = os.path.join(APP_ROUTE, "uploads/")
    ready_template_name = uploads + FILE_READY_TEMPLATE_NAME

    document = Document(ready_template_name)

    #  get styles of document
    style = document.styles
    latent_styles = document.styles.latent_styles
    line_spacing = None

    # get current line spacing.
    for latent_style in latent_styles:
        try:
            st = style[latent_style.name]

            if hasattr(st, 'paragraph_format'):
                if st.paragraph_format.line_spacing is not None:
                    line_spacing = st.paragraph_format.line_spacing
        except KeyError:
            pass

    # get new line spacing value from possible values.
    line_spacing_index_in_arr = LINE_SPACING_VALUES.index(line_spacing)
    try:
        new_line_spacing = LINE_SPACING_VALUES[line_spacing_index_in_arr + 1]
    except IndexError:
        new_line_spacing = LINE_SPACING_VALUES[line_spacing_index_in_arr]

    # set new line spacing.
    for latent_style in latent_styles:
        try:
            st = style[latent_style.name]

            if hasattr(st, 'paragraph_format'):
                st.paragraph_format.line_spacing = new_line_spacing
        except KeyError:
            pass

    document.save(ready_template_name)

    return send_file(ready_template_name)


@app.route('/download', methods=['GET', 'POST'])
def download():
    """Generates a file and returns to the user."""

    data = set(cache.get('current_data'))
    filename = cache.get('filename')

    if filename is None:
        return render_template('entry.html', headings=headings, data=data)
    else:
        filename = str(filename)

    uploads = os.path.join(APP_ROUTE, "uploads/")

    document = MailMerge(uploads + filename)
    data = set(cache.get('current_data'))

    initials = request.form.get('full_name')
    county_name = request.form.get('county_name')
    count_cars = request.form.get('count_cars')

    document.merge(
        fio=initials,
        county_name=county_name,
        supplier=count_cars
    )

    # list of data that will be substituted into the word template.
    data_word_list = []

    # Populating the list with data.
    for row in data:
        data_word_list.append(
            {
                'model_name': str(row[0]),
                'date_of_purchase': str(row[1]),
                'count_of_cars': str(row[2]),
                'cost': str(row[3]),
            },
        )

    document.merge_rows('model_name', data_word_list)

    ready_template_name = uploads + FILE_READY_TEMPLATE_NAME

    document.write(ready_template_name)

    return send_file(ready_template_name)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    target = os.path.join(APP_ROUTE, 'uploads/')

    if request.method == 'POST':
        f = request.files['file']

        try:
            data = set(cache.get('current_data'))
        except TypeError:
            data = static_data

        if f.filename != '':
            cache.set('filename', f.filename)
            destination = "/".join([target, f.filename])
            f.save(destination)
            return render_template('entry.html', headings=headings, data=data)

        return render_template('entry.html', headings=headings, data=data)


@app.route('/random-data', methods=['POST'])
def random_data_page():
    if request.form.get('count_records') != '':
        count_records = int(request.form['count_records'])

        random_table_data = TableData(models_names=models_names, headings=headings)
        random_data = random_table_data.get_random_data(count_records)
        cache.set('current_data', random_data)

        return render_template('entry.html', headings=headings, data=random_data)

    try:
        data = set(cache.get('current_data'))
    except TypeError:
        return render_template('entry.html', headings=headings, data=static_data)

    if data is not None:
        return render_template('entry.html', headings=headings, data=data)


@app.route('/')
def main_page():
    cache.set('current_data', static_data)

    return render_template('entry.html', headings=headings, data=static_data)


if __name__ == '__main__':
    app.run()
