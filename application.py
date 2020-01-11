from flask import Flask, request, render_template
import json
import re

application = Flask(__name__)

@application.route('/')
def hello():
    return "Hello"
    
@application.route('/Login')
def hello():
    return json.dumps(["Status": "Success"])


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.templates_auto_reload = True
    application.run()