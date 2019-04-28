import wsgiref,logging
from flask import Flask, render_template, request 
app = Flask(__name__)


@app.route('/')
def hello():
    text="<h1>Top Page!</h1>"
    return text

if __name__ == "__main__":
    app.run(debug=True)

