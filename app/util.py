from flask import render_template as flask_render_template


def render(template, **args):
    args['template'] = template
    return flask_render_template('flame.html', **args)


def get_school_year(date):
    if date.month < 4:
        return date.year - 1
    else:
        return date.year
