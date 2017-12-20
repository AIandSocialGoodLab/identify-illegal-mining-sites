##############################################
# CMU 05-899E Computing for Good
# Group: Detecting Minging Sites in DR Congo
# Wen Li
# wenl2@anderw.cmu.edu
# Dec. 2017
##############################################
import math
from openpyxl import Workbook
import Tkinter as tk
import os
import xlrd
import csv
# Window
window = tk.Tk()
window.title('detectMiningSites')
window.geometry('650x270')
#######################################Guidance####################
guidance = tk.Label(window,
             text='Step1: Creat coordinates csv\n '
             'Step2: Use QGIS to create new images\n'
             'Step3: Delete the images with low resolution\n',
             bg='gray',
             font=('Arial', 12),
             width=200, height=4)
guidance.pack()
#######################################Guidance####################

#######################################Step1#######################
# Layout
s1 = tk.Frame()
s1_label = tk.Label(s1, text='step1', font=('Arial', 12), width=17, height=1)
s1_label.pack()
s1_1 = tk.Frame(s1)
step1_x1_label = tk.Label(s1_1, text='    x of lower left point',
                          font=('Arial', 12), width=17, height=1)
step1_x1_label.pack(side="left")
step1_x1 = tk.Entry(s1_1, show=None)
step1_x1.pack(side="left")

s1_2 = tk.Frame(s1)
step1_y1_label = tk.Label(s1_2, text='    y of lower left point',
                          font=('Arial', 12), width=17, height=1)
step1_y1_label.pack(side="left")
step1_y1 = tk.Entry(s1_2, show=None)
step1_y1.pack(side="left")

s1_3 = tk.Frame(s1)
step1_x2_label = tk.Label(s1_3, text=' x of upper right point ',
                          font=('Arial', 12), width=17, height=1)
step1_x2_label.pack(side="left")
step1_x2 = tk.Entry(s1_3, show=None)
step1_x2.pack(side="left")

s1_4 = tk.Frame(s1)
step1_y2_label = tk.Label(s1_4, text=' y of upper right point ',
                          font=('Arial', 12), width=17, height=1)
step1_y2_label.pack(side="left")
step1_y2 = tk.Entry(s1_4, show=None)
step1_y2.pack(side="left")

s1_5 = tk.Frame(s1)
step1_y2_label = tk.Label(s1_5, text='path and name of csv',
                          font=('Arial', 12), width=17, height=1)
step1_y2_label.pack(side="left")
step1_path = tk.Entry(s1_5, show=None)
step1_path.pack(side="left")

s1_1.pack()
s1_2.pack()
s1_3.pack()
s1_4.pack()
s1_5.pack()

# Get coordinates
def regionCoors(x1 = 0.0, y1 = 0.0, x2 = 0.0, y2 = 0.0, coorsCsvPath = "D:/coor.csv"):
    # Step
    # According to the internal feature of QGIS
    l = abs(28.702384 - 28.694822)
    w = abs(0.323010 - 0.320145)
    nL = int(math.ceil((x2 - x1) / l))
    nW = int(math.ceil((y2 - y1) / w))

    csvName = coorsCsvPath
    f = open(csvName, 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['cId', 'X', 'Y'])
    no = 1
    for i in range(nL):
        x = 0. + x1 + l / 2.0 + i * l
        for j in range(nW):
            y = 0. + y1 + w/2.0 + j * w
            writer.writerow([no, x, y])
            no += 1
    f.close()

# Action
def step1():
    step1X1 = float(step1_x1.get())
    step1X2 = float(step1_x2.get())
    step1Y1 = float(step1_y1.get())
    step1Y2 = float(step1_y2.get())
    step1Path = step1_path.get()
    regionCoors(step1X1, step1Y1, step1X2, step1Y2, step1Path)

# The first button
step1_button = tk.Button(s1, text='Create coors.csv', width=15, height=2, command=step1)
step1_button.pack()
s1.pack(side="left")
#######################################Step1##############################

#######################################Step3##############################
#Layout
s3 = tk.Frame()
s3_label = tk.Label(s3, text='step3', font=('Arial', 12), width=25, height=1)
s3_label.pack(side="top")

s3_1 = tk.Frame(s3)
step3_path_label = tk.Label(s3_1, text='    file path of images    ',
                          font=('Arial', 12), width=25, height=1)
step3_path_label.pack(side="left")
step3_path = tk.Entry(s3_1, show=None)
step3_path.pack(side="left")
s3_1.pack(side="top")

s3_2 = tk.Frame(s3)
step3_sizeBar_label = tk.Label(s3_2, text='smallest size of images (KB)',
                          font=('Arial', 12), width=25, height=1)
step3_sizeBar_label.pack(side="left")
step3_sizeBar = tk.Entry(s3_2, show=None)
step3_sizeBar.pack(side="left")
s3_2.pack(side="top")

# Detect and delete low-resolution images
def detectLowRes(file_dir = "D:\\coor.xlsx", sizeBar = 220):
    # file_dir: Directory of files
    # sizeBar: KB
    # delete all the low resolution images and extract their names (Format: RelativeInfo_longitude_latitude.type.
    # Including information about coordinates into DeletedInfoLog.txt.
    for root, dirs, files in os.walk(file_dir):
        pass
    # files are filenames

    log = os.path.join(root, "DeletedInfoLog.txt")
    f = open(log, 'w')
    sum = 0
    for i in range(len(files)):
        str1 = files[i].split('.')
        typeStr = str1[-1]
        if typeStr == "jpg":
            # Get the size of images in KB
            size = os.path.getsize(os.path.join(root, files[i]))/1024
            if size < sizeBar:
                sum += 1
                f.write(files[i] + '\n')
                correspondingJgw = ".".join(str1[0:-1]) + ".jgw"
                if os.path.isfile(os.path.join(root, files[i])):
                    os.remove(os.path.join(root, files[i]))
                if os.path.isfile(os.path.join(root, correspondingJgw)):
                    os.remove(os.path.join(root, correspondingJgw))
    f.write("There are " + str(sum) + " low-resolution images." + '\n')
    f.close()

# Action
def step3():
    step3Path = step3_path.get()
    step3SizeBar = float(step3_sizeBar.get())
    detectLowRes(step3Path, step3SizeBar)

step3_button = tk.Button(s3, text='Delete useless images', width=20, height=2, command=step3)
step3_button.pack(side="bottom")
s3.pack(side="top")
#######################################Step3#################################
window.mainloop()