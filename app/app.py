from flask import Flask, render_template, url_for
from util import get_school_year, year_to_grade
from datetime import datetime
import model as m
app = Flask(__name__)


@app.route('/')
def index():
    render_args = {}
    render_args['title'] = 'index page'
    render_args['links'] = {"after": url_for('after'),
                            "training": url_for('training'),
                            "member": url_for('member'),
                            "result": url_for('result'),
                            "ranking": url_for('ranking')}
    return render_template('index.html', **render_args)


@app.route('/manage')
def manage():
    render_args = {}
    render_args['title'] = 'manage page'
    render_args['links'] = {
        "after register": url_for('after_register'),
        "training_register": url_for('training_register'),
        }
    return render_template('index.html', **render_args)


@app.route('/member')
def member():
    current_year = get_school_year(datetime.now())
    render_args = {}
    render_args['title'] = 'member page'
    render_args['body'] = '''
            <h1>member Page!</h1>
            <p>not implemented yet</>
        '''
    render_args['members'] = {
        year: m.session.query(m.Member).filter_by(year=year)
        for year in range(current_year, current_year-6, -1)
        }
    render_args['start'] = current_year
    return render_template('member.html', **render_args)


@app.route('/member/register', methods=["GET", "POST"])
def member_register():
    current_year = get_school_year(datetime.now())
    render_args = {}
    render_args['current_year'] = current_year
    render_args['title'] = 'member register page'
    render_args['body'] = '''
            <h1>training register Page!</h1>
            <p>not implemented yet</>
    '''
    return render_template('member_register.html', **render_args)


@app.route('/training')
def training():
    render_args = {}
    render_args['title'] = 'training page'
    render_args['body'] = '''
        <h1>training Page!</h1>
        <p>not implemented yet</>
    '''
    render_args['trainings'] = m.session.query(m.Training)\
        .order_by(m.Training.date.desc())\
        .limit(20)
    return render_template('training.html', **render_args)


@app.route('/training/register', methods=["GET", "POST"])
def training_register():
    current_year = get_school_year(datetime.now())
    render_args = {}
    render_args['title'] = 'training page'
    render_args['body'] = '''
            <h1>training register Page!</h1>
            <p>not implemented yet</>
        '''
    render_args['members'] = {
        year_to_grade(year, current_year):
            {
                member.member_id: member.show_name
                for member in m.session.query(m.Member).filter_by(year=year)
            }
        for year in range(current_year, current_year-6, -1)
        }
    return render_template('training_register.html', **render_args)


@app.route('/after')
def after():
    render_args = {}
    render_args['title'] = 'after page'
    render_args['body'] = '''
            <h1>after Page!</h1>
            <p>not implemented yet</>
        '''
    render_args['afters'] = m.session.query(m.After)\
        .order_by(m.After.date.desc())\
        .limit(20)
    render_args['Member'] = m.Member
    render_args['After'] = m.After
    return render_template('after.html', **render_args)


@app.route('/after/register', methods=["GET", "POST"])
def after_register():
    current_year = get_school_year(datetime.now())
    render_args = {}
    render_args['title'] = 'manage page'
    render_args['body'] = '''
            <h1>after register Page!</h1>
            <p>not implemented yet</>
        '''
    render_args['members'] = {
        year_to_grade(year, current_year):
            {
                member.member_id: member.show_name
                for member in m.session.query(m.Member).filter_by(year=year)
            }
        for year in range(current_year, current_year-6, -1)
        }
    return render_template('after_register.html', **render_args)


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
