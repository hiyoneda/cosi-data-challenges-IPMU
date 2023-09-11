# Imports:
import os


def make_bins(num_bins,orientation_file,lightcurve,lightcurve_file):

    # Upload main orientation file:
    f = open(orientation_file,"r")
    lines = f.readlines()
    f.close()

    if lightcurve :
        # Upload main light curve file:
        f1 = open(lightcurve_file,"r")
        lines1 = f1.readlines()
        #remove fst and lst line
        lines1 = lines1[1:-1]
        f1.close()

    
    # Make orientation bin directory:
    if os.path.isdir("Orientation_Bins") == False:
        os.system("mkdir Orientation_Bins")

    # Determine number of lines per file:
    num_lines_tot = len(lines) - 2

    if lightcurve :
        num_lines_tot_LC = len(lines1) 
        assert num_lines_tot == num_lines_tot_LC, "The number of lines is not equal betwneen the ori and light curve file {0} vs {1}".format(num_lines_tot,num_lines_tot_LC) 
        assert lines[1].split(" ")[1] == lines1[0].split(" ")[1] and lines[-2].split(" ")[1] == lines1[-1].split(" ")[1], "Start/stop time are different between LC and ori file"
        assert float(lines[2].split(" ")[1]) - float(lines[1].split(" ")[1]) == float(lines1[1].split(" ")[1]) - float(lines1[0].split(" ")[1]), "Time binning is different between LC and ori file"
    
    num_lines_bin = num_lines_tot/num_bins
    num_lines_bin = int(num_lines_bin) #rounds down to nearest integer
    
    # Need to include one additional file if num_lines_bin is not integer:
    remainder = num_lines_tot % num_bins
    is_divisible = remainder == 0
    
    # Make sure remainder isn't too high:
    if remainder > num_lines_bin:
        print()
        print("###WARNING###")
        print("total lines in file: " + str(num_lines_tot))
        print("# of lines per time bin: " + str(num_lines_bin))
        print("# of remaining lines: " + str(remainder))
        print("Note: If the remainder is too large,")
        print("then try changing the total lines a little!")
        print()

    # Make orientation and light curve files:
    for k in range(0,num_bins):

        #orientation file
        this_file = "Orientation_Bins/bin_%s.ori" %str(k)
        g = open(this_file,"w")
        g.write(lines[0])

        if lightcurve :

            #light curve file
            this_file1 = "Orientation_Bins/bin_%s.dat" %str(k)
            g1 = open(this_file1,"w")
            g1.write("IP LinLin\n")
 
        low = num_lines_bin*k+1
        high = low + num_lines_bin
    
        for i in range(low,high+1):
            g.write(lines[i])
            
            if lightcurve :
                g1.write(lines1[i-1])

        g.write("EN\n")
        g.close()

        if lightcurve :
            g1.write("EN\n")
            g1.close()
        
    # Write last orientation file if num_lines_bin is not integer:
    # Note: function returns 0 or 1 depending if an extra file is needed.
    extra = 0 
    if is_divisible == False:
        
        #orientation
        this_file = "Orientation_Bins/bin_%s.ori" %str(num_bins)
        g = open(this_file,"w")
        g.write(lines[0])
    
        if lightcurve :
            #lightcurve
            this_file1 = "Orientation_Bins/bin_%s.dat" %str(num_bins)
            g1 = open(this_file1,"w")
            g1.write("IP LinLin\n")
        
        for i in range(high,num_lines_tot+1):
            g.write(lines[i])

            if lightcurve :
                g1.write(lines1[i-1])
        
        g.write("EN\n")        
        g.close()

        if lightcurve :
            g1.write("EN\n")
            g1.close()
        
        extra = 1
    
    return extra
