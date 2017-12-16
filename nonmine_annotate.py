import numpy as np
import os
import cv2
import shutil

folder = input("File to images of non mines: ")
i = int(input("File number to start on: "))

text = '''<annotation>
    <folder>%s</folder>
    <filename>%s</filename>
    <path>/shared/SharedProjects/MiningSites/MiningSites/TensorFlow/models/research/mine-detection/%s/%s</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
    <object>
        <name>nonmine</name>
        <pose>Unspecified</pose>
        <truncated>1</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>0</xmin>
            <ymin>0</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
</annotation>'''
files = []
for filename in os.listdir(folder):
	if (filename.endswith(".jpg")): files.append(filename)
length = len(files)
mineLength = 1132

for i in range(mineLength):
    
    image = mineJPG[:-4]
    import sys
    try: fn = sys.argv[1]
    except: fn = '%s/%s'%(folder, mineJPG)
    print(__doc__)

    img = cv2.imread(fn, True)
    h, w = img.shape[:2]
    f = open("%s/%s.xml"%(folder, image),"w")
    f.write((text)%(folder, mineJPG, folder, mineJPG, w, h, w, h))
    f.close()

# for i in range(mineLength, length):
#     mineJPG = files[i]
#     shutil.move("%s/%s"%(folder, mineJPG), "NonlabeledImages/%s"%(mineJPG))
            