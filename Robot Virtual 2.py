#Control Robot
#Proyecto programado
#Jasson Rodriguez
#Marco Herrera

import pygame
import time
import os 

class Robot:

    def __init__(self):
        self.Nombre = "Nombre"
        self.sprite = pygame.image.load("Robot Sprite\Idle (1).png")
        self.posx = 200
        self.posy = 200

    def getNombre (self):
        return self.Nombre
    def get_posx(self):
        return self.posx
    def get_posy(self):
        return self.posy
    def mov_posx(self, pos):
        self.posx += pos
    def mov_posy(self, pos):
        self.posy += pos

def scale_img(image,width,height):
    image = pygame.transform.smoothscale(image,(width,height))
    return image

clock = pygame.time.Clock()
x_speed = 0
y_speed = 0

paco = Robot()
paco.sprite = scale_img(paco.sprite,200,200)

pygame.init()

ventana = pygame.display.set_mode((800,600))
pygame.display.set_caption(paco.getNombre())


inGame = True

while inGame :
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            inGame = False

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT:
                x_speed = -5
                y_speed = 0
            elif event.key == pygame.K_RIGHT:
                x_speed = 5
                y_speed = 0
            elif event.key == pygame.K_UP:
                y_speed = -5
                x_speed = 0
            elif event.key == pygame.K_DOWN:
                y_speed = 5
                x_speed = 0
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0
            
    paco.mov_posx(x_speed)
    paco.mov_posy(y_speed)
    ventana.fill((255,255,255))
    ventana.blit(paco.sprite,(paco.posx,paco.posy))
    pygame.display.update()
    clock.tick(30)


pygame.quit()
quit()
