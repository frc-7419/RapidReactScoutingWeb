#!/usr/bin/env python3
from flask import Flask, render_template, request
from collections import namedtuple
import json
from sheets import Sheets

sheet = Sheets("credentials.json", "scouting-test")
sheet.init_sheet()

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
    for k in ['team_number', 'auton_upper', 'auton_lower', 'teleop_upper', 'teleop_lower', 'hang_level', 'scoring_bonus', 'hanger_bonus']:
        if form[k] in ['on', 'off']:
            value = True if form[k] == 'on' else False
        else:
            value = form[k]
        submission[k] = value

    # parse problems
    submission['problems'] = []
    names = form.getlist('problem_name[]')
    sections = form.getlist('problem_game_section[]')
    toggles = form.getlist('problem_toggle[]')
    for name, section, toggle in zip(names, sections, toggles):
        toggle = True if toggle == 'on' else False
        submission['problems'].append((name, section,toggle))

    print(tuple(str(d) for d in submission.values()))
    sheet.append_row(tuple(str(d) for d in submission.values()))
    # redirect
    # TODO: google sheets integration
    return render_template("submitted.html")

@app.template_filter('set_dict_attr')
def set_dict_attr(inp, *args):
    out = inp.copy() # copy, we don't want pass by ref
    for arg in args:
        key, val = arg
        out[key] = val
    return out

if __name__ == "__main__":
    app.run()
