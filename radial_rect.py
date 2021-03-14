import numpy as np
import math
import matplotlib.pyplot as plt
import copy
import random

def distancelength(x1,y1,x2,y2):
    return np.linalg.norm(np.array([x1 - x2, y1 - y2]))

def NNplotupdate():
    ax.clear()
    ax.plot(finalX,finalY)
    fig.canvas.draw()
    plt.pause(0.0000001)

def optplotupdate():
    ax.clear()
    ax.plot(twooptX,twooptY)
    ax.plot(finalX,finalY)
    fig.canvas.draw()
    plt.pause(0.0000001)

def pathlength(xpoints,ypoints):
    optdistance = 0
    for i in range(len(xpoints)-1):
        #optdistance += distancelength(xpoints[i+1],ypoints[i+1],xpoints[i],ypoints[i])
        if (np.abs(xpoints[i+1]-xpoints[i]) > np.abs(ypoints[i+1]-ypoints[i])):
            optdistance += np.abs(xpoints[i+1]-xpoints[i])
        else:
            optdistance += np.abs(ypoints[i+1]-ypoints[i])
    return optdistance

def three_closest(myXarray, myYarray, tempX, tempY):
    first = 10
    second = 11
    third = 13
    first_index = 1
    second_index = 2
    third_index = 3
    for i in range(len(myXarray)):
        if distancelength(tempX,tempY,myXarray[i],myYarray[i]) <= first:
            third_index = second_index
            second_index = first_index
            first_index = i
            third = second
            second = first
            first = distancelength(tempX,tempY,myXarray[i],myYarray[i])
        elif distancelength(tempX,tempY,myXarray[i],myYarray[i]) <= second:
            third_index = second_index
            second_index = i
            third = second
            second = distancelength(tempX,tempY,myXarray[i],myYarray[i])
        elif distancelength(tempX,tempY,myXarray[i],myYarray[i]) <= third:
            third_index = i
            third = distancelength(tempX,tempY,myXarray[i],myYarray[i])
    return first_index, second_index, third_index

class Points:
    """ Points class represents x,y coords """
    def __init__(self, N, x_max, anglestep,rayoffset,M):
        self.N = N
        self.x_max = x_max
        self.anglestep = anglestep
        self.rayoffset = rayoffset
        self.M = M
    def Xpoints(self):
        ray = np.logspace(0, math.log(self.x_max+self.rayoffset,10), self.N, endpoint=True)
        ray = ray - self.rayoffset
        lines = np.linspace(-(self.x_max)/10, (self.x_max)/10, M) 
        allthexpoints = []
        circle = range(0,360,anglestep)
        for theta in circle:
            x45 = math.cos(theta*np.pi/180)*ray
            for i in range(len(x45)):
                allthexpoints.append(round(x45[i]/10,4)) 
        for i in range(len(lines)):     
            for j in range(len(lines)): 
                allthexpoints.append(round(lines[i],4))
        return allthexpoints
    def Ypoints(self):
        ray = np.logspace(0, math.log(self.x_max+self.rayoffset,10), self.N, endpoint=True)
        ray = ray - self.rayoffset
        lines = np.linspace(-(self.x_max)/10, (self.x_max)/10, M) 
        alltheypoints = []
        circle = range(0,360,anglestep)
        for theta in circle:
            y45 = math.sin(theta*np.pi/180)*ray
            for i in range(len(y45)):
                alltheypoints.append(round(y45[i]/10,4)) 
        for i in range(len(lines)):     
            for j in range(len(lines)): 
                alltheypoints.append(round(lines[j],4))
        return alltheypoints

fig = plt.figure()
ax = fig.add_subplot(111)
plt.ion()
fig.show()
fig.canvas.draw()

# Parameters
N = 21              # controls the number of points in each ray
x_max = 3           # controls the length of each ray, each ray goes from 1 to x_max
anglestep = 4       # controls the angle between each ray in degrees
rayoffset = 0.9     # log rays start at 1. to pull each ray closer to the origin, an offset from 0 to 1 will shift them in
M = 31              # controls the resolution of the square spread 
NNscaling = 0.9835   


############# Point Spread #############
radial_rect = Points(N,x_max,anglestep,rayoffset,M)
allthexpoints = radial_rect.Xpoints()
alltheypoints = radial_rect.Ypoints()

############# Nearest Neighbor #############
# Initializing
finalX = []
finalY = []
alltheXXpoints = copy.copy(allthexpoints)
alltheYYpoints = copy.copy(alltheypoints)
tempXval = 0
tempYval = 0
for i in range(len(allthexpoints)): #to cover all the points in the array
    distance = 10 #arbitrary long distance
    for j in range(len(alltheXXpoints)): #to cover all the unvisited points
        if distancelength(tempXval*NNscaling,tempYval*NNscaling,alltheXXpoints[j],alltheYYpoints[j]) < distance:
            distance = distancelength(tempXval*NNscaling,tempYval*NNscaling,alltheXXpoints[j],alltheYYpoints[j])
            indexsaver = j
    tempXval = alltheXXpoints[indexsaver]
    tempYval = alltheYYpoints[indexsaver]
    finalX.append(alltheXXpoints[indexsaver])
    finalY.append(alltheYYpoints[indexsaver])
    alltheXXpoints.pop(indexsaver)
    alltheYYpoints.pop(indexsaver)
    NNplotupdate()
print(pathlength(finalX,finalY))

############# 2-opt #############
twooptX = copy.copy(finalX)
twooptY = copy.copy(finalY)
oldX = 0
oldY = 0
shrinkingdistance = pathlength(twooptX,twooptY)
optswaplength = 3
for i in range(len(twooptX)):
    for rand in reversed(range(0,5)):
        #rand = random.randint(1,3)
        oldX = twooptX[(i+(rand))%len(twooptX)]
        oldY = twooptY[(i+(rand))%len(twooptX)]
        twooptX[(i+(rand))%len(twooptX)] = twooptX[i]
        twooptY[(i+(rand))%len(twooptX)] = twooptY[i]
        twooptX[i] = oldX
        twooptY[i] = oldY
        optplotupdate()
        optdistance = pathlength(twooptX,twooptY)
        if optdistance < shrinkingdistance:     #keep the swap
            shrinkingdistance = optdistance
            optplotupdate()
            print(pathlength(twooptX,twooptY))
        else:                                   #undo the swap
            oldX = twooptX[(i+(rand))%len(twooptX)]
            oldY = twooptY[(i+(rand))%len(twooptX)]
            twooptX[(i+(rand))%len(twooptX)] = twooptX[i]
            twooptY[(i+(rand))%len(twooptX)] = twooptY[i]
            twooptX[i] = oldX
            twooptY[i] = oldY
            #optdistance = 0
print(pathlength(twooptX,twooptY))
print( (pathlength(finalX,finalY)/pathlength(twooptX,twooptY)) - 1 )
