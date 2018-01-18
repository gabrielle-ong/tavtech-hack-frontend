# #!/usr/bin/env python
import argparse
import numpy as np
import os

# #flask imports
from flask import Flask, redirect, render_template, request
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.config['CACHE_TYPE'] = "null"

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images/uploads'
configure_uploads(app, photos)
'''
4 Routes:
GET / - upload image page
POST /convert + CSS loading
GET /databases
GET /knn

GET / - static about page
'''

@app.route('/', methods=['GET'])
def upload():
  return render_template('upload.html')

@app.route('/convert', methods=['POST'])
def convert():
  filename = photos.save(request.files['fileToUpload'])
  pix2pix(filename)
  return redirect('/loading')

@app.route('/loading', methods=['GET'])
def loading():
  return render_template('loading.html')

@app.route('/result', methods=['GET'])
def result():
  # get photo from /static/images/results
  sketch_img_path = "/static/images/uploads/"+os.listdir('static/images/uploads')[0]
  result_img_path = "/static/images/uploads/"+os.listdir('static/images/uploads')[1]
  return render_template('result.html', sketch_img_path=sketch_img_path, result_img_path=result_img_path)

@app.route('/databases', methods=['GET'])
def databases():
  return render_template('databases.html')

@app.route('/knn', methods=['GET'])
def knn():
  return render_template('knn.html')


def pix2pix(filename):
  sketch = os.listdir('')
  os.system("cp static/images/uploads/"+filename + " static/images/uploads/"+filename[:-4]+"_photo.png")
  # save output to /static/images/results


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
