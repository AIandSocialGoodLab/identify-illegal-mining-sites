##############################################
# CMU 05-899E Computing for Good
# Group: Detecting Minging Sites in DR Congo
# Wen Li
# wenl2@anderw.cmu.edu
# Dec. 2017
##############################################
from PyQt4.QtCore import *
from qgis.core import *
from qgis.utils import *
from qgis.gui import QgsMapCanvas
from PyQt4.QtCore import QTimer
import csv
import os

canvas = iface.mapCanvas()
layer = iface.mapCanvas().layers()[0]
vLayer = iface.mapCanvas().layers()[1]
extent = vLayer.extent()

# File path of extracted images
file_dir = "D:\DetectMiningSites\Images"
# File path of coordinates csv
csv_file = "D:\DetectMiningSites\ori.csv"
sleepTime = 1500
var = 1  
gap = 1
# Number of coordinates  
end = 20
factor = 0.000003
# Arrange layers
def prepareMap(): 
  canvas.setExtent(extent)
  varStr = str(var)
  expr = QgsExpression( " \"cId\" = '{}' ".format(varStr) )
  it = layer.getFeatures( QgsFeatureRequest( expr ) )
  ids = [i.id() for i in it]
  print "ids:", ids
  layer.setSelectedFeatures(ids)
  iface.mapCanvas().zoomToSelected(layer)
  iface.mapCanvas().zoomByFactor(factor)
  # Wait a second and export the map
  QTimer.singleShot(sleepTime, exportMap) 

def exportMap():
  # We need this because we'll modify its value
  global var 
  global gap
  # refresh_layers(layer)
  varStr = str(var)
  path=file_dir + '\\images_'+varStr+'.jpg'
  qgis.utils.iface.mapCanvas().saveAsImage(path)
  print "Image_",varStr,"exported!"
  #####Iteration
  if var < end:
    # Wait a second and prepare next map
    QTimer.singleShot(sleepTime, prepareMap) 
  var = var + gap
  #####

def fileName():
  # Modify the names so that they can indicate coordinates of the images.
  for root, dirs, files in os.walk(file_dir):
    print len(files)
  # files are filenames
  # global nameList
  # nameList = range(len(files))
  csvfile = open(csv_file, 'rb')
  reader = csv.reader(csvfile)
  ex = 0
  longitude = []
  latitude = []
  for line in reader:
    table=line
    if ex != 0:
      longitude.append(table[1])
      latitude.append(table[2])
    ex += 1
  csvfile.close()
  for i in range(len(files)):
    str1 = files[i].split('_')
    str2 = str1[1].split('.')
    num = int(str2[0])
    newName = file_dir + "\\" + str1[0] + '_' + str(num) + '_' + str(longitude[num-1]) + '_' + str(latitude[num - 1]) + '.' + str2[1]
    files[i] = file_dir + "\\" + files[i]
    os.rename(files[i], newName)

prepareMap()
fileName()