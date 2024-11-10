""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""nfrom flask_socketio import SocketIO, emit, join_room, leave_room
from app import socketio

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'username': 'System', 'msg': f'{username} has joined the room.'}, room=room)

@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    emit('message', {'username': data['username'], 'msg': data['msg']}, room=room)
