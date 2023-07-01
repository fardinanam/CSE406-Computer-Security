from AES128 import *
from bcolors import bcolors

logger.setIsLogging(True)

key = input(f'{bcolors.BOLD}{bcolors.OKCYAN}Write the key: {bcolors.ENDC}')

plaintext = input(
      f'{bcolors.BOLD}{bcolors.OKCYAN}Write the plaintext: {bcolors.ENDC}')

encryptionTime = time.time()
cipherText = aesEncrypt(plaintext, key)
encryptionTime = time.time() - encryptionTime

decryptionTime = time.time()
aesDecrypt(cipherText, key)
decryptionTime = time.time() - decryptionTime

print(f"Key Scheduling Time: {bcolors.OKGREEN}" +
      str(keySchedulingTime) + f"{bcolors.ENDC} seconds")
print(f"Encryption Time: {bcolors.OKGREEN}" +
      str(encryptionTime) + f"{bcolors.ENDC} seconds")
print(f"Decryption Time: {bcolors.OKGREEN}" +
      str(decryptionTime) + f"{bcolors.ENDC} seconds")
