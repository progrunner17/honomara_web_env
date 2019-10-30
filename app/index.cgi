#!/usr/bin/env python3
import cgitb
import os
from wsgiref.handlers import CGIHandler
#from app import app
from honomara_members_site import app

cgitb.enable()
os.environ['SCRIPT_NAME'] = '/cgi-bin'
app.debug = True
CGIHandler().run(app)
