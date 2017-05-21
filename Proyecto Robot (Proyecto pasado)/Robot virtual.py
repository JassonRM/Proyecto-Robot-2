#Robot Virtual
#Proyecto Programado
#Jasson Rodriguez

#Importacion librerias
from tkinter import *
from threading import Thread
import time
import os
import pygame
import speech_recognition

#Funcion: cargarImagen
#Entrada: nombre
#Salida: imagen
#Restricciones: el archivo debe estar contenido en la carpeta Imagenes
def cargarImagen(nombre):
    ruta = os.path.join("Imagenes", nombre)
    imagen = PhotoImage(file=ruta)
    return imagen

#Funcion: cargarSonido
#Entrada: nombre
#Salida: sonido
#Restricciones: el archivo debe estar contenido en la carpeta Audio
def cargarSonido(nombre):
    ruta = os.path.join("Audio", nombre)
    sonido = pygame.mixer.Sound(ruta)
    return sonido

#Inicializa el mixer de pygame y carga a memoria la musica
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

#Funcion: cerrar
#Entrada: ninguna
#Salidas: actualiza los datos del archivo robot.txt, cierra la ventana y detiene los sonidos
#Restricciones: la energia_original debe ser un string y la energia debe ser int
def cerrar():
    datos[3] = datos[3].replace(energia_original, str(energia))
    with open("robot.txt", "w") as archivo:
        archivo.write(datos[0] + "\n" + datos[1] + "\n" + datos[2] + "\n" + datos[3])
    archivo.close()
    fondo.destroy()
    pygame.mixer.stop()

#Crea la ventana principal
fondo = Tk()
fondo.minsize(1280,720)
fondo.title("Robot virtual")
fondo.config(bg="#AAAAAA")

#Guarda los datos del robot al salir de la ventana principal
fondo.protocol("WM_DELETE_WINDOW", cerrar)


#Pone la imagen del robot
front = cargarImagen(imagen)
posx=0.5
robot = Label(fondo, image=front, bg="#AAAAAA")
robot.place(relx=posx, rely=0.38, anchor=CENTER)
imagenRobot = "front"

#Crea el shell
shell = Text(fondo, bg="#FFFFFF", height=15, width=50)
shell.place(relx=0.5, rely=0.81, anchor=CENTER)
shell.insert(END, ">>>")

#Crea el indicador de bateria
imagenBat = cargarImagen("battery.gif")
bat = Label(fondo, image=imagenBat, bg="#AAAAAA")
bat.place(relx=0.06,rely=0.05, anchor=CENTER)
carga = Canvas(bat, bg="#00AA00", width=energia, height=37, highlightthickness=0)
carga.place(x=6, y=6)
labelCarga = Label(fondo, text=str(energia) + "%", bg="#AAAAAA", font=("Arial", 20))
labelCarga.place(relx=0.11, rely=0.05, anchor=W)

#Funcion: bateria
#Entrada: ninguna
#Salidas: actualiza el indicador de bateria y cambia la imagen del robot, inhabilita el shell y detiene la musica si la energia llega a 0
#Restricciones: los valores de energia deben estar entre 0 y 100
def bateria():
    global vivo
    if energia == 0:
        carga.config(bg="#AA0000", width=energia)
        labelCarga.config(fg="#AA0000", text=str(energia) + "%")
        shell.config(state=DISABLED)
        muerto = cargarImagen("dead.gif")
        robot.config(image=muerto)
        robot.image = muerto
        imagenRobot = "muerto"
        pygame.mixer.stop()
    elif energia > 20:
        carga.config(bg="#00AA00", width=energia)
        labelCarga.config(fg="#00AA00", text=str(energia) + "%")
        
    else:
        carga.config(bg="#AA0000", width=energia)
        labelCarga.config(fg="#AA0000", text=str(energia) + "%")
        
bateria()

#Hilo 1
#Funcion: hilo_shell
#Entrada: evento del boton Return
#Salida: ejecuta la funcion de la consola
#Restricciones: ninguna
def hilo_shell(event):
    hilo1 = Thread(target=consola, args=())
    hilo1.start()

#Funcion; consola
#Entrada: texto del cuadro de texto shell
#Salida: ejecucion de la funcion especificada
#Restricciones: solo son permitidas funciones validas
def consola():
    text = shell.get(1.0, END)
    comando = text.split("\n")[-3]
    comando = comando.replace(">>>", "")
    if comando.split("(")[-1] == comando:
        comando = comando + "()"
    try:
        exec(comando)
    except Exception:
        shell.insert(END, "Comando no válido\n")
    shell.insert(END, ">>>")

#Hilo 6
#Funcion: reconocimiento
#Entrada: microfono
#Salida: string con lo que se decia en el microfono
#Restricciones: acceso a internet
def reconocimiento():
    hilo6 = Thread(target=reconocimiento_aux, args=())
    hilo6.start()

def reconocimiento_aux():
    shell.insert(END, "\nIniciando reconocimiento de voz...\n>>>")
    reconocedor = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as fuente:
        audio = reconocedor.listen(fuente)
    try:
        comando = reconocedor.recognize_google(audio, language="en-US")
        if comando == "music on":
            comando = "music_on"
        elif comando == "music off":
            comando = "music_off"
        elif comando == "go ahead":
            comando = "goahead"
        elif comando == "go back":
            comando = "goback"
        elif comando.split()[0] == "power":
            comando = "power(" + comando.split()[1] + ")"
        shell.insert(END, comando + "\n")
        consola()
    except speech_recognition.UnknownValueError:
        shell.insert(END, "No fue posible entender el audio")
    except speech_recognition.RequestError:
        shell.insert(END, "No fue posible conectar con el servicio de \nreconocimiento de voz")

#Boton de reconocimiento de voz
mic = cargarImagen("mic.gif")
escuchando = Button(fondo, image=mic, command=reconocimiento, bg="#AAAAAA", relief=FLAT)
escuchando.place(relx=0.33, rely=0.81, anchor=S)

#Comandos ocultos
    
#Hilo 3
#Funcion: moveRight
#Entrada: t
#Salida: mueve el robot hacia la derecha durante un tiempo t
#Restricciones: t es un entero positivo
def moveRight(t):
    hilo3 = Thread(target=moveRightAux, args=(0, t))
    hilo3.start()
    
def moveRightAux(cont, t):
    global posx
    while cont <= t and posx < 0.9:
        robot.place(relx=posx, rely=0.38, anchor=CENTER)
        posx += 0.0025
        time.sleep(1 / 30)
        cont += 1 / 30

#Hilo 4
#Funcion: moveLeft
#Entrada: t
#Salida: mueve el robot hacia la izquierda durante un tiempo t
#Restricciones: t es un entero positivo
def moveLeft(t):
    hilo4 = Thread(target=moveLeftAux, args=(0, t))
    hilo4.start()
    
def moveLeftAux(cont, t):
    global posx
    while cont <= t and posx > 0.1:
        robot.place(relx=posx, rely=0.38, anchor=CENTER)
        posx -= 0.0025
        time.sleep(1 / 30)
        cont += 1 / 30
        
def leftAux():
    global imagenRobot
    if imagenRobot == "right":
        robot.config(image=front)
        imagenRobot = "front"
    else:
        left = cargarImagen("left.gif")
        robot.config(image=left)
        robot.image = left
        imagenRobot = "left"
        
def rightAux():
    global imagenRobot
    if imagenRobot == "left":
        robot.config(image=front)
        imagenRobot = "front"
    else:
        right = cargarImagen("right.gif")
        robot.config(image=right)
        robot.image = right
        imagenRobot = "right"

def jumpAux():
    tiempo = 0
    v0 = 0.4
    aceleracion = -1
    posy = 0.38
    saltando = True
    while saltando:
        delta_pos = v0 * tiempo + (aceleracion * tiempo ** 2) / 2
        tiempo += 1 / 30
        posy = 0.38 - delta_pos
        robot.place(relx=posx, rely=posy, anchor=CENTER)
        time.sleep(1 / 30)
        if delta_pos < 0:
            tiempo = 0
            posy = 0.38
            saltando = False
            robot.place(relx=posx, rely=posy, anchor=CENTER)
            
#Comandos que va a aceptar el robot
            
#Funcion: hello
#Entrada: nombre
#Salida: frase en el shell con un saludo y un sonido
#Restricciones: nombre es un string
def hello():
    shell.insert(END, "Hola, mi nombre es " + nombre + "\n")
    sonido = cargarSonido("hello.wav")
    sonido.play()
    
#Funcion: built
#Entrada: fecha
#Salida: frase en el shell con la fecha de creacion y un sonido
#Restricciones: fecha es un string
def built():
    shell.insert(END, "Fui creado el día " + fecha + "\n")
    sonido = cargarSonido("built.wav")
    sonido.play()
    
#Funcion: power
#Entrada: n
#Salida: el valor de energia del robot aumenta en n, si pasa de 100 se limita a 100
#Restricciones: n es entero y mayor o igual a 0
def power(n):
    global energia
    if isinstance(n, int) and n >= 0:
        energia += n
        if energia > 100:
            energia = 100
    else:
        shell.insert(END, "Valor de energía no aceptado\n")
    bateria()

#Funcion: status
#Entrada: energia
#Salida: si la energia es mayor a 20 indica la energia en una frase, si es menor da una advertencia en el shell y por medio de audio
#Restricciones: energia es una valor entero entre 0 y 100
def status():
    if energia > 20:
        shell.insert(END, "La energía restante es del " + str(energia) + "%\n")
    else:
        shell.insert(END, "Batería baja! Por favor conecte a la corriente. \n" + str(energia) + "% restante.\n")
        advertencia = cargarSonido("battery.wav")
        advertencia.play()

#Funcion: goahead
#Entrada: orientacion del robot
#Salida: el robot se mueve hacia adelante, si esta viendo hacie el frente se gira a la derecha y avanza. Disminuye la energia en 1
#Restricciones: la orientacion del robot tiene valores especificos
def goahead():
    global energia
    if imagenRobot == "right":
        moveRight(2)
    elif imagenRobot == "left":
        moveLeft(2)
    else:
        rightAux()
        moveRight(2)
    energia -= 1
    time.sleep(2.5)
    bateria()
    
#Funcion: goback
#Entrada: orientacion del robot
#Salida: el robot se mueve hacia atras, si esta viendo hacie el frente se gira a la derecha y avanza. Disminuye la energia en 1
#Restricciones: la orientacion del robot tiene valores especificos
def goback():
    global energia
    if imagenRobot == "right":
        moveLeft(2)
    elif imagenRobot == "left":
        moveRight(2)
    else:
        rightAux()
        moveLeft(2)
    time.sleep(2.5)
    energia -= 1
    bateria()

#Funcion: right
#Entrada: orientacion del robot
#Salida: el robot se gira hacia la derecha y disminuye en 1 la energia
#Restricciones: la orientacion del robot tiene valores especificos
def right():
    global energia
    rightAux()
    energia -= 1
    bateria()

#Funcion: left
#Entrada: orientacion del robot
#Salida: el robot se gira hacia la izquierda y disminuye en 1 la energia
#Restricciones: la orientacion del robot tiene valores especificos    
def left():
    global energia
    leftAux()
    energia -= 1
    bateria()

#Funcion: dance
#Entrada: orientacion de robot
#Salida: animacion del robot bailando. Disminuye en 2 el valor de energia
#Restricciones: la orientacion del robot tiene valores especificos
def dance():
    global energia, imagenRobot
    if energia != 1:
        if imagenRobot == "right":
            leftAux()
        leftAux()
        moveLeft(0.5)
        time.sleep(0.5)
        moveRight(0.5)
        time.sleep(0.5)
        rightAux()
        rightAux()
        moveRight(0.5)
        time.sleep(0.5)
        moveLeft(0.5)
        time.sleep(0.5)
        leftAux()
        leftAux()
        moveLeft(0.5)
        time.sleep(0.5)
        moveRight(0.5)
        time.sleep(0.5)
        rightAux()
        rightAux()
        moveRight(0.5)
        time.sleep(0.5)
        moveLeft(0.5)
        time.sleep(0.5)
        leftAux()
        energia -= 2
        bateria()
    else:
        shell.insert(END, "La energía restante es insuficiente\n")

#Hilo 2
#Funcion: music_on
#Entrada: ninguna
#Salida: reproduccion de musica y disminuye en 1 la energia
#Restricciones: ninguna
def music_on():
    hilo2 = Thread(target=music_on_aux, args=())
    hilo2.start()
    
def music_on_aux():
    musica.play()
    global energia
    energia -= 1
    bateria()

#Funcion: music_off
#Entrada: ninguna
#Salida: detiene la reproduccion de musica
#Restricciones: ninguna
def music_off():
    musica.stop()

#Funcion: smile
#Entrada: ninguna
#Salida: cambia la imagen del robot a una sonrisa y reproduce una risa
#Restricciones: ninguna
def smile():
    sonrisa = cargarImagen("smile.gif")
    robot.config(image=sonrisa)
    robot.image = sonrisa
    risa = cargarSonido("smile.wav")
    risa.play()
    
#Funcion: cry
#Entrada: ninguna
#Salida: cambia la imagen del robot por una llorando y reproduce un llanto. Disminuye en 1 la energia
#Restricciones: ninguna
def cry():
    global energia
    llorar = cargarImagen("cry.gif")
    robot.config(image=llorar)
    robot.image = llorar
    llanto = cargarSonido("cry.wav")
    llanto.play()
    energia -= 1
    bateria()

#Hilo 5
#Funcion: jump
#Entrada: ninguna
#Salida: hace al robot saltar. Disminuye en 1 la energia
#Restricciones: ninguna
def jump():
    global energia
    energia -= 1
    bateria()
    hilo5 = Thread(target=jumpAux, args=())
    hilo5.start()

#Funcion: sing
#Entrada: ninguna
#Salida: cambia la imagen del robot a una sonrisa y reproduce un canto
#Restricciones: ninguna
def sing():
    global energia
    sonrisa = cargarImagen("smile.gif")
    robot.config(image=sonrisa)
    robot.image = sonrisa
    canto = cargarSonido("sing.wav")
    canto.play()
    energia -= 1
    bateria()
    
#Binding de la consola
    
shell.bind("<Return>", hilo_shell)



#Pantalla ayuda

def ayuda():
    fondo.withdraw()
    pantalla_ayuda = Toplevel()
    pantalla_ayuda.title("Ayuda")
    pantalla_ayuda.minsize(460, 700)
    pantalla_ayuda.resizable(width=NO, height=NO)
    pantalla_ayuda.config(bg="#FFFFFF")
    texto_ayuda = "Para la utilización del robot virtual se debe hacer uso de la consola para darle los comandos. Los comandos deben ser introducidos exactamente como se muestra a continuación. \n\nLos comandos aceptados por el robot son:\n\nhello: ​el robot saluda y da su nombre.\n\nbuilt: el robot da su fecha de creación.\n\npower(n): el robot recibe n de energía.\n\nstatus: el robot indica la cantidad de energía restante.\n\ngoahead: el robot camina hacia adelante. Reduce en uno la energía.\n\ngoback: el robot camina hacia atrás. Reduce en uno la energía.\n\nright: el robot gira a la derecha. Reduce en uno la energía.\n\nleft: el robot gira a la izquierda. Reduce en uno la energía.\n\ndance: el robot baila. Reduce en dos la energía.\n\nmusic-on: el robot reproduce música. Reduce en uno la energía.\n\nmusic-off: el robot para la reproducción de música.\n\nsmile: el robot ríe. No se modifica la energía.\n\ncry: el robot llora. Reduce en uno la energía.\n\njump: el robot salta. Reduce en uno la energía.\n\nsing: el robot canta. Disminuye en uno la energía."
    informacion = Label(pantalla_ayuda, text=texto_ayuda, bg="#FFFFFF", font=("Arial", 11), justify=LEFT, wraplength=440)
    informacion.place(x=10, y=60)

    #Funcion de volver
    def cerrar_ventana():
        pantalla_ayuda.destroy()
        fondo.deiconify()
        
    #Boton de volver
    volver = cargarImagen("volver.gif")
    boton_volver = Button(pantalla_ayuda, image=volver, command=cerrar_ventana, relief=FLAT, bg="#FFFFFF")
    boton_volver.place(x=5, y=5)

    pantalla_ayuda.mainloop()
    
#Boton de ayuda
imagen_ayuda = cargarImagen("help.gif")
boton_ayuda = Button(fondo, image=imagen_ayuda, command=ayuda, relief=FLAT, bg="#AAAAAA")
boton_ayuda.place(relx=1, rely=1, anchor=SE)


fondo.mainloop()
