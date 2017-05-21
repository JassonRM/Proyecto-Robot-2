#Control Robot
#Proyecto programado
#Jasson Rodriguez
#Marco Herrera

import pygame
import time
import os 

pygame.mixer.init()

def cargarImagen(nombre):
    ruta = os.path.join("Robot Sprite", nombre)
    imagen = pygame.image.load(ruta)
    return imagen

def cargarSonido(nombre):
    ruta = os.path.join("Audio", nombre)
    sonido = pygame.mixer.Sound(ruta)
    return sonido

class Robot:

    def __init__(self):
        self.Nombre = "Nombre"
        self.sprite = cargarImagen("Idle (1).png")
        self.posx = 300
        self.posy = 300
        self.x_velocidad = 0
        self.y_velocidad = 0
        self.aceleracion = 3
    def get_nombre (self):
        return self.Nombre
    
    def get_posx(self):
        return self.posx
    def get_posy(self):
        return self.posy
    
    def set_posx(self, pos):
        self.posx += pos
    def set_posy(self, pos):
        self.posy += pos


    def acelerar_x(self,direccion): #direccion 1 acelera der , direccion -1 acelera izq
        self.x_velocidad += direccion*self.aceleracion
        self.set_posx(self.x_velocidad) 
    def go_left(self):
        pass
    
def scale_img(image,width,height):
    image = pygame.transform.smoothscale(image,(width,height))
    return image


clock = pygame.time.Clock()

pygame.init()

ventana = pygame.display.set_mode((800,600))
pygame.display.set_caption("Nombre ventana")



def inGame (robot):
    in_Game = True
    while in_Game :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_Game = False

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT:
                    robot.acelerar_x(-1)
                elif event.key == pygame.K_RIGHT:
                    robot.acelerar_x(1)
                pygame.event.clear()
                pygame.event.post(event)
                
            elif event.type == pygame.KEYUP:
                if robot.x_velocidad == 0:
                    pygame.event.clear()
                elif event.key == pygame.K_LEFT:
                    robot.acelerar_x(1)
                elif  event.key == pygame.K_RIGHT:
                    robot.acelerar_x(-1)
                pygame.event.clear()
                pygame.event.post(event)
        
        ventana.fill((255,255,255))
        ventana.blit(robot.sprite,(robot.posx,robot.posy))
        pygame.display.update()
        clock.tick(30)


    pygame.quit()
    quit()

paco = Robot()
paco.sprite = scale_img(paco.sprite,200,200)

inGame(paco)
