#!/usr/bin/env python
# -*- coding:utf8 -*-

from flask import Flask, request, render_template, redirect
import markdown as md
import logging as log
import json


with open("tpassist.conf.json", 'r') as f:
    conf = json.loads(f.read())

user = False

app = Flask("tpassist")

# if(not self.app.debug):
#     file_handler = log.handlers.RotatingFileHandler("tpassist", maxBytes=65535, backupCount=5)
#     self.app.logger.setLevel(log.WARNING)
#     self.app.logger.add_handler(file_handler)


@app.route("/update_md", methods=['POST'])
def update_md():
    data = json.loads(request.form.keys()[0])
    html = md.markdown(data["markdown"], ['codehilite', 'extra', 'nl2br'])
    print html
    with open(data["title"] + ".md", 'w+') as f:
        f.write(data["markdown"])
    return html

@app.route("/upload_file", methods=['POST'])
def upload_file():
    pass

@app.route('/', methods=['GET'])
def home():
    # if(not user):
    #     return redirect('/login')
    return render_template('home.html')

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
