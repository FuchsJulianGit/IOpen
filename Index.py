from PIL import Image
import keras.models as models
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageDraw
#import RPi.GPIO as io
import time

#import camera
#


#img = Image.open("bild3.jpg")
#img = img.resize((round(img.size[0] / 5), round(img.size[1] / 5)), resample=Image.BICUBIC)

#io.setmode(io.BOARD)  #pinnumber instead of gpio numbers
#io.setup(7,io.OUT)  #pin 7 als Ausgang


filename = "Untitled Folder\cardetector.h5"

model = models.load_model(filename)

ACCURACY_UP_TO = 0.98
ACCURACY_DOWN_TO = 0.70

sizes = [
         400,350,300,
         250,200,150,
         100, 50,
            ]
step_size = 50
cars = []


carDetectedAlready = True

while True:
    #Getting Img
    
    img = Image.open("Untitled Folder\Bild3.jpg")
    img = img.resize((round(img.size[0] * 5), round(img.size[1] * 5)), resample=Image.BICUBIC)
    ##img = camera.captureJPEG(300, 200)
    

    #print(img)
    #Reshaping
    for size in sizes:
        for x in range(0, img.size[0]- 100, step_size):
            for y in range(0, img.size[1] - size, step_size):
                part = img.crop((x, y, x + size, y + size))
                data =np.asarray(part.resize((32,32), resample=Image.BICUBIC))
                data = data.astype(np.float32)/ 255.

                pred = model.predict(data.reshape(-1, 32, 32, 3))
                
                if pred[0][0] > ACCURACY_UP_TO:
                    cars.append((x,y, size))
                    if carDetectedAlready: 
                        print("Car detected")
                        ##io.output(7,io.HIGH) #pin 7 ein
                        ##time.sleep(100)
                        ##io.output(7,io.LOW) #pin 7 wieder aus
                        ##io.cleanup()
                        carDetectedAlready = False
                    
                    else:
                        if pred[0][0] < ACCURACY_DOWN_TO:
                            carDetectedAlready = True
                    
                    
                    
                #plt.imshow(part)
                #plt.show()
                #else:
                   # print("No Car detected")
            
    out = img.copy()
    draw = ImageDraw.Draw(out)
    #img.show(out)

    cars_drawn = []