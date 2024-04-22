# ---------------------- MARIO KART 2D -------------------------
# Landon R
# Dylan
# Brayden
# Connor
# ICS4U
# let it cook

# Game setup
import pygame
import items
from sys import exit
import math



#joysticks
from pygame.locals import *
pygame.init()
pygame.joystick.init() #controllers are more fun (sutup is currently for ps5 controller so other controllers may not work as intended)
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
leftStickMotion = [0,0] #[x-axis,y-axis]
leftTriggerValue = 0
rightTriggerValue = 0
screenW = 800
screenH = 800
screen = pygame.display.set_mode((screenW,screenH)) #make screen
pygame.display.set_caption('Mariokart 2d') #create title
font = pygame.font.Font(None,50)
gameState = 'play'

#clock for frames
clock = pygame.time.Clock()
fps = 60

# initialize game variables
cc = 100 #just like in mariokart this will determine the speed of the game (top speed of karts)
pink = pygame.color.Color(255,0,255)
black = pygame.color.Color(0,0,0)
blue = pygame.color.Color(0,0,255)
red = pygame.color.Color(255,0,0)
maps = [] #list containing all map layers (wall layer, item layer, visible track layer, etc) so that all of their values can be changed at the same time
karts = []# list containing all karts so that they're values can be changed at the same time
objects = []# list of all objects in the game that aren't mario

def devTools(ToDo): 
    #quick devTools function that will be added to whenever long print stamtents or complicated methods of game testing are used. 
    #This way testing methods can be saved for use later
    testSurface = pygame.image.load('Karts/testSurf.png')
    if ToDo == 'printCollisions': #prints true/false for each part of the kart if it's colliding with a wall
        print(map1Walls.image.get_at([int(mario.pos[0]),int(mario.pos[1])]) == pink,map1Walls.image.get_at([int(mario.posTop[0]),int(mario.posTop[1])])==pink,map1Walls.image.get_at([int(mario.posBottom[0]),int(mario.posBottom[1])])==pink,map1Walls.image.get_at([int(mario.posLeft[0]),int(mario.posLeft[1])])==pink,map1Walls.image.get_at([int(mario.posRight[0]),int(mario.posRight[1])])==pink)
    elif ToDo == 'showPos':
        screen.blit(testSurface,(mario.pos[0],mario.pos[1])) #ya i need to fix this it wont work this way


def getPosition(self): #gets the position of mario ralative to the map #made by Landon
        self.pos =[(map1.rect.width/2+map1Walls.offsetX),(map1.rect.height/2+map1Walls.offsetY)]
        self.posTop = [(self.pos[0]),(self.pos[1]-self.image.get_height()/2)]
        self.posBottom = [(self.pos[0]),(self.pos[1]+self.image.get_height()/2)]
        self.posLeft = [(self.pos[0]-self.image.get_width()/2),int(self.pos[1])]
        self.posRight = [(self.pos[0]+self.image.get_width()/2),(self.pos[1])]

def getPositionObject(self): #gets the position of an object ralative to the map #made by Landon
        self.pos =[(map1.rect.width/2+self.offsetX-map1Walls.offsetX),(map1.rect.height/2+self.offsetY-map1Walls.offsetY)]
        self.posTop = [(self.pos[0]),(self.pos[1]-self.image.get_height()/2)]
        self.posBottom = [(self.pos[0]),(self.pos[1]+self.image.get_height()/2)]
        self.posLeft = [(self.pos[0]-self.image.get_width()/2),int(self.pos[1])]
        self.posRight = [(self.pos[0]+self.image.get_width()/2),(self.pos[1])]

def getScreenPos(self): #gets the position of an object relative to the center of the screen #MAde by Landon
    self.offsetToCenter = [mario.pos[0]-self.pos[0],mario.pos[1]-self.pos[1]] #mario position - the position of the object = the offset of the position to the center (mario is always in the center so his position on the map will always be [400,400] on the screen)
    self.sPos = [(screenW/2)-self.offsetToCenter[0],(screenH/2)-self.offsetToCenter[1]] # center of the screen - the offset = the scrren position

#========================KART CLASS=======================================
class Kart(pygame.sprite.Sprite):#made by Landon
    def __init__(self,x,y,image,type,startPosXShift,startPosYShift):
        #a shit ton of variables initializing all of the karts images, rectangles, stats, laptimes, position, and whatever else gets added
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x+startPosXShift,y+startPosYShift]
        self.type = type
        self.sPos = [400,400] #sPos stands for screen position

        self.weight = 0 #can be used later for adjusting car stats
        self.throttle = 0
        self.steer = 0
        self.maxSteer = -5
        self.brake = 0
        self.speedTotal = 0
        self.speedy = 0
        self.speedx = 0
        self.image2 = self.image #seccond image is for rotation (rotate image 2 and set image 1 equal to it to avoid distortion)
        self.angle = -90
        self.maxThrottle = 0.1 - (0.01*self.weight) #subtact acceleration based on the weight of the kart
        self.maxBrake = 0.1

        
        self.offsetX = 0.00 - startPosXShift #offset to the center of the map
        self.offsetY = 0.00 - startPosYShift
        self.offsetToCenter = 0 #offset to the center of the screen
        #initialize kart positions
        self.pos = [0+startPosXShift,0+startPosYShift] # initial position will be the center of the map plus the initial shift 
        self.posTop = [self.pos[0],self.pos[1]+self.image.get_height()/2] #all other positions use the width and height of the kart to get the positions of the sides
        self.posBottom = [self.pos[0],self.pos[1]-self.image.get_height()/2]
        self.posLeft = [self.pos[0]-self.image.get_width()/2,self.pos[1]]
        self.posRight = [self.pos[0]+self.image.get_width()/2,self.pos[1]]

        self.sector = 1 # each map is broken into 3 sectors to be used as checkpoints
        self.lap = 1 
        self.sectors = [False,False,False] #stores which sectors the kart has visited to know when a lap has been completed

        #surface that displays the lap
        self.lapSurf = font.render(str('Lap: ' + str(self.lap)),False,(255,255,255))
        self.lapRect = self.lapSurf.get_rect()

        #surface that displays the lap time
        self.lapTimer = pygame.time.Clock()
        self.lapTime = 0.000
        self.totalGameTime = pygame.time.get_ticks()
        self.lapTimes = [0]
        self.totalLapTimes = 0
        self.mills = 0
        self.sec = 0
        self.min = 0
        self.lapTimeSurf = font.render(str(self.lapTime),False,(255,255,255))
        self.lapTimeRect = self.lapTimeSurf.get_rect(center=(screenW/2,50))

        #surface for fastest lap time
        self.fl = '0:00.000'
        self.flMills = 0
        self.flSec = 0
        self.flMin = 0
        self.flSurf = font.render(str(self.fl),False,(255,255,255))
        self.flRect = self.lapTimeSurf.get_rect(center=(screenW/2 + 250,50))

    def wallCollision(self): #detect wall collisions and adjust the kart or map accordingly #made by Landon
        if pygame.surface.Surface.get_at(map1Walls.image, (int(self.posTop[0]),int(self.posTop[1]))) == pink and self.speedy>0:
            for surface in range(0,len(objects)): #use a loop to change the position of all map layers
                objects[surface].rect.centery-=cc/10 #moves the map based of the max speed of the player so that they "bounce" off of walls
                objects[surface].offsetY+=cc/10 #adjust the offset of the map to account for the change in position
        if map1Walls.image.get_at((int(self.posBottom[0]),int(self.posBottom[1]))) == pink and self.speedy<0:
            for surface in range(0,len(objects)):
                objects[surface].rect.centery+=cc/10
                objects[surface].offsetY-=cc/10
        if map1Walls.image.get_at((int(self.posLeft[0]),int(self.posLeft[1]))) == pink and self.speedx>0:
            for surface in range(0,len(objects)):
                objects[surface].rect.centerx-=cc/10
                objects[surface].offsetX+=cc/10
        if map1Walls.image.get_at((int(self.posRight[0]),int(self.posRight[1]))) == pink and self.speedx<0:
            for surface in range(0,len(objects)):
                objects[surface].rect.centerx+=cc/10
                objects[surface].offsetX-=cc/10
    
    def boxCollision(self):
        pass
    
    def checkpoints(self): #made by Landon
        if map1Checkpoints.image.get_at((int(self.pos[0]),int(self.pos[1]))) == blue: #checks if the player reaches checkpoint 1
            self.sector = 2 #change the sector the player is in (sectors are 1,2,3)
            self.sectors[0] = True
        if map1Checkpoints.image.get_at((int(self.pos[0]),int(self.pos[1]))) == red and self.sectors[0]:#check if player is at checkpoint 2
            self.sector = 3
            self.sectors[1] = True
        if map1Checkpoints.image.get_at((int(self.pos[0]),int(self.pos[1]))) == pink and self.sectors[0] and self.sectors[1]: #check if player is at checkpoint three the finish line and has passed all other checkpoints
            self.sector = 1
            self.sectors[2] = True
        if self.sectors[0] and self.sectors[1] and self.sectors[2]:
            if self.lap == 1: #just deletes the inital zero I had to store in the laptimes list after the first lap
                self.lapTimes.pop()
            self.lap+=1 #increase the lap
            self.lapSurf = font.render(str('Lap: ' + str(self.lap)),False,(255,255,255))
            self.lapRect = self.lapSurf.get_rect()
            self.lapTimes.append(self.lapTime) #add this laptime to the current list of laptimes
            for i in range(0,len(self.sectors)): # set all sectors to false
                self.sectors[i] = False

    def getLapTime(self): #gets the ongoing time of the current lap #made by Landon
        self.totalGameTime = pygame.time.get_ticks()
        self.totalLapTimes = 0
        for i in range(0,len(self.lapTimes)): #uses a loop to calculate the total millisecconds of all previous laps
            self.totalLapTimes += self.lapTimes[i] 
        self.lapTime = self.totalGameTime - self.totalLapTimes #current laptame = total millisecconds - milliseconds of all previous laps
        self.mills = self.lapTime % 1000 #calculations that converts from millisecconds to minutes, secconds, and millisecconds
        self.sec = self.lapTime // 1000
        self.min = self.sec // 60
        self.sec = self.sec % 60
        #updates the laptime surface
        self.lapTimeSurf = font.render(str(str(self.min) + ':' + str(self.sec) + '.' + str(self.mills)),False,(255,255,255))
        self.lapTimeRect = self.lapTimeSurf.get_rect(center=(screenW/2,50))
    
    def fastestLap(self): #made by Landon
        self.lapTimes.sort() #sort laps in accending order according to their time
        self.fl = self.lapTimes[0] #fastest lap is the first element of the list because it will be the one will the least millisecconds
        self.flMills = self.fl % 1000
        self.flSec = self.fl // 1000
        self.flMin = self.flSec // 60
        self.sec = self.sec % 60
        #update the fastest lap surface
        self.flSurf = font.render(str('FL:'+str(self.flMin)+':'+str(self.flSec)+'.'+str(self.flMills)),False,(255,255,255))
        self.flRect = self.lapTimeSurf.get_rect(center=(screenW/2 + 225,50))
    
    def getInputs(self): #get player inputs and update mario's kart values #made by Landon
        keys = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos()
        mouseX = mousePos[0] #was using mouse to steer, now using controller, will add back in future hopefully along with a settings menu
        #mario.steer = -1*(mouseX - screenW/2)/100 #re add when ready for mouse keep disabled for easy testing
        if keys[pygame.K_w]: #option to use keys or controller for inputs (keys will be constant controller will be variable)
            self.throttle = self.maxThrottle
        else:
            self.throttle = rightTriggerValue * self.maxThrottle
        if keys[pygame.K_s] and self.speedTotal>0:
            self.brake = self.maxBrake
        else: 
            self.brake = leftTriggerValue * self.maxBrake
        if keys[pygame.K_a]:
            self.steer = -self.maxSteer
        elif keys[pygame.K_d]:
            self.steer = self.maxSteer
        else:
            self.steer = leftStickMotion[0] * self.maxSteer #uses the x-axis value of the controller times the maxSteer value to steer
    
    def turnKart(self): #turns kart #made by Landon
        self.angle+=self.steer #updates the angle of the image according to how much the car is steering
        if abs(self.angle) > 360: #keeps angle within 360, not required But keeps it simple
            self.angle = 0
        #transforms the duplicate image by the angle and sets the first image equal to it
        #using this method of transforming a duplicate image avoids compounding distortion of the rotation method
        #the seccond image is never permenently changed it stays as the orriginal image
        self.image = pygame.transform.rotate(self.image2,self.angle)
        #updates the the rectangle to ensure a smooth rotation without a more bouncy apearence 
        self.rect.topleft = ((screenW/2)-self.image.get_width()/2,((screenH/2)-self.image.get_height()/2))
        
    def applyInputs(self):#again will probably need to make work for all karts in future but works for now #made by Landon
        self.speedTotal += self.throttle - self.brake #get the total speed
        if self.speedTotal>cc//10: #keeps speed within the limit set by the cc's and stops the kart at speed 0
            self.speedTotal = cc//10
        if self.speedTotal < 0:
            self.speedTotal = 0
        self.maxSteer = -5 + (0.35 * self.speedTotal) #updates the maximum steering so that the kart steers slower as it's going faster
        self.speedx = (math.sin(math.radians(self.angle))) * self.speedTotal #break total speed into its vector components for x and y direction speed
        self.speedy = (math.cos(math.radians(self.angle))) * self.speedTotal
        for i in range(0,len(objects)): #uses a loop to adjust the position of all objects including maps based on marios movement
            objects[i].rect.centerx += round(self.speedx) #update object position and offsets based on self
            objects[i].offsetX -= round(self.speedx)
            objects[i].rect.centery += round(self.speedy)
            objects[i].offsetY -= round(self.speedy)


    def update(self): #updates the kart using all available methods #made by Landon
        if self.type == 'player': #uses the type of the kart to separate methods as Ai functions and player functions
            getPosition(self) #gets marios position
        if self.type == 'Ai':
            getPositionObject(self) #gets position of object relative to the center of the map [0,0]
            getScreenPos(self) #gets position relative to the center of the screen [400,400]
        self.wallCollision()
        self.checkpoints()
        self.getLapTime()
        self.fastestLap()
        if self.type == 'player':
            self.getInputs()
            self.applyInputs()
        self.turnKart()
        if self.type == 'Ai': #have to do this at the end so it does not get overrided by other functions
            self.rect.center = self.sPos


        
#--------------------------- MAP CLASS ------------------------#
class map(pygame.sprite.Sprite): #made by Landon
    def __init__(self,x,y,image,startPosXShift,startPosYShift): #can probably fix so that x and y shift are not needed but dont feel like it right now
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.center = [x+startPosXShift,y+startPosYShift]
        self.offsetX = 0.00000000000000 - startPosXShift #after the long amount of time trying to get positions and offset to work im sure i could get rid of this long decimal but im not touching it
        self.offsetY = 0.00000000000000 - startPosYShift

    def update(self): 
        pass

startMenu = map(screenW/2,screenH/2,'Karts/startmenu.png',0,0)
kartGroup = pygame.sprite.Group() #group of all karts
mario = Kart(screenW/2,screenH/2,'Karts/mario.png','player',0,0)
bowser = Kart(screenW/2,screenH/2,'Karts/bowser.png','Ai',250,-3050)
kartGroup.add(mario)
kartGroup.add(bowser)
karts.append(bowser)
objects.append(bowser)
mapgroup = pygame.sprite.Group()#group of all maps
map1 = map(screenW/2,screenH/2,'Karts/track1.png',0,-1500)
#mapgroup.add(map1) #this is only here to quickly change the order of the maps to see the background instead of the visable layer
maps.append(map1)
objects.append(map1)
map1Walls = map(screenW/2,screenH/2,'Karts/track1Walls2550255.png',0,-1500)
mapgroup.add(map1Walls)
maps.append(map1Walls)
objects.append(map1Walls)
map1Checkpoints = map(screenW/2,screenH/2,'Karts/track1Checkpoints.png',0,-1500)
mapgroup.add(map1Checkpoints)
maps.append(map1Checkpoints)
objects.append(map1Checkpoints)
mapgroup.add(map1)

#game loop
while True:
    
    #event handler
    for event in pygame.event.get():
        if gameState == 'play':
            if event.type == JOYBUTTONDOWN:
                print(event)
            if event.type == JOYBUTTONUP:
                print(event)
            if event.type == JOYAXISMOTION:
                if event.axis == 0:
                    if event.value > 0.02 or event.value < -0.02:
                        leftStickMotion[0] = event.value
                if event.axis == 4:
                    if event.value >0.005:
                        leftTriggerValue = event.value
                if event.axis == 5:
                    if event.value > 0.005:
                        rightTriggerValue = event.value
            if event.type == JOYHATMOTION:
                print(event)
        
        if gameState == 'startMenu':
            pass

        if event.type == pygame.QUIT: #quits
            pygame.quit()
            exit()
    
    #update screen
    if gameState == 'play':
        mapgroup.draw(screen)
        mapgroup.update()
        kartGroup.update()
        kartGroup.draw(screen)
        screen.blit(mario.lapSurf,mario.lapRect)
        screen.blit(mario.lapTimeSurf,mario.lapTimeRect)
        screen.blit(mario.flSurf,mario.flRect)
        pygame.display.update()

    if gameState == 'startMenu':
        screen.blit(startMenu)
        pygame.draw.rect(startMenu, 'Red', pygame.Rect(30, 30, 60, 60))


    clock.tick(fps)