#All code based on object_detection.ipynb which comes with TensorFlow Object Detection


from __future__ import division
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO

from PIL import Image
import csv
import xml.etree.ElementTree as ET
from object_detection.utils import label_map_util

from object_detection.utils import visualization_utils as vis_util


# What model to download.

MODEL_NAME = raw_input("Path to trained model folder (mine-detection/mine_graph in original code): ")

#Get path to set of images to test (in original training data, is mine-detection/SatelliteImages/testing)
PATH_TO_TEST_IMAGES_DIR = raw_input("Path to folder of testing images and their annotations: ")

#Path to folder where excel file, images, and precision and recall will be stored. For initial test was mine-detection/output
PATH_TO_OUTPUT_DIR = raw_input("Path to folder where output of testing will be stored: ")

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.

#Get folder which contains the training folder. For the original training set it it is mine-detection
label_path = raw_input("Path to folder containing the training folder (which must be named training and contain object-detection.pbtxt): ")
PATH_TO_LABELS = os.path.join(label_path, 'training', 'object-detection.pbtxt')

#Two classes, mine and non-mine
NUM_CLASSES = 2


#import graph
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

#import labels to get classes
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

#Function with transforms each testing image to a numpy array
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      	(im_height, im_width, 3)).astype(np.uint8)


#create list of images in testing folder
images = []
for filename in os.listdir(PATH_TO_TEST_IMAGES_DIR):
	if (filename.endswith(".jpg")): images.append(filename)

#Convert images that are in rgba to rgb, images in rgba cannot be used
length = len(images)

for image in images:
        png = Image.open("%s/%s"%(PATH_TO_TEST_IMAGES_DIR, image))
        png.load() # required for png.split()

        if(png.mode == 'RGBA'):
                background = Image.new("RGB", png.size, (255, 255, 255))
                background.paste(png, mask=png.split()[3]) # 3 is the alpha channel

                background.save("%s/%s"%(PATH_TO_TEST_IMAGES_DIR, image), 'JPEG', quality=80)


#create list of paths to test images
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, image) for image in images ]

#get list of label names and then create a list of paths to each label
labels = []
for filename in os.listdir(PATH_TO_TEST_IMAGES_DIR):
	if (filename.endswith(".jpg")): labels.append(filename[:-4] + ".xml")
TEST_ANNOTATION_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, label) for label in labels ]
TEST_IMAGES_NUM = len(TEST_IMAGE_PATHS)


mine_score = .5 #value score must be over to be considered mine

with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    mines = []
    true_positives = 0
    mines_identified = 0
    num_mines = 0
    for i in range(0, TEST_IMAGES_NUM):
      mine = 'false'
      image_path = TEST_IMAGE_PATHS[i]
      image = Image.open(image_path)
      # the array based representation of the image will be used later in order to prepare the
      # result image with boxes and labels on it.
      image_np = load_image_into_numpy_array(image)
      
      print(image_path)
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      image_np_expanded = np.expand_dims(image_np, axis=0)
      # Actual detection.
      (boxes, scores, classes, num) = sess.run(
          [detection_boxes, detection_scores, detection_classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
      scoresN = np.squeeze(scores)
      classesN = np.squeeze(classes)

      #if a bounding box has a score over the mine_score and the class for that bounding box is a mine (class = 1.0)< count the image as a mine
      for j in range(len(scoresN)):
            if(scoresN[j] > mine_score and classesN[j] == 1.0):
		mine = 'true'
      
      #load the annotation and parse to see if the image is actually a mine
      tree = ET.parse(TEST_ANNOTATION_PATHS[i])
      root = tree.getroot()
      label = root.find('./object/name')
      print(label)
      if(label.text == 'mine'): 
        
        num_mines = num_mines + 1 #number of actual mines in the testing set
    
      #if the program thinks its a mine
      if(mine == 'true'): 
        
        mines.append(images[i]) #add to list of mines
        if(label.text == 'mine'): true_positives = true_positives + 1 #true positives found by program
        mines_identified = mines_identified + 1 #number of mines identified by program
        
	#find the highest scored detection box containing a mine
        maxScore = 0
        maxScoreI = 0

        for x in range(len((np.squeeze(scores)))):
                if (scoresN[x]>maxScore and classesN[x] == 1.0):
                        maxScore = scoresN[x]
                        maxScoreI = i
        #append to list of max scores for mine
        max_scores.append(maxScore)
        #scale the ymin, xmin, ymax, and xmax given in boxes
        (im_width, im_height) = image.size
        ymin = int(boxes[0][maxScoreI][0]*im_height)
        xmin = int(boxes[0][maxScoreI][1]*im_width)
        ymax = int(boxes[0][maxScoreI][2]*im_height)
        xmax = int(boxes[0][maxScoreI][3]*im_width)

        #draw the box on the image and save it to the output directory in output_images 
        outputImage = cv2.imread(image_path)
        cv2.rectangle(outputImage, (xmin, ymin), (xmax, ymax), (0, 255,0),2)
        if not os.path.exists(os.path.join(PATH_TO_OUTPUT_DIR, 'output_images')):
                os.makedirs(os.path.join(PATH_TO_OUTPUT_DIR, 'output_images'))
        filename = os.path.join(PATH_TO_OUTPUT_DIR, 'output_images/%s.png'%((images[i])[:-4]))
        cv2.imwrite(filename, outputImage)     

        
#save the list of detected mines in a csv file of their name, coordinates, and maximum score in the output directory 

#iterate through list of mines to create lists of the mine names, latitudes, and longitudes
mine_names = []
mine_lat = []
mine_long = []
for m in mines:
        underscores = [i for i, ltr in enumerate(m) if ltr == '_']
        mine_number_start = underscores[0] + 1
        mine_number_end = underscores[1]
        mine_number = m[mine_number_start:mine_number_end]
        long_start = underscores[1] + 1
        long_end = underscores[2]
        long_start = underscores[2] + 1
        long_end = -4
        latitude = m[lat_start:lat_end]
        longitude = m[long_start:long_end]
        mine_names.append(mine_number)
        mine_lat.append(latitude)
        mine_long.append(longitude)

#create the csv file
with open(os.path.join(PATH_TO_OUTPUT_DIR, 'mines.csv'), 'wb') as myfile:
     myFields = ['mine_number', 'latitude', 'longitude', 'max_score']
     writer = csv.DictWriter(myfile, fieldnames=myFields)
     writer.writeheader()
     for i in range(len(mines)):
        writer.writerow({'mine_number' : mine_names[i], 'latitude' : mine_lat[i], 'longitude': mine_long[i], 'max_score': max_scores[i]})

#calculate precisoin and recall of model and save in file
precision = float(true_positives)/float(mines_identified)

recall = float(true_positives)/(float(num_mines))
file = open(os.path.join(PATH_TO_OUTPUT_DIR, 'precision_recall.txt'),'w') 
file.write('Precision: %f \n Recall: %f'%(precision, recall))
file.close()
