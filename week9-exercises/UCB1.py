import math

# 9.4.4 Exercise games-ucb1

# Consider the UCB1 formula, which has turned out to be useful in both reinforcement learning and in Monte Carlo methods for computer game playing.
# We have observed the following state sequences.

sequences = [
    [3,3,3,2,2,2,2,1,1,1],
    [3,3,2,2],
    [4]
  ]

# The sequence with the highest value obtained with the UCB1 formula will be played next.
# What are the values for these three sequences given by the UCB1 formula?
# Give the values of these sequences as a comma-separate list (no white spaces) of three rounded decimal numbers of the form X.YZ (two digits after the decimal point.)

def UCB1(sequences):
  N = sum( len(seq) for seq in sequences) #the number of round
  UCB1_Values = []
  for seq in sequences:
    Nt_a = len(seq) #number of times the option is chosen
    Qt_a = sum(seq) / Nt_a #the average return of the option
    ucb1_val = Qt_a + math.sqrt( (2 * math.log(N)) / Nt_a )
    UCB1_Values.append(ucb1_val) 
  return UCB1_Values

print(UCB1(sequences)) #2.74,3.66,6.33