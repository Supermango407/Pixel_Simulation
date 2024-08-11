from PIL import Image
import os, os.path

images = []
path = "Fractal_10"

# for image in os.listdir(path):
#     images.append(Image.open(os.path.join(path,image)))

with Image.open(os.path.join(path,'0_Fractal_10.png')) as image:
    image.show()
