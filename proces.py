import cv2
import numpy as np
import face_recognition
from time import sleep
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
async def proces( websocket: WebSocket):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    Andrea_image = cv2.imread("andrea.JPG")
    Andrea_face_encoding = face_recognition.face_encodings(Andrea_image)[0]
    Juan_image = cv2.imread("Juan.JPG")
    Juan_face_encoding = face_recognition.face_encodings(Juan_image)[0]
    known_face_encodings = [
        Andrea_face_encoding,
        Juan_face_encoding
    ]
    known_face_names = [
        "Andrea Moreno",
        "Juan Moreno"
    ]
    #camera_ip_url = "http://192.168.18.43:8080/video"
    #cap = cv2.VideoCapture(camera_ip_url)
    if not cap.isOpened():
        print("Error al abrir el stream de la cámara IP")
        exit()
    des = 0
    det = 0
    nodet = 0
    while True:       

        ret, frame = cap.read()
        if ret == False:
            break
        
        frame = cv2.flip(frame, 1)
        face_locations= face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)       
        if face_locations != []:         
            for pos, face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)            
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    rostro = name                   
                    det+=1  
                    des = 0
                    nodet = 0
                else:
                    rostro = "desconocido"                    
                    des+=1
                    det=0
                    nodet=0
        else:
            rostro = "vacio"            
            nodet+=1
            des=0
            det=0
                        
        if det == 3 or   det ==50000:
            await websocket.send_text(f"La camara detectó a {rostro}")
        elif des==3 or des==50000:
            await websocket.send_text(f"La camara detectó un rostro {rostro}")
        elif nodet ==3 or nodet ==50000:
           await websocket.send_text(f"No se detectó ningún rostro aun")
        
        
        
    cap.release()



   #face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
                # result = face_recognition.compare_faces([face_image_encodings], face_frame_encodings)