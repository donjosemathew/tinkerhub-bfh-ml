from tensorflow.keras import models
import cv2
import numpy as np
import tensorflow
model = models.load_model('F:\PythonLearning\Tinker Hub\BFH 2021\Models\Model9.h5')
img = np.zeros((1,200,200,3), dtype = 'uint8')
# img[0]= cv2.resize(cv2.imread('F:\PythonLearning\Tinker Hub\BFH 2021\Test for analysis\Images\Jackfruit.jpg'), (200,200))
img[0]= cv2.resize(cv2.imread('F:\PythonLearning\Tinker Hub\BFH 2021\Test for analysis\Images\Mango.jpg'), (200,200))
img/255
predictions = model.predict({'input':img})
class_names = ['Jackfruit', 'Mango']

print(class_names[(np.argmax(predictions))])