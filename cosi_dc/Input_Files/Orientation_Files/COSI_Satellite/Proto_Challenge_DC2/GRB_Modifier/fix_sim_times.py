# Imports:
import os

# Inputs:
this_file = "GRB_511.inc1.id1.sim"
time_constant = 1835478000.0
new_file = "fixed_" + this_file

# Open new file for writing:
g = open(new_file,"w")

# Read through sim file and fix times:
f = open(this_file,"r")

i = 0
j = 0
while True:
    
    this_line = f.readline().strip()
    
    i += 1
    
    if len(this_line) == 0:
        g.write(this_line+"\n")

    if this_line:
             
        if this_line.split()[0] != "TI":
            g.write(this_line+"\n")

        if this_line.split()[0] == "TI":
            new_time = str(float(this_line.split()[1]) + time_constant)
            g.write("TI %s\n" %new_time)

    if not this_line:
        if i > 100:
            j += 1
            if j > 1:
                break

g.close()
os.system("gzip %s" %new_file)
