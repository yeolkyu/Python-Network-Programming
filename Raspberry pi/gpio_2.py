import RPi.GPIO as GP
import time

#setup GPIO pin numbering
GP.setmode(GP.BCM)
GP.setwarnings(False)
#LED = {'L1':18, 'L2':24, 'L3':25, 'L4':8}
LED = [18, 24, 25, 8]
#S1 = 23
PAT = [[1, 0, 0, 0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
for p in LED:
    GP.setup(p, GP.OUT) #setup as OUT

#GP.setup(S1, GP.IN) #setup GPIO23 as IN
i = 0
while True:
    for j in range(4):
        for p in LED:
            GP.output(p, PAT[j][i])
#            print(p, PAT[j][i])
            i += 1
            i = i % 4
        time.sleep(0.5)
