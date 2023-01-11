from fastapi import FastAPI
from src.routes import user_routes, doctor_routes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# from src.database.database import create_index
# from src.database.database import Mongo
from fastapi_socketio import SocketManager
import socketio


app = FastAPI()

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


app.include_router(user_routes.routes)
app.include_router(doctor_routes.doctor_routes)

app_socket = socketio.ASGIApp(socketio_server=sio, other_asgi_app=app)


# @sio.on('message', namespace='/chat')
# async def chat(sid, data):
#     await sio.send(data, to=sid)
