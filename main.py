from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import numpy as np
import base64
from io import BytesIO
import pyrebase
from firebaseConfig  import auth
import firebase_admin
from firebase_admin import credentials
from PIL import Image
import requests
import cv2
import numpy as np
import face_recognition
from proces import proces
from TokenFunctions import create_session_token,verify_session_token
app = FastAPI()
class Usuario(BaseModel):
    email: str
    password: str


@app.websocket("/sigin")
async def SigIn():  
    return {"status"}

@app.websocket("/sigin/{id}")
async def SigIn(websocket: WebSocket,us:Usuario,id:str,msg:str):   
    
    try:
        user = auth.sign_in_with_email_and_password(us.email, us.password)
        token = user.token
        create_session_token(token)
        print(token)
        try:
            await websocket.accept()             
            await proces(websocket)
            print("exito")
        except:
            print("Client disconnected")
            return {"error"} 
    except:
      print("fallo en registro")      
      return {"error"}   
    print(f"Received data: {us}")
    return {"status": "success"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)