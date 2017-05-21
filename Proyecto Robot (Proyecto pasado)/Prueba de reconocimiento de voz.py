import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Diga algo")
    audio = r.listen(source)
try:
    mensaje = r.recognize_google(audio)
    print(mensaje)
except sr.UnknownValueError:
    print("No se pudo entender el audio")
