import serial
import time
port="/dev/rfcomm0" #setial comm port for SPP
print('hello world')
bluetooth= serial.Serial(port,9600)#Serial object
print ('hello world 2')
bluetooth.flushInput()#flush buffer
print ('hello world 3')
for i in range(100):
    print("we are in the for loop",i)
    bluetooth.write("a".encode()) #send "a"
    inputs=bluetooth.readline() #receive response
    print("we are in the inputs for loop",i)
    inputasinteger= int(inputs)
    if inputs:
            print('we have inputs')
            fileb= open("blue.txt",'wU') #open a file
            fileb.write(inputasInteger*10)#save the received msg into file
    time.sleep(.5)
    print('sleeping')
fileb.close() #close the file
print('file has been closse')
exit()