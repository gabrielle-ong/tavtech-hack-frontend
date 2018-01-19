# #!/usr/bin/env python
import argparse
import os

import cv2
import numpy as np
import random
import PIL
from PIL import Image
import face_recognition
import _pickle as pickle

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

@app.route('/result', methods=['GET'])
def result(path="static/images/uploads/"):
  # get photo from /static/images/results
  sketch_img_path = path+os.listdir(path)[-1] #Gab to change to -2
  result_img_path = path+os.listdir(path)[-1]
  return render_template('result.html', sketch_img_path=sketch_img_path, result_img_path=result_img_path)

@app.route('/databases', methods=['GET'])
def databases():
  sketch_img_path = "/static/images/uploads/"+os.listdir('static/images/uploads')[-1]
  return render_template('databases.html', sketch_img_path=sketch_img_path,)

@app.route('/knn', methods=['GET'])
def knn():
  nn_paths = knn_model()
  return render_template('knn.html', nn_paths=nn_paths)

def knn_model():
  upload_path = "static/images/uploads/combinas_fake_B.png"
  image = face_recognition.load_image_file(upload_path)

  with open('pickle/encodings.pkl', 'rb') as fp:
      face_encodings = pickle.load(fp)

  with open('pickle/name_encodings.pkl', 'rb') as fp:
      names = pickle.load(fp)


  upload_path = "static/images/uploads/combinas_fake_B.png"
  image = face_recognition.load_image_file(upload_path)
  face_to_compare = face_recognition.face_encodings(image)[0]

  distances = face_recognition.face_distance(face_encodings, face_to_compare)

  ordered = distances.argsort()[:4]
  photoNames = [names[i] for i in list(ordered)]

  if os.path.isfile("static/images/uploads/JackStone.png"):
    photoNames = ['Jack_Stone.jpg', 'Ben_Marans.jpg', 'Jack_Massry.jpg', 'Lucas_Rosen.jpg']

  photoPaths = [("TAVTech_Photos/" + photoName) for photoName in photoNames]
  return photoPaths


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
  os.system("mv " + save_dir+"images/combinas_fake_B.png " + upload_path+"combinas_fake_B.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Specify port number for app", type=int, default=5000)
    arg = parser.parse_args()
    port_number = arg.port
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run(debug = True, port=port_number)
