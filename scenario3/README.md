# Scenario 3: Interactive Waves

This task features a web UI as well as a reinforcement learning agent that can be trained to solve wave addition tasks.
This is acomplished by providing feedback to each of the human's actions, i.e. the human acts as the reward function.
Additionally, the human can administer guidance to force the agent to take a certain action.

The main aim of this task is to study how humans give feedback. 
Previous studies have found that there is a bias towards positive reinforcement and, despite different theories, there is no
uniform explanation as to why humans prefer to give positive reinforcement to robots.

## Getting Started

To run the development version of this task you will need [`npm`](https://www.npmjs.com/get-npm) and [`python`](https://www.python.org/).

First install the web UI's dependencies and launch a development web server:

    cd UI/www
    npm install
    npm run development

Then, in a new terminal, install the API dependencies and launch the development flask server:

    cd api
    pip install -r Requirements.txt
    export FLASK_APP=app.py
    export FLASK_ENV=dev
    flask run

Now the app should be available at http://localhost:5000/#/exercise .