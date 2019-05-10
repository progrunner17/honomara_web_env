from flask import Flask, render_template, url_for, request, redirect
from util import year_to_grade, current_year
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
    render_args['sorted'] = sorted
    return render_template('member.html', **render_args)


@app.route('/member/register')
def member_register():
    render_args = {}
    render_args['method'] = 'POST'
    render_args['action'] = url_for('member_confirm')
    render_args['current_year'] = current_year
    render_args['title'] = 'member register page'
    render_args['body'] = '''
            <h1>training register Page!</h1>
            <p>not implemented yet</>
    '''
    # TODO: ADD render_args['member'] with session
    return render_template('member_edit.html', **render_args)


@app.route('/member/confirm', methods=["POST", "PUT", "DELETE"])
def member_confirm():
    if request.form['confirmed'] == "true":
        if request.method == "POST":
            pass
            # session.add(form=Member(request.form))
            # session.commit()
        elif request.method == "PUT":
            # member = session.query(Member).get(request.form['member_id'])
            # member. = request.form[]
            # session.add(member)
            # session.commit
            pass
        else:  # DELETE
            # member = session.query(Member).get(request.form['member_id'])
            # session.delete(Member)
            # sesstion.commit()
            pass
        return redirect(url_for('member'))
    else:
        render_args = {}
        render_args['method'] = request.method
        render_args['action'] = url_for('member_confirm')
        render_args['title'] = 'member register page'
        render_args['body'] = '''
                <h1>register confirm Page!</h1>
                <p>not implemented yet</>
        '''
        # TODO: add error check especially about None
        # TODO: move member generation code to Member constructor
        member = {}
        member['member_id'] = int(request.form.get('member_id', -1))
        member['family_name'] = request.form.get('family_name')
        member['first_name'] = request.form.get('first_name')
        member['show_name'] = request.form.get('show_name')
        member['kana'] = request.form.get('kana')
        member['year'] = int(request.form.get('year'))
        member['sex'] = int(request.form.get('sex'))
        member['visible'] = int(request.form.get('visible'))
        render_args['member'] = m.Member(**member)

        return render_template('member_confirm.html', **render_args)


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
    return render_template('training_edit.html', **render_args)


@app.route('/training/confirm', methods=["POST", "PUT", "DELETE"])
def training_confirm():
    return "not implemented"


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
    render_args['today'] = "{:%Y-%m-%d}".format(datetime.now())
    render_args['after'] = None
    return render_template('after_edit.html', **render_args)


@app.route('/after/confirm', methods=["POST", "PUT", "DELETE"])
def after_confirm():
    return "not implemented"


@app.route('/result')
def result():
    render_args = {}
    render_args['title'] = 'result page'
    render_args['body'] = '''
            <h1>Result Page!</h1>
            <p>not implemented yet</>
        '''
    return render_template('template.html', **render_args)


@app.route('/ranking')
def ranking():
    render_args = {}
    render_args['title'] = 'ranking page'
    render_args['body'] = '''
            <h1>Ranking Page!</h1>
            <p>not implemented yet</>
        '''
    return render_template('template.html', **render_args)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
