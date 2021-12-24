from fastapi import FastAPI
from src.routes import user_routes, doctor_routes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from src.database.database import create_index
from src.database.database import Mongo
from fastapi_socketio import SocketManager
import socketio
import asyncio
app = FastAPI()


app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
sio = socketio.AsyncServer(
  async_mode='asgi',
  cors_allowed_origins='*',
  logger=True,
  engineio_logger=True
)

#
# setattr(sio, 'database', Mongo())

app.include_router(user_routes.routes)
app.include_router(doctor_routes.doctor_routes)
# sio.start_background_task(create_index, sio)
# @sio.event
# def connect():
#     print("I'm connected!")
#
# @sio.event
# def connect_error(data):
#     print("The connection failed!")
#
# @sio.event
# def disconnect():
#     print("I'm disconnected!")

# socket_manager = SocketManager(app=app)


@sio.on('message', namespace='/chat')
async def chat(sid, data):
    await sio.send(data, to=sid)




# asyncio
# sio_client = socketio.AsyncClient()
# async def connect():
#     await sio_client.connect('http://localhost:8000')


# @sio_client.event(namespace='/chat')
# def my_custom_event(sid, data):
#     print(sid)
#     print(data)
#
#
# @sio_client.on('connect', namespace='/chat')
# async def con():
#     print('conectado')

doc = """"
<!DOCTYPE html>
<html>

<head>
  <script src="//code.jquery.com/jquery-3.3.1.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/3.1.3/socket.io.js"
    integrity="sha512-2RDFHqfLZW8IhPRvQYmK9bTLfj/hddxGXQAred2wNZGkrKQkLGj8RCkXfRJPHlDerdHHIzTFaahq4s/P4V6Qig=="
    crossorigin="anonymous"></script>
  <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>

<body>

  <script type="text/javascript">

    $(document).ready(function () {

      var socket = io.connect('http://' + document.domain + ':' + location.port);

      socket.on('connect', function (event) {
        console.log('user is connected now');
        socket.emit('client_connect_event', { data: 'User connected' });
      });

      socket.on('server_antwort_01', function (msg, cb) {
        $('#log0').append('<br>' + $('<div/>').text('logs #' + msg.count + ': ' + msg.data).html());
        if (cb)
          cb();
      });

      $('form#start').submit(function (event) {
        socket.emit('client_start_event', { data: 'Start doing something' });
        return false;
      });

      $('form#stop').submit(function (event) {
        socket.emit('client_stop_event', { data: 'Stop doing something' });
        return false;
      });
    });
  </script>

  <h1>Websocket Demo</h1>

  <h2> Press below to display something send from Server</h2>
  <form id="start" method="post" action="#">
    <input type="submit" value="Start">
  </form>

  <form id="stop" method="post" action="#">
    <input type="submit" value="Stop">
  </form>

  <h3> Log </h3>
  <div id="log0"></div>
</body>
</html>"""

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.create_task(connect)

#
# @sio.event(namespace='/chat')
# def chat(sid, data):
#     await sio.send(data, to=sid)


