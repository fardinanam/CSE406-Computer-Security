import numpy as np
import sbox as sb

KEY_SIZE = 128
WORD_ARRAY_SIZE = 4
WORD_SIZE = int(KEY_SIZE / WORD_ARRAY_SIZE)

def stringToHex(string: str) -> list:
  """
  Converts a string to a list of hex values
  """
  return [hex(ord(c)) for c in string]

def keyToMatrix(key: list) -> list:
  """
  Converts a list of hex values to a 4x4 matrix
  """
  return np.matrix(np.reshape(key, (WORD_ARRAY_SIZE, int(KEY_SIZE / WORD_SIZE)))).tolist()

def g(key: list) -> list:
  """
  Performs the g() operation on a key
  1. Rotates the key by 1 byte
  2. Applies the sbox to each byte
  3. Add the round constant (XOR)
  """
  key = np.concatenate((key[1:], key[:1]))
  key = [hex(sb.Sbox[int(x, 16)]) for x in key]
  key[0] = hex(int(key[0], 16) ^ 0x01)

  return key

def xor(key1, key2):
  """
  XORs two keys
  """
  key = []
  key1 = np.matrix(key1).tolist()[0]
  key2 = np.matrix(key2).tolist()[0]
  
  print("in xor:", key1, key2)
  for i in range(WORD_ARRAY_SIZE):
    print(key1[i], type(key1[i]), key2[i], type(key2[i]))
    key.append(hex(int(key1[i], 16) ^ int(key2[i], 16)))
    
  return key

def nextRoundKey(key: list) -> list:
  """
  Generates the next round's key from the previous round's key
  """
  # print("init key:", key, type(key))
  # print("xor", xor(key[0], g(key[3])))
  # key = np.array(key)
  w = [xor(key[0], g(key[WORD_ARRAY_SIZE - 1]))]
  
  print("w:", w)
  for i in range(1, WORD_ARRAY_SIZE):
    # print("in for loop: ", i)
    # print(f"w[{i-1}]:", w[i-1], type(w[i-1]))
    # print(f"key[{i}]:", key[i], type(key[i]))
    
    newKey = xor(w[i - 1], key[i])
    # print("newKey:", newKey, type(newKey))
    
    w.append(newKey)
    # np.append(w, xor(w[i - 1], key[i]))
    
  return w

string = "Thats my Kung Fu"
w = keyToMatrix(stringToHex(string))

print("Round 0 Key:", w)
print("Round 1 Key:", nextRoundKey(w))
print("Round 2 Key:", nextRoundKey(nextRoundKey(w)))

