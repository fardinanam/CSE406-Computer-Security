from primeutils import *

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