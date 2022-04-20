############################################################
# 
# Written by Chris karwin; November 2021; Clemson University.
#
# Purpose: Main script for generating simulation challenge.
# 
# Index of functions:
#
#   RunDataChallenge(superclass)
#       -define_sim()
#       -run_cosima(seed="none")
#       -run_nuclearizer(config_file="none")
#       -run_revan(config_file="none")
#       -run_mimrec(config_file="none", combine="none", extract_root=False)
#
###########################################################

######################
# Imports:
import os,sys,shutil 
import yaml
import pandas as pd
######################


# Superclass:
class RunDataChallenge:
    
    
    """Main inputs are specified in inputs.yaml file"""
    
    def __init__(self,input_yaml):

        # Get home directory:
        self.home = os.getcwd()
        
        # Load main inputs from yaml file:
        with open(input_yaml,"r") as file:
            inputs = yaml.load(file,Loader=yaml.FullLoader)

        self.dc_dir = inputs["dc_dir"]
        self.geo_file = inputs["geometry_file"]
        self.name = inputs["name"]
        self.source_file = self.name + ".source"
        self.time = inputs["time"]
        self.src_list = inputs["src_list"]
        self.orientation_file = inputs["orientation_file"]
        self.src_lib = os.path.join(self.dc_dir,"Data_Challenge/Source_Library")
        self.run_nuc = inputs["run_nuc"]

    def define_sim(self):

        """
        This function makes the main source file for the simulation. 

        The input source list is passed from inputs.yaml,
        and it must be a list of strings, where each string is from 
        the available options.
        """

        # Make print statement:
        print()
        print("********** Run_Data_Challenge_Module ************")
        print("Running define_sim...")
        print()

        ########################
        # Unit testing:

        # Verify that input sources are given as list:
        if isinstance(self.src_list,list) == False:
            raise TypeError("Input sources must be a list!")

        # Check that input sources are included in library:
        master_list_file = os.path.join(self.src_lib,"master_source_list.txt")
        f = open(master_list_file,"r")
        master_list = eval(f.read())
        master_name_list = []
        for i in range(0,len(master_list)):
            master_name_list.append(master_list[i][0])
        for each in self.src_list:
            if each not in master_name_list:
                print()
                print("ERROR: Input source is not defined!")
                print() 
                print("Sources must be selected from available list:")
                print(master_name_list)
                print()
                sys.exit()
        
        ##########################   

        # Print source list:      
        print()
        print("Simulation will include the following sources:")
        print(self.src_list)
        print()

        # Make output data directory:
        if os.path.isdir("Output") == True:
            shutil.rmtree("Output")
        os.system("mkdir Output")

        # Move orientation file if running parallel jobs:
        if os.path.exists("GalacticScan.ori"):
            os.system("mv GalacticScan.ori Output")

        # Write source file:
        f = open(os.path.join("Output",self.source_file),"w")
        f.write("#Source file for data challenge, version 1\n")
        f.write("#The detector rotates in the Galactic coordiante system as given in the ori file.\n")
        f.write("#The point sources are fixed in Galactic coordinates.\n\n")
        f.write("#geometry file\n")
        f.write("Version         1\n")
        f.write("Geometry %s\n\n" %self.geo_file)
        f.write("#Physics list\n")
        f.write("PhysicsListEM                        LivermorePol\n\n")
        f.write("#Output formats\n")
        f.write("StoreSimulationInfo                  init-only\n\n")
        f.write("#Define run:\n")
        f.write("Run DataChallenge\n")
        f.write("DataChallenge.FileName               %s\n" %self.name)
        f.write("DataChallenge.Time                   %s\n" %self.time)
        f.write("DataChallenge.OrientationSky         Galactic File NoLoop %s\n\n" %self.orientation_file)
        
        # Write sources:
        for each in self.src_list:
            this_file = os.path.join(each,each + ".source")
            this_path = os.path.join(self.dc_dir,"Data_Challenge/Source_Library/")
            this_src = os.path.join(this_path,this_file)
            f.write("#include %s\n" %each)
            f.write("Include %s\n\n" %this_src)
        
        # Close file:
        f.close()
    
        return
    
    def run_cosima(self,seed="none"):
        
        """
        input definitions:
        
        seed: Optional input. Specify seed to be used in simulations for reproducing results.
        """

        # Make print statement:
        print()
        print("********** Run_Data_Challenge_Module ************")
        print("Running run_cosima...")
        print()
 
        # Change to output directory:
        os.chdir("Output")
    
        # Run Cosima:
        if seed != "none":
            print("running with a seed...")
            os.system("cosima -v 1 -s %s -z %s | tee cosima_terminal_output.txt" %(seed,self.source_file))
        if seed == "none":
            print("running with no seed...")
            os.system("cosima -z %s | tee cosima_terminal_output.txt" %(self.source_file))

        # Return home:
        os.chdir(self.home)

        return

    def run_nuclearizer(self,config_file="none"):
        
        """
        input definitions:
        
         config_file: Optional input. 
            - Configuration file specifying selections for nuclearlizer.
        """

        # Make print statement:
        print()
        print("********** Run_Data_Challenge_Module ************")
        print("Running run_nuclearizer...")
        print()

        # Change to output directory:
        os.chdir("Output")

        # Define input sim file:
        sim_file = self.name + ".inc1.id1.sim.gz"

        # Run revan:
        if config_file != "none":

            print("running with a configuration file...")
            os.system("nuclearizer -a -g %s -c %s \
                    -C ModuleOptions.XmlTagSimulationLoader.SimulationFileName=%s \
                    | tee nuclearizer_terminal_output.txt" %(self.geo_file, config_file, sim_file))

        if config_file == "none":
            print("running without a configuration file...")
            os.system("nuclearizer -a -g %s \
                    -C ModuleOptions.XmlTagSimulationLoader.SimulationFileName=%s \
                    | tee nuclearizer_terminal_output.txt" %(self.geo_file, sim_file))

        # Go home:
        os.chdir(self.home)

        return

    def run_revan(self,config_file="none"):
        
        """
        input definitions:
        
         config_file: Optional input. 
            - Configuration file specifying selections for event reconstruction.
        """

        # Make print statement:
        print()
        print("********** Run_Data_Challenge_Module ************")
        print("Running run_revan...")
        print()

        # Change to output directory:
        os.chdir("Output")

        # Define input sim file:
        if self.run_nuc == False:
            sim_file = self.name + ".inc1.id1.sim.gz"
        if self.run_nuc == True:
            sim_file = "output.evta.gz" # depends on name in nuclearizer configuration file!

        # Run revan:
        if config_file != "none":

            print("running with a configuration file...")
            os.system("revan -g %s -c %s -f %s -n -a | tee revan_terminal_output.txt" %(self.geo_file, config_file, sim_file))

        if config_file == "none":
            print("running without a configuration file...")
            os.system("revan -g %s -f %s -n -a | tee revan_terminal_output.txt" %(self.geo_file, sim_file))
    
        # Zip output tra file and change name if running nuclearizer:
        if self.run_nuc == True:
            tra_file_name = self.name + ".inc1.id1.tra.gz"
            #os.system("gzip output.tra") # depends on name in nuclearizer configuration file!
            os.system("mv output.tra.gz %s" %tra_file_name)
        
        # Go home:
        os.chdir(self.home)

        return

    def run_mimrec(self, config_file="none", combine="none", extract_root=False):
        
        """
        input definitions:
        
         config_file: Optional input. 

         combine: Option to combine input tra file with another tra file.
            - must specify name and full path of combine file. 
        
         extract_root: if true will extract data for LC and spectrum. 
         Default is False.
        """

        # Make print statement:
        print()
        print("********** Run_Data_Challenge_Module ************")
        print("Running run_mimrec...")
        print()

        # Change to output directory:
        os.chdir("Output")
    
        # Define tra file:
        tra_file = self.name + ".inc1.id1.tra.gz"

        # Option to combine current run with other tra file:
        if combine != "none":
            combine_file = combine
            f = open("combined.inc1.id1.tra","w")
            f.write("TYPE TRA\n\n")
            f.write("IN %s\n" %tra_file)
            f.write("IN %s\n" %combine_file)
            f.write("EN")
            f.close()
            os.system("gzip %s" %"combined.inc1.id1.tra")
            tra_file = "combined.inc1.id1.tra.gz"

        # Define outputs:
        output_events = "%s.inc1.id1.extracted.tra.gz" %self.name

        # Set pdf or root output:
        file_type = ".pdf"
        if extract_root == True:
            file_type = ".root"
        
        # Specify output files:
        output_spec = "sim_counts_spectrum" + file_type
        output_image = "sim_image" + file_type
        output_LC = "sim_LC" + file_type

        # Run mimrec:
        if config_file != "none":
            
            print("running with a configuration file...")
           
            # Extract events:
            os.system("mimrec -g %s -c %s -f %s -x -o %s -n \
                    | tee mimrec_events_terminal_output.txt" %(self.geo_file, config_file, tra_file, output_events))
                 
            # Make spectrum:
            os.system("mimrec -g %s -c %s -f %s -s -o %s -n \
                    | tee mimrec_spectrum_terminal_output.txt" %(self.geo_file, config_file, tra_file, output_spec))
           
            # Make image:
            os.system("mimrec -g %s -c %s -f %s -i -o %s -n \
                    | tee mimrec_image_terminal_output.txt" %(self.geo_file, config_file, tra_file, output_image))

            # Make LC:
            os.system("mimrec -g %s -c %s -f %s -l -o %s -n \
                    | tee mimrec_LC_terminal_output.txt" %(self.geo_file, config_file, tra_file, output_LC))


        if config_file == "none":
            
            print("running without a configuration file...")
            
            # Extract events:
            os.system("mimrec -g %s -f %s -x -o %s -n \
                    | tee mimrec_events_terminal_output.txt" %(self.geo_file, tra_file, output_events))

            # Make spectrum:
            os.system("mimrec -g %s -f %s -s -o %s -n \
                    | tee mimrec_spectrum_terminal_output.txt" %(self.geo_file, tra_file, output_spec))
      
            # Make image:
            os.system("mimrec -g %s -f %s -i -o %s -n \
                    | tee mimrec_image_terminal_output.txt" %(self.geo_file, tra_file, output_image))
            
            # Make LC:
            os.system("mimrec -g %s -f %s -l -o %s -n \
                    | tee mimrec_LC_terminal_output.txt" %(self.geo_file, tra_file, output_LC))

        if extract_root == True:
            
            # Extract spectrum histogram:
            extract_spectrum_file = os.path.join(self.dc_dir,"Data_Challenge/Run_Data_Challenge/ExtractSpectrum.cxx")
            os.system("root -q -b %s" %extract_spectrum_file)

            # Extract light curve  histogram:
            extract_lc_file = os.path.join(self.dc_dir,"Data_Challenge/Run_Data_Challenge/ExtractLightCurve.cxx")
            os.system("root -q -b %s" %extract_lc_file)
        
            # Extract image histogram:
            extract_image_file = os.path.join(self.dc_dir,"Data_Challenge/Run_Data_Challenge/ExtractImage.cxx")
            os.system("root -q -b %s" %extract_image_file)

        # Go home:
        os.chdir(self.home)

        return

