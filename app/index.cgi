#!/usr/bin/env python3
import cgitb, os
cgitb.enable()
from wsgiref.handlers import CGIHandler
from app import app

os.environ['SCRIPT_NAME'] = '/cgi-bin'

CGIHandler().run(app)
