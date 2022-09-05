import socket
import time


HOST = socket.gethostname()
PORT = 33060

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input("mysql> ")
        s.sendall(message.encode())
        data = s.recv(1024).decode()
        if data == "Bye":
            print(data)
            break
        elif data is not None:
            print(data)
        else:
            pass
