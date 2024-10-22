from flask_socketio import emit, join_room, leave_room
from app import socketio

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'{data["username"]} has entered the room.'}, room=room)

@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    emit('message', {'username': data['username'], 'msg': data['msg']}, room=room)
