from pynput import keyboard
import socket
import json
import time
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
client.bind(('', 4040))

username = input("Enter your username: ")

# Debounce ensures that we only send out one request per wait-time. 
# Thus, not every keystroke triggers network traffic.
def debounce(wait_time):
    def decorator(fn):
        last_executed = [0]  

        def wrapped(args):
            now = time.time()
            if now - last_executed[0] > wait_time:
                fn(args)
                last_executed[0] = now

        return wrapped
    return decorator    


@debounce(1)
def on_press(key):
    try:
        body = {
            'user': username,
            'key': str(key)
        }
        client.sendto(json.dumps(body).encode(), ('localhost', 5000))
        
    except AttributeError:
        pass


# Listen for broadcasts
def listen_for_res():
    while True:
        data, addr = client.recvfrom(1024)
        res = json.loads(data.decode())
        print("Received from server:", res)

# Start UDP listener in a background thread
udp_thread = threading.Thread(target=listen_for_res)
udp_thread.daemon = True
udp_thread.start()


# Collect events until released
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()



