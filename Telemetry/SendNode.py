
"""
Instituto Tecnologico de Costa Rica
Ingenieria en Computadores
Compiladores

Proyecto Esfera
2023

Restricciónes: Python3.7 
Uso del módudo NodeMCU de wifiConnection
"""

#           _____________________________
#__________/BIBLIOTECAS
from tkinter import *               
from threading import Thread        
import threading                    
import os                           
import time                         
from tkinter import messagebox      
import tkinter.scrolledtext as tkscrolled
from WiFiClient import NodeMCU #Archivo Arduino
#import archivo

#["pwm:100;", "pwm:-100;", "led;"]
acciones = ["pwm:100;", "pwm:-100;", "led;"]

#           _____________________________________
#__________/Cliente para NodeMCU
myCar = NodeMCU()
myCar.start()


def send():
    for i in acciones:
        myCar.send(i)
        time.sleep(3)
        print("Respuesta: " + myCar.read())

send()

