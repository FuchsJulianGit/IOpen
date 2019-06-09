from PIL import Image
import keras.models as models
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageDraw
import RPi.GPIO as io
import time

from picamera import PiCamera
from time import sleep

io.setmode(io.BOARD) #Pinnumber instead of gpio numbers
io.setup(31,io.OUT)  #Pin 31 als Ausgang
io.output(31,io.LOW) #Pin 31 wieder aus
io.cleanup()         #

camera = PiCamera()

filename = "/home/pi/cardetector.h5"

model = models.load_model(filename)

ACCURACY_UP_TO = 0.98
#sizes of the clip to go through the images
sizes = [
         400,350,300,
         250,200,150,
         100, 50,
            ]
step_size = 50

def DoThatShit():
    #Getting Img
    camera.start_preview()
    #wait to get a good image because of the light
    sleep(3)
    # get a picture and save it
    camera.capture('/home/pi/actualPic.jpg')
    camera.stop_preview()
    #get the image from the folder
    img = Image.open("/home/pi/actualPic.jpg")
    #make the image smaller to get the programm faster
    img = img.resize((round(img.size[0]/5), round(img.size[1]/5)), resample=Image.BICUBIC)
    #plt.imshow(img)
    #plt.show()
    #Reshaping
    for size in sizes:      #go trough all the sizes
        for x in range(0, img.size[0]- 100, step_size): #go trough the images
            for y in range(0, img.size[1] - size, step_size):
                part = img.crop((x, y, x + size, y + size)) #get a clipping from the image
                data =np.asarray(part.resize((32,32), resample=Image.BICUBIC))  #make it in a numpy array
                data = data.astype(np.float32)/ 255.#make the numbers little
                pred = model.predict(data.reshape(-1, 32, 32, 3)) #make a prediction
                
                if pred[0][0] > ACCURACY_UP_TO:     #if there is a probability over 98%
                    print("Car detected")
                    io.setmode(io.BOARD)  #pinnumber instead of gpio numbers
                    io.setup(31,io.OUT)  #pin 31 als Ausgang
                    io.output(31,io.HIGH) #pin 31 ein
                    time.sleep(30)
                    io.output(31,io.LOW) #pin 31 wieder aus
                    io.cleanup()
                    return      #there was a car  and the door was opend then return
while True:
    DoThatShit()
