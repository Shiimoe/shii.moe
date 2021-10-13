#!/usr/bin/env python3

from flask import Flask, render_template, send_from_directory, request, redirect
import jinja2

import markdown
import markdown.extensions.codehilite
import markdown.extensions.fenced_code
import pymdownx, pymdownx.emoji
import bleach

from datetime import datetime
import os
import random
import json
import re

BLOG_PATH = os.path.realpath('./blog')
STATIC_PATH = os.path.realpath('./static')
PUBLIC_PATH = os.path.realpath('./public')
TEMPLATE_PATH = os.path.realpath('./shiimoe/templates')
COMMENT_FILE = os.path.realpath('./comments.json')
DATE_FORMAT = "%Y-%m-%d %H:%M"

app = Flask(__name__, static_folder=PUBLIC_PATH)

md = markdown.Markdown(
    extensions=[
        'fenced_code', 'codehilite',
        'pymdownx.emoji', 'smarty', 'attr_list',
        'full_yaml_metadata', 'markdown_captions'],
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

MASCOT_COUNT = int(len(os.listdir(f"{PUBLIC_PATH}/mascots")) / 2)

def get_blog_posts():
    posts = []
    for file in os.listdir(BLOG_PATH):
        slug = file[:-3]
        meta = None
        with open(f"{BLOG_PATH}/{file}", 'r') as f:
            md.convert(f.read())
            meta = md.Meta
        posts.append({
            'slug': slug,
            'title': meta['title'],
            'published': meta['published'],
            'date': datetime.strftime(meta['published'], '%Y-%m-%d'),
            'datetime': meta['published'].isoformat()
        })
    posts.sort(key = lambda post: post['published'], reverse=True)
    return tuple(posts)

def get_blog_post(slug):
    keywords = {
        'slug': slug,
        'title': None
    }
    try:
        with open(f"{BLOG_PATH}/{slug}.md", 'r') as file:
            content = file.read()
            keywords["content"] = md.convert(content)
            keywords["title"] = md.Meta['title']
    except FileNotFoundError:
        return None

    return keywords

STATIC_BLOG_POSTS = get_blog_posts()

def _template(tmplt, **kw):
    kw['mascot'] = random.randint(1, MASCOT_COUNT)
    return render_template(tmplt, **kw)

def static_template(tmplt, **kw):
    kw['mascot'] = random.randint(1, MASCOT_COUNT)
    kw['request'] = { 'path': f"/{tmplt[:-5]}" }
    if tmplt == 'blogindex.html':
        kw['request']['path'] = '/blog'
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('shiimoe','templates'))
    template = env.get_template(tmplt)
    return template.render(**kw)

def frozen(d):
    if isinstance(d, dict):
        return frozenset(frozen(item) for item in d.items())
    if isinstance(d, list) or isinstance(d, tuple):
        return tuple(frozen(item) for item in d)
    return d

STATIC_TEMPLATES = {
    ('index.html',  frozen({})): static_template('index.html'),
    ('music.html',  frozen({})): static_template('music.html'),
    ('school.html', frozen({})): static_template('school.html'),
    ('norsk.html',  frozen({})): static_template('norsk.html'),
    ('books.html',  frozen({})): static_template('books.html'),
    ('blogindex.html', frozen({
        'posts': STATIC_BLOG_POSTS
    })): static_template('blogindex.html', posts=STATIC_BLOG_POSTS),
}

for blogpost in os.listdir(BLOG_PATH):
    slug = blogpost[:-3]
    kw = get_blog_post(slug)
    STATIC_TEMPLATES[('blogpost.html', frozen(kw))] = (
        static_template('blogpost.html', **kw)
    )

def template(tmplt, **kw):
    rendered = STATIC_TEMPLATES.get((tmplt, frozen(kw)))
    if rendered:
        print("Serving cached static template:", tmplt)
        return rendered
    print("Server rendering template:", tmplt)
    return _template(tmplt, **kw)

def read_comments():
    comments = None
    try:
        with open(COMMENT_FILE, 'r') as f:
            comments = json.load(f)
    except FileNotFoundError:
        comments = []

    return comments

def is_subpath(path, dir):
    return path.startswith(dir)

def send_static_page(path, filename):
    path = os.path.realpath(os.path.join(STATIC_PATH, path))
    if not is_subpath(path, STATIC_PATH):
        return 403

    if not filename.endswith('.html'):
        filename += '.html'
    return send_from_directory(path, filename)

def send_public_asset(path, filename):
    path = os.path.realpath(os.path.join(PUBLIC_PATH, path))
    if not is_subpath(path, PUBLIC_PATH):
        return 403

    return send_from_directory(path, filename)

@app.route('/')
def home():
    return template('index.html')

def render_guestbook(**kw):
    comments = read_comments()
    comments.reverse()

    for comment in comments:
        comment['comment'] = bleach.clean(comment['comment'],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=ALLOWED_PROTOCOLS)
        comment['comment'] = md.convert(comment['comment'])

    kw['comments'] = comments
    return template('guestbook.html', **kw)

@app.route('/guestbook')
@app.route('/guestbook.html')
def guestbook():
    return render_guestbook()

@app.route('/blog')
@app.route('/blog/index.html')
def blogindex():
    posts = get_blog_posts()
    return template('blogindex.html', posts=posts)

@app.route('/blog/<slug>')
@app.route('/blog/<slug>.html')
def blogpost(slug):
    keywords = get_blog_post(slug)
    if keywords is None:
        return send_static_page('./', '404.html'), 404

    return template('blogpost.html', **keywords)

LINK_MATCH = re.compile("https?://")

@app.route('/postcomment', methods=['POST'])
def postcomment():
    now = datetime.now()

    name = request.form.get('name')
    comment = request.form.get('comment')
    date = request.form.get('date') or datetime.strftime(now, DATE_FORMAT)
    ip = (request.environ.get('HTTP_X_REAL_IP')
       or request.environ.get('REMOTE_ADDR')
       or request.remote_addr)

    err = lambda msg: render_guestbook(error_msg=msg, dcomment=comment, dname=name)

    # Comment or name left empty, send error message.
    if not (name or "").strip() or not (comment or "").strip():
        return err("Please provide a name and comment.")

    # Spam filtering!!
    if len(name) > 110:
        return err("You're taking the piss with a name that long mate.")
    if len(comment) > 850:
        return err("No more than 850 characters!")
    if name.lower() == "annasysdek":
        return err("Sorry, that name is toxic. Pick another.")
    if len(LINK_MATCH.findall(comment)) != 0:
        return err("No links!")

    comments = read_comments()
    if any(c['comment'] == comment for c in comments):
        return err("Duplicate comment. Please write unique comments.")

    comments.append({
        'name': name,
        'comment': comment,
        'date': date,
        'ip': ip
    })

    with open(COMMENT_FILE, 'w') as f:
        json.dump(comments, f, indent=4, separators=(",", ": "))

    return redirect('/guestbook', code=302)


@app.route('/<path:filepath>')
def serve_static(filepath):
    path, filename = os.path.split(filepath)
    if os.path.exists(os.path.join(PUBLIC_PATH, path, filename)):
        return send_public_asset(path, filename)
    if not filename.endswith('.html'):
        filename += '.html'
    if os.path.exists(os.path.join(TEMPLATE_PATH, path, filename)):
        return template(os.path.join(path, filename))
    if os.path.exists(os.path.join(STATIC_PATH, path, filename)):
        return send_static_page(path, filename)
    # Otherwise, 404.
    return send_static_page('./', '404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
