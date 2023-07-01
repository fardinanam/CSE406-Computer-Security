from rsa import *
from bcolors import bcolors

n, e, d = generateRsaKeys()

print(f"Public key: {bcolors.OKGREEN}{e}{bcolors.ENDC}")
print(f"Private key: {bcolors.OKGREEN}{d}{bcolors.ENDC}")
print(f"n: {bcolors.OKGREEN}{n}{bcolors.ENDC}")

plaintext = int(input("Enter the an integer: "))
ciphertext = encryptWithRSA(plaintext, e, n)

print(f"Ciphertext: {bcolors.OKGREEN} {ciphertext}{bcolors.ENDC}")
plaintext = decryptWithRSA(ciphertext, d, n)
print(f"Plaintext: {bcolors.OKGREEN} {plaintext}{bcolors.ENDC}")