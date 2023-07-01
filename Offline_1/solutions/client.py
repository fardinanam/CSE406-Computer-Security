
import socket
from AES128 import aesDecrypt, aesEncrypt
from diffiehellman import *
from bcolors import bcolors
from rsa import *

PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('localhost', PORT))
print('Connected to server!')

print('Generating RSA keys...')
n, e, d = generateRsaKeys()
print('Generated RSA keys!')
print(f'Public key:{bcolors.OKGREEN} {e}{bcolors.ENDC}')
print(f'Private key:{bcolors.OKGREEN} {d}{bcolors.ENDC}')
print(f'n:{bcolors.OKGREEN} {n}{bcolors.ENDC}')

print('Sending public key and n to server...')
s.send((str(e) + ' ' + str(n)).encode())

print('Waiting for server\'s public key and n...')
serverRsaParams = str(s.recv(1024).decode()).split()
server_e = int(serverRsaParams[0])
server_n = int(serverRsaParams[1])
print('Received server\'s public key and n!')
print(f'server_e:{bcolors.OKGREEN} {server_e}{bcolors.ENDC}')
print(f'server_n:{bcolors.OKGREEN} {server_n}{bcolors.ENDC}')

print('Waiting for p, g, A from server...')

data = (s.recv(1024).decode()).split()
p = int(data[0])
g = int(data[1])
A = int(data[2])

print('Received encrypted p, g, A from server!')
print('Decrypting p, g, A with private key...')
p = decryptWithRSA(p, d, n)
g = decryptWithRSA(g, d, n)
A = decryptWithRSA(A, d, n)

print(f'p:{bcolors.OKGREEN} {p}{bcolors.ENDC}')
print(f'g:{bcolors.OKGREEN} {g}{bcolors.ENDC}')
print(f'A:{bcolors.OKGREEN} {A}{bcolors.ENDC}')

print('Generating a random prime number b of 64 bits...')
b = generatePrime(64)
print('Generated b:', b)
print('Generating B...')

B = powmod(g, b, p)
print('Generated B:', B)
print('Sending B to server...')

encryptedB = encryptWithRSA(B, server_e, server_n)
s.send(str(encryptedB).encode())

print('Generating key...')
key = powmod(A, b, p)
print('Generated key:', key)

data = input(
    f'{bcolors.BOLD}{bcolors.OKCYAN}Write something to send to server: {bcolors.ENDC}')

data = aesEncrypt(data, key)
data = s.send(data.encode())
print(f'{bcolors.OKGREEN}Data sent successfully!{bcolors.ENDC}')
print('Waiting for server response...')

received = s.recv(1024)
received = aesDecrypt(received.decode(), key)
print(f'Received data:{bcolors.OKBLUE} {received}{bcolors.ENDC}')

s.close()
