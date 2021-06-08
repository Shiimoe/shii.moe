from flask import Flask, render_template, send_from_directory, request, redirect

import markdown
import markdown.extensions.codehilite
import markdown.extensions.fenced_code
import pymdownx, pymdownx.emoji
import bleach

from datetime import datetime
from os import path
import json

app = Flask(__name__, static_url_path="", static_folder="./")
md = markdown.Markdown(
    extensions=['fenced_code', 'codehilite', 'pymdownx.emoji'],
    extension_configs={
        'pymdownx.emoji': {
            'emoji_index': pymdownx.emoji.gemoji,
            'emoji_generator': pymdownx.emoji.to_png,
        }
    })


ALLOWED_TAGS = list(set(bleach.sanitizer.ALLOWED_TAGS + [
    'ul', 'ol', 'li', 'p', 'pre', 'code', 'blockquote',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'br',
    'strong', 'em', 'a', 'img'
]))
ALLOWED_ATTRIBUTES = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    'a': ['href', 'title'],
    'img': ['src', 'title', 'alt']
}
ALLOWED_PROTOCOLS = list(set(bleach.sanitizer.ALLOWED_PROTOCOLS
    + ['http', 'https', 'mailto']))

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
    for comment in comments:
        comment['comment'] = bleach.clean(comment['comment'],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=ALLOWED_PROTOCOLS)
        comment['comment'] = md.convert(comment['comment'])
    return render_template('guestbook.html', **kw)

@app.route('/guestbook')
def guestbook():
    return render_guestbook()

LINK_MATCH = re.compile("https?://")

@app.route('/postcomment', methods=['POST'])
def postcomment():
    now = datetime.now()

    name = request.form.get('name')
    comment = request.form.get('comment')
    date = request.form.get('date') or datetime.strftime(now, DATE_FORMAT)
    ip = (request.environ.get('HTTP_X_REAL_IP') or
          request.environ.get('REMOTE_ADDR')    or
          request.remote_addr)

    err = lambda msg: render_guestbook(error_msg=msg)

    # Comment or name left empty, send error message.
    if not (name or "").strip() or not (comment or "").strip():
        return err("Please provide a name and comment.")

    # Spam filtering!!
    if len(name) > 130:
        return err("You're taking the piss with a name that long mate.")
    if len(comment) > 850:
        return err("No more than 850 characters!")
    if name.lower() == "annasysdek":
        return err("Sorry, that name is toxic. Pick another.")
    if len(LINK_MATCH.findall(comment)) > 2:
        return err("No more than two (2) links!")

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
