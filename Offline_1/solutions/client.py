
import socket
from AES128 import aesDecrypt, aesEncrypt
from diffiehellman import *
from bcolors import bcolors

PORT = 12345

s = socket.socket()

s.connect(('localhost', PORT))
print('Connected to server!')

p = int(s.recv(1024))
g = int(s.recv(1024))
A = int(s.recv(1024))

print('Received p, g, A from server!')
print('p:', p)
print('g:', g)
print('A:', A)

print('Generating a random prime number b of 64 bits...')
b = generatePrime(64)
print('Generated b:', b)
print('Generating B...')

B = powmod(g, b, p)
print('Generated B:', B)
print('Sending B to server...')
s.send(str(B).encode())

print('Generating key...')
key = powmod(A, b, p)
print('Generated key:', key)

print(f'{bcolors.BOLD}{bcolors.OKCYAN}Write something to send to server...{bcolors.ENDC}')
data = input()
data = aesEncrypt(data, key)
data = s.send(data.encode())
print(f'{bcolors.OKGREEN}Data sent successfully!{bcolors.ENDC}')
print('Waiting for server response...')

received = s.recv(1024)
received = aesDecrypt(received.decode(), key)
print(f'Received data:{bcolors.OKBLUE} {received}{bcolors.ENDC}')

s.close()
