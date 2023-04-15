"""
Instituto Tecnologico de Costa Rica
Ingenieria en Computadores
Compiladores

Proyecto Esfera
2023

Restricciónes: Python3.7 
Uso del módudo NodeMCU de wifiConnection

"""

"""Como llamar un comando: ???
Directo: pwm:1; = adelante
         pwm:-1; = atras
         
Detenerse: det;
            
"""
#           _____________________________
#__________/BIBLIOTECAS
from tkinter import *               # Tk(), Label, Canvas, Photo
from threading import Thread        # p.start()
import threading                    #
import os                           
import time                         
from tkinter import messagebox      
import tkinter.scrolledtext as tkscrolled
from WiFiClient import NodeMCU #Archivo Arduino


#           ____________________________
#__________/Ventana Principal
root=Tk()
root.title('Esfera')
root.minsize(800,420)
root.resizable(width=NO,height=NO)

#           ______________________________
#__________/Se crea un lienzo para objetos
C_root=Canvas(root, width=800,height=600, bg='white')
C_root.place(x=0,y=0)

title = Label(C_root,text="Esfera",font=('Agency FB Bold',20),bg='white',fg='hotpink')
title.place(x=360, y=2)


#           _____________________________________
#__________/Se titulo de los Cuadros de texto
L_Titulo = Label(C_root,text="Mensajes Enviados",font=('Agency FB',14),bg='white',fg='hotpink')
L_Titulo.place(x=100,y=50)

L_Titulo = Label(C_root,text="Respuesta Mensaje",font=('Agency FB',14),bg='white',fg='hotpink')
L_Titulo.place(x=490,y=50)


SentCarScrolledTxt = tkscrolled.ScrolledText(C_root, height=10, width=45)
SentCarScrolledTxt.place(x=10,y=90)

RevCarScrolledTxt = tkscrolled.ScrolledText(C_root, height=10, width=45)
RevCarScrolledTxt.place(x=400,y=90)


#           _____________________________________
#__________/Creando el cliente para NodeMCU
myCar = NodeMCU()
myCar.start()


def get_log():
    """
    Hilo que actualiza los Text cada vez que se agrega un nuevo mensaje al log de myCar
    """
    indice = 0
    # Variable del carro que mantiene el hilo de escribir.
    while(myCar.loop):
        while(indice < len(myCar.log)):
            mnsSend = "[{0}] cmd: {1}\n".format(indice,myCar.log[indice][0])
            SentCarScrolledTxt.insert(END,mnsSend)
            SentCarScrolledTxt.see("end")

            mnsRecv = "[{0}] result: {1}\n".format(indice,myCar.log[indice][1])
            RevCarScrolledTxt.insert(END, mnsRecv)
            RevCarScrolledTxt.see('end')

            indice+=1
        time.sleep(0.200)
    
p = Thread(target=get_log)
p.start()
           


L_Titulo = Label(C_root,text="Mensaje:",font=('Agency FB',14),bg='white',fg='hotpink')
L_Titulo.place(x=100,y=280)

E_Command = Entry(C_root,width=30,font=('Agency FB',14))
E_Command.place(x=200,y=280)

L_Titulo = Label(C_root,text="ID mensaje:",font=('Agency FB',14),bg='white',fg='hotpink')
L_Titulo.place(x=100,y=340)

E_read = Entry(C_root,width=30,font=('Agency FB',14))
E_read.place(x=200,y=340)


def send(event):
    
    #Enviar un mensaje 
    
    mns = str(E_Command.get())
    
    if(len(mns)>0 and mns[-1] == ";"):
        E_Command.delete(0, 'end')
        myCar.send(mns)
        
    else:
        messagebox.showwarning("Error del mensaje", "Mensaje sin caracter de finalización (';')") 


def sendShowID():
    
    #Capturar un ID de un mensaje específico
    
    mns = str(E_Command.get())
    
    if(len(mns)>0 and mns[-1] == ";"):
        E_Command.delete(0, 'end')
        mnsID = myCar.send(mns)
        messagebox.showinfo("Mensaje pendiente", "Intentando enviar mensaje, ID obtenido: {0}\n\
La respuesta definitiva se obtine en un máximo de {1}s".format(mnsID, myCar.timeoutLimit))
        
    else:
        messagebox.showwarning("Error del mensaje", "Mensaje sin caracter de finalización (';')")

def read():

    #Leer un mensaje enviado con un ID específico

    mnsID = str(E_read.get())
    if(len(mnsID)>0 and ":" in mnsID):
        mns = myCar.readById(mnsID)
        if(mns != ""):
            messagebox.showinfo("Resultado Obtenido", "El mensaje con ID:{0}, obtuvo de respuesta:\n{1}".format(mnsID, mns))
            E_read.delete(0, 'end')
        else:
            messagebox.showerror("Error de ID", "No se obtuvo respuesta\n\
El mensaje no ha sido procesado o el ID es invalido\n\
Asegurese que el ID: {0} sea correcto".format(mnsID))

    else:
        messagebox.showwarning("Error en formato", "Recuerde ingresar el separador (':')")

root.bind('<Return>', send) #Vinculando tecla Enter a la función send

#           ____________________________
#__________/Botones de ventana principal

Btn_ConnectControl = Button(C_root,text='Send',command=lambda:send(None),fg='black',bg='hotpink', font=('Agency FB',12))
Btn_ConnectControl.place(x=450,y=290)

Btn_Controls = Button(C_root,text='Send & Show ID',command=sendShowID,fg='black',bg='hotpink', font=('Agency FB',12))
Btn_Controls.place(x=500,y=290)

Btn_ConnectControl = Button(C_root,text='Leer Mensaje',command=read,fg='black',bg='hotpink', font=('Agency FB',12))
Btn_ConnectControl.place(x=450,y=340)
root.mainloop()
