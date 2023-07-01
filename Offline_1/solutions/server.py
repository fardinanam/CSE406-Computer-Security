import socket
from AES128 import aesDecrypt, aesEncrypt
from diffiehellman import *
from bcolors import bcolors
from rsa import *

PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', PORT))

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

  print('Waiting for public key and n from client...')
  rsaParams = str(conn.recv(1024).decode()).split()
  client_e = int(rsaParams[0])
  client_n = int(rsaParams[1])

  print('Received public key and n from client!')
  print(f'e:{bcolors.OKGREEN} {client_e}{bcolors.ENDC}')
  print(f'client_n:{bcolors.OKGREEN} {client_n}{bcolors.ENDC}')
  
  print('Generating public key and n...')
  n, e, d = generateRsaKeys()
  print(f'Public key:{bcolors.OKGREEN} {e}{bcolors.ENDC}')
  print(f'Private key:{bcolors.OKGREEN} {d}{bcolors.ENDC}')
  print(f'n:{bcolors.OKGREEN} {n}{bcolors.ENDC}')

  print('Sending public key and n to client...')
  data = str(e) + ' ' + str(n)
  conn.send(data.encode())

  print('Generating p, g, A...')
  p, g, a, A = generatePGaA()

  print('Encrypting p, g, A with client\'s public key...')
  encryptedP = encryptWithRSA(p, client_e, client_n)
  encryptedG = encryptWithRSA(g, client_e, client_n)
  encyptedA = encryptWithRSA(A, client_e, client_n)

  # generate signature using RSA for authentication
  signature = hashForAuth(encryptedP)
  print(f'encryptedP: {bcolors.FAIL}{encryptedP}{bcolors.ENDC}')
  print(f'Hashed signature: {bcolors.FAIL}{signature}{bcolors.ENDC}')
  signature = decryptWithRSA(signature, d, n)

  # send signature, p, g, A to client
  data = str(signature) + ' ' + str(encryptedP) + ' ' + str(encryptedG) + ' ' + str(encyptedA)
  conn.send(data.encode())

  print('Waiting for B from client...')
  data = conn.recv(1024).decode().split()
  signature = int(data[0])
  encryptedB = int(data[1])

  # verify signature
  signature = encryptWithRSA(signature, client_e, client_n)
  if signature != hashForAuth(encryptedB):
    print(f'{bcolors.FAIL}Client authentication failed!{bcolors.ENDC}')
    conn.close()
    continue
  else:
    print(f'{bcolors.OKGREEN}Client authentication successful!{bcolors.ENDC}')

  B = decryptWithRSA(encryptedB, d, n)
  print('Received B:', B)

  print('Generating key...')
  key = powmod(B, a, p)
  print('Generated key:', key)
  print('Waiting for data from client...')

  received = conn.recv(1024)
  received = aesDecrypt(received.decode(), key)
  print(f'Received data:{bcolors.OKBLUE} {received}{bcolors.ENDC}')

  data = input(
      f'{bcolors.BOLD}{bcolors.OKCYAN}Write something to send to client: {bcolors.ENDC}')
  data = aesEncrypt(data, key)
  data = conn.send(data.encode())
  print(f'{bcolors.OKGREEN}Data sent successfully!{bcolors.ENDC}')

  conn.close()