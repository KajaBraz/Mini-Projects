import flask
from examples.main import get_details

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_data():
    if flask.request.method == 'POST':
        url = flask.request.form.get('link')
        extra_stopwords = flask.request.form.get('stop_words')
        collocations = flask.request.form.get('collocations')
        data = get_details(url, collocations, extra_stopwords)
        data['cloud'] = '../' + data['cloud']
        return flask.render_template('returned_data.html', data=data)
    return flask.render_template('form.html')


if __name__ == '__main__':
    app.run()
