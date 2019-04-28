from flask import Flask, render_template, url_for
from util import get_school_year
from model import After, Member, Training
from datetime import datetime
app = Flask(__name__)


@app.route('/')
def index():
    render_args = {}
    render_args['title'] = 'index page'
    render_args['body'] = '''
    <h1>index Page!</h1>
    <p>not implemented yet</>
    '''
    render_args['links'] = {"after": url_for('after'),
                            "training": url_for('training'),
                            "member": url_for('member'),
                            "result": url_for('result'),
                            "ranking": url_for('ranking')}
    return render_template('index.html', **render_args)


@app.route('/training')
def training():
    body = "<h1>training Page!</h1>"
    body += "<p>not implemented yet</>"
    render_args = {}
    render_args['title'] = 'training page'
    render_args['body'] = body
    training = Training()
    render_args['articles'] = training.get(limit=20)
    render_args['n'] = len(render_args['articles'])
    # return render_template('template.html', **render_args)
    return render_template('training.html', **render_args)


@app.route('/member')
def member():
    body = "<h1>member Page!</h1>"
    body += "<p>not implemented yet</>"
    render_args = {}
    render_args['title'] = 'member page'
    render_args['body'] = body
    members = {}
    current_year = get_school_year(datetime.now())
    member = Member()
    for year in range(current_year, current_year-6, -1):
        members[year] = member.get(year=year)
    render_args['members'] = members
    render_args['start'] = current_year
    return render_template('member.html', **render_args)


@app.route('/after')
def after():
    body = "<h1>after Page!</h1>"
    body += "<p>not implemented yet</>"
    after = After()
    # data = after.get_colnames()
    # body += "<ul>"
    # for col in data:
    #     body += "<li>{}</li>".format(col)
    # body += "</ul>"
    # body += "<p>{}</p>".format(str(after.get(limit=10)))
    render_args = {}
    render_args['title'] = 'after page'
    render_args['body'] = body
    render_args['articles'] = after.get(limit=20)
    render_args['n'] = len(render_args['articles'])
    # return render_template('template.html', **render_args)
    return render_template('after.html', **render_args)


@app.route('/result')
def result():
    body = "<h1>result Page!</h1>"
    body += "<p>not implemented yet</>"
    render_args = {}
    render_args['title'] = 'result page'
    render_args['body'] = body
    return render_template('template.html', **render_args)


@app.route('/ranking')
def ranking():
    body = "<h1>ranking Page!</h1>"
    body += "<p>not implemented yet</>"
    render_args = {}
    render_args['title'] = 'ranking page'
    render_args['body'] = body
    return render_template('template.html', **render_args)


@app.route('/search')
def search():
    body = "<h1>search Page!</h1>"
    body += "<p>not implemented yet</>"
    render_args = {}
    render_args['title'] = 'search page'
    render_args['body'] = body
    return render_template('template.html', **render_args)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
