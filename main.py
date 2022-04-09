#!/usr/bin/env python3
from flask import Flask, render_template, request
from collections import namedtuple
import json
from sheets import Sheet
import os

if os.path.exists("credentials.json"):
    with open("credentials.json", 'r') as f:
        credentials = json.loads(f.read())
else: # load from env vars
    credentials = {}
    for key in ["type", "project_id", "private_key_id", "private_key", "client_email", "client_id", "auth_uri", "token_uri", "auth_provider_x509_cert_url", "client_x509_cert_url"]:
        credentials[key] = os.getenv(key)

sheet = Sheet(credentials, "Scouting Data")
# sheet.init_sheet()
Level_to_points = {"No Hang": 0,
						"Low": 4,
						"Mid": 6,
						"High": 10,
						"Traversal":15}
app = Flask(__name__)

ENTRY_FILE = "config/RapidReact.json"

Section = namedtuple("Section", 'name entries options')
Entry = namedtuple('Entry', 'name id type options')


def load_entries(file):
    with open(file, 'r') as f:
        data = json.loads(f.read())
    return data


entries = load_entries(ENTRY_FILE)

@app.route("/")
def index():
    return render_template('index.html', entries=entries)


@app.route("/submit", methods=['POST'])
def submit():
    form = request.form
    submission = {} 
    for k in ['team_number', 'scouter_name', 'auton_tarmac', 'auton_upper', 'auton_lower', 'auton_total', 'teleop_lower', 'teleop_upper', 'teleop_total', 'endgame_lower', 'endgame_upper', 'hang_level', 'scoring_bonus', 'hanger_bonus', 'endgame_total', 'hang_time', 'auton_comments', 'teleop_comments', 'endgame_comments']:
        if k.endswith("_total"):
            if k == 'auton_total':
                submission[k] = int(submission['auton_upper'])*4 + int(submission['auton_lower'])*2 + (2 if submission['auton_tarmac'] else 0)
            if k == 'teleop_total':
                submission[k] = int(submission['teleop_upper'])*2 + int(submission['teleop_lower'])
            if k == 'endgame_total':
                submission[k] = Level_to_points[submission["hang_level"]] + int(submission['endgame_upper'])*2 + int(submission['endgame_lower'])
            continue

        if form[k] in ['on', 'off']:
            value = True if form[k] == 'on' else False
        else:
            value = form[k]
        submission[k] = value

    print(tuple(str(d) for d in submission.values()))
    to_submit = []
    for k in ['team_number', 'scouter_name', 'auton_tarmac', 'auton_upper', 'auton_lower', 'auton_total', 'teleop_lower', 'teleop_upper', 'teleop_total', 'endgame_lower', 'endgame_upper', 'hang_level', 'scoring_bonus', 'hanger_bonus', 'endgame_total', 'hang_time', 'auton_comments', 'teleop_comments', 'endgame_comments']:
            to_submit.append(submission[k])
    print(to_submit)
    sheet.append_to_next_empty_row(to_submit)
    return render_template("submitted.html")


@app.template_filter('set_dict_attr')
def set_dict_attr(inp, *args):
    out = inp.copy()  # copy, we don't want pass by ref
    for arg in args:
        key, val = arg
        out[key] = val
    return out


if __name__ == "__main__":
    app.run()
