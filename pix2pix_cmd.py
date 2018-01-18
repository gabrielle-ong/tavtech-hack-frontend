filename = "JS1.png"

### 0. Dependencies
import os

import cv2
import numpy as np

### 1. Remove + Create test folder in pix2pix
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
os.system("mv " + save_dir+"images/combinas_fake_B.png " + upload_path+filename[:-4]+"_photo.png")