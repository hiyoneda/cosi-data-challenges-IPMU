# Purpose: scale the Ling BG components.

input_file = "ling_continuum_33.500_km_00.cosimadat"
scaling_factor = 0.41 
output_file = "scaled_0p41_" + input_file

# Open new file for writing 
g = open(output_file,"w")

with open(input_file) as f:
    
    for line in f:
        
        split = line.split()
     
        if len(split) == 0:
            g.write(line)
         
        elif split[0] != "AP":
            g.write(line)

        elif split[0] == "AP":

            new_flux = scaling_factor * float(split[4])
            new_line = split[0] + " " + split[1] + " " + split[2] + " " + split[3] + " " +  str(new_flux) + "\n"
            g.write(new_line)

g.close()
