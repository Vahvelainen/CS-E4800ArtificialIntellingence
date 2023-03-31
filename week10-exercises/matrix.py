import numpy

M = [
    [ 0, 1, 0 ],
    [ 0, 0, 1 ],
    [ 0.2, 0.8, 0 ],
]

print( numpy.matmul(M, M) )

B = [ 0.1, 0.2, 0.7 ]

print( numpy.matmul(B, M) )


ports = ( 0.05, 0.8, 0.15 )
temps = ( 0.01, 0.00001, 0.02 )

p15c = temps[0] + \
      temps[0] * temps[1] + \
      temps[0] * temps[1] * temps[2] + \
                 temps[1] * temps[2] + \
                            temps[2] + \
                 temps[1] + \
      temps[0]*temps[2]

print(p15c)
p15c = sum(temps)
print(p15c)

props = []

for i, _ in enumerate(ports):
  props.append( ports[i] * temps[i] / p15c )

print(props)

