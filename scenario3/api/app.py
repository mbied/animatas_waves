from flask import Flask, jsonify, request, render_template, abort, session
import requests
import json

from functools import wraps
import firebase_admin
from firebase_admin import auth, credentials, db

app = Flask(__name__)
cred = credentials.Certificate('animatas-scenario3-key.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://animatas-scenario3.firebaseio.com/'
})
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

def login_required(f):
    @wraps(f)
    def verify_token(*args, **kwargs):
        token = request.headers.get("Authorization")
        try:
            decoded_token = auth.verify_id_token(token)
        except ValueError:
            abort(403)
        
        return f(*args, user_id=decoded_token["uid"], **kwargs)
    return verify_token

def requre_task_data(f):
    @wraps(f)
    def get_task_data(*args, **kwargs):

        if not request.headers.get("Task"):
            print("Gotcha")
            abort(418)

        user_id = kwargs["user_id"]
        task_id = request.headers.get("Task")
        root = db.reference('/user_data/{0}/{1}'.format(user_id, task_id), default_app)

        if not "task_data" in session:
            # retrieve state from the DB
            session["task_data"] = {
                "id": task_id,
                "target": root.child('target').get(),
                "wave1": root.child('wave1').get(),
                "wave2": root.child('wave2').get()    
            }

        params = f(*args, **kwargs)
        
        # trigger flask session callback
        # this line is totally random but REQUIRED
        session['task_data'] = session['task_data']

        root.child('wave1').set(session['task_data']['wave1'])
        root.child('wave2').set(session['task_data']['wave2'])
            
        return params

    return get_task_data

@app.route('/api/feedback')
@login_required
@requre_task_data
def provide_feedback(user_id=''):
    """ This Callback is used by the agent to receive feedback or guidance. 
        It receives a feedback value as well as a guidance dict (can be empty)
        and returns the new configuration of both waves for the UI to consume.

        The feedback is an float stored in the variable `feedback_value`.
        
        The guidance is put in as a json string and looks something like this

        {
            'wave1': {
                'amplitude': 1
            }
        }

        where `wave1` or `wave2` indicate which wave has been given guidance
        for. `amplitude`, or `frequency` respectively, indicates what type
        of guidance has been given and the number indicates the desired amount
        of change.

        Note: The respective type of guidance (`amplitude` or `phase`) will
        only be present if this kind of guidance has been given.

        Example output of this function:

        response = {
            'wave1': {
                'amplitude': 1,
                'frequency': 2,
            },
            'wave2': {
                'amplitude': 1,
                'frequency': 2,
            }
        }
    """

    try:
        feedback_value = float(request.values["feedback"])
    except KeyError:
        feedback_value = 0

    try:
        guidance_action = json.loads(request.values["guidance"])
    except KeyError:
        guidance_action = dict()

    for (wave, params) in guidance_action.items():
        for (param, value) in params.items():
            session['task_data'][wave][param] += value

    wave1 = session['task_data']['wave1']
    wave2 = session['task_data']['wave2']

    response = {
        'wave1': wave1,
        'wave2': wave2
    }

    return jsonify(response)