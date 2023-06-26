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
    bits: The number of bits the prime number should be.
  """
  while True:
    n = random.getrandbits(bits)
    if millerRabinPrimalityTest(n, 2):
      return n


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



def generator(p, minimum, maximum):
  fact = []
  phi = p - 1
  n = phi

  i = 2
  while i * i <= n:
    if n % i == 0:
      fact.append(i)
      while n % i == 0:
        n //= i
    i += 1

  if n > 1:
    fact.append(n)

  for res in range(minimum, maximum + 1):
    ok = True
    for i in range(len(fact)):
      ok &= powmod(res, phi // fact[i], p) != 1
    if ok:
      return res

  return -1


p = generatePrime(128)
print("Generated prime:", p)
g = generator(p, 2, p-1)
print("Generator:", g)