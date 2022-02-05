#!/usr/bin/env python3
from flask import Flask, render_template, request
from collections import namedtuple

app = Flask(__name__)

Entry = namedtuple('Entry', 'name id type options')
# TODO: problems collapsible and add rows
entries = {
    "Scouting": [
        Entry('Team Number', 'team_number', 'input', {
            'type': 'number',
            'required': True
        }),
    ],
    "Autonomous": [
        Entry("Upper Hub Scored", 'auton_upper', 'stepper', None),
        Entry("Lower Hub Scored", 'auton_lower', 'stepper', None)
    ],
    "Tele-Op": [
        Entry("Upper Hub Scored", 'teleop_upper', 'stepper', None),
        Entry("Lower Hub Scored", 'teleop_lower', 'stepper', None),

    ],
    "Endgame": [
        Entry("Hang Level", 'hang_level', 'segmented', {
            'choices': [
                'No Hang',
                'Low',
                'Mid',
                'High',
                'Traversal'
            ],
            'width': 120 # in pixels
        }),
        Entry("Scoring Bonus", 'scoring_bonus', 'switch', None),
        Entry("Hanger Bonus", 'hanger_bonus', 'switch', None)
    ]
}

@app.route("/")
def index():
    return render_template('index.html', entries=entries)

@app.route("/submit", methods=['POST'])
def submit():
    # redirect
    print(request.form)
    # TODO: google sheets integration
    return 'hi'

if __name__ == "__main__":
    app.run()
