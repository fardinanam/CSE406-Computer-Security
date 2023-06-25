from AES128 import *

if __name__ == "__main__":
  key = "BUET CSE18 Batch"

  encryptionTime = time.time()
  cipherText = aesEncrypt("Can They Do This", key)
  encryptionTime = time.time() - encryptionTime

  decryptionTime = time.time()
  aesDecrypt(cipherText, key)
  decryptionTime = time.time() - decryptionTime

  logger.log("Key Scheduling Time: " + str(keySchedulingTime) + " seconds")
  logger.log("Encryption Time: " + str(encryptionTime) + " seconds")
  logger.log("Decryption Time: " + str(decryptionTime) + " seconds")

