from flask import Flask, render_template, send_from_directory, request, redirect
from datetime import datetime
from os import path
app = Flask(__name__, static_url_path="", static_folder="./")

import json

COMMENT_FILE = "comments.json"
DATE_FORMAT = "%Y-%m-%d %H:%M"

@app.route('/')
def home():
    return send_from_directory('./', 'index.html')

@app.route('/guestbook')
def guestbook():
    comments = None
    with open(COMMENT_FILE, 'r') as f:
        comments = json.load(f)
    return render_template('guestbook.html', comments=reversed(comments))

@app.route('/postcomment', methods=['POST'])
def postcomment():
    name = request.form['name']
    comment = request.form['comment']
    date = datetime.now()

    comments = None
    with open(COMMENT_FILE, 'r') as f:
        comments = json.load(f)
    
    comments.append({
        'name': name,
        'comment': comment,
        'date': datetime.strftime(date, DATE_FORMAT)
    }) 

    with open(COMMENT_FILE, 'w') as f:
        json.dump(comments, f, indent=4, separators=(",", ": "))

    return redirect('/guestbook', code=302)


@app.route('/<p>')
def serve_static(p):
    print("testets")
    if path.exists(p + '.html'):
        return send_from_directory('./', p + '.html')
    return send_from_directory('./', p)