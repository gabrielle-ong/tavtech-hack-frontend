# #!/usr/bin/env python
import argparse
import numpy as np
import os

# #flask imports
from flask import Flask, flash, redirect, render_template, request, session, url_for
# from flask import send_file
# from flask_restful import Resource, Api
# from flask import send_from_directory

# #config import
# import config

'''
4 Routes:
GET /upload - upload image page
POST /transform + CSS loading
GET /result

GET / - static about page
'''

app = Flask(__name__)
app.config['CACHE_TYPE'] = "null"

@app.route('/', methods=['GET'])
def about():
    return render_template('home.html')

@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

@app.route('/transform', methods=['POST])
def transform():
    return render_template('upload.html')

# @app.route('/login')
# def login():
#     oauth_verifier = request.args.get('oauth_verifier')

#     #Set OAUTH keys
#     tl.first_login(session, oauth_verifier)

#     #login with updated OAUTH keys
#     twitter = tl.login(session)

#     response = twitter.get("account/verify_credentials")
#     speaker_id = response[u"id_str"]
#     exists = os.path.exists(os.path.join('./static/traindata/', speaker_id))

#     url = '/train' if not exists else '/home'
#     return redirect(url)

# @app.route("/train")
# def train():
#     def getArticle():
#         text = []
#         with open('article.txt','r') as f:
#             for line in f:
#                 text.append(line)
#         return text

#     twitter = tl.login(session)
#     articles = getArticle()
#     return render_template('train.html', articles = articles)


# @app.route("/home")
# def home():
#     return render_template('home.html')

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Specify port number for app", type=int, default=5000)
    arg = parser.parse_args()
    port_number = arg.port
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run(debug = True, port=port_number)
