# Control Robot
# Proyecto programado
# Jasson Rodriguez
# Marco Herrera

# Importar librerias
import pygame
import time
import os
import sys
import serial
from threading import Thread

puerto = '/dev/tty.HC-06-DevB'

#objeto serial
arduino = serial.Serial(puerto, 9600, timeout=None)
arduino.flushInput()

#Tamaño de sprites 
spriteSize = 200
bulletSize = 20

# Variables globales
right = True
inbullet = False
sliding = False
bala = None

#------------------------------------------------------------------------Funciones------------------------------------------------------------------------#

#Funcion: serialCom
#Entrada: Dispositivo
#Salida: Diccionario con las teclas
#Restricciones: Dispostivo conectado
def serialCom():
        try:
            entrada = str(arduino.readline())
            keys = eval(entrada[(entrada.find("{")):entrada.find("}")+1])
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
    sonido = pygame.mixer.Sound(ruta)
    return sonido

#Funcion: cargarMusica
#Entrada: nombre
#Salida: musica con ese nombre en el directorio audio
#Restricciones: nombre es un string
def cargarMusica(nombre):
    ruta = os.path.join("Audio", nombre)
    musica = pygame.mixer.music.load(ruta)
    return musica

#Funcion: scale_img
#Entradas: imagen, ancho y altura
#Salida: imagen reescalada
#Restricciones: imagen de tipo pygame, ancho y altura son enteros
def scale_img(image,width,height):    
    image = pygame.transform.smoothscale(image,(width,height))
    return image

#Diccionario con las imagenes del robot
Sprite = {"idle1":scale_img(cargarImagen("Idle (1).png"),spriteSize,spriteSize),"idle2":scale_img(cargarImagen("Idle (2).png"),spriteSize,spriteSize),
          "idle3":scale_img(cargarImagen("Idle (3).png"),spriteSize,spriteSize),"idle4":scale_img(cargarImagen("Idle (4).png"),spriteSize,spriteSize),
          "idle4":scale_img(cargarImagen("Idle (4).png"),spriteSize,spriteSize),"idle5":scale_img(cargarImagen("Idle (5).png"),spriteSize,spriteSize),
          "idle6":scale_img(cargarImagen("Idle (6).png"),spriteSize,spriteSize),"idle7":scale_img(cargarImagen("Idle (7).png"),spriteSize,spriteSize),
          "idle8":scale_img(cargarImagen("Idle (8).png"),spriteSize,spriteSize),"idle9":scale_img(cargarImagen("Idle (9).png"),spriteSize,spriteSize),
          "idle10":scale_img(cargarImagen("Idle (10).png"),spriteSize,spriteSize),"run1":scale_img(cargarImagen("Run (1).png"),spriteSize,spriteSize),
          "run2":scale_img(cargarImagen("Run (2).png"),spriteSize,spriteSize), "run3":scale_img(cargarImagen("Run (3).png"),spriteSize,spriteSize),
          "run4":scale_img(cargarImagen("Run (4).png"),spriteSize,spriteSize), "run5":scale_img(cargarImagen("Run (5).png"),spriteSize,spriteSize),
          "run6":scale_img(cargarImagen("Run (6).png"),spriteSize,spriteSize), "run7":scale_img(cargarImagen("Run (7).png"),spriteSize,spriteSize),
          "run8":scale_img(cargarImagen("Run (8).png"),spriteSize,spriteSize), "jump1":scale_img(cargarImagen("Jump (1).png"),spriteSize,spriteSize),
          "jump2":scale_img(cargarImagen("Jump (2).png"),spriteSize,spriteSize), "jump3":scale_img(cargarImagen("Jump (3).png"),spriteSize,spriteSize),
          "jump4":scale_img(cargarImagen("Jump (4).png"),spriteSize,spriteSize), "jump5":scale_img(cargarImagen("Jump (5).png"),spriteSize,spriteSize),
          "jump6":scale_img(cargarImagen("Jump (6).png"),spriteSize,spriteSize), "jump7":scale_img(cargarImagen("Jump (7).png"),spriteSize,spriteSize),
          "jump8":scale_img(cargarImagen("Jump (8).png"),spriteSize,spriteSize), "jump9":scale_img(cargarImagen("Jump (9).png"),spriteSize,spriteSize),
          "jump10":scale_img(cargarImagen("Jump (10).png"),spriteSize,spriteSize), "run_s1":scale_img(cargarImagen("RunShoot (1).png"),spriteSize,spriteSize),
          "run_s2":scale_img(cargarImagen("RunShoot (2).png"),spriteSize,spriteSize),"run_s3":scale_img(cargarImagen("RunShoot (3).png"),spriteSize,spriteSize),
          "run_s4":scale_img(cargarImagen("RunShoot (4).png"),spriteSize,spriteSize), "run_s5":scale_img(cargarImagen("RunShoot (5).png"),spriteSize,spriteSize),
          "run_s6":scale_img(cargarImagen("RunShoot (6).png"),spriteSize,spriteSize), "run_s7":scale_img(cargarImagen("RunShoot (7).png"),spriteSize,spriteSize),
          "run_s8":scale_img(cargarImagen("RunShoot (8).png"),spriteSize,spriteSize), "shoot1":scale_img(cargarImagen("Shoot (1).png"),spriteSize,spriteSize),
          "bullet1":scale_img(cargarImagen("Bullet_001.png"),bulletSize,bulletSize),"slide1":scale_img(cargarImagen("Slide (1).png"),spriteSize,spriteSize),
          "slide2":scale_img(cargarImagen("Slide (2).png"),spriteSize,spriteSize),"slide3":scale_img(cargarImagen("Slide (3).png"),spriteSize,spriteSize),
          "slide4":scale_img(cargarImagen("Slide (4).png"),spriteSize,spriteSize),"slide5":scale_img(cargarImagen("Slide (5).png"),spriteSize,spriteSize),
          "slide6":scale_img(cargarImagen("Slide (6).png"),spriteSize,spriteSize),"slide7":scale_img(cargarImagen("Slide (7).png"),spriteSize,spriteSize),
          "slide8":scale_img(cargarImagen("Slide (8).png"),spriteSize,spriteSize)}

#------------------------------------------------------------------------Clases------------------------------------------------------------------------#

class Robot:
    def __init__(self):
        self.sprite = Sprite["idle1"]
        self.posx = 300
        self.posy = 675
        self.x_velocidad = 0
        self.y_velocidad = 0
        self.imagen = 2
        self.tiempo = 0

    #Metodo: get_posx
    #Entrada: ninguna
    #Salida: posicion en x del robot
    #Restricciones: ninguna
    def get_posx(self):
        return self.posx

    #Metodo: get_posy
    #Entrada: ninguna
    #Salida: posicion en y del robot
    #Restricciones: ninguna
    def get_posy(self):
        return self.posy

    #Metodo: set_posx
    #Entrada: un cambio en la posicion
    #Salida: Cambia la posicion de la instancia
    #Restricciones: pos entero
    def set_posx(self, pos):
        self.posx += pos

    #Metodo: cambiar_sprite_derecha
    #Entrada: nombre del sprite
    #Salida: Cambia el sprite de la instancia viendo hacia la derecha
    #Restricciones: nombre valido
    def cambiar_sprite_derecha(self,nombre):
        self.sprite = Sprite[nombre]
        global right
        right = True

    #Metodo: cambiar_sprite_izquierda
    #Entrada: nombre del sprite
    #Salida: Cambia el sprite de la instancia vienda hacia la izquierda
    #Restricciones: nombre valido
    def cambiar_sprite_izquierda(self,nombre):
        global right 
        right = False
        self.sprite = pygame.transform.flip(Sprite[nombre],True,False)

    #Metodo: run
    #Entrada: velocidad
    #Salida: cambia la posicion y el sprite del robot de acuerdo a la velocidad
    #Restricciones: velocidad entero
    def run(self,velocidad):
        self.set_posx((velocidad - 502) // 40)
        if self.tiempo == 0:
            if self.imagen >= 8:
                self.imagen = 1
            else:
                self.imagen += abs((velocidad - 511.5)/ 511.5)
            if velocidad > 550:
                self.cambiar_sprite_derecha("run"+ str(int((self.imagen))))
            else:
                self.cambiar_sprite_izquierda("run"+ str(int(self.imagen)))

    #Metodo: runshoot
    #Entrada: velocidad
    #Salida: cambia la posicion y el sprite del robot de acuerdo a la velocidad, disparando mientras corre
    #Restricciones: velocidad entero
    def runshoot(self,velocidad):
        self.set_posx((velocidad - 502) // 40)
        if self.tiempo == 0:
            if self.imagen >= 8:
                self.imagen = 1
            else:
                self.imagen += abs((velocidad - 511.5)/ 511.5)
            if velocidad > 550:
                self.cambiar_sprite_derecha("run_s"+ str(int((self.imagen))))
            else:
                self.cambiar_sprite_izquierda("run_s"+ str(int(self.imagen)))

    #Metodo: shoot
    #Entrada: ninguna
    #Salida: cambia el sprite a posicion de disparo
    #Restricciones:
    def shoot(self):
        if right:
            self.cambiar_sprite_derecha("shoot1")
        else:
            self.cambiar_sprite_izquierda("shoot1")

    #Metodo: shoot
    #Entrada: ninguna
    #Salida: cambia el sprite en modo standing
    #Restricciones:
    def stand(self):
        if self.imagen >= 8:
            self.imagen = 1
        else:
            self.imagen += 0.5
        if right:
            self.cambiar_sprite_derecha("idle"+ str(int((self.imagen))))
        else:
            self.cambiar_sprite_izquierda("idle"+ str(int(self.imagen)))
    
        

    #Metodo: jump
    #Entrada: ninguna
    #Salida: cambia la posicion en y y el sprite para que salte
    #Restricciones: ninguna
    def jump(self):
        v0 = 1000
        aceleracion = -4000
        posy = 675
        delta_pos = v0 * self.tiempo + (aceleracion * self.tiempo ** 2) / 2
        self.tiempo += 1 / 30
        self.posy = posy - delta_pos
        if delta_pos < 0:
            self.posy = posy
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

    #Metodo: slide
    #Entrada: velocidad y teclas
    #Salida: muestra la animacion para deslizarse
    #Restricciones: velocidad entero y teclas un diccionario valido
    def slide(self,velocidad,keys):
        global sliding
        sliding  = True
        while (velocidad > 550 or velocidad < 450) and self.get_posx() > -75 and self.get_posx() < windowWidth -125:
                self.set_posx((velocidad - 502) // 50)
                if self.imagen >= 7:
                    self.imagen = 1
                else:
                    self.imagen += 0.125
                if velocidad > 550:
                    self.cambiar_sprite_derecha("slide"+ str(int((self.imagen))))
                    velocidad -= 15
                else:
                    velocidad += 15
                    self.cambiar_sprite_izquierda("slide"+ str(int(self.imagen)))
                clock.tick(30)
        while keys["Y"] > 750 or (keys["X"] > 561 or keys["X"] < 461):
                keys = serialCom()
        sliding = False

class Bullet:
    def __init__(self, robot):
        if right:
            self.posx = robot.get_posx() + 150
            self.posy = robot.get_posy() + 100
            self.velocidad = 20
            self.imagen = Sprite["bullet1"]
        else:
            self.posx = robot.get_posx()
            self.posy = robot.get_posy() + 100
            self.velocidad = -20
            self.imagen = pygame.transform.flip(Sprite["bullet1"],True,False)
            
    #Metodo: shoot
    #Entrada: ninguna
    #Salida: cambia la posicion en x de la bala
    #Restricciones: ninguna
    def shoot(self):
        global inbullet
        if self.posx > 0 and self.posx < windowWidth:
            self.posx += self.velocidad
        else:
            inbullet = False

#------------------------------------------------------------------------Interfaz------------------------------------------------------------------------#

#Inicializar pygame
pygame.init()
clock = pygame.time.Clock()

#Inicializar el mixer de pygame y cargar audios 
pygame.mixer.init(frequency=8000)
cancion = "Epic Orchestral Action.wav"
cargarMusica(cancion)
mensaje = "Presentación.wav"
presentacion = cargarSonido(mensaje)


#Crear ventana
windowWidth = 1650
windowHeight = 1050
ventana = pygame.display.set_mode((windowWidth,windowHeight), pygame.FULLSCREEN)
pygame.display.set_caption("Robot Virtual 2")
bg = scale_img(cargarImagen("bg.png"), windowWidth,windowHeight)

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
                pygame.quit()
                sys.exit()
                break
        ventana.fill((255, 255, 255))
        ventana.blit(bg,(0,0))
        ventana.blit(robot.sprite,(robot.posx,robot.posy))
        if inbullet:
            ventana.blit(bala.imagen, (bala.posx,bala.posy))
        pygame.display.flip()
        clock.tick(60)

#-------------------------------------------------------------------Analisis de Datos Recibidos-------------------------------------------------------------------#

#Funcion: controller
#Entrada: instancia del robot a controlar
#Salida: Llama a todos los metodos del robot
#Restricciones: Que la instancia exista
def controller(robot):
    global inbullet
    global bala
    music_on = False
    musica_anterior = 0
    disparo_anterior = 0
    while in_Game:
        keys = serialCom()
        if keys != None and not sliding:
            # Jump
            if inbullet:
                bala.shoot()
            if keys["C"] or robot.tiempo != 0:
                robot.jump()
            # Right
            if keys["X"] > 561 and robot.get_posx() < windowWidth - 125:
                # Slide
                if keys["Y"] > 600 and robot.tiempo == 0 and keys["X"] > 950:
                    robot.slide(keys["X"],keys)
                # Run-Shoot
                elif keys["B"] == 1 and robot.tiempo == 0 and not inbullet:
                    inbullet = True
                    bala = Bullet(robot)
                    robot.runshoot(keys["X"])
                    
                # Run
                else:
                    robot.run(keys["X"])
            # Left
            elif keys["X"] < 461 and robot.get_posx() > -75:
                # Slide
                if keys["Y"] > 600 and robot.tiempo == 0 and keys["X"] < 50:
                    robot.slide(keys["X"],keys)
                # Run-Shoot
                elif keys["B"] == 1 and robot.tiempo == 0 and not inbullet:
                    inbullet = True
                    bala = Bullet(robot)
                    robot.runshoot(keys["X"])
                    
                # Run
                else:
                    robot.run(keys["X"])
            #Shoot
            elif keys["B"] == 1 and robot.tiempo == 0 and not inbullet:
                inbullet = True
                bala = Bullet(robot)
                robot.shoot()
            #Stand
            elif robot.tiempo == 0:
                robot.stand()

            disparo_anterior = keys["B"]
            # Music
            if keys["A"] == 0 and musica_anterior == 1 and not music_on:
                if pygame.mixer.music.get_pos() != -1:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.play(-1)
                music_on = True         
            elif keys["A"] == 0 and musica_anterior == 1 :
                pygame.mixer.music.pause()
                music_on = False
            #Presentacion
            if keys["D"] == 1 and not music_on:
                presentacion.play()            
                
            musica_anterior = keys["A"]
            
            
#Ejecutar el programa
paco = Robot()
serialInput = Thread(target=serialCom, args=())
inGame(paco)
