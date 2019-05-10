from flask import render_template as flask_render_template
from datetime import datetime


def render(template, **args):
    args['template'] = template
    return flask_render_template('flame.html', **args)


def year_to_grade(year, current_year):
    return current_year + 1 - year


def get_school_year(date):
    if date.month < 4:
        return date.year - 1
    else:
        return date.year


current_year = get_school_year(datetime.now())
