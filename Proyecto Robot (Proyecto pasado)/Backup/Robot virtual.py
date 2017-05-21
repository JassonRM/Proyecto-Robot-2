#Robot Virtual
#Proyecto Programado
#Jasson Rodriguez

#Importa librerias
from tkinter import *
from threading import Thread
import time
import os
import pygame


#Funcion para cargar una imagen
def cargarImagen(nombre):
    ruta = os.path.join("Imagenes", nombre)
    imagen = PhotoImage(file=ruta)
    return imagen

#Funcion para cargar un sonido
def cargarSonido(nombre):
    ruta = os.path.join("Audio", nombre)
    sonido = pygame.mixer.Sound(ruta)
    return sonido

#Inicializa el mixer de pygame y carga a memoria la musica del robot
pygame.mixer.init(frequency=8000)
musica = cargarSonido("music.wav")

#Abrir los datos del robot
with open("robot.txt", "r") as archivo:
    info = archivo.read()
datos =  info.split("\n")
nombre = datos[0].split(": ")[1]
imagen = datos[1].split(": ")[1]
fecha = datos[2].split(": ")[1]
energia_original = datos[3].split(": ")[1]
energia = int(energia_original)
if energia > 100:
    energia = 100
if energia < 0:
    energia = 0
archivo.close()

#Guardar los datos del robot
def cerrar():
    global energia
    with open("robot.txt", "w") as archivo:
        archivo.write(info.replace(energia_original, str(energia)))
    archivo.close()
    ventana_principal.destroy()

#Crea la ventana principal
ventana_principal = Tk()
ventana_principal.minsize(1280,720)
ventana_principal.title("Robot virtual")

#Guarda los datos del robot al salir de la ventana principal
ventana_principal.protocol("WM_DELETE_WINDOW", cerrar)

#Crea el fondo
fondo = Canvas(ventana_principal, width=1920, height=1080, bg="#AAAAAA")
fondo.place(relx=0.5, rely=0.5, anchor=CENTER)

#Pone la imagen del robot
front = cargarImagen(imagen)
posx=0.5
robot = Label(fondo, image=front, bg="#AAAAAA")
robot.place(relx=posx, rely=0.38, anchor=CENTER)
imagenRobot = "front"

#Crea el shell
shell = Text(fondo, bg="#FFFFFF", height=15, width=50)
shell.place(relx=0.5, rely=0.70, anchor=CENTER)
shell.insert(END, ">>>")

#Crea el indicador de bateria
imagenBat = cargarImagen("battery.gif")
bat = Label(fondo, image=imagenBat, bg="#AAAAAA")
bat.place(relx=0.21,rely=0.2, anchor=CENTER)
carga = Canvas(bat, bg="#00AA00", width=energia, height=37, highlightthickness=0)
carga.place(x=6, y=6)
labelCarga = Label(fondo, text=str(energia) + "%", bg="#AAAAAA", font=("Arial", 20))
labelCarga.place(relx=0.24, rely=0.2, anchor=W)

#Funcion para actualizar el indicador de la bateria
def bateria():
    if energia > 20:
        carga.config(bg="#00AA00", width=energia)
        labelCarga.config(fg="#00AA00", text=str(energia) + "%")
        
    else:
        carga.config(bg="#AA0000", width=energia)
        labelCarga.config(fg="#AA0000", text=str(energia) + "%")
        
bateria()

#Funcion para el shell
def consola():
    text = shell.get(1.0, END)
    comando = text.split("\n")[-3]
    comando = comando.replace(">>>", "")
    if comando.split("(")[-1] == comando:
        comando = comando + "()"
    try:
        exec(comando)
    except NameError:
        shell.insert(END, "Comando no válido\n")
    shell.insert(END, ">>>")
#Comandos ocultos
def moveRightAux(cont, t):
    global posx
    while cont <= t and posx < 0.9:
        robot.place(relx=posx, rely=0.38, anchor=CENTER)
        posx += 0.005
        time.sleep(1 / 30)
        cont += 1 / 30
        
#Comandos que va a aceptar el robot
def hello():
    shell.insert(END, "Hola, mi nombre es " + nombre + "\n")
    sonido = cargarSonido("hello.wav")
    sonido.play()

def built():
    shell.insert(END, "Fui creado el día " + fecha + "\n")
    sonido = cargarSonido("built.wav")
    sonido.play()

def power(n):
    global energia
    if isinstance(n, int) and n >= 0:
        energia += n
        if energia > 100:
            energia = 100
    else:
        shell.insert(END, "Valor de energía no aceptado")
    bateria()
def status():
    if energia > 20:
        shell.insert(END, "La energía restante es del " + str(energia) + "%\n")
    else:
        shell.insert(END, "Batería baja! Por favor conecte a la corriente. \n" + str(energia) + "% restante.\n")
        advertencia = cargarSonido("bateria.wav")
        advertencia.play()

def goahead():
    if imagenRobot == "right":
        moveRight(5)
    elif imagenRobot == "left":
        moveLeft(5)
    else:
        right()
        moveRight(5)
        
def goback():
    if imagenRobot == "right":
        moveLeft(5)
    elif imagenRobot == "left":
        moveRight(5)
    else:
        right()
        moveLeft(5)
        
def right():
    global imagenRobot
    right = cargarImagen("right.gif")
    robot.config(image=right)
    robot.image = right
    imagenRobot = "right"

def left():
    global imagenRobot
    left = cargarImagen("left.gif")
    robot.config(image=left)
    robot.image = left
    imagenRobot = "left"
    
def music_on_aux():
    musica.play()
    global energia
    energia -= 1
    bateria()

def music_off():
    musica.stop()

def smile():
    sonrisa = cargarImagen("smile.gif")
    robot.config(image=sonrisa)
    robot.image = sonrisa
    
#Hilo 1
def hilo_shell(event):
    hilo1 = Thread(target=consola, args=())
    hilo1.start()
#Hilo 2
def music_on():
    hilo2 = Thread(target=music_on_aux, args=())
    hilo2.start()
#Hilo 3
def moveRight(t):
    hilo3 = Thread(target=moveRightAux, args=(0, t))
    hilo3.start()
    
shell.bind("<Return>", hilo_shell)

ventana_principal.mainloop()
