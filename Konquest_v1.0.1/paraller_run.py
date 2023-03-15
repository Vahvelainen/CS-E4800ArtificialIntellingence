import os
import time

#For apple only
import appscript

scriptPath = os.path.realpath(os.path.dirname(__file__))
wdir = os.getcwd()
filename = 'testresults.txt'

with open(filename) as file:
    lines = [line.rstrip() for line in file]
    if len(lines):
        if input('The result file is not empty. Continue? (Y/n)') != 'Y':
            exit()

# empty the file
open(filename, 'w').close()

N = 10 # Total amount
P = 2 # paraller threaths

def lauchThread():
    script = "python3 " + scriptPath + "/" + "test_thread.py " + wdir + "/" + filename
    # Windows
    # os.system('start cmd /c "%s"' % script)
    # Apple
    appscript.app('Terminal').do_script(script)


for _ in range(P):
    lauchThread()

launchedThreads = P
finishedThreads = 0
notFinished = True

while notFinished:
    lines = []
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    while("" in lines):
        lines.remove("")

    finished = len(lines)
    if len(lines) >= N:
        notFinished = False

    #thread is 2 runs 
    while finished - ( finishedThreads * 2 ) >= 2 and launchedThreads < N/2:
        finishedThreads += 1
        launchedThreads += 1
        lauchThread()
        print(str(finished) + " games finished")

    time.sleep(0.1)

player1wins = 0
lines = []
with open(filename) as file:
    lines = [line.rstrip() for line in file]
for line in lines:
    if bool(line):
        player1wins += 1

print('Player 1 won ' + str(player1wins) + ' times out of ' + str(N))