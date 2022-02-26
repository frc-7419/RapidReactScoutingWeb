#!/usr/bin/env python3
from flask import Flask, render_template, request
from collections import namedtuple
import json
from sheets import Sheet

sheet = Sheet("credentials.json", "Scouting Data")
# sheet.init_sheet()

app = Flask(__name__)

ENTRY_FILE = "config/RapidReact.json"

Section = namedtuple("Section", 'name entries options')
Entry = namedtuple('Entry', 'name id type options')


def load_entries(file):
    with open(file, 'r') as f:
        data = json.loads(f.read())
    return data


entries = load_entries(ENTRY_FILE)
# TODO: problems collapsible and add rows


@app.route("/")
def index():
    return render_template('index.html', entries=entries)


@app.route("/submit", methods=['POST'])
def submit():
    form = request.form
    submission = {}
    for k in ['team_number', 'auton_tarmac', 'auton_upper', 'auton_lower', 'auton_total', 'teleop_lower', 'teleop_upper', 'teleop_total', 'endgame_lower', 'endgame_upper', 'hang_level', 'scoring_bonus', 'hanger_bonus', 'endgame_total']:
        if k.endswith("_total"):
            if k == 'auton_total':
                submission[k] = int(submission['auton_upper'])*4 + int(submission['auton_lower'])*2 + (2 if submission['auton_tarmac'] else 0)
            if k == 'teleop_total':
                submission[k] = int(submission['teleop_upper'])*2 + int(submission['teleop_lower'])
            if k == 'endgame_total':
                submission[k] = 'not implemented yet: https://github.com/frc-7419/RapidReactScoutingWeb' # TODO
            continue

        if form[k] in ['on', 'off']:
            value = True if form[k] == 'on' else False
        else:
            value = form[k]
        submission[k] = value

    # parse problems
    submission['problems'] = []
    names = form.getlist('problem_name[]')
    sections = form.getlist('problem_game_section[]')
    # maximum is 8, change if you want
    for name, section in list(zip(names, sections))[:8]:
        submission['problems'].append(name)
        submission['problems'].append(section)

    print(tuple(str(d) for d in submission.values()))
    to_submit = []
    for k in ['team_number', 'auton_tarmac', 'auton_lower', 'auton_upper', 'auton_total', 'teleop_lower', 'teleop_upper', 'teleop_total', 'endgame_lower', 'endgame_upper', 'hang_level', 'scoring_bonus', 'hanger_bonus', 'endgame_total', 'problems']:
        if k == 'problems':
            # unwrap
            for p in submission['problems']:
                to_submit.append(p)
        else:
            to_submit.append(submission[k])
    print(to_submit)
    sheet.append_to_next_empty_row(to_submit)
    # redirect
    # TODO: google sheets integration
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
