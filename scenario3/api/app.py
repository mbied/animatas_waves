from flask import Flask, jsonify, request, render_template
import requests
import json

import os
import sys

file_dir = "/home/manuel/Documents/WAVE/animatas_waves/scenario3/api/"
sys.path.append(file_dir)

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")

#print("This file path, relative to os.getcwd()")
#print(__file__ + "\n")

#print("This file full path (following symlinks)")
#full_path = os.path.realpath(__file__)
#print(full_path + "\n")

#print("This file directory and name")
#path, filename = os.path.split(full_path)
#print(path + ' --> ' + filename + "\n")

#print("This file directory only")
#print(os.path.dirname(full_path))

from QLearning import QLearning
from DiscreteWavesGridWorld import DiscreteWavesGridWorld

app = Flask(__name__)
env = DiscreteWavesGridWorld()
qLearning = QLearning(env)

def encode_action(dict_guidance_action):
    action = 0
    
    if 'wave2' in dict_guidance_action:
        action += 4
    
    wave = list(dict_guidance_action.keys())[0]
    
    if 'frequency' in dict_guidance_action[wave]:
        action += 2
        
    param = list(dict_guidance_action[wave].keys())[0]    
    print(param)
    
    if dict_guidance_action[wave][param] == -1:
        action += 1
    #print(dict_guidance_action[wave])
    
    return action

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

    print(encode_action(guidance_action))
    #print(guidance_action.keys())
   # print(guidance_action, type(guidance_action))
    action = encode_action(guidance_action)
    next_state, reward, done, _ = env.step(action)
    print(next_state)
    response = {
        'wave1': {
            'amplitude': next_state[0],
            'frequency': next_state[1],
        },
        'wave2': {
            'amplitude': next_state[2],
            'frequency': next_state[3],
        }
    }

    return jsonify(response)

@app.route('/api/getGoal')
def get_goal():
    """Returns the parameters of the current goal wave"""

    response = {'target': {'amplitude': 4 , 'frequency': 2}}

    return jsonify(response)
