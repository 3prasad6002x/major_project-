import cv2
import h5py
import numpy as np
import mahotas
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from matplotlib.colors import hsv_to_rgb
import os
train_path="C:\\Users\\saipr\\Videos\\plant_disease_detection\\dataset\\train"
h5_train_data          = 'C:\\Users\\saipr\\Videos\\plant_disease_detection\\output\\train_data.h5'
h5_train_labels        = 'C:\\Users\\saipr\\Videos\\plant_disease_detection\\output\\train_label.h5'
images_per_class=800
fixed_size=tuple((256,256))
bins=8
# images_per_class=1200
train_labels = os.listdir(train_path)
# sort the training labels
train_labels.sort()
print(train_labels)
global_features = []
labels          = []

def rgb_bgr(img): #convert the image from BGR to RGB
    rgb_img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return rgb_img
def hsv_img(img): #convert the image from RGB to HSV
    hsv_img1=cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
    return hsv_img1
def img_seg(rgb_img,hsv_img): # Masking the image
    lower_green=np.array([25,0,20])
    upper_green=np.array([100,255,255])
    healthy_mask=cv2.inRange(hsv_img,lower_green,upper_green)
    result=cv2.bitwise_and(rgb_img,rgb_img,mask=healthy_mask)
    lower_brown=np.array([10,0,10])
    upper_brown=np.array([30,255,255])
    disease_mask=cv2.inRange(hsv_img,lower_brown,upper_brown)
    disease_result=cv2.bitwise_and(rgb_img,rgb_img,mask=disease_mask)
    final_mask=healthy_mask+disease_mask
    final_result=cv2.bitwise_and(rgb_img,rgb_img,mask=final_mask)
    return final_result
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
for training_name in train_labels:
    # join the training data path and each species training folder
    dir = os.path.join(train_path, training_name)

    # get the current training label
    current_label = training_name

    # loop over the images in each sub-folder
    for x in range(1,images_per_class+1):
        # get the image file name
        file = dir + "\\" + "image ("+str(x)+")" + ".jpg"
        
    
        #print(file)
        #read the image and resize it to a fixed-size
        image1 = cv2.imread(file)
        #print(image1)
        image = cv2.resize(image1, fixed_size)

        
        #Running Function Bit By Bit
        
        RGB_BGR       = rgb_bgr(image)
        BGR_HSV       = hsv_img(RGB_BGR)
        IMG_SEGMENT   = img_seg(RGB_BGR,BGR_HSV)

        # Call for Global Fetaure Descriptors
        
        fv_hu_moments = fd_hu_moments(IMG_SEGMENT)
        fv_haralick   = fd_haralick(IMG_SEGMENT)
        fv_histogram  = fd_histogram(IMG_SEGMENT)
        
        # Concatenate 
        
        global_feature = np.hstack([fv_histogram, fv_haralick, fv_hu_moments])
        
        

        # update the list of labels and feature vectors'''
        labels.append(current_label)
        global_features.append(global_feature)

    print("[STATUS] processed folder: {}".format(current_label))

print("[STATUS] completed Global Feature Extraction...")

def label_binary(train_labels):
    c=0
    my_dict={}
    for i in train_labels:
        my_dict[i]=c
        c+=1
    return my_dict 

label_dict=label_binary(train_labels)
print(label_dict) 

for i in range(0,len(labels)):
    #print(i)
    for j in label_dict.keys():
        if(labels[i]==j):
            labels[i]=label_dict[j]

global_feature_data=np.array(global_features)
target=np.array(labels)
for i in range(0,25):
    print(labels.count(i))
print(target.shape)
print(global_feature_data.shape)
print(global_feature_data)

h5f_data = h5py.File(h5_train_data, 'w')
h5f_data.create_dataset('dataset_1', data=np.array(global_feature_data))

h5f_label = h5py.File(h5_train_labels, 'w')
h5f_label.create_dataset('dataset_1', data=np.array(target))

h5f_data.close()
h5f_label.close()
