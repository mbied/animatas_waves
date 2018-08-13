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
    try:
        feedback_value = request.values["feedback"]
    except KeyError:
        feedback_value = 0

    try:
        guidance_action = json.loads(request.values["guidance"])
    except KeyError:
        guidance_action = dict()

    print(guidance_action, type(guidance_action))

    response = {
        "a": [feedback_value, guidance_action],
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
    response = {'target': {'amplitude': 0.5 , 'frequency': 2}}
    return jsonify(response)