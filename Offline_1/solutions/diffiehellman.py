from math import sqrt
import random

def millerRabinPrimalityTest(n, a = 2):
  """
  Uses the Miller-Robin Primality Test to check if a number is prime.
  
  args:
    n: The number to check for primality.
    a: The base to use for the test.
  """
  # factor out powers of 2 from n-1
  m = n - 1
  k = 0
  while m % 2 == 0:
    m >>= 1
    k += 1

  t = pow(a, m, n)

  if t == 1 or t == -1:
    return True
  
  for i in range(k - 1):
    t = pow(t, 2, n)
    if t == 1:
      return False
    if t == -1:
      return True
  
  return False

def generatePrime(bits):
  """
  Generates a prime number which is atleast as large as the given number of bits.
  
  args:
    bits: The number of bits of the prime number.
  """
  while True:
    n = random.getrandbits(bits)
    if millerRabinPrimalityTest(n, 2):
      return n
    
def generatePrimeAndFactors(bits: int) -> list:
  """
  Generates a prime number which is atleast as large as the given number of bits.

  returns: [prime, [factors]] A prime number and its factors.
  """
  factor = generatePrime(bits - 1)

  while True:
    prime = (factor << 1) + 1
    if millerRabinPrimalityTest(prime, 2):
      return prime, [2, factor]
    factor = generatePrime(bits - 1)


def powmod(a, b, p):
  res = 1
  while b:
    if b & 1:
      res = int(res * a % p)
      b -= 1
    else:
      a = int(a * a % p)
      b >>= 1
  return res



def generator(p, factors, minimum, maximum):
  phi = p - 1

  for res in range(minimum, maximum + 1):
    ok = True
    for i in range(len(factors)):
      ok &= powmod(res, phi // factors[i], p) != 1
    if ok:
      return res

  return -1