#!/usr/bin/env python
# -*- coding:utf8 -*-

import os

from flask import Flask, request, render_template, redirect, send_file
from werkzeug import secure_filename
import markdown as md
import json

from models import Document

version = "0.0.9"

with open("tpassist.conf.json", 'r') as f:
    conf = json.loads(f.read())

docs = {}

app = Flask("tpassist")
UPLOAD_FOLDER = 'static/media'
MD_SAVE_FOLDER = 'documents'  # not used for now
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/<name>/update_md", methods=['POST'])
def update_md(name):
    data = json.loads(request.form.keys()[0])
    app.logger.info(data)
    global docs
    try:
        doc = docs[name]
    except KeyError:
        app.logger.error("index \"%s\" does not exist in the global document index! that means the server has been restarted. Please go to / and try reopening the document." % name)
        return "ERROR: please see logs", 500
    doc.markdown += data["markdown"]
    doc.save()
    return md.markdown(doc.markdown, ['codehilite', 'extra', 'nl2br', 'toc'])


@app.route("/<fname>/dl/<format>")
def dl(fname, format):
    if(format == "md"):
        return docs[fname].markdown
    elif(format == "html"):
        return docs[fname]._gen_html()
    elif(format == "pdf"):
        return send_file(docs[fname].get_pdf_file_descriptor())
    return "501 Not implemented", 501


@app.route("/<name>/upload", methods=["POST"])
def upload_file(name):
    f = request.files['file_up']
    desired_path = request.form['file_to']
    if(f):
        if(not os.path.exists(UPLOAD_FOLDER)):
            os.mkdir(UPLOAD_FOLDER)
        desired_path = secure_filename(desired_path)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], desired_path))
        return "", 200
    else:
        return "No file", 400


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/<fname>/edit')
def edit(fname):
    global docs
    document = Document(fname)
    docs[fname] = document
    return render_template('editor.html', doc=document)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if(request.method == 'GET'):
        return render_template('login.html')
    elif(request.method == 'POST'):
        for user in conf["users"]:
            if(request.form['user'] == user['username'] and request.form['passwd'] == user['passwd']):
                user = user['username']
                print("logged user %s" % user)
                return redirect('/')

@app.route('/logout')
def logout():
    if(user):
        user = False
    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0")
