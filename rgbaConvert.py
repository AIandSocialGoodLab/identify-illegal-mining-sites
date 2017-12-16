import os
from PIL import Image

folder = raw_input("Path to images folder:")
files = []
for filename in os.listdir(folder):
	if filename.endswith(".jpg"): files.append(filename)
length = len(files)

for image in files:
	png = Image.open("%s/%s"%(folder, image))
	png.load() # required for png.split()

	background = Image.new("RGB", png.size, (255, 255, 255))
	background.paste(png, mask=png.split()[3]) # 3 is the alpha channel

	background.save("%s/%s"%(folder, image), 'JPEG', quality=80)
