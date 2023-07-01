from primeutils import *
import random
import math

def extendedEuclidean(a: int, b: int) -> tuple:
  """
  Calculates the Bezout's coefficients of a and b.

  returns: (s, t, r) such that s * a + t * b = r = gcd(a, b)
  """
  s = 0
  r = b
  old_s = 1
  old_r = a

  while r != 0:
    quotient = old_r // r
    old_r, r = r, old_r - quotient * r
    old_s, s = s, old_s - quotient * s
  
  if b != 0:
    bezout_t = (old_r - old_s * a) // b
  else:
    bezout_t = 0
  
  return old_s, bezout_t, old_r

def generateRsaKeys():
  """
  Generates public, private keys and n of RSA

  returns: e: public key, d: private key, n: n of RSA
  """
  # generate two large primes p and q
  p = generatePrime()
  q = generatePrime()
  #  calculate n = P * Q
  n = p * q

  # calculate carmichael's totient function lambda(n)
  lambda_n = math.lcm(p - 1, q - 1)

  # calculate e such that 2 < e < lambda(n) and gcd(e, lambda(n)) = 1
  e = random.getrandbits(16)

  while True:
    if math.gcd(e, lambda_n) == 1:
      break

    e = random.getrandbits(16)

  # calculate d such that d * e congruent to 1 (mod lambda(n))
  d, t, r = extendedEuclidean(e, lambda_n)

  return n, e, d

def encryptWithRSA(plaintext: int, e: int, n: int) -> int:
  """
  Encrypts a plaintext using RSA

  args:
    plaintext: The plaintext to encrypt
    e: The public key
    n: n of RSA

  returns: The ciphertext
  """
  return pow(plaintext, e, n)

def decryptWithRSA(ciphertext: int, d: int, n: int) -> int:
  """
  Decrypts a ciphertext using RSA

  args:
    ciphertext: The ciphertext to decrypt
    d: The private key
    n: n of RSA

  returns: The plaintext
  """
  return pow(ciphertext, d, n)