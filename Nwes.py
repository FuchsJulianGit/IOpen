from PIL import Image
import keras.models as models
# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import camera
from PIL import ImageDraw

def detectedCar():
    print("Works")
    #OpenGarageDoor
    #Pin ACtivation
def GetRecentPiture():
    
    #Picture = new Picture()
    return "Picture/Bild";
    
def CheckForMovementDetection():
    #getPicture
    print("Works")
    
def detectedMovement():
    
    print("Works")
    
###
###
###   KI CODE -> ACCESS MODEL, SHAPE OF IMG, SELECT IMAGE
###
###



def KiCode():

    
    
    Picture = GetRecentPiture() 
    #"Pictures/Bild2.jpg"


    img = Image.open(Picture) #Input Image Here
    img = img.resize((round(img.size[0] / 5), round(img.size[1] / 5)), resample=Image.BICUBIC)

    filename = "cardetector.h5"

    model = models.load_model(filename)

    sizes = [
             400,350,300,
             250,200,150,
             100, 50,
                ]
    step_size = 50
    cars = []
    for size in sizes:
        for x in range(0, img.size[0]- 100, step_size):
            for y in range(0, img.size[1] - size, step_size):
                part = img.crop((x, y, x + size, y + size))
                data =np.asarray(part.resize((32,32), resample=Image.BICUBIC))
                data = data.astype(np.float32)/ 255.

                pred = model.predict(data.reshape(-1, 32, 32, 3))
                if pred[0][0] > 0.98:
                    cars.append((x,y, size))
                #plt.imshow(part)
                #plt.show()

            
    out = img.copy()
    draw = ImageDraw.Draw(out)

    cars_drawn = []


    for car in cars:
        exists = False
        #points = [
         #   car,
          #  (car[0]+ size,car[1]+size)
        #]
        #print(points)
        #draw.rectangle(points)
        #print(car)
        for car_drawn in cars_drawn:
            if car[0] >= car_drawn[0] and car[0] <= car_drawn[0] + car_drawn[2]:
                if car[1]>= car_drawn[1] and car[1]<= car_drawn[1] + car_drawn[2]:
                    exists = True

    exists == False
    
    
    if exists == False:
        points = [
            (car[0], car[1]),
            (car[0], car[1]+car[2]),
            (car[0]+car[2], car[1]+ car[2]),
            (car[0] +car[2], car[1]),
            (car[0], car[1])
        ]
        draw.line(points, "yellow", 5)
        cars_drawn.append(car)
        print(car)
        print("True")
        detectedCar()
    else:
        print("False")



   out