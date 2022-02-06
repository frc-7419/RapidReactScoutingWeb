#!/usr/bin/env python3
from flask import Flask, render_template, request
from collections import namedtuple
import json

app = Flask(__name__)

ENTRY_FILE = "config/RapidReact.json"

Section = namedtuple("Section", 'name entries options')
Entry = namedtuple('Entry', 'name id type options')

def load_entries(file):
    parsed = []
    with open(file, 'r') as f:
        data = json.loads(f.read())
        for section in data:
            parsed_entries = []
            for entry in section['entries']:
                parsed_entries.append(Entry(entry['name'], entry['id'], entry['type'], entry['options']))
            parsed.append(Section(section['name'], parsed_entries, section['options']))
    return parsed

entries = load_entries(ENTRY_FILE)
# TODO: problems collapsible and add rows

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
