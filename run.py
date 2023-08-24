import os
f = open("file.txt","r")
lines = f.readlines()
for each in lines:
 os.system("du -h %s" %each)
