from PIL import Image
import time
import progressbar
  
# Create an image as input: 
input_image = Image.new(mode="RGB", size=(800, 800), 
                        color="blue") 
  
# save the image as "input.png" 
#(not mandatory) 
input_image.save("input.png", format="png") 
  
# Extracting pixel map: 
pixel_map = input_image.load() 
  
# Extracting the width and height 
# of the image: 
width, height = input_image.size 
z = 100
 
widgets = [' [',
        progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
        '] ',
        progressbar.Bar('*'),' (',
        progressbar.ETA(), ') ',
        ]

bar = progressbar.ProgressBar(max_value=width, 
                              widgets=widgets).start()

for i in range(width): 
    bar.update(i)

    for j in range(height):
        
        # the following if part will create 
        # a square with color orange 
        if((i >= z and i <= width-z) and (j >= z and j <= height-z)): 
            
            # RGB value of orange. 
            pixel_map[i, j] = (255, 165, 0) 
  
        # the following else part will fill the 
        # rest part with color light salmon. 
        else: 
            
            # RGB value of light salmon. 
            pixel_map[i, j] = (255, 160, 122) 
  
# The following loop will create a cross 
# of color blue. 
for i in range(width): 
    
    # RGB value of Blue. 
    pixel_map[i, i] = (0, 0, 255) 
    pixel_map[i, width-i-1] = (0, 0, 255) 
  
# Saving the final output 
# as "output.png": 
input_image.show()
# input_image.save("output.png", format="png") 
  
# use input_image.show() to see the image on the 
# output screen. 