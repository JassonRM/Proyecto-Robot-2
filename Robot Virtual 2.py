#Control Robot
#Proyecto programado
#Jasson Rodriguez
#Marco Herrera

#Importar librerias
import pygame
import time
import os
import sys

#Funcion: cargarImagen
#Entrada: nombre
#Salida: imagen con ese nombre en el directorio Robot Sprite
#Restricciones: nombre es un string
def cargarImagen(nombre):
    ruta = os.path.join("Robot Sprite", nombre)
    imagen = pygame.image.load(ruta)
    return imagen

#Funcion: cargarSonido
#Entrada: nombre
#Salida: sonido con ese nombre en el directorio audio
#Restricciones: nombre es un string
def cargarSonido(nombre):
    ruta = os.path.join("Audio", nombre)
    sonido = pygame.mixer.Sound(ruta)
    return sonido

#Funcion: scale_img
#Entradas: imagen, ancho y altura
#Salida: imagen reescalada
#Restricciones: imagen de tipo pygame, ancho y altura son enteros
def scale_img(image,width,height):    
    image = pygame.transform.smoothscale(image,(width,height))
    return image

spriteSize = 200
Sprite = {"idle1":scale_img(cargarImagen("Idle (1).png"),spriteSize,spriteSize), "run1":scale_img(cargarImagen("Run (1).png"),spriteSize,spriteSize), "run2":scale_img(cargarImagen("Run (2).png"),spriteSize,spriteSize), "run3":scale_img(cargarImagen("Run (3).png"),spriteSize,spriteSize), "run4":scale_img(cargarImagen("Run (4).png"),spriteSize,spriteSize), "run5":scale_img(cargarImagen("Run (5).png"),spriteSize,spriteSize), "run6":scale_img(cargarImagen("Run (6).png"),spriteSize,spriteSize), "run7":scale_img(cargarImagen("Run (7).png"),spriteSize,spriteSize), "run8":scale_img(cargarImagen("Run (8).png"),spriteSize,spriteSize)}
global right
right = True

class Robot:
    def __init__(self):
        self.Nombre = "Nombre"
        self.sprite = Sprite["idle1"]
        self.posx = 300
        self.posy = 300
        self.x_velocidad = 0
        self.y_velocidad = 0
        self.aceleracion = 1
        self.imagen = 2
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
    def cambiar_sprite_derecha(self,nombre):
        self.sprite = Sprite[nombre]
        global right
        right = True
    def cambiar_sprite_izquierda(self,nombre):
        global right 
        right = False
        self.sprite = pygame.transform.flip(Sprite[nombre],True,False)

    def turnRight(self):
        if self.x_velocidad < 0:
            self.acelerar_x(2.25)
        else:
            self.acelerar_x(1)
        if self.imagen == 8:
            self.imagen = 1
        else:
            self.imagen += 1
        self.cambiar_sprite_derecha("run"+ str(self.imagen))

    def turnLeft(self):
        if self.x_velocidad < 0:
            self.acelerar_x(-2.25)
        else:
            self.acelerar_x(-1)
        if self.imagen == 8:
            self.imagen = 1
        else:
            self.imagen += 1
        self.cambiar_sprite_izquierda("run"+ str(self.imagen))
        
    def stop(self):
        if self.imagen == 8:
            self.imagen = 1                        
        if self.x_velocidad < -1:
            self.acelerar_x(1.5)
            self.cambiar_sprite_izquierda("run"+ str(self.imagen))
        elif self.x_velocidad > 1:
            self.acelerar_x(-1.5)
            self.cambiar_sprite_derecha("run"+ str(self.imagen))       
        else:
            if right:
                self.cambiar_sprite_derecha("idle1")
            else:
                self.cambiar_sprite_izquierda("idle1")
        self.imagen += 1



#Inicializar pygame
pygame.init()
clock = pygame.time.Clock()

#Inicializar el mixer de pygame
pygame.mixer.init()

#Crear ventana
windowWidth = 800
windowHeight = 600
ventana = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("Robot Virtual 2")

#Funcion: inGame
#Entrada: instancia del robot
#Salida: Entradas y salidas de las animaciones
#Restricciones: robot es una instancia
def inGame (robot):
    in_Game = True
    while in_Game :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_Game = False

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT:
                    robot.turnLeft()
                elif event.key == pygame.K_RIGHT:
                    robot.turnRight()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    robot.stop()
            pygame.event.clear()
            pygame.event.post(event)
                       
        ventana.fill((255,255,255))
        ventana.blit(robot.sprite,(robot.posx,robot.posy))
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    sys.exit()

paco = Robot()

inGame(paco)


