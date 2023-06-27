import socket
from AES128 import aesDecrypt, aesEncrypt
from diffiehellman import *
from bcolors import bcolors

PORT = 12345

s = socket.socket()
s.bind(('', PORT))

s.listen(5)

def generatePGaA():
  print('Generating a prime of 128 bits...')
  p, factors = generatePrimeAndFactors(128)
  print('Generated p:', p)
  print('Generating a generator of p...')
  g = generator(p, factors, 2, p - 1)
  print('Generated g:', g)
  print('Generating a random prime number a of 64 bits...')
  a = generatePrime(64)
  print('Generated a:', a)
  print('Generating A...')
  A = powmod(g, a, p)

  return p, g, a, A

while True:
  print('Waiting for client...')
  conn, addr = s.accept()
  print('Connection established with', addr)
  
  p, g, a, A = generatePGaA()

  print('Sending p, g, A to ', addr, "...")
  conn.send(str(p).encode())
  conn.send(str(g).encode())
  conn.send(str(A).encode())

  print('Waiting for B from client...')
  B = int(conn.recv(1024))
  print('Received B:', B)

  print('Generating key...')
  key = powmod(B, a, p)
  print('Generated key:', key)
  print('Waiting for data from client...')

  received = conn.recv(1024)
  received = aesDecrypt(received.decode(), key)
  print(f'Received data:{bcolors.OKBLUE} {received}{bcolors.ENDC}')

  print(f'{bcolors.BOLD}{bcolors.OKCYAN}Write something to send to client...{bcolors.ENDC}')
  data = input()
  data = aesEncrypt(data, key)
  data = conn.send(data.encode())
  print(f'{bcolors.OKGREEN}Data sent successfully!{bcolors.ENDC}')

  conn.close()
