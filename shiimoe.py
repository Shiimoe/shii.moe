from flask import Flask, render_template, send_from_directory, request, redirect
from datetime import datetime
from os import path
app = Flask(__name__, static_url_path="", static_folder="./")

import json

COMMENT_FILE = "comments.json"
DATE_FORMAT = "%Y-%m-%d %H:%M"

def read_comments():
    comments = None
    try:
        with open(COMMENT_FILE, 'r') as f:
            comments = json.load(f)
    except FileNotFoundError:
        comments = []

    return comments


@app.route('/')
def home():
    return send_from_directory('./', 'index.html')

def render_guestbook(**kw):
    comments = read_comments()

    kw['comments'] = reversed(comments)
    return render_template('guestbook.html', **kw)

@app.route('/guestbook')
def guestbook():
    return render_guestbook()

@app.route('/postcomment', methods=['POST'])
def postcomment():
    now = datetime.now()

    name = request.form.get('name')
    comment = request.form.get('comment')
    date = request.form.get('date') or datetime.strftime(now, DATE_FORMAT)
    ip = (request.environ.get('HTTP_X_REAL_IP') or
          request.environ.get('REMOTE_ADDR')    or
          request.remote_addr)

    # Comment or name left empty, send error message.
    if not (name or "").strip() or not (comment or "").strip():
        return render_guestbook(error_msg="Please provide a name and comment.")

    comments = read_comments()
    comments.append({
        'name': name,
        'comment': comment,
        'date': date,
        'ip': ip
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

if __name__ == "__main__":
    app.run(debug=True)
