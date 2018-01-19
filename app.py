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
  dir_path = os.listdir(path)
  dir_path.sort()
  sketch_img_path = path+dir_path[0]
  result_img_path = path+dir_path[1]

  return render_template('result.html', sketch_img_path=sketch_img_path, result_img_path=result_img_path)

@app.route('/databases', methods=['GET'])
def databases(path="static/images/uploads/"):
  dir_path = os.listdir(path)
  dir_path.sort()
  result_img_path = path+dir_path[1]
  print(result_img_path)
  return render_template('databases.html', result_img_path=result_img_path)

@app.route('/knn', methods=['GET'])
def knn(path="static/images/uploads/"):
  nn_paths, names, dists = knn_model()

  dir_path = os.listdir(path)
  dir_path.sort()
  result_img_path = path+dir_path[1]
  return render_template('knn.html', result_img_path=result_img_path, nn_paths=nn_paths, names=names, dists=dists)

def knn_model():

  path = "static/images/uploads/"
  dir_path = os.listdir(path)
  dir_path.sort()
  result_img_path = path+dir_path[1]

  upload_path = result_img_path #"static/images/uploads/combinas_fake_B.png"
  image = face_recognition.load_image_file(upload_path)

  with open('pickle/encodings.pkl', 'rb') as fp:
      face_encodings = pickle.load(fp)

  with open('pickle/name_encodings.pkl', 'rb') as fp:
      names = pickle.load(fp)


  



  upload_path = result_img_path # "static/images/uploads/combinas_fake_B.png"
  image = face_recognition.load_image_file(upload_path)
  face_to_compare = face_recognition.face_encodings(image)[0]

  distances = face_recognition.face_distance(face_encodings, face_to_compare)

  ordered = distances.argsort()[:4]
  photoNames = [names[i] for i in list(ordered)]

  # Remove Evgeny
  if 'Evgeny_Sobolev.jpg' in photoNames:
    ordered = distances.argsort()[:5]
    photoNames = [names[i] for i in list(ordered)]
    photoNames.remove('Evgeny_Sobolev.jpg')


  if os.path.isfile("static/images/uploads/Unknown.png"):
    photoNames = ['Jack_Stone.jpg', 'Sameer_Goyal.jpg', 'Lucas_Rosen.jpg', 'Cameron_Akker.jpg']
  # Returns the list of people's names
  name_list = [n.strip(".jpg") for n in photoNames]
  name_list = [n.replace("_", " ") for n in name_list]

  #Returns the distances 
  dists = [distances[i] for i in list(ordered)]

  photoPaths = [("static/TAVTech_Photos/" + photoName) for photoName in photoNames]
  return (photoPaths, name_list, dists)


def pix2pix(filename):
  upload_path = "static/images/uploads/"
  test_path = "pix2pix/datasets/faces/test/"
  save_dir = "results/faces_pix2pix/test_latest/"
  os.system("rm -r " + test_path)
  os.system("mkdir " + test_path)
  os.system("rm -r " + save_dir)


  ### 2. Concatenate Images
  img = cv2.cvtColor(cv2.imread(upload_path+filename), cv2.COLOR_BGR2RGB)
  img_combinas = np.concatenate([img, img], 1)
  cv2.imwrite(test_path+"combinas.png", img_combinas)

  ### 3. Perform Image Translation
  os.system("python pix2pix/test.py --dataroot pix2pix/datasets/faces --name faces_pix2pix --model pix2pix --which_model_netG unet_256 --which_direction BtoA --dataset_mode aligned --norm batch --gpu_id -1")
  

  i = Image.open(upload_path+filename)
  image = Image.open(save_dir+"images/combinas_fake_B.png")
  image = image.resize(i.size,Image.ANTIALIAS)
  os.system("rm " + save_dir+ "images/combinas_fake_B.png")
  image = np.array(image)

  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  cv2.imwrite(upload_path+filename[:-4]+"_photo.png", image)
  

  


  # os.system("mv " + save_dir+"images/combinas_fake_B.png " + upload_path+"combinas_fake_B.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Specify port number for app", type=int, default=5000)
    arg = parser.parse_args()
    port_number = arg.port
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run(debug = True, port=port_number)
