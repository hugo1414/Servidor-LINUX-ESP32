# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 20:40:15 2022
@author: Hugo Delgado - Roddy Catagua
@title: pyServer
"""
import socket
import random
from datetime import datetime
#from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
#import threading

host, port = "192.168.0.106", 4444
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cred = credentials.Certificate("/home/hugo/Desktop/apppaneles-firebase-adminsdk-s2c2p-1d3564304e.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
#contador = 0

def recv(): 
	
    try:
        client.bind((host, port))
    finally:
        pass
    client.listen(10) # how many connections can it receive at one time
    print ("Se inicio correctamente el servidor entregando datos...")
    V_panel="0"
    I_panel="0"
    V_bateria="0"
    I_bateria="0"
    datoCont = 0
    
    while True:
        conn, addr = client.accept()
        print ("cliente con la direccion: ", addr, " esta conectado.")
        data = conn.recv(1024)
        data2=str(data)
        list_data3 = data2.split("'")
        list_data2 = list_data3[1]
        list_data=list_data2.split(',')
        cabecera = list_data[0]
        print (list_data)
        print (list_data[0])
        cabecera = int(list_data[0])
        
        print ("Recibiendo datos: <", data, "> desde el ESP32 .")
        if cabecera == 0:
            print ("contador",str(datoCont))
            V_panel=list_data[1]
            I_panel=list_data[2]
            V_bateria=list_data[3]
            I_bateria=list_data[4]
            potenciaCal=float(V_bateria)*float(I_bateria)
            datoCont = str(datoCont)
            data = {
                u'fecha': datetime.now(),
                u'potencia': potenciaCal
            }
            db.collection(u'mediciones').document(datoCont).set(data)
            reply = "ok data"
            conn.send(reply.encode("utf-8"))
            conn.close()
            datoCont=int(datoCont)+1
        if cabecera == 1:
            print ("cabecera 1")
            #reply = V_panel + "," +I_panel
            reply = V_panel + "," +I_panel + "," + V_bateria + "," +I_bateria+","+"0"
            conn.send(reply.encode("utf-8"))
            print (reply)
            conn.close()
        if cabecera == 2:
            print ("cabecera 2")
            #reply = V_bateria + "," +I_bateria
            reply = V_panel + "," +I_panel + "," + V_bateria + "," +I_bateria+","+"0"
            print (reply)
            conn.send(reply.encode("utf-8"))
            conn.close()
        if cabecera == 3:
            print ("cabecera 3")
            potencia = 0
            #una_fecha = '24/07/2022'
            #otra_fecha = '23/07/2022'
            otra_fecha=list_data[1]
            una_fecha=list_data[2]
            fecha_fin = datetime.strptime(una_fecha, '%m/%d/%Y')
            fecha_ini = datetime.strptime(otra_fecha, '%m/%d/%Y')
            print(fecha_fin)
            print(fecha_ini)

            consulta = db.collection(u'mediciones').where(u'fecha', u'<=', fecha_fin).where(u'fecha', u'>=', fecha_ini)
            docs=consulta.stream()
            for doc in docs:
                #print(f'{doc.id} => {doc.to_dict()}')
                s = doc.to_dict()
                potencia = potencia + int(s['potencia'])
                print(' Fecha: {} \n Potencia: {} \n'.format(s['fecha'],s['potencia']))

            print('potencia final: ', potencia)
            reply = "3" + "," +"1" + "," + "12" + "," +"3"+","+str(potencia)
            conn.send(reply.encode("utf-8"))
            print (reply)
            conn.close()
        if data == "Correct":
            reply = "Success"
            conn.send(reply.encode("utf-8"))
            conn.close()
            print ("-----------------------------")
        elif data == "Disconnect":
            reply = "Disconnected and the listen has Stopped"
            conn.send(reply.encode("utf-8"))
            conn.close()
            break
        else:
            v = random.randint(10,14)
            i = random.randint(0,10)
            sv = str(v)
            si = str(i)
            print ("--------------1-------------")
            reply = sv + "," +si
			#conn.send(reply.encode("utf-8"))
			#conn.close()
            print ("-----------------------------")		
            
    client.close()
"""
You can use thread for the recieve operation so that the execution in main thread
isn't wait until complete the recieve operation. 
"""
#thread = threading.Thread(target = recvFromAndroid, args = ())
#thread.start()
recv()
#print "completed"

