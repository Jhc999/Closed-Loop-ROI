import socket, os, io, sys

HOST = ''  # Standard loopback interface address (localhost)
PORT1 = 8000
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((HOST, PORT1))
s1.listen()
conn1, addr1 = s1.accept() 
print("Connected")   

while True:
    data = conn1.recv(1400)

