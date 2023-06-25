import socket
from AES128 import aesDecrypt, aesEncrypt

PORT = 12345
KEY = "Thats my Kung Fu"

s = socket.socket()
s.bind(('', PORT))

s.listen(5)

while True:
  conn, addr = s.accept()
  print('Connection established with', addr)
  print('Waiting for data to send...')

  data = input()
  data = aesEncrypt(data, KEY)
  data = conn.send(data.encode())
  print('Data sent successfully!')

  received = conn.recv(1024)
  received = aesDecrypt(received.decode(), KEY)
  print('Received data:', received)

  conn.close()
