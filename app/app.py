from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route('/')
def index():
    body = "<h1>index Page!</h1>"
    body += "<p>not implemented yet</>"
    links = {"afters": url_for('afters'),
             "training": url_for('trainings'),
             "results": url_for('results'),
             "ranking": url_for('ranking')}
    return render_template('flame.html', template='index.html',
                           title='index page', body=body, links=links)


@app.route('/trainings')
def trainings():
    body = "<h1>trainings Page!</h1>"
    body += "<p>not implemented yet</>"
    return render_template('flame.html', template='template.html',
                           title='trainings page', body=body)


@app.route('/afters')
def afters():
    body = "<h1>afters Page!</h1>"
    body += "<p>not implemented yet</>"
    return render_template('flame.html', template='template.html',
                           title='afters page', body=body)


@app.route('/results')
def results():
    body = "<h1>results Page!</h1>"
    body += "<p>not implemented yet</>"
    return render_template('flame.html', template='template.html',
                           title='results page', body=body)


@app.route('/ranking')
def ranking():
    body = "<h1>ranking Page!</h1>"
    body += "<p>not implemented yet</>"
    return render_template('flame.html', template='template.html',
                           title='ranking page', body=body)


@app.route('/search')
def search():
    body = "<h1>search Page!</h1>"
    body += "<p>not implemented yet</>"
    return render_template('flame.html', template='template.html',
                           title='search page', body=body)


if __name__ == "__main__":
    app.run(debug=True)
