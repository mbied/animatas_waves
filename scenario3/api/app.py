from flask import Flask, jsonify, request, render_template
import requests
import json

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

@app.route('/api/feedback')
def provide_feedback():
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

    print(guidance_action, type(guidance_action))

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

    return jsonify(response)

@app.route('/api/getGoal')
def get_goal():
    """Returns the parameters of the current goal wave"""

    response = {'target': {'amplitude': 0.5 , 'frequency': 2}}
    return jsonify(response)