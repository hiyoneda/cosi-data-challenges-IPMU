# Imports:
import os,sys,shutil 
import yaml
import cosi_dc

class Setup:
        
    """Main inputs are specified in inputs.yaml file"""
    
    def __init__(self,input_yaml):

        # Get home directory:
        self.home = os.getcwd()
       
        # Get install directory:
        self.dc_dir = os.path.split(cosi_dc.__file__)[0]

        # Load main inputs from yaml file:
        with open(input_yaml,"r") as file:
            inputs = yaml.load(file,Loader=yaml.FullLoader)

        self.name = inputs["name"]
        self.src_list = inputs["src_list"]
        self.include_transmission_prob = inputs["include_transmission_prob"]
        self.transmission_prob_file = inputs["transmission_prob_file"]

    def setup_srcs(self):
    
        """Sets up source directory for simulation run."""

        # Verify that input sources are given as list:
        if isinstance(self.src_list,list) == False:
            raise TypeError("Input sources must be a list!")

        # Check that input sources are included in library:
        master_list_file = os.path.join(self.dc_dir, "Source_Library", "master_source_list.txt")
        f = open(master_list_file,"r")
        master_list = eval(f.read())
        for each in self.src_list:
            if each not in master_list:
                print()
                print("ERROR: Input source is not defined!")
                print()
                print("Sources must be selected from available list:")
                print(master_list)
                print()
                sys.exit()

        # Remove existing source dictionary:
        if os.path.isdir("Sources") == True:
            shutil.rmtree("Sources")

        # Make new source dictionary:
        os.system("mkdir Sources")
        os.chdir("Sources")
    
        # Known beam types:
        beam_list = ["FarFieldPointSource",\
                     "FarFieldNormalizedEnergyBeamFluxFunction",\
                     "FarFieldAssymetricGaussian",\
                     "FarFieldGaussian",\
                     "FarFieldIsotropic",\
                     "FarFieldFileZenithDependent"]

        # Copy source files:
        for each in self.src_list:
        
            # Initiate beam type:
            beam_type = "None"
       
            # Initiate source name:
            this_name = os.path.basename(each)
        
            # Exit if not using source from source library:
            if this_name == "other":
                f = open("README.txt","w")
                f.write("Using own source file.\n")
                f.write("The source file still needs to be copied to this directory!\n")
                f.write("Make sure that name in input file matches name of source file.")
                f.close()
                break
           
            # For activation backgrounds, copy all files to Source director:
            if this_name in ["PrimaryProtons","PrimaryAlphas",
                    "AtmosphericNeutrons","PrimaryElectrons","PrimaryPositrons",
                    "SecondaryProtons"]:
                print("WARNING: Simulating instrumental background component:")
                print("Make sure to set the correct paths in the source files!")
                this_src_dir = os.path.join(self.dc_dir,"Source_Library",each,"*")
                os.system("scp %s ." %this_src_dir)
                break

            # Get source from source library:
            this_src_dir = os.path.join(self.dc_dir,"Source_Library",each)
            this_src = this_name + ".source"
            this_src_file = os.path.join(this_src_dir,this_src)
   
            # Open source file for reading:
            g = open(this_src_file,"r")
            all_lines = g.readlines()    

            # Open new file for writting:
            h = open(this_src, "w")

            for line in all_lines:
                    
                split = line.split()
        
                if len(split) == 0:
                    h.write(line)

                elif (".Source" in split[0]) & (split[1] != each):
                    h.write(line)
                    this_name = split[1]

                elif "Beam" in split[0]:
                
                    beam_type = split[1]
                
                    if beam_type in ["FarFieldPointSource","FarFieldAssymetricGaussian",\
                            "FarFieldGaussian","FarFieldIsotropic"]:
                        h.write(line)
                
                    if beam_type == "FarFieldNormalizedEnergyBeamFluxFunction":
                        spectrum_file = os.path.join(self.dc_dir, "Source_Library", each, split[2])
                        shutil.copy2(spectrum_file, split[2])
                        new_line = this_name + ".Beam FarFieldNormalizedEnergyBeamFluxFunction " \
                            + os.path.join(self.home, "Sources", split[2]) + "\n"
                        h.write(new_line)
                    
                    if beam_type == "FarFieldFileZenithDependent":
                        beam_file = os.path.join(self.dc_dir, "Source_Library", each, split[2])
                        shutil.copy2(beam_file, split[2])
                        new_line = this_name + ".Beam FarFieldFileZenithDependent " \
                            + os.path.join(self.home, "Sources", split[2]) + "\n"
                        h.write(new_line)

                elif "Spectrum" in split[0]:
                
                    if beam_type in ["FarFieldPointSource","FarFieldAssymetricGaussian",\
                            "FarFieldGaussian","FarFieldIsotropic","FarFieldFileZenithDependent"]:
                        
                        if split[1] == "File":
                            spectrum_file = os.path.join(self.dc_dir, "Source_Library", each, split[2])
                            shutil.copy2(spectrum_file, split[2])
                            new_line = this_name + ".Spectrum File " + os.path.join(self.home, "Sources", split[2]) + "\n"
                            h.write(new_line)
                        
                        if split[1] != "File":
                            h.write(line)

                    if beam_type == "FarFieldNormalizedEnergyBeamFluxFunction":
                        h.write(line)
                 
                    if beam_type not in beam_list:
                        print("ERROR: Beam type is not defined")
                        print("Source: %s" %each)
                        sys.exit()

                elif "FarFieldTransmissionProbability" in split[0]:
                
                    if self.include_transmission_prob == True:
                        new_line = this_name + ".FarFieldTransmissionProbability " + self.transmission_prob_file + "\n"
                        h.write(new_line)
                
                    if self.include_transmission_prob == False:
                        pass
    
                else:
                    h.write(line)
       
        # Go home:
        os.chdir(self.home)

        return
