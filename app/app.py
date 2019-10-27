from flask import Flask, render_template, url_for, request, redirect
from util import year_to_grade, current_year
from datetime import date
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
    render_args['sorted'] = sorted
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


@app.route('/member/<member_id>')
def member_individual(member_id):
    render_args = {}
    render_args['title'] = 'member page'
    render_args['body'] = '''
            <h1>member individual Page!</h1>
        '''
    render_args['member'] = m.session.query(m.Member).get(member_id)
    return render_template('member_individual.html', **render_args)


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
    render_args['member'] = None
    return render_template('member_edit.html', **render_args)


@app.route('/member/confirm', methods=["POST", "PUT", "DELETE"])
def member_confirm():
    if request.form['confirmed'] == "True":
        if request.method == "DELETE":
            member = m.session.query(m.Member).get(request.form['member_id'])
            # TODO: delete related entries first!!
            
            m.session.delete(member)
        else:
            member = m.Member(form=request.form)
            m.session.add(member)
        m.session.commit()
        return redirect(url_for('member'))
    else:
        render_args = {}
        render_args['member'] = m.Member(form=request.form)
        render_args['method'] = request.method
        render_args['action'] = url_for('member_confirm')
        render_args['title'] = 'member register page'
        render_args['body'] = '''
                <h1>register confirm Page!</h1>
                <p>not implemented yet</>
        '''
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


@app.route('/training/<training_id>')
def training_individual(training_id):
    render_args = {}
    render_args['title'] = 'training page'
    render_args['body'] = '''
            <h1>training individual Page!</h1>
        '''
    render_args['training'] = m.session.query(m.Training).get(training_id)
    return render_template('training_individual.html', **render_args)


@app.route('/training/register', methods=["GET", "POST"])
def training_register():
    render_args = {}
    render_args['method'] = 'POST'
    render_args['action'] = ''
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
    render_args['today'] = date.today()
    # TODO: ADD render_args['training'] with session
    if request.form.get('title') is None:
        render_args['training'] = None
    else:
        render_args['training'] = m.Training(form=request.form)

    render_args['participants'] = request.form.getlist('participants')
    return render_template('training_edit.html', **render_args)


@app.route('/training/confirm', methods=["POST", "PUT", "DELETE"])
def training_confirm():
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
        return redirect(url_for('training'))
    else:
        pass
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


@app.route('/after/<after_id>')
def after_individual(after_id):
    render_args = {}
    render_args['title'] = 'after page'
    render_args['body'] = '''
            <h1>after individual Page!</h1>
        '''
    render_args['after'] = m.session.query(m.After).get(after_id)
    return render_template('after_individual.html', **render_args)


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
    render_args['today'] = date.today()
    render_args['after'] = None
    render_args['restaurants'] = m.session.query(m.Restaurant).all()
    return render_template('after_edit.html', **render_args)


@app.route('/after/confirm', methods=["POST", "PUT", "DELETE"])
def after_confirm():
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
        return redirect(url_for('training'))
    else:
        pass
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
