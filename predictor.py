import cv2
import h5py
import numpy as np
import mahotas
import joblib
from picamera import PiCamera
from time import sleep
print(joblib.__version__)
from joblib import load
from matplotlib.colors import hsv_to_rgb
import os
bins=8
hist_gradient_predictor,random_forest_predictor=load("C:\\Users\\saipr\\Videos\\plant_disease_detection\\model_predictor_saved.joblib")
train_path="C:\\Users\\saipr\\Videos\\plant_disease_detection\\dataset\\train"
fixed_size=tuple((256,256))
train_labels = os.listdir(train_path)
train_labels.sort()
print(train_labels)
print(joblib.__version__)

def fd_hu_moments(image): #identifying the outline of the images
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    feature = cv2.HuMoments(cv2.moments(image)).flatten()
    return feature
def fd_haralick(image): #Describe the "texture" of an image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    haralick = mahotas.features.haralick(gray).mean(axis=0)
    return haralick
def fd_histogram(image, mask=None): # colour histogram
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist  = cv2.calcHist([image], [0, 1, 2], None, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()

import matplotlib.pyplot as plt
import cv2
camera=PiCamera()
camera.resolution=(800,600)
camera.start_preview() # capture the image
camera.brightness=70
sleep(10)
camera.capture("/home/pi/Downloads/plant-disease-detection21.jpg")
camera.stop_preview()

dir="C:\\Users\\saipr\\Videos\\plant_disease_detection\\dataset\\train\\"
disease_name="Apple___healthy"
image_name="\\image (998).JPG"
file_name=dir+disease_name+image_name
print(file_name)
image=cv2.imread(file_name)
image=cv2.imread("/home/pi/Downloads/plant-disease-detection21.jpg")
image = cv2.resize(image, fixed_size)
c=0
disease_name_dict={}
for i in train_labels:
    disease_name_dict[i]=c
    c+=1


#converting the image from bgr to rgb
rgb_img=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
#converting the image from rgb to hsv
hsv_img1=cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
#masking the image
lower_green=np.array([25,0,20])
upper_green=np.array([100,255,255])
healthy_mask=cv2.inRange(hsv_img1,lower_green,upper_green)
result=cv2.bitwise_and(rgb_img,rgb_img,mask=healthy_mask)
lower_brown=np.array([10,0,10])
upper_brown=np.array([30,255,255])
disease_mask=cv2.inRange(hsv_img1,lower_brown,upper_brown)
disease_result=cv2.bitwise_and(rgb_img,rgb_img,mask=disease_mask)
final_mask=healthy_mask+disease_mask
final_result=cv2.bitwise_and(rgb_img,rgb_img,mask=final_mask)
fv_hu_moments = fd_hu_moments(final_result)
fv_haralick   = fd_haralick(final_result)
fv_histogram  = fd_histogram(final_result)      
global_feature1 = np.hstack([fv_histogram, fv_haralick, fv_hu_moments])

prediction_1=hist_gradient_predictor.predict(np.array(global_feature1).reshape(1,-1))
prediction_2=random_forest_predictor.predict(np.array(global_feature1).reshape(1,-1))

for key,value in disease_name_dict.items():
    if(prediction_1==value):
        print(key)
for key,value in disease_name_dict.items():
    if(prediction_2==value):
        print(key) 

print(disease_name_dict)
fig,(ax1,ax2,ax3)=plt.subplots(ncols=3,nrows=1,figsize=(9,8))

ax1.imshow(rgb_img)
ax1.set_title("original")
ax2.imshow(final_mask,cmap="gray")
ax2.set_title("processing")
ax3.imshow(final_result)
ax3.set_title("final")
fig.suptitle("\n \n \n input disease name is    '{}' \n    Random_forest_prediction is      '{}' \n     hist_gradient_boosting is       '{}'".format(disease_name,y,x))
fig.tight_layout()
plt.show()

