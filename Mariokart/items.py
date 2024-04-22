import pygame
from marioKartStart import getPositionObject

class banana():
    def __init__(self,x,y):
        self.image = pygame.image.load('Karts/banana.png')
        self.rect = self.image.get_rect()
        self.pos = 0
        self.posTop = 0
        self.posBottom = 0
        self.posLeft = 0
        self.posRight = 0
        self.sPos = 0
        self.offsetX = 0
        self.offSetY = 0
        self.offsetToCenter = 0
        getPositionObject(self)

    def throwBanana():
        pass

