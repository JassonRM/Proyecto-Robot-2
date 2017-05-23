#Control Robot
#Proyecto programado
#Jasson Rodriguez
#Marco Herrera

#Importar librerias
import pygame
import time
import os 

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

Sprite = {"idle1":scale_img(cargarImagen("Idle (1).png"),200,200), "run1":scale_img(cargarImagen("Run (1).png"),200,200), "run2":scale_img(cargarImagen("Run (2).png"),200,200), "run3":scale_img(cargarImagen("Run (3).png"),200,200), "run4":scale_img(cargarImagen("Run (4).png"),200,200), "run5":scale_img(cargarImagen("Run (5).png"),200,200), "run6":scale_img(cargarImagen("Run (6).png"),200,200), "run7":scale_img(cargarImagen("Run (7).png"),200,200), "run8":scale_img(cargarImagen("Run (8).png"),200,200)}
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


clock = pygame.time.Clock()

#Inicializar pygame
pygame.init()

#Inicializar el mixer de pygame
pygame.mixer.init()

#Crear ventana
ventana = pygame.display.set_mode((800,600))
pygame.display.set_caption("Robot Virtual 2")


#Funcion: inGame
#Entrada: instancia del robot
#Salida: Entradas y salidas de las animaciones
#Restricciones: robot es una instancia
def inGame (robot):
    in_Game = True
    i = 2
    while in_Game :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_Game = False

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT:
                    if robot.x_velocidad > 0:
                        robot.acelerar_x(-2.25)
                    else:
                        robot.acelerar_x(-1)
                    if i == 8:
                        i = 1
                    else:
                        i += 1
                    robot.cambiar_sprite_izquierda("run"+ str(i))
                elif event.key == pygame.K_RIGHT:
                    if robot.x_velocidad < 0:
                        robot.acelerar_x(2.25)
                    else:
                        robot.acelerar_x(1)
                    if i == 8:
                        i = 1
                    else:
                        i += 1
                    robot.cambiar_sprite_derecha("run"+ str(i))
                pygame.event.clear()
                pygame.event.post(event)
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if i == 8:
                        i = 1                        
                    if robot.x_velocidad < -1:
                        robot.acelerar_x(1.5)
                        robot.cambiar_sprite_izquierda("run"+ str(i))
                        pygame.event.clear()
                        pygame.event.post(event)
                    elif robot.x_velocidad > 1:
                        robot.acelerar_x(-1.5)
                        robot.cambiar_sprite_derecha("run"+ str(i))
                        pygame.event.clear()
                        pygame.event.post(event)
                    else:
                        if right:
                            robot.cambiar_sprite_derecha("idle1")
                        else:
                            robot.cambiar_sprite_izquierda("idle1")
                        pygame.event.clear()
                    i += 1
                
                
        
        ventana.fill((255,255,255))
        ventana.blit(robot.sprite,(robot.posx,robot.posy))
        pygame.display.update()
        clock.tick(15)

    pygame.quit()
    quit()

paco = Robot()

inGame(paco)


