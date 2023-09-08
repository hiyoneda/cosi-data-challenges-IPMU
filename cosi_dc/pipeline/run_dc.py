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
#       -msimconcatter()
#       -run_nuclearizer(geo_file="default")
#       -run_revan(geo_file="default")
#       -run_mimrec(extract_root=False, geo_file="default")
#       -clear_unessential_data()
#
###########################################################

######################
# Imports:
import os,sys,shutil 
import yaml
import pandas as pd
import numpy as np
import scipy.integrate as integrate
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import math
import gzip
import cosi_dc
######################


# Superclass:
class RunDataChallenge:
    
    
    """Main inputs are specified in inputs.yaml file"""
    
    def __init__(self,input_yaml):

        # Get home directory:
        self.home = os.getcwd()
        
        # Get install directory:
        self.dc_dir = os.path.split(cosi_dc.__file__)[0]

        # Load main inputs from yaml file:
        with open(input_yaml,"r") as file:
            inputs = yaml.load(file,Loader=yaml.FullLoader)

        self.run_dir = inputs["run_dir"]
        self.geo_file = inputs["geometry_file"]
        self.name = inputs["name"]
        self.source_file = self.name + ".source"
        self.time = inputs["time"]
        self.src_list = inputs["src_list"]
        self.orientation_file = inputs["orientation_file"]
        self.lightcurve_file = inputs["lightcurve_file"]
        self.lightcurve = inputs["lightcurve"]
        self.parallel_time_sims = inputs["parallel_time_sims"]
        self.num_sims = inputs["num_sims"]
        self.run_type = inputs["run_type"]
        self.clear_sims = inputs["clear_sims"]
        self.src_lib = os.path.join(self.dc_dir,"Source_Library")
        self.run_nuc = inputs["run_nuc"]
        self.nuc_config = inputs["nuc_config"]
        self.revan_config = inputs["revan_config"]
        self.mimrec_config = inputs["mimrec_config"]
        self.mcosima = inputs["mcosima"]
        self.num_cores = inputs["num_cores"]
        self.ntriggers = inputs["ntriggers"]
        self.ASphere = inputs["ASphere"]
        self.include_transmission_prob = inputs["include_transmission_prob"]
        self.transmission_prob_file = inputs["transmission_prob_file"]

    def define_sim(self, external_src=False):

        """
        This function makes the main source file for the simulation. 

        The input source list is passed from inputs.yaml,
        and it must be a list of strings, where each string is from 
        the available options.
        
        Optional input: 
        external_src: Option to use source outside of source library. 
            - True or False; default is False.
        """

        # Make print statement:
        print()
        print("********** Run_Data_Challenge_Module ************")
        print("Running define_sim...")
        print()

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
        
        # Also need to move LC file for parallel jobs:
        if self.lightcurve == True:
            os.system("mv lightcurve.dat Output")

        # Need to update name of orientation file if running parallel time sims:
        if self.parallel_time_sims == True:
            orientation_file = "GalacticScan.ori"
        else: orientation_file = self.orientation_file

        # Option to use source outside of library:
        if external_src == True:
            src_files = os.path.join(self.run_dir,"Sources","*.source")
            os.system("scp %s %s" %(src_files,"./Output"))

        if external_src == False:
           
            # Write source file:
            f = open(os.path.join("Output",self.source_file),"w")
            f.write("#Source file for data challenge\n")
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
            f.write("DataChallenge.OrientationSky         Galactic File NoLoop %s\n\n" %orientation_file)
        
            # Add sources:
            for each in self.src_list:

                this_name = os.path.basename(each)
                this_src = os.path.join(self.run_dir, "Sources" ,this_name + ".source")
                f.write("#include %s\n" %each)
                f.write("Include %s\n\n" %this_src)
            
            f.close()
    
        return
    
    def run_cosima(self, seed="none", verbosity=0):
        
        """
        input definitions:
        
        seed: Specify seed to be used in simulations for reproducing results.
            - Default is no seed. 
        verbosity: Verbosity level of cosima output. 
            - Default is same as cosima default (0). 
        """

        # Make print statement:
        print()
        print("Running run_cosima...")
        print()
 
        # Change to output directory:
        os.chdir("Output")
   
        # Construct executable:
        # Option to run cosima or mcosima with numerous cores.
        if self.mcosima == False:
            executable = "cosima -v %s" %str(verbosity)
        if self.mcosima == True:
            executable = "mcosima -t %s -w -a" %self.num_cores
            # Check that no seed has been passed:
            if seed != "none":
                print("ERROR: mcosima needs to be ran without a seed.")
                print("Exiting code.")
                sys.exit()

        # Run executable:
        if seed != "none":
            print("running with a seed...")
            os.system("%s -s %s -z %s | tee cosima_terminal_output.txt" %(executable,seed,self.source_file))
        if seed == "none":
            print("running with no seed...")
            os.system("%s -z %s | tee cosima_terminal_output.txt" %(executable,self.source_file))

        # Concatenate sim files:
        if self.mcosima == True:
            self.msimconcatter()
        
        # Return home:
        os.chdir(self.home)

        return

    def msimconcatter(self):
        
        """Concatenate output sim files from mcosima."""

        # Construct string of files to concatenate:
        cat_string = ""
        for i in range(0,self.num_cores):
            cat_string += " %s.p1.inc%s.id1.sim.gz" %(self.name,str(i+1))
        
        # Concatenate files:
        os.system("msimconcatter %s" %cat_string)
        
        return

    def run_nuclearizer(self, geo_file="default"):
        
        """
        input definitions:
            
         geo_file: Optional input.
            - Option to use a different geometry file. Must specify full path.  
            - This option is for cosima runs only.

        Note: If running mcosima, then the nuclearizer configuration file 
              must point to the correct geometry file. 
        """

        # Make print statement:
        print()
        print("Running run_nuclearizer...")
        print()

        # Option to use a different geo file:
        if geo_file != "default":
            self.geo_file = geo_file

        # Change to output directory:
        os.chdir("Output")
   
        # Default mode:
        if self.mcosima == False:

            # Remove output file if it already exists (for rerunning option):
            if os.path.exists("output.evta.gz"):
                os.system("rm output.evta.gz nuclearizer_terminal_output.txt")
        
            # Define input sim file:
            sim_file = self.name + ".inc1.id1.sim.gz"

            # Make sure input sim file exists:
            if os.path.exists(sim_file) == False:
                print("ERROR: The input file needed for nuclearizer does not exist.") 
                print("Exiting Code!")
                sys.exit()
                  
            if self.nuc_config != "none":
                os.system("nuclearizer -a -g %s -c %s \
                    -C ModuleOptions.XmlTagSimulationLoader.SimulationFileName=%s \
                    | tee nuclearizer_terminal_output.txt" %(self.geo_file, self.nuc_config, sim_file))
        
            if self.nuc_config == "none":
                print("running without a configuration file...")
                os.system("nuclearizer -a -g %s \
                    -C ModuleOptions.XmlTagSimulationLoader.SimulationFileName=%s \
                    | tee nuclearizer_terminal_output.txt" %(self.geo_file, sim_file))

        # mcosima mode:
        if self.mcosima == True:
            sim_files = "%s.p1.inc{1..%s}.id1.sim.gz"  %(self.name, str(self.num_cores))
            os.system("mnuclearizer -c %s -f %s\
                    | tee nuclearizer_terminal_output.txt" %(self.nuc_config, sim_files))

        # Go home:
        os.chdir(self.home)

        return

    def run_revan(self, geo_file="default"):
        
        """
        input definitions:
         
         geo_file: Optional input.
            - Option to use a different geometry file. Must specify full path. 
        """

        # Make print statement:
        print()
        print("Running run_revan...")
        print()

        # Option to use a different geo file:
        if geo_file != "default":
            self.geo_file = geo_file
        
        # Change to output directory:
        os.chdir("Output")
 
        # Default mode:
        if self.mcosima == False:
       
            # Remove output file if it already exists (option for rerunning):
            tra_file_name = self.name + ".inc1.id1.tra.gz"
            if os.path.exists(tra_file_name):
                os.system("rm %s revan_terminal_output.txt" %tra_file_name)

            # Define input sim file:
            if self.run_nuc == False:
                sim_file = self.name + ".inc1.id1.sim.gz"
            if self.run_nuc == True:
                sim_file = "output.evta.gz" # depends on name in nuclearizer configuration file!
            
            # Make sure input sim file exists:
            if os.path.exists(sim_file) == False:
                print("ERROR: The input file needed for revan does not exist.")
                print("Exiting code!")
                sys.exit()
        
            # Run revan:
            if self.revan_config != "none":

                print("running with a configuration file...")
                os.system("revan -g %s -c %s -f %s -n -a | tee revan_terminal_output.txt" %(self.geo_file, self.revan_config, sim_file))

            if self.revan_config == "none":
                print("running without a configuration file...")
                os.system("revan -g %s -f %s -n -a | tee revan_terminal_output.txt" %(self.geo_file, sim_file))
    
            # Change name of output if running nuclearizer:
            if self.run_nuc == True:
                os.system("mv output.tra.gz %s" %tra_file_name)
        
        # mcosima mode:
        if self.mcosima == True:
            sim_files = "%s.p1.inc{1..%s}.id1.evta.gz"  %(self.name, str(self.num_cores))
            os.system("mrevan -g %s -c %s -f %s\
                    | tee revan_terminal_output.txt" %(self.geo_file, self.revan_config, sim_files))
            
        # Go home:
        os.chdir(self.home)

        return

    def run_mimrec(self, extract_root=False, geo_file="default", energy=None):
        
        """
        input definitions:
         
         extract_root: if true will extract data for LC and spectrum. 
            - Default is False.

         geo_file: Option to use a different geometry file. Must specify full path. 
        
         energy: Energy in keV. For calculating Aeff from monoenergetic sims. 
        """

        # Make print statement:
        print()
        print("Running run_mimrec...")
        print()

        # Option to use a different geo file:
        if geo_file != "default":
            self.geo_file = geo_file

        # Change to output directory:
        os.chdir("Output")
    
        # Define tra file:
        tra_file =  self.name + ".inc1.id1.tra.gz"

        # Define outputs:
        output_events =  "%s.inc1.id1.extracted.tra.gz" %self.name

        # Set pdf or root output:
        file_type = ".pdf"
        if extract_root == True:
            file_type = ".root"
        
        # Specify output files:
        output_spec = "sim_counts_spectrum" + file_type
        output_image = "sim_image" + file_type
        output_LC = "sim_LC" + file_type

        # Run mimrec:
        if self.mimrec_config != "none":
            
            print("running with a configuration file...")
           
            # Extract events:
            os.system("mimrec -g %s -c %s -f %s -x -o %s -n \
                    | tee mimrec_events_terminal_output.txt" %(self.geo_file, self.mimrec_config, tra_file, output_events))
            
            # Note: the output file from the extracted events is now used as inputs below:

            # Make spectrum:
            os.system("mimrec -g %s -c %s -f %s -s -o %s -n \
                    | tee mimrec_spectrum_terminal_output.txt" %(self.geo_file, self.mimrec_config, output_events, output_spec))
           
            # Make image:
            os.system("mimrec -g %s -c %s -f %s -i -o %s -n \
                    | tee mimrec_image_terminal_output.txt" %(self.geo_file, self.mimrec_config, output_events, output_image))

            # Make LC:
            os.system("mimrec -g %s -c %s -f %s -l -o %s -n \
                    | tee mimrec_LC_terminal_output.txt" %(self.geo_file, self.mimrec_config, output_events, output_LC))

            # Extract arm:
            if energy is not None:
                elow = energy - 11
                ehigh = energy + 11
                os.system("mimrec -g %s -c %s -f %s -a -n \
                    -C EventSelections.FirstEnergyWindow.Min=%s \
                    -C EventSelections.FirstEnergyWindow.Max=%s \
                    | tee mimrec_arm_output.txt" \
                    %(self.geo_file, self.mimrec_config, tra_file, str(elow), str(ehigh)))
            
        if self.mimrec_config == "none":
            
            print("running without a configuration file...")
            
            # Extract events:
            os.system("mimrec -g %s -f %s -x -o %s -n \
                    | tee mimrec_events_terminal_output.txt" %(self.geo_file, tra_file, output_events))

            # Make spectrum:
            os.system("mimrec -g %s -f %s -s -o %s -n \
                    | tee mimrec_spectrum_terminal_output.txt" %(self.geo_file, output_events, output_spec))
      
            # Make image:
            os.system("mimrec -g %s -f %s -i -o %s -n \
                    | tee mimrec_image_terminal_output.txt" %(self.geo_file, output_events, output_image))
            
            # Make LC:
            os.system("mimrec -g %s -f %s -l -o %s -n \
                    | tee mimrec_LC_terminal_output.txt" %(self.geo_file, output_events, output_LC))
        
        if extract_root == True:
            
            # Extract spectrum histogram:
            extract_spectrum_file = os.path.join(self.dc_dir,"pipeline/ExtractSpectrum.cxx")
            os.system("root -q -b %s" %extract_spectrum_file)

            # Extract light curve histogram:
            extract_lc_file = os.path.join(self.dc_dir,"pipeline/ExtractLightCurve.cxx")
            os.system("root -q -b %s" %extract_lc_file)
        
            # Extract image histogram:
            extract_image_file = os.path.join(self.dc_dir,"pipeline/ExtractImage.cxx")
            os.system("root -q -b %s" %extract_image_file)

        # Go home:
        os.chdir(self.home)

        return

    def clear_unessential_data(self):

        """By default the main simulation pipeline saves all of the output,
        for diagnostic purposes. This method removes un-needed output 
        files in order to reduce disk space."""

        # Get initial disk usage:
        print()
        print("Checking initial directory size...")
        os.system("du -h -d0 Simulations/")
        
        # Change to Simulations directory:
        os.chdir("Simulations")
        
        # Write directories to temporary file and read:
        os.system("ls -d */ > dirs.dat")
        df = pd.read_csv("dirs.dat", names=["dirs"], header=None)
        dirs_list = df["dirs"].tolist()
        
        # Remove un-needed files:
        print("Removing un-needed files...")
        for each in dirs_list:
            os.chdir(os.path.join(each,"Output"))
            os.system("rm -rf crossections cosima_terminal_output.txt \
                    revan_terminal_output.txt nuclearizer_terminal_output.txt")
            os.chdir("../..")
        os.system("rm dirs.dat")
        
        # Go home:
        os.chdir(self.home)

        # Get final disk usage:
        print("Checking final directory size...")
        os.system("du -h -d0 Simulations/")
        print()

        return

