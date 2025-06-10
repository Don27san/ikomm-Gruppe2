import socket
import json
import time
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('', 5000))
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

is_typing = []

# Keep is_typing state up to date
def cleanup_typing():
    global is_typing
    while True:
        current_time = time.time()
        is_typing = [user for user in is_typing if current_time - user['timestamp'] < 1]
        time.sleep(1)
      

cleanup_thread = threading.Thread(target=cleanup_typing)
cleanup_thread.daemon = True
cleanup_thread.start()  

# Listen for incoming type-indicator
while True:
    data, addr = server.recvfrom(1024)
    body = json.loads(data.decode())
    
    users = [item['user'] for item in is_typing]

    if body['user'] not in users:
        is_typing.append({'user': body['user'], 'timestamp': time.time()})
    else:
        for item in is_typing:
            if item['user'] == body['user']:
                item['timestamp'] = time.time()

    try:
        server.sendto(json.dumps(is_typing).encode(), ('<broadcast>', 4040))
    except:
        print('Broadcasting failed')
