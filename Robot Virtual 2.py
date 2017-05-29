#Control Robot
#Proyecto programado
#Jasson Rodriguez
#Marco Herrera

#Importar librerias
import pygame
import time
import os
import sys
import serial
from threading import Thread

puerto = 'COM3'
arduino = serial.Serial(puerto, 9600, timeout=None)
arduino.flushInput()


def serialCom():
        try:
            entrada = str(arduino.readline())
            keys = eval(entrada[(entrada.find("{")):entrada.find("}")+1])
            print (keys)
            return keys
        except:
            print("Data could not be read")

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
    sonido = pygame.mixer.music.load(ruta)
    return sonido

#Funcion: scale_img
#Entradas: imagen, ancho y altura
#Salida: imagen reescalada
#Restricciones: imagen de tipo pygame, ancho y altura son enteros
def scale_img(image,width,height):    
    image = pygame.transform.smoothscale(image,(width,height))
    return image

spriteSize = 200
Sprite = {"idle1":scale_img(cargarImagen("Idle (1).png"),spriteSize,spriteSize), "run1":scale_img(cargarImagen("Run (1).png"),spriteSize,spriteSize), "run2":scale_img(cargarImagen("Run (2).png"),spriteSize,spriteSize), "run3":scale_img(cargarImagen("Run (3).png"),spriteSize,spriteSize), "run4":scale_img(cargarImagen("Run (4).png"),spriteSize,spriteSize), "run5":scale_img(cargarImagen("Run (5).png"),spriteSize,spriteSize), "run6":scale_img(cargarImagen("Run (6).png"),spriteSize,spriteSize), "run7":scale_img(cargarImagen("Run (7).png"),spriteSize,spriteSize), "run8":scale_img(cargarImagen("Run (8).png"),spriteSize,spriteSize), "jump1":scale_img(cargarImagen("Jump (1).png"),spriteSize,spriteSize), "jump2":scale_img(cargarImagen("Jump (2).png"),spriteSize,spriteSize), "jump3":scale_img(cargarImagen("Jump (3).png"),spriteSize,spriteSize), "jump4":scale_img(cargarImagen("Jump (4).png"),spriteSize,spriteSize), "jump5":scale_img(cargarImagen("Jump (5).png"),spriteSize,spriteSize), "jump6":scale_img(cargarImagen("Jump (6).png"),spriteSize,spriteSize), "jump7":scale_img(cargarImagen("Jump (7).png"),spriteSize,spriteSize), "jump8":scale_img(cargarImagen("Jump (8).png"),spriteSize,spriteSize), "jump9":scale_img(cargarImagen("Jump (9).png"),spriteSize,spriteSize), "jump10":scale_img(cargarImagen("Jump (10).png"),spriteSize,spriteSize)}
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
        self.tiempo = 0
        
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

    def cambiar_sprite_derecha(self,nombre):
        self.sprite = Sprite[nombre]
        global right
        right = True
        
    def cambiar_sprite_izquierda(self,nombre):
        global right 
        right = False
        self.sprite = pygame.transform.flip(Sprite[nombre],True,False)

    def run(self,velocidad):
        self.set_posx((velocidad - 502) // 40)
        if self.tiempo == 0:
            print (self.imagen)
            if self.imagen >= 8:
                self.imagen = 1
            else:
                self.imagen += abs((velocidad - 511.5)/ 511.5)
            if velocidad > 550:
                self.cambiar_sprite_derecha("run"+ str(int((self.imagen))))
            else:
                self.cambiar_sprite_izquierda("run"+ str(int(self.imagen)))
    

    def jump(self):
        v0 = 1000
        aceleracion = -4000
        posy = 300
        delta_pos = v0 * self.tiempo + (aceleracion * self.tiempo ** 2) / 2
        self.tiempo += 1 / 30
        self.posy = posy - delta_pos
        if delta_pos < 0:
            self.posy = 300
            self.tiempo = 0
        self.imagen = int(self.tiempo // (0.5666666666666667 / 10))
        if self.imagen == 0:
            self.imagen = 1
            if right:
                self.cambiar_sprite_derecha("idle1")
            else:
                self.cambiar_sprite_izquierda("idle1")
        else:
            if right:
                self.cambiar_sprite_derecha("jump"+ str(self.imagen))
            else:
                self.cambiar_sprite_izquierda("jump"+ str(self.imagen))
            


#Inicializar pygame
pygame.init()
clock = pygame.time.Clock()

#Inicializar el mixer de pygame
pygame.mixer.init()

#Crear ventana
windowWidth = 1000
windowHeight = 600
ventana = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("Robot Virtual 2")

#Variable del juego
in_Game = True

#Funcion: inGame
#Entrada: instancia del robot
#Salida: Entradas y salidas de las animaciones
#Restricciones: robot es una instancia
def inGame (robot):
    global in_Game
    control = Thread(target=controller, args=(robot,))
    control.start()
    while in_Game:                       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_Game = False
                        
        ventana.fill((255,255,255))
        ventana.blit(robot.sprite,(robot.posx,robot.posy))
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    sys.exit()

cancion = "High.wav"
cargarSonido(cancion)

def controller(robot):
    music_on = False
    while in_Game:
        keys = serialCom()
        if keys != None :
            if keys["X"] > 561 and robot.get_posx() < windowWidth - 125:
                robot.run(keys["X"])
            elif keys["X"] < 461 and robot.get_posx() > -75:
                robot.run(keys["X"])
            elif right:
                robot.cambiar_sprite_derecha("idle1")
            else:
                robot.cambiar_sprite_izquierda("idle1")
                
            if keys["boton1"] == 1 and not music_on:
                if pygame.mixer.music.get_pos() != -1:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.play(-1)
                music_on = True         
            elif keys["boton1"] == 1:
                pygame.mixer.music.pause()
                music_on = False
            
                
            

    



paco = Robot()
serialInput = Thread(target=serialCom, args=())
inGame(paco)

