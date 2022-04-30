import sys

myfile = open("test.txt", "r")
while myfile:
    line  = myfile.readline()
    print(line)
    if line == "":
        break
myfile.close() 
