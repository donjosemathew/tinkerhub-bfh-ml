import numpy as np
%tensorflow_version 2.x
from numpy.core.fromnumeric import shape
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from keras.preprocessing.image import ImageDataGenerator
import random
import sklearn as sk
import cv2
%tensorflow_version 2.x
from keras.preprocessing import image
import matplotlib.pyplot as plt
import os



IMG_SIZE = 200

class_names = ['Jackfruit', 'Mango']

def create_data(DATADIR, img_array = [],x=0):
    img_array = []
    CATEGORIES = ['0', '1']
    for category in CATEGORIES :
        path = os.path.join(DATADIR, category)
        for img in os.listdir(path):
            x+=1
            # print(os.path.join(path,img))
            img = cv2.imread(os.path.join(path, img))
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))   
            # img = img/255         
            img_array.append(img)
     
          
    return img_array,x

training_images,len1 = create_data(DATADIR = '/content/drive/MyDrive/TinkerHub BFH 2021/train')
testing_images,len2 = create_data(DATADIR = '/content/drive/MyDrive/TinkerHub BFH 2021/test')



# Importing labels

def create_training_label(DATADIR, label = []):
    k=0
    CATEGORIES = ['0', '1']
    label = []
    for category in CATEGORIES :
        path = os.path.join(DATADIR, category)
        for img in os.listdir(path):
            path = os.path.join(DATADIR, category)
        
            label.append(int(category))
        
         
    return label

train_labels = create_training_label(DATADIR = '/content/drive/MyDrive/TinkerHub BFH 2021/train')
test_labels = create_training_label(DATADIR = '/content/drive/MyDrive/TinkerHub BFH 2021/test')


# Data Augmentation

def augment(lenx, test, training_images = [], testing_images = [], train_labels = [], test_labels = []):
    
    print(lenx)
    datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')
    
    for k in range(0,lenx):
    
        if test == True:
            img = testing_images[k]     
        else:
            img = training_images[k]
            
        img = img.reshape((1,) + img.shape)  # reshape image
        i=0

        for batch in datagen.flow(img, save_prefix='test', save_format='jpeg'): 
            
            if test == True:
                
                
                testing_images.append(batch)
                test_labels.append(test_labels[k])

            else:
                
                training_images.append(batch)
                train_labels.append(train_labels[k])
            
            i += 1 
            if i > 4:  
                break

    if test == True:
        return testing_images, test_labels
    else:
        return training_images, train_labels

    
test_images, test_labels = augment(lenx = len2, testing_images = testing_images,  test = True, test_labels= test_labels)
train_images, train_labels = augment(lenx = len1, training_images = training_images, test = False, train_labels= train_labels)

len3 = len(train_images)
len4 = len(test_images)

train_images_arr = np.zeros((len3,200,200,3), 'uint8')
test_images_arr = np.zeros((len4,200,200,3), 'uint8')
train_labels_arr = np.zeros(len3, dtype = np.int32)
test_labels_arr = np.zeros(len4, dtype = np.int32)

for i in range(0,len3):
    train_images_arr[i] = train_images[i]/255
    train_labels_arr[i] = train_labels[i]
for i in range(0,len4):
    test_images_arr[i] = test_images[i]/255
    test_labels_arr[i] = test_labels[i]

# Shuffling input data
train_images_arr, train_labels_arr = sk.utils.shuffle(train_images_arr, train_labels_arr)
test_images_arr, test_labels_arr = sk.utils.shuffle(test_images_arr, test_labels_arr)  

"""
CNN Architecture
"""

model = models.Sequential()
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# Model summary

model.summary()



# Adding the layers
model.add(layers.Flatten()) 
model.add(layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.3))
model.add(layers.Dense(50, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(layers.Dense(50, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(layers.Dense(50, activation='relu'))
model.add(tf.keras.layers.Dropout(0.3))
model.add(layers.Dense(50, activation='relu'))
model.add(tf.keras.layers.Dropout(0.3))
model.add(layers.Dense(40, activation='softmax'))

model.add(layers.Dense(2))

# Printing model summary
model.summary()

# Now we're training the model

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# To access some statistics.
history = model.fit(train_images_arr, train_labels_arr, epochs=25, 
                    validation_data=(test_images_arr, test_labels_arr))


test_loss, test_acc = model.evaluate(test_images_arr,  test_labels_arr, verbose=2)
# Printing accuracy
print(test_acc)

# Saving Model
model.save('/content/drive/MyDrive/TinkerHub BFH 2021/Models/Model9.h5')