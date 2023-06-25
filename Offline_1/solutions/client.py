
import socket
from AES128 import aesDecrypt, aesEncrypt

PORT = 12345
KEY = "Thats my Kung Fu"

s = socket.socket()

s.connect(('localhost', PORT))

print('Waiting for data to receive...')
received = s.recv(1024)
received = aesDecrypt(received.decode(), KEY)
print('Received data:', received)

print('Waiting for data to send...')
data = input()
data = aesEncrypt(data, KEY)
data = s.send(data.encode())

s.close()
