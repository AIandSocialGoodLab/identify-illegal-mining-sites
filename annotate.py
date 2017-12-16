import numpy as np
import cv2
import os
import shutil

folder = input("File to images of mines: ")
i = int(input("File number to start on: "))


text = '''<annotation>
    <folder>%s</folder>
    <filename>%s</filename>
    <path>~/Projects/MiningSites/TensorFlow/models/research/mine-detection1/%s/%s</path>
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
        <name>mine</name>
        <pose>Unspecified</pose>
        <truncated>1</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
</annotation>'''
files = []
for filename in os.listdir(folder):
	if filename.endswith(".jpg"): files.append(filename)
length = len(files)



if __name__ == '__main__':
    mineJPG = files[i]
    mine = mineJPG[:-4]
    import sys
    try: fn = sys.argv[1]
    except: fn = '%s/%s'%(folder, mineJPG)
    print(__doc__)

    img = cv2.imread(fn, True)
    h, w = img.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    seed_pt = None
    fixed_range = True
    connectivity = 4
    flood = True
    boundingBox = False
    boxes = []
    
    
    doneDrawing = False

    bWidth = 10
    bHeight = 10
    global drawn
    drawn = False
    global upRight
    global downRight
    global downLeft
    global upLeft
    upRight = False
    downRight = False
    downLeft = False
    upLeft = False

 
   
       
    #image = image.open("mine1.jpg")
    #pixals = image.load()
    #(width, height) = image.size

    # def floodfill1:
    # 	if(seed_pt is not None):
    # 		for i in range(width):
    # 			for j in range(height):
    # 				if img[i][j] =
    #for i in range(width):
    #    for j in range(height):
    #    	(r, g, b) = (pixals[i,j])
    #    	if(seed_pt == None and g<50): seed_pt = i, j
    global rect1
    
    
   
    


    def floodfillUpdate(dummy=None):
        global flooded
        flooded = img.copy()   
        global mask
        mask[:] = 0
            #lo = cv2.getTrackbarPos('lo', 'floodfill')
            #hi = cv2.getTrackbarPos('hi', 'floodfill')
        flags = connectivity
        if fixed_range:
            flags |= cv2.FLOODFILL_FIXED_RANGE
        
        num1,im1,mask1,rect1 = cv2.floodFill(flooded, mask, seed_pt, (255, 255, 255), (200, 200, 50), (255, 255, 50), flags)
            

        
        global minX
        global minY
        global maxX
        global maxY
        minX = rect1[0]
        minY = rect1[1]
        maxX = minX
        maxY = minY
        foundX = False
        foundY = False
        startX, startY = seed_pt
        r = flooded[startY][startX][0]
        g = flooded[startY][startX][1]
        b = flooded[startY][startX][2]

        for j in range(minY, h):
            for i in range(minX, w):
                        # if(im1[j][i][0] == 255 and im1[j][i][1] == 255 and im1[j][i][2] == 255 and foundY == False):
                        #   minY = j
                        #   foundY = True
                if(im1[j][i][0] == 255 and im1[j][i][1] == 255 and im1[j][i][2] == 255 and 
                    (img[j][i][0] != 255 or img[j][i][1] != 255 or img[j][i][2] != 255)):
                    maxY = j


        for i in range(minX, w):
            for j in range(minY, h):
                    # if(im1[j][i][0] == 255 and im1[j][i][1] == 255 and im1[j][i][2] == 255 and foundX == False):
              #         minX = i
              #         foundX = True
                if(im1[j][i][0] == 255 and im1[j][i][1] == 255 and im1[j][i][2] == 255 and
                    (img[j][i][0] != 255 or img[j][i][1] != 255 or img[j][i][2] != 255)):
                    maxX = i



    def update(dummy=None):
        if seed_pt is None:
            img2 = img.copy()
            if(boundingBox):
                cv2.rectangle(img2, (minX, minY), (maxX, maxY), (0, 0, 0), 3)
                cv2.rectangle(img2, (max(0, minX-bWidth), max(0, minY-bHeight)), (minX, minY), (255, 255, 255), 1)
                cv2.rectangle(img2, (maxX, maxY), (min(w, maxX+bWidth), min(h, maxY+bHeight)), (255, 255, 255), 1)
                cv2.rectangle(img2, (max(0, minX-bWidth), maxY), (minX, min(h, maxY+bHeight)), (255, 255, 255), 1)
                cv2.rectangle(img2, (maxX, max(0, minY-bHeight)), (min(w, maxX+bWidth), minY), (255, 255, 255), 1)
            cv2.imshow('floodfill', img2)
            return

        

	     # def rect2(x, y, minX, minY, maxX, maxY):
	       #  if(flooded[y][x][0] < (r+20) and flooded[y][x][0] > (r-20) and flooded[y][x][1] < (g+20) 
	       #  	and flooded[y][x][1] > (g-20) and flooded[y][x][2] <  (b+20) and flooded[y][x][2] > (b-20)):
	       #  	#print('a')
	       #  	if(x < minX): minX = x
	       #  	if(x > maxX): maxX = x
	       #  	if(y < minY): minY = y
	       #  	if(y > maxY): maxY = y
	       #  	if(x<w): rect2(x+1, y, minX, minY, maxX, maxY)
	       #  	if(x>0): rect2(x-1, y, minX, minY, maxX, maxY)
	       #  	if(y<h): rect2(x, y+1, minX, minY, maxX, maxY)
	       #  	if(y>0): rect2(x, y-1, minX, minY, maxX, maxY)
	       #  else: return
	   
        
        #rect2(startX, startY, startX, startY, startX, startY)
        

        cv2.circle(flooded, seed_pt, 2, (0, 0, 255), -1)
        cv2.rectangle(flooded, (minX, minY), (maxX, maxY), (0, 0, 0), 3)
        cv2.imshow('floodfill', flooded)


    def onmouse(event, x, y, flags, param):
        global seed_pt
        if flags & cv2.EVENT_FLAG_LBUTTON and boundingBox == False:
            seed_pt = x, y
            floodfillUpdate()
            update()
        global drawn
        global upRight
        global downRight
        global downLeft
        global upLeft
        global minX
        global minY
        global maxX
        global maxY
        if boundingBox == True and drawn == False:
            if event == cv2.EVENT_LBUTTONDOWN:
                #print 'Start Mouse Position: '+str(x)+', '+str(y)
                
        
                minX = min(w, max(0, x))
                minY = min(h, max(0, y))
                # print count
                # print sbox

            if event == cv2.EVENT_LBUTTONUP:
                #print 'End Mouse Position: '+str(x)+', '+str(y)
                
                maxX = min(w, max(0, x))
                maxY = min(h, max(0, y))
                drawn  = True
                update()

        if boundingBox and drawn:
            if event == cv2.EVENT_LBUTTONDOWN:
                if(x>(minX-bWidth) and x < minX):
                    if(y>(minY-bHeight) and y<minY):
                        upLeft = True
                    elif(y > maxY and y < (maxY+bHeight)):
                        downLeft = True
                elif(x>maxX and x<(maxX + bWidth)):
                    if(y>(minY-bHeight) and y<minY):
                        upRight = True
                    elif(y>maxY and y<(maxY+bHeight)):
                        downRight = True
            if event == cv2.EVENT_LBUTTONUP:
                if(upLeft):
                    minX = min(w, max(0, x))
                    minY = min(h, max(0, y))
                    upLeft = False
                    update()
                elif(downLeft):
                    minX = min(w, max(0, x))
                    maxY = min(h, max(0, y))
                    downLeft = False
                    update()
                elif(upRight):
                    maxX = min(w, max(0, x))
                    minY = min(h, max(0, y))
                    upRight = False
                    update()
                elif(downRight):
                    maxX = min(w, max(0, x))
                    maxY = min(h, max(0, y))
                    downRight = False
                    update()





        # rectangle = False
        # if(flood == False):
        #     if event == cv2.EVENT_LBUTTONDOWN:
        #         rectangle = True
        #         global ix
        #         global iy
        #         ix,iy = x,y

        #     elif event == cv2.EVENT_MOUSEMOVE:
        #         if rectangle == True:
        #             cv2.rectangle(flooded,(ix,iy),(x,y),(0,255,0),2)
        #             rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))


        #     elif event == cv2.EVENT_LBUTTONUP:
        #         rectangle = False
        #         rect_over = True

        #         cv2.rectangle(flooded,(ix,iy),(x,y),(0,255,0),2)
        #         rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))


    update()
    cv2.setMouseCallback('floodfill', onmouse)

    # if boundingBox == True:
    #     fromCenter = False
    #     r = cv2.selectROI("floodfill", img, fromCenter)
    #     minX = int(r[0])
    #     minY = int(r[1])
    #     maxX = int(r[0]) + int(r[2])
    #     maxY = int(r[1]) + int(r[3])

    while True:
        ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break
        if ch == ord('f'):
            fixed_range = not fixed_range
            print('using %s range' % ('floating', 'fixed')[fixed_range])
            update()
        if ch == ord('c'):
            connectivity = 12-connectivity
            print('connectivity =', connectivity)
            update()
        if ch == ord('s'):
            seed_pt = None
            update()
        if ch == ord('r'):
            boundingBox = True
            drawn = False
            seed_pt = None
        if ch == ord('d'):
            oldFolder = folder
            oldMine = mineJPG
            if (i < length-1):
                i = i+1
                mineJPG = files[i]
                mine = mineJPG[:-4]
                import sys
                try: fn = sys.argv[1]
                except: fn = '%s/%s'%(folder, mineJPG)
                print(__doc__)

                img = cv2.imread(fn, True)
                h, w = img.shape[:2]
                mask = np.zeros((h+2, w+2), np.uint8)
                seed_pt = None
                fixed_range = True
                connectivity = 4
                print("image name: ", mine, ", index: ", i)
                shutil.move("%s/%s"%(oldFolder, oldMine), "NonlabeledImages")
                update()
            else:
                shutil.move("%s/%s"%(folder, mineJPG), "NonlabeledImages")
                break   
            
        if ch == ord('a'):
            f = open("%s/%s.xml"%(folder, mine),"w")
            f.write((text)%(folder, mineJPG, folder, mineJPG, w, h, min(minX, maxX), min(minY,maxY), max(minX, maxX), max(minY, maxY)))
            f.close()
            if (i < length-1):
                i = i+1
                mineJPG = files[i]
                mine = mineJPG[:-4]
                import sys
                try: fn = sys.argv[1]
                except: fn = '%s/%s'%(folder, mineJPG)
                print(__doc__)

                img = cv2.imread(fn, True)
                h, w = img.shape[:2]
                mask = np.zeros((h+2, w+2), np.uint8)
                seed_pt = None
                fixed_range = True
                connectivity = 4
                boxes = []
                boundingBox = False
                drawn  = False
                upRight = False
                downRight = False
                downLeft = False
                upLeft = False
                bWidth = 10
                bHeight = 10
                print("image name: ", mine, ", index: ", i)
                update()
            else:
                break
        if ch == ord('b'):
            
            if (i>0):
                i = i-1
                mineJPG = files[i]
                mine = mineJPG[:-4]
                import sys
                try: fn = sys.argv[1]
                except: fn = '%s/%s'%(folder, mineJPG)
                print(__doc__)

                img = cv2.imread(fn, True)
                h, w = img.shape[:2]
                mask = np.zeros((h+2, w+2), np.uint8)
                seed_pt = None
                fixed_range = True
                connectivity = 4
                boxes = []
                boundingBox = False
                drawn  = False
                upRight = False
                downRight = False
                downLeft = False
                upLeft = False
                bWidth = 10
                bHeight = 10
                print("image name: ", mine, ", index: ", i)
                update()

        
    	
        
        #if ch == 13
    cv2.destroyAllWindows() 
