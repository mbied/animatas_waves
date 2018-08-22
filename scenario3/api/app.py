from flask import Flask, jsonify, request, render_template, abort
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

@app.route('/api/feedback')
@login_required
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

    # retrieve state from the DB
    task_id = request.headers.get("Task")
    root = db.reference('/user_data/{0}/{1}'.format(user_id, task_id),default_app)

    target = root.child('target').get()
    wave1 = root.child('wave1').get()
    wave2 = root.child('wave2').get()
    
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
            old_value = root.child(wave).child(param).get()
            root.child(wave).update({param: old_value + value})

    response = {
        'wave1': wave1,
        'wave2': wave2
    }

    return jsonify(response)

@app.route('/api/getGoal')
@login_required
def get_goal(user_id=""):
    """Returns the parameters of the current goal wave
    
    Example response:
        
        "target": {
            'wave1': {
                'amplitude': 1,
                'frequency': 1
            },
            'wave2': {
                'amplitude': 1,
                'frequency': 1
            }
        }  
    """

    task_id = request.headers.get("Task")
    root = db.reference('/user_data/{0}/{1}'.format(user_id, task_id),default_app)

    response = {"target": root.child('target').get()}
    return jsonify(response)

@app.route('/api/setGoal')
def set_goal():
    try:
        target = json.loads(request.values['target'])
    except KeyError:
        return "Failed to set a new target"
    
    return "Set new target"