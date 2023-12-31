import time
from primeutils import generatePrime
from diffiehellman import *
from bcolors import bcolors
import tabulate

def computationTime(k: int):
  timeForP = time.time()
  generatePrimeAndFactors(k)
  timeForP = time.time() - timeForP

  timeForG = time.time()
  generator(p, factors, 2, p - 1)
  timeForG = time.time() - timeForG

  timeFora = time.time()
  generatePrime(k // 2)
  timeFora = time.time() - timeFora

  timeForA = time.time()
  powmod(g, a, p)
  timeForA = time.time() - timeForA

  timeForKey = time.time()
  powmod(A, a, p)
  timeForKey = time.time() - timeForKey

  return timeForP, timeForG, timeFora, timeForA, timeForKey

def generateComputationTimeAvg(k: int, i: int):
  """
  generates the average computation time for a given k and i
  
  args: k: number of bits of p
        i: number of iterations
  """
  timeForPAvg = 0
  timeForGAvg = 0
  timeForaAvg = 0
  timeForAAvg = 0
  timeForKeyAvg = 0

  for j in range(i):
    timeForP, timeForG, timeFora, timeForA, timeForKey = computationTime(k)

    timeForPAvg += timeForP
    timeForGAvg += timeForG
    timeForaAvg += timeFora
    timeForAAvg += timeForA
    timeForKeyAvg += timeForKey
  
  timeForPAvg /= i
  timeForGAvg /= i
  timeForaAvg /= i
  timeForAAvg /= i
  timeForKeyAvg /= i

  return [timeForPAvg, timeForGAvg, timeForaAvg, timeForAAvg, timeForKeyAvg]



# verify Diffie Hellman
print(f'{bcolors.BOLD}{bcolors.OKCYAN}Write the value of k in bits:{bcolors.ENDC}')
k = int(input())
p, factors = generatePrimeAndFactors(k)
g = generator(p, factors, 2, p-1)
a = generatePrime(k // 2)
b = generatePrime(k // 2)
A = powmod(g, a, p)
B = powmod(g, b, p)
A_b = powmod(A, b, p)
B_a = powmod(B, a, p)

print(f'Generated p: {bcolors.OKGREEN}{p}{bcolors.ENDC}')
print(f'Generated g: {bcolors.OKGREEN}{g}{bcolors.ENDC}')
print(f'Generated a: {bcolors.OKGREEN}{a}{bcolors.ENDC}')
print(f'Generated b: {bcolors.OKGREEN}{b}{bcolors.ENDC}')
print(f'Generated A: {bcolors.OKGREEN}{A}{bcolors.ENDC}')
print(f'Generated B: {bcolors.OKGREEN}{B}{bcolors.ENDC}')
print()
print(f'A^b: {bcolors.OKGREEN}{A_b}{bcolors.ENDC}')
print(f'B^a: {bcolors.OKGREEN}{B_a}{bcolors.ENDC}')

print()

if A_b == B_a:
  print(f'{bcolors.OKGREEN}{bcolors.BOLD}A^b and B^a are equal{bcolors.ENDC}')
else:
  print(f'{bcolors.WARNING}{bcolors.BOLD}A^b and B^a are not equal{bcolors.ENDC}')


# generate report in tabular form
print('Generating execution times\n')

print(f'{bcolors.BOLD}{bcolors.OKCYAN}\t\t\tComputation Times{bcolors.ENDC}')

output = []
for k in [128, 192, 256]:
  out = generateComputationTimeAvg(k, 5)
  out.insert(0, k)
  output.append(out)

print(tabulate.tabulate(output, headers=['k', 'P', 'g', 'a', 'A', 'Shared Key'], tablefmt='psql'))