import socket, os, io, sys

HOST = '192.168.1.71'  # Standard loopback interface address (localhost)
PORT1 = 9003           # Port to listen on (non-privileged ports are > 1023)
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((HOST, PORT1))
s1.listen()
conn1, addr1 = s1.accept() 
print("connected")   

while True:
    data = conn1.recv(1400)

