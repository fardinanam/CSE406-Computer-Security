from AES128 import *
from bcolors import bcolors

logger.setIsLogging(True)

print(f'{bcolors.BOLD}{bcolors.OKCYAN}Write the key...{bcolors.ENDC}')
key = input()

print(f'{bcolors.BOLD}{bcolors.OKCYAN}Write the plaintext...{bcolors.ENDC}')
plaintext = input()

encryptionTime = time.time()
cipherText = aesEncrypt(plaintext, key)
encryptionTime = time.time() - encryptionTime

decryptionTime = time.time()
aesDecrypt(cipherText, key)
decryptionTime = time.time() - decryptionTime

print(f"{bcolors.OKGREEN}Key Scheduling Time:{bcolors.ENDC} " + str(keySchedulingTime) + " seconds")
print(f"{bcolors.OKGREEN}Encryption Time:{bcolors.ENDC} " +
      str(encryptionTime) + " seconds")
print(f"{bcolors.OKGREEN}Decryption Time:{bcolors.ENDC} " + str(decryptionTime) + " seconds")
