import random
import math

def randomPoint(scale=1000):
  #(x, y)
  x = random.randint(0, scale)
  y = random.randint(0, scale)
  return (x, y)

def M(x1, y1, x2, y2):
  return abs(x1 - x2) + abs(y1 - y2)

def E(x1, y1, x2, y2):
  return  math.sqrt( abs(x1 - x2)**2 + abs(y1 - y2)**2 )

#manhattan is bigger than euclidean

bigger = 0
same = 0
smaller = 0
for i in range(0, 10000):
  x1 = random.randint(0, 1000)
  y1 = random.randint(0, 1000)
  x2 = random.randint(0, 1000)
  y2 = random.randint(0, 1000)

  m = M(x1, y1, x2, y2)
  e = E(x1, y1, x2, y2)

  if (m == e):
    same += 1

  if (m > e):
    bigger += 1

  if (m < e):
    smaller += 1

print('MANHATTAN VS EUCLIDEAN')
print('Bigger:' + str(bigger))
print('Same:' + str(same))
print('Smaller:' + str(smaller))


#Manhattan * square root of 2 

bigger = 0
same = 0
smaller = 0
for i in range(0, 10000):
  x1 = random.randint(0, 1000)
  y1 = random.randint(0, 1000)
  x2 = random.randint(0, 1000)
  y2 = random.randint(0, 1000)

  m = M(x1, y1, x2, y2) * math.sqrt(2)
  e = E(x1, y1, x2, y2)

  if (m == e):
    same += 1

  if (m > e):
    bigger += 1

  if (m < e):
    smaller += 1

print('MANHATTAN * sqrt(2) VS EUCLIDEAN')
print('Bigger:' + str(bigger))
print('Same:' + str(same))
print('Smaller:' + str(smaller))


#Manhattan / square root of 2 

bigger = 0
same = 0
smaller = 0
for i in range(0, 10000):
  x1 = random.randint(0, 1000)
  y1 = random.randint(0, 1000)
  x2 = random.randint(0, 1000)
  y2 = random.randint(0, 1000)

  m = M(x1, y1, x2, y2) / math.sqrt(2)
  e = E(x1, y1, x2, y2)

  if (m == e):
    same += 1

  if (m > e):
    bigger += 1

  if (m < e):
    smaller += 1

print('MANHATTAN / sqrt(2) VS EUCLIDEAN')
print('Bigger:' + str(bigger))
print('Same:' + str(same))
print('Smaller:' + str(smaller))