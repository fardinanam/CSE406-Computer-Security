import numpy as np
import time
import sbox as sb
from consts import *
from logger import Logger
from bcolors import bcolors

BLOCK_SIZE_BITS = 128
BLOCK_SIZE_BYTES = BLOCK_SIZE_BITS // 8
WORD_SIZE = 4
WORD_ARRAY_SIZE = BLOCK_SIZE_BYTES // WORD_SIZE
COLUMN_SIZE = BLOCK_SIZE_BYTES // WORD_ARRAY_SIZE

logger = Logger(False)

keySchedulingTime = 0
encryptionTime = 0
decryptionTime = 0

def stringToHex(string: str) -> list:
  """
  Converts a string to a list of hex values
  """
  return [hex(ord(c)) for c in string]


def textToMatrix(text: str) -> list:
  """
  Converts a string to a 4x4 matrix of Hex values
  """
  key = stringToHex(text)
  return np.matrix(np.reshape(key, (WORD_ARRAY_SIZE, COLUMN_SIZE))).tolist()

def roundConst(round: int) -> int:
  """
  Returns the round constant for the given round
  """
  if round == 1:
    return 0x01
  prevRoundConst = roundConst(round - 1)
  return (prevRoundConst << 1) ^ (0x11b & -(prevRoundConst >> 7))


def g(key: list, round: int) -> list:
  """
  Performs the g() operation on a key
  1. Rotates the key by 1 byte
  2. Applies the sbox to each byte
  3. Add the round constant (XOR)
  """
  key = np.concatenate((key[1:], key[:1]))
  key = [hex(sb.Sbox[int(x, 16)]) for x in key]
  key[0] = hex(int(key[0], 16) ^ roundConst(round))

  return key


def xor(array1: list, array2: list) -> list:
  """
  XORs two matrices
  args: array1, array2 - 1D arrays of hex values
  """
  key = []

  for i in range(WORD_ARRAY_SIZE):
    key.append(hex(int(array1[i], 16) ^ int(array2[i], 16)))

  return key


def roundKey(round: int, prevkey: list) -> list:
  """
  Generates the next round's key from the previous round's key
  """
  w = [xor(prevkey[0], g(prevkey[3], round))]

  for i in range(1, WORD_ARRAY_SIZE):
    newKey = xor(w[i - 1], prevkey[i])
    w.append(newKey)

  return w


def convertToBlockSize(text: str) -> str:
  """
  Converts the given key to 128 bits
  """
  if len(text) > BLOCK_SIZE_BYTES:
    return text[:BLOCK_SIZE_BYTES]
  elif len(text) < BLOCK_SIZE_BYTES:
    return text + "0" * (BLOCK_SIZE_BYTES - len(text))

  return text


def createAllKeys(text: str) -> list:
  """
  Generates all round keys from the initial key
  """
  text = convertToBlockSize(text)
  keys = [textToMatrix(text)]
  for i in range(10):
    keys.append(roundKey(i+1, keys[i]))
  return keys


def stateMatrix(text: str) -> list:
  """
  Converts the given text to a 4x4 matrix in column major order
  args: text: str - the text to convert. It is assumed that the text is 128 bits. 
    If the text is less than 128 bits, it is padded with 0s. If it is greater than 128 bits,
    it is truncated to 128 bits.
  """
  text = convertToBlockSize(text)
  matrix = textToMatrix(text)

  return np.array(matrix).T.tolist()


def invStateMatrix(cipherText: str) -> list:
  """
  Converts the given cipher text to a 4x4 matrix in column major order
  args: text: str - the text to convert. It is assumed that the text is 128 bits. 
    If the text is less than 128 bits, it is padded with 0s. If it is greater than 128 bits,
    it is truncated to 128 bits.
  """
  if len(cipherText) % 2 != 0:
    raise Exception("Invalid cipher text. Cipher text must be of even length.")

  matrix = list(cipherText[i:i+2] for i in range(0, len(cipherText), 2))

  return np.reshape(matrix, (WORD_ARRAY_SIZE, COLUMN_SIZE)).T.tolist()


def addRoundKey(stateMatrix: list, roundKey: list) -> list:
  """
  Adds the round key to the state matrix
  
  args: stateMatrix: list - the state matrix (assumed to be in column major order)
        roundKey: list - the round key (assumed to be in row major order)
  """
  roundKey = np.array(roundKey).T.tolist()
  newStateMatrix = []

  for i in range(WORD_ARRAY_SIZE):
    newStateMatrix.append(xor(stateMatrix[i], roundKey[i]))

  return newStateMatrix


def subBytes(stateMatrix: list) -> list:
  """
  Applies the sbox to each byte in the state matrix
  """
  newStateMatrix = []

  for i in range(WORD_ARRAY_SIZE):
    newStateMatrix.append([hex(sb.Sbox[int(x, 16)]) for x in stateMatrix[i]])

  return newStateMatrix


def invSubBytes(stateMatrix: list) -> list:
  """
  Applies the inverse sbox to each byte in the state matrix
  """
  newStateMatrix = []

  for i in range(WORD_ARRAY_SIZE):
    newStateMatrix.append([hex(sb.InvSbox[int(x, 16)])
                          for x in stateMatrix[i]])

  return newStateMatrix


def shiftRow(stateMat: list):
  """
  Round Shifts the rows of the state matrix to the left by the row number
  """
  newStateMatrix = []
  for i in range(WORD_ARRAY_SIZE):
    newStateMatrix.append(np.roll(stateMat[i], -i))

  return newStateMatrix


def invShiftRow(stateMat: list):
  """
  Round Shifts the rows of the state matrix to the right by the row number
  """
  newStateMatrix = []
  for i in range(WORD_ARRAY_SIZE):
    newStateMatrix.append(np.roll(stateMat[i], i))

  return newStateMatrix


def mixColumn(stateMat: list) -> list:
  """
  Mixes the columns of the state matrix with a fixed matrix
  """
  stateMat = np.array(stateMat).T
  newStateMatrix = []

  for i in range(WORD_ARRAY_SIZE):
    row = []
    for j in range(COLUMN_SIZE):
      dotProd = 0

      for k in range(WORD_ARRAY_SIZE):
        bv1 = Mixer[i][k]
        bv2 = BitVector(intVal=int(stateMat[j][k], 16))

        dotProd ^= (bv1.gf_multiply_modular(bv2, AES_modulus, 8)).int_val()

      row.append(hex(dotProd))

    newStateMatrix.append(row)

  return newStateMatrix


def invMixColumn(stateMat: list) -> list:
  """
  Mixes the columns of the state matrix with a fixed matrix
  """
  stateMat = np.array(stateMat).T
  newStateMatrix = []

  for i in range(WORD_ARRAY_SIZE):
    row = []
    for j in range(COLUMN_SIZE):
      dotProd = 0

      for k in range(WORD_ARRAY_SIZE):
        bv1 = InvMixer[i][k]
        bv2 = BitVector(intVal=int(stateMat[j][k], 16))

        dotProd ^= (bv1.gf_multiply_modular(bv2, AES_modulus, 8)).int_val()

      row.append(hex(dotProd))

    newStateMatrix.append(row)

  return newStateMatrix


def pad(text: str) -> str:
  """
  Pads the text to be a multiple of block size with the number of bytes added
  """
  padLength = BLOCK_SIZE_BYTES - len(text) % BLOCK_SIZE_BYTES

  if padLength == 0 or padLength == BLOCK_SIZE_BYTES:
    return text

  return text + chr(padLength) * padLength


def unpad(text: str) -> str:
  """
  Removes the padding from the text
  """
  padLength = ord(text[-1])
  paddedText = text[-padLength:]

  if padLength == 0 or padLength > BLOCK_SIZE_BYTES or paddedText != chr(padLength) * padLength:
    return text

  return text[:-padLength]


def aesEncryptOneBlock(plainText: str, keys: list) -> str:
  """
  Performs the AES cipher on the given text with the given keys. The provided plain text and key texts are assumed to be 128 bits of hex values.

  args: plainText: str - the text to encrypt
        keys: list - the list containing the round keys
  
  returns: cipherText: str - the encrypted text

  raises: ValueError - if the plain text is not equal to block size
  """

  if len(plainText) != BLOCK_SIZE_BYTES:
    raise ValueError(f"The plain text must be {BLOCK_SIZE_BYTES} bytes")

  stateMat = stateMatrix(plainText)
  stateMat = addRoundKey(stateMat, keys[0])

  for i in range(1, 10):
    stateMat = subBytes(stateMat)
    stateMat = shiftRow(stateMat)
    stateMat = mixColumn(stateMat)
    stateMat = addRoundKey(stateMat, keys[i])

  stateMat = subBytes(stateMat)
  stateMat = shiftRow(stateMat)
  stateMat = addRoundKey(stateMat, keys[10])

  #  Convert the matrix to a string of hex values without the 0x prefix
  cipherText = ""

  for i in range(WORD_ARRAY_SIZE):
    for j in range(COLUMN_SIZE):
      extractedHex = stateMat[j][i]

      if extractedHex.startswith("0x"):
        extractedHex = extractedHex[2:]

      if len(extractedHex) == 1:
        extractedHex = "0" + extractedHex

      cipherText += extractedHex

  return cipherText


def aesEncrypt(plainText: str, keyText: str) -> str:
  """
  Performs the AES cipher on the given text with the given key

  args: plainText: str - the text to encrypt
        keyText: str - the key to use for encryption

  returns: cipherText: str - the encrypted text
  """
  # convert plain text and key text to strings to be safe
  plainText = str(plainText)
  keyText = str(keyText)

  logger.log(f"{bcolors.OKCYAN}Plain Text: {bcolors.ENDC}")
  logger.log(f"In ASCII: {bcolors.OKGREEN}" + plainText + f"{bcolors.ENDC}")
  logger.log(f"In Hex: {bcolors.OKGREEN}" + plainText.encode("utf-8").hex() + f"{bcolors.ENDC}")
  logger.log("")

  logger.log(f"{bcolors.OKCYAN}Key: {bcolors.ENDC}")
  logger.log(f"In ASCII: {bcolors.OKGREEN}" + keyText + f"{bcolors.ENDC}")
  logger.log(f"In Hex: {bcolors.OKGREEN}" + keyText.encode("utf-8").hex() + f"{bcolors.ENDC}")
  logger.log("")

  plainText = pad(plainText)

  keySchedulingTime = time.time()
  keys = createAllKeys(keyText)
  keySchedulingTime = time.time() - keySchedulingTime

  cipherText = ""
  for i in range(0, len(plainText), BLOCK_SIZE_BYTES):
    cipherText += aesEncryptOneBlock(plainText[i:i + BLOCK_SIZE_BYTES], keys)

  logger.log(f"{bcolors.OKCYAN}Cipher Text: {bcolors.ENDC}")
  logger.log(f"In Hex: {bcolors.OKGREEN}" + cipherText + f"{bcolors.ENDC}")
  logger.log(f"In ASCII: {bcolors.OKGREEN}" + 
        BitVector(hexstring=cipherText).get_bitvector_in_ascii() + f"{bcolors.ENDC}")
  logger.log("")

  return cipherText


def aesDecryptOneBlock(cipherText: str, keys: list) -> str:
  """
  Performs the AES cipher on the given text with the given keys. The provided cipher text is assumed to be 128 bits of hex values.

  args: cipherText: str - the text to decrypt
        keys: list - the list containing the round keys
  
  returns: plainText: str - the decrypted text
  """

  if len(cipherText) != BLOCK_SIZE_BYTES * 2:
    raise ValueError(f"The cipher text must be {BLOCK_SIZE_BYTES * 2} bytes")

  stateMat = invStateMatrix(cipherText)
  stateMat = addRoundKey(stateMat, keys[10])

  for i in range(9, 0, -1):
    stateMat = invShiftRow(stateMat)
    stateMat = invSubBytes(stateMat)
    stateMat = addRoundKey(stateMat, keys[i])
    stateMat = invMixColumn(stateMat)

  stateMat = invShiftRow(stateMat)
  stateMat = invSubBytes(stateMat)
  stateMat = addRoundKey(stateMat, keys[0])

  #  Convert the matrix to a string of hex values without the 0x prefix
  hexValue = ""
  for i in range(WORD_ARRAY_SIZE):
    for j in range(COLUMN_SIZE):
      elemHexValue = stateMat[j][i][2:]
      if len(elemHexValue) == 1:
        elemHexValue = "0" + elemHexValue
      hexValue += elemHexValue

  #  Convert the hex value to ascii
  plainText = bytearray.fromhex(hexValue).decode()

  return plainText


def aesDecrypt(cipherText: str, keyText: str) -> str:
  """
  Performs the AES cipher on the given text with the given key

  args: cipherText: str - the text to decrypt
        keyText: str - the key to use for decryption

  returns: plainText: str - the decrypted text
  """
  # convert plain text and key text to strings to be safe
  cipherText = str(cipherText)
  keyText = str(keyText)
  
  cipherTextBlockSize = BLOCK_SIZE_BYTES * 2
  keys = createAllKeys(keyText)

  plainText = ""
  for i in range(0, len(cipherText), cipherTextBlockSize):
    plainText += aesDecryptOneBlock(
        cipherText[i:i + cipherTextBlockSize], keys)

  plainText = unpad(plainText)

  logger.log(f"{bcolors.OKCYAN}Decrypted Text: {bcolors.ENDC}")
  logger.log(f"In Hex: {bcolors.OKGREEN}" + plainText.encode("utf-8").hex() + f"{bcolors.ENDC}")
  logger.log(f"In ASCII: {bcolors.OKGREEN}" + plainText + f"{bcolors.ENDC}")
  logger.log("")

  return plainText

