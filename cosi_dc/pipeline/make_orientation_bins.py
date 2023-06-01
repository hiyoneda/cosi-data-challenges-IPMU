# Imports:
import os

def make_bins(num_bins,orientation_file):

    # Upload main orientation file:
    f = open(orientation_file,"r")
    lines = f.readlines()
    f.close()

    # Make orientation bin directory:
    if os.path.isdir("Orientation_Bins") == False:
        os.system("mkdir Orientation_Bins")

    # Determine number of lines per file:
    num_lines_tot = len(lines) - 1
    num_lines_bin = num_lines_tot/num_bins
    num_lines_bin = int(num_lines_bin) #rounds down to nearest integer
    
    # Need to include one additional file if num_lines_bin is not integer:
    remainder = num_lines_tot % num_bins
    is_divisible = remainder == 0

    # Make orientation files:
    for k in range(0,num_bins):
        this_file = "Orientation_Bins/bin_%s.ori" %str(k)
        g = open(this_file,"w")
        g.write(lines[0])
    
        low = num_lines_bin*k+1
        high = low + num_lines_bin
    
        for i in range(low,high+1):
            g.write(lines[i])

        g.close()

    # Write last orientation file if num_lines_bin is not integer:
    # Note: function returns 0 or 1 depending if an extra file is needed.
    extra = 0 
    if is_divisible == False:
        this_file = "Orientation_Bins/bin_%s.ori" %str(num_bins)
        g = open(this_file,"w")
        g.write(lines[0])

        for i in range(high,num_lines_tot+1):
            g.write(lines[i])
        g.close()

        extra = 1
    
    return extra
