from AES128 import *

if __name__ == "__main__":
  key = "BUET CSE18 Batch"
  # logger.setIsLogging(False)
  encryptionTime = time.time()
  cipherText = aesEncrypt("Can They Do This", key)
  encryptionTime = time.time() - encryptionTime

  decryptionTime = time.time()
  aesDecrypt(cipherText, key)
  decryptionTime = time.time() - decryptionTime

  print("Key Scheduling Time: " + str(keySchedulingTime) + " seconds")
  print("Encryption Time: " + str(encryptionTime) + " seconds")
  print("Decryption Time: " + str(decryptionTime) + " seconds")

