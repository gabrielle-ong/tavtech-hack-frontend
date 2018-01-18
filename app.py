# #!/usr/bin/env python
import argparse
import os

import cv2
import numpy as np

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
  redirect('/loading')
  upload_path = "static/images/uploads/"
  os.system("rm -r " + upload_path)
  os.system("mkdir " + upload_path)
  filename = photos.save(request.files['fileToUpload'])
  pix2pix(filename)
  return redirect('/result')

@app.route('/loading', methods=['GET'])
def loading():
  return render_template('loading.html')

@app.route('/result', methods=['GET'])
def result(path="static/images/uploads/"):
  # get photo from /static/images/results
  sketch_img_path = path+os.listdir(path)[0]
  result_img_path = path+os.listdir(path)[1]
  return render_template('result.html', sketch_img_path=sketch_img_path, result_img_path=result_img_path)

@app.route('/databases', methods=['GET'])
def databases():
  return render_template('databases.html')

@app.route('/knn', methods=['GET'])
def knn():
  return render_template('knn.html')


def pix2pix(filename):

  upload_path = "static/images/uploads/"
  test_path = "pix2pix/datasets/faces/test/"
  save_dir = "results/faces_pix2pix/test_latest/"
  os.system("rm -r " + test_path)
  os.system("mkdir " + test_path)
  os.system("rm -r " + save_dir)


  ### 2. Concatenate Images
  img = cv2.cvtColor(cv2.imread(upload_path+filename), cv2.COLOR_BGR2RGB)
  img = cv2.resize(img, (200, 250))
  img_combinas = np.concatenate([img, img], 1)
  cv2.imwrite(test_path+"combinas.png", img_combinas)

  ### 3. Perform Image Translation
  os.system("python pix2pix/test.py --dataroot pix2pix/datasets/faces --name faces_pix2pix --model pix2pix --which_model_netG unet_256 --which_direction BtoA --dataset_mode aligned --norm batch --gpu_id -1")
  os.system("mv " + save_dir+"images/combinas_fake_B.png " + upload_path+filename[:-4]+"_photo.png")


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
