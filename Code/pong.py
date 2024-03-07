from machine import Pin
from neopixel import NeoPixel
from time import sleep, ticks_ms

  
pin = Pin(4, Pin.OUT)   # D2=GPIO4
buttonLeftRight = Pin(5, Pin.IN, Pin.PULL_UP)#D1=GPIO5
buttonLeftLeft = Pin(14, Pin.IN, Pin.PULL_UP)#D5=GPIO14
buttonRightLeft = Pin(12, Pin.IN, Pin.PULL_UP)#D6=GPIO12
buttonRightRight = Pin(13, Pin.IN, Pin.PULL_UP)#D7=GPIO13 
np = NeoPixel(pin, 256)   # 256 pixeli
positionLeftPadle = []  #left padle position
positionRightPadle = [] #right padle position
width = 6
buttonLeft = 0
buttonRight = 0
speedPadle = 200
ballSpeedEncrease = 5
time1 = ticks_ms()
time2 = ticks_ms()
timeBall = ticks_ms() 
positionBall = 119
endBall = True
across = ""
ballMovemntPosition = True
upWall = [0,31,32,63,64,95,96,127,128,159,160,191,192,223,224,255]
downWall = [15,16,47,48,79,80,111,112,143,144,175,176,207,208,239,240]
scoreLeft = 0
scoreRight = 0
point = 0
play = True


for i in range(width/2):
        positionLeftPadle.append(7-i)
        positionLeftPadle.append(8+i)
        positionRightPadle.append(247-i)
        positionRightPadle.append(248+i)

#left padle
def leftPadle():
    for i in range(len(positionLeftPadle)):
        np[positionLeftPadle[i]]= (32, 0, 0)
    np.write()
    
#right padle
def rightPadle():
    for i in range(len(positionRightPadle)):
        np[positionRightPadle[i]]= (32, 0, 0)
    np.write()
        
        
def PadleMovePadle():
    global time1
    global time2
    global positionLeftPadle
    global positionRightPadle
    global buttonLeft
    if ticks_ms() > time1 + speedPadle and (buttonLeft != 0):
        endRight1 = True
        endLeft1 = True
        time1 = ticks_ms()
        #end
        if (positionLeftPadle[-1] == 15):
            endRight1 = False
        elif positionLeftPadle[-2] == 0:
            endLeft1 = False
        
        if buttonLeft == 1 and endLeft1:
            np[positionLeftPadle[-1]]= (0, 0, 0)
            for i in range(len(positionLeftPadle)):
                positionLeftPadle[i] -= 1
                np[positionLeftPadle[i]]= (32, 0, 0)
            np.write()
        elif buttonLeft == 2 and endRight1:
            np[positionLeftPadle[-2]]= (0, 0, 0)
            for i in range(len(positionLeftPadle)):
                positionLeftPadle[i] += 1
                np[positionLeftPadle[i]]= (32, 0, 0)
            np.write()
            
                
    if ticks_ms() > time2 + speedPadle and (buttonRight != 0):
        endRight2 = True
        endLeft2 = True
        time2 = ticks_ms()
        if positionRightPadle[-2] == 240:
            endLeft2 = False
        elif positionRightPadle[-1] == 255:
            endRight2 = False
            
            
            
        if buttonRight == 1 and endLeft2:
            np[positionRightPadle[-1]]= (0, 0, 0)
            for i in range(len(positionRightPadle)):
                positionRightPadle[i] -= 1
                np[positionRightPadle[i]]= (32, 0, 0)
            np.write()
        elif buttonRight == 2 and endRight2:
            np[positionRightPadle[-2]]= (0, 0, 0)
            for i in range(len(positionRightPadle)):
                positionRightPadle[i] += 1
                np[positionRightPadle[i]]= (32, 0, 0)
            np.write()
            
      
    
    
def resetPadles():
    for i in range(16):
        np[i] = (0,0,0)
        
    for i in range(16):
        np[i+240] = (0,0,0)
        
def ball():
    np[positionBall] = (32,0,0)
    np.write()
    
def ballMove():
    global timeBall
    global positionBall
    global endBall
    global ballMovemntPosition
    global ballMove2
    global ballMove1
    global across
    global speedBall
    if ticks_ms() > timeBall + speedBall:
        endBall = True
        timeBall = ticks_ms()
        
        if (positionBall == positionRightPadle[-2] -  (2*abs(downWall[15] - positionRightPadle[-2])+1) or positionBall == positionRightPadle[-4] - (2*abs(downWall[15] - positionRightPadle[-4])+1)) and across == "" :
            ballMove1,ballMove2 = ballMoveAcrossdown("left")
            across = "left down"
            speedBall -= ballSpeedEncrease
            
        elif (positionBall == positionLeftPadle[-1] +  (2*abs(downWall[0] - positionLeftPadle[-1])+1) or positionBall == positionLeftPadle[-3] + (2*abs(downWall[0] - positionLeftPadle[-3])+1)) and across == ""  :
            ballMove1,ballMove2 = ballMoveAcrossdown("right")
            across = "right down"
            speedBall -= ballSpeedEncrease
        elif (positionBall == positionLeftPadle[-2] +  (2*abs(downWall[0] - positionLeftPadle[-2])+1) or positionBall == positionLeftPadle[-4] + (2*abs(downWall[0] - positionLeftPadle[-4])+1)) and across == "":
            ballMove1,ballMove2 = ballMoveAcrossup("right")
            across = "right up"
            speedBall -= ballSpeedEncrease
        elif (positionBall == positionRightPadle[-1] -  (2*abs(downWall[15] - positionRightPadle[-1])+1) or positionBall == positionRightPadle[-3] - (2*abs(downWall[15] - positionRightPadle[-3])+1)) and across == "":
            ballMove1,ballMove2 = ballMoveAcrossup("left")
            across = "left up"
            speedBall -= ballSpeedEncrease
            
            
        elif (positionBall == positionRightPadle[-2] -  (2*abs(downWall[15] - positionRightPadle[-2])+2) or positionBall == positionRightPadle[-4] - (2*abs(downWall[15] - positionRightPadle[-4])+2)) and across == "right down" :
            ballMove1,ballMove2 = ballMoveAcrossdown("left")
            across = "left down"
            speedBall -= ballSpeedEncrease
            
        elif (positionBall == positionLeftPadle[-1] +  (2*abs(downWall[0] - positionLeftPadle[-1])+2) or positionBall == positionLeftPadle[-3] + (2*abs(downWall[0] - positionLeftPadle[-3])+2)) and across == "left down"  :
            ballMove1,ballMove2 = ballMoveAcrossdown("right")
            across = "right down"
            speedBall -= ballSpeedEncrease
        elif (positionBall == positionLeftPadle[-2] +  (2*abs(downWall[0] - positionLeftPadle[-2])+2) or positionBall == positionLeftPadle[-4] + (2*abs(downWall[0] - positionLeftPadle[-4])+2)) and across == "left down":
            ballMove1,ballMove2 = ballMoveAcrossup("right")
            across = "right up"
            speedBall -= ballSpeedEncrease
        elif (positionBall == positionRightPadle[-1] -  (2*abs(downWall[15] - positionRightPadle[-1])+2) or positionBall == positionRightPadle[-3] - (2*abs(downWall[15] - positionRightPadle[-3])+2)) and across == "right down":
            ballMove1,ballMove2 = ballMoveAcrossup("left")
            across = "left up"
            speedBall -= ballSpeedEncrease
        
        
        elif (positionBall == positionRightPadle[-2] -  (2*abs(downWall[15] - positionRightPadle[-2])) or positionBall == positionRightPadle[-4] - (2*abs(downWall[15] - positionRightPadle[-4]))) and across == "right up" :
            ballMove1,ballMove2 = ballMoveAcrossdown("left")
            across = "left down"
            speedBall -= ballSpeedEncrease
            
        elif (positionBall == positionLeftPadle[-1] +  (2*abs(downWall[0] - positionLeftPadle[-1])) or positionBall == positionLeftPadle[-3] + (2*abs(downWall[0] - positionLeftPadle[-3]))) and across == "left up"  :
            ballMove1,ballMove2 = ballMoveAcrossdown("right")
            across = "right down"
            speedBall -= ballSpeedEncrease
        elif (positionBall == positionLeftPadle[-2] +  (2*abs(downWall[0] - positionLeftPadle[-2])) or positionBall == positionLeftPadle[-4] + (2*abs(downWall[0] - positionLeftPadle[-4]))) and across == "left up":
            ballMove1,ballMove2 = ballMoveAcrossup("right")
            across = "right up"
            speedBall -= ballSpeedEncrease
        elif (positionBall == positionRightPadle[-1] -  (2*abs(downWall[15] - positionRightPadle[-1])) or positionBall == positionRightPadle[-3] - (2*abs(downWall[15] - positionRightPadle[-3]))) and across == "right up":
            ballMove1,ballMove2 = ballMoveAcrossup("left")
            across = "left up"
            speedBall -= ballSpeedEncrease
            
            
        else:
            for i in range(len(positionRightPadle)):
                if (positionBall == positionRightPadle[i] - (2*abs(downWall[15] - positionRightPadle[i])+1)) and across == "":
                    ballMove1,ballMove2 = ballMoveStright("left")
                    across = ""
                    speedBall -= ballSpeedEncrease
                elif (positionBall == positionLeftPadle[i] + (2*abs(downWall[0] - positionLeftPadle[i])+1)) and across == "":
                    ballMove1,ballMove2 = ballMoveStright("right")
                    across = ""
                    speedBall -= ballSpeedEncrease
                elif (positionBall == positionRightPadle[i] - (2*abs(downWall[15] - positionRightPadle[i])+2)) and across == "right down":                    
                    across = ""
                    np[positionBall]= (0, 0, 0)
                    positionBall = positionBall +1
                    np[positionBall]= (32, 0, 0)
                    np.write()
                    ballMove1,ballMove2 = ballMoveStright("left")
                    speedBall -= ballSpeedEncrease
                elif (positionBall == positionLeftPadle[i] + (2*abs(downWall[0] - positionLeftPadle[i])+2)) and across == "left down":                   
                    across = ""
                    np[positionBall]= (0, 0, 0)
                    positionBall = positionBall -1
                    np[positionBall]= (32, 0, 0)
                    np.write()
                    ballMove1,ballMove2 = ballMoveStright("right")
                    speedBall -= ballSpeedEncrease
                
                elif (positionBall == positionRightPadle[i] - (2*abs(downWall[15] - positionRightPadle[i]))) and across == "right up":                    
                    across = ""
                    np[positionBall]= (0, 0, 0)
                    positionBall = positionBall -1
                    np[positionBall]= (32, 0, 0)
                    np.write()
                    ballMove1,ballMove2 = ballMoveStright("left")
                    speedBall -= ballSpeedEncrease
                elif (positionBall == positionLeftPadle[i] + (2*abs(downWall[0] - positionLeftPadle[i]))) and across == "left up":                   
                    across = ""
                    np[positionBall]= (0, 0, 0)
                    positionBall = positionBall +1
                    np[positionBall]= (32, 0, 0)
                    np.write()
                    ballMove1,ballMove2 = ballMoveStright("right")
                    speedBall -= ballSpeedEncrease
        if (across == "left down"):
            ballMove1,ballMove2 = ballMoveAcrossdown("left")
                
        elif (across == "right down"):
            ballMove1,ballMove2 = ballMoveAcrossdown("right")
        elif (across == "right up"):
            ballMove1,ballMove2 = ballMoveAcrossup("right")
        elif (across == "left up"):
            ballMove1,ballMove2 = ballMoveAcrossup("left")
            
            
        if (positionBall in upWall and across == "right up"):
            ballMove1,ballMove2 = ballMoveAcrossdown("right")
            across = "right down"
        elif (positionBall in upWall and across == "left up"):
            ballMove1,ballMove2 = ballMoveAcrossdown("left")
            across = "left down"
        elif (positionBall in downWall and across == "left down"):
            ballMove1,ballMove2 = ballMoveAcrossup("left")
            across = "left up"
        elif (positionBall in downWall and across == "right down"):
            ballMove1,ballMove2 = ballMoveAcrossup("right")
            across = "right up"
            
        for i in range(16):
            if positionBall == i:
                endBall = False
                np[positionBall]= (0, 0, 0)
                np.write()
                return 1
            elif positionBall == i+240:
                endBall = False
                np[positionBall]= (0, 0, 0)
                np.write()
                return 2
                
               
            
        
        if endBall:
            np[positionBall]= (0, 0, 0)
            
            if ballMovemntPosition:
                positionBall = positionBall + ballMove1
                np[positionBall]= (32, 0, 0)
                ballMovemntPosition = False
            else:
                positionBall = positionBall + ballMove2
                np[positionBall]= (32, 0, 0)
                ballMovemntPosition = True
            np.write()
        return 0
def ballMoveStright(i):
    a = (positionBall *16) / 255
    ballMove1 = 2*abs((upWall[int(a)] - positionBall)) + 1
    ballMove2 = 2*abs((downWall[int(a)] - positionBall)) +1
    if i == "right":
        return ballMove1,ballMove2
    elif i == "left":
        return -ballMove2,-ballMove1
def ballMoveAcrossdown(i):
    a = (positionBall *16) / 255    
    if i == "left":
        ballMove1 = -2*abs((downWall[int(a)] - positionBall))
        ballMove2 = -(2*abs((upWall[int(a)] - positionBall))+2)
        return ballMove1,ballMove2
    elif i == "right":
        ballMove1 = 2*abs((upWall[int(a)] - positionBall)) + 2
        ballMove2 = 2*abs((downWall[int(a)] - positionBall))
        return ballMove1,ballMove2
        
        

def ballMoveAcrossup(i):
    a = (positionBall *16) / 255
    if i == "right":
        ballMove1 = 2*abs((upWall[int(a)] - positionBall))
        ballMove2 = (2*abs((downWall[int(a)] - positionBall))+2)
        return ballMove1,ballMove2
    elif i == "left":
        ballMove1 = -(2*abs((downWall[int(a)] - positionBall))+2)
        ballMove2 = -(2*abs((upWall[int(a)] - positionBall)))
        return ballMove1, ballMove2
        
        
        
    



ballMove1,ballMove2 = ballMoveStright("left")
# ballMove1 = -18
# ballMove2 = -12
if __name__ == '__main__':
    speedBall = 200
    leftPadle()
    rightPadle()
    ball()
    while play:
        point = ballMove()
        if(point == 1):
            scoreRight += 1
            play = False
        elif(point == 2):
            scoreLeft += 1
            play = False
        PadleMovePadle()
        
        if(buttonLeftRight.value()==0):
            buttonLeft = 1
            
        elif(buttonLeftLeft.value()==0):
            buttonLeft = 2
#         else:
#             buttonLeft = 0   
        if(buttonRightRight.value()==0):
            buttonRight = 1
            
        elif(buttonRightLeft.value()==0):
            buttonRight = 2
#         else:
#             buttonRight = 0
    print(scoreRight)
    print(scoreLeft)
            
            
        
        
            
        
        
    
    
