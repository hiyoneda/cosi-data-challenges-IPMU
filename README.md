# COSI Data Challenge

## Required Software <br />
The data challenge module requires the MEGAlib code, available [here](http://megalibtoolkit.com/home.html). Among other things, MEGAlib simulates the emission from any (MeV) gamma-ray source, simulates the instrument response, performs the event reconstruction, and performs the high-level data analysis. See the above link for more details regarding the MEGAlib package.   

## Getting Help <br />
For any help/problems with running the data challenge module please contact Chris Karwin at: christopher.m.karwin@nasa.gov. 

## Data Products <br />
All final data products for the data challenge are available on the COSI sftp account.

## Purpose <br />
The main purpose of this repository is to simulate the all-sky data that will be observed by COSI. The primary code is **run_data_challenge_module.py**, which can be called with **run_sims.py**, with the main input parameters passed via **inputs.yaml**. Additionally, parallel simulations with multiple time bins can be ran using **run_parellel_sims.py**, which distributes the time bins to seperate compute nodes. The pipeline also supports the use of mcosima with numerous cores per compute node. The modules can be ran directly from the command line, or submitted to a batch system, which allows them to be easily employed for generating multiple/long simulations. 

## Directory Structure <br />
The schematic below shows the directory structure. Full installation instructions and a quickstart guide are given below.   

```mermaid
%%{init: {'theme':'default'}}%%
graph TD;
    A[cosi-data-challenges<br>inputs.yaml<br>run_setup.py<br>run_sims.py<br>run_parallel_sims.py<br>submit_jobs.py] --- C[Input_Files] & D[Run_Data_Challenge<br>run_data_challenge.py<br>setup.py<br>make_orientation_bins.py<br>ExtractImage.cxx<br>ExtractLightCurve.cxx<br>ExtractSpectrum.cxx] & E[Source_Library<br>master_source_list.txt];
    C --- Ca["Orientation_Files"];
    C --- Cb[Geometry_Files];
    C --- Cd[Configuration_Files];
    C --- Ce["Transmission_Probability"];
    E --- Ea[Source1<br>source1.source<br>source1_spec.dat<br>source1_LC.dat<br>source1_pol.dat];
    E --- Eb[Source2<br>source2.source<br>source2_spec.dat<br>source2_LC.dat<br>source2_pol.dat];
    E --- Ec[SourceN<br>sourceN.source<br>sourceN_spec.dat<br>sourceN_LC.dat<br>sourceN_pol.dat];
    E --- Ed[Make_Sources<br>make_sources.py];
```

## Available Sources for Simulations <br />
The simulated sources are passed via the inputs.yaml file. The following sources are available:

**Point Sources:**  <br />
crab <br />
crab_10xFlux <br />
vela <br /> 
vela_10xFlux <br />
cenA <br />
cenA_10xFlux <br />
cygX1 <br />
cygX1_10xFlux <br />

**Diffuse:**  <br />
Al26 <br />
Al26_10xFlux <br />
GC511A (based on Knoedlseder+05) <br />
GC511A_10xFlux <br />
GC511B (based on Skinner+14) <br />
GalBrem <br />
GalIC <br />
GalTotal_SA100_F98 <br />

**Background:**  <br />
LingBG <br />

## Quickstart Guide <br /> 
<pre>
1. Download cosi-data-challenges directory:
  - git clone https://github.com/cositools/cosi-data-challenges.git
  - Add the Run_Data_Challenge directory to your python path.
  - Note: This repository does not include the geometery file. 

2. For any new analysis, copy the following files to a new analysis directory: inputs.yaml, run_setup.py
     
3. Specify inputs in inputs.yaml </b>
     
4. Run setup script: python run_setup.py
  - This will setup the source directory and copy all needed files for running the code.
  
5. To run the code:  </b>
  - Uncomment the functions inside run_sims.py that you want to run.
  - The code can be ran directly from the terminal or submitted to a batch system.
  - To run from the terminal use python run_sims.py.
  - To run parallel jobs in cosima with numerous time bins use python run_parallel_sims.py. 
  - To submit a single job use python submit_jobs.py. 

6. If running parallel jobs:
  - In run_sims.py uncomment all functions except mimrec.
  - Run: python run_parallel_sims.py.  
  - After all the jobs finish, uncomment just the mimrec function in run_sims.py, then run: python submit_jobs.py.

7. Note that the batch submission commands in run_parallel_sims.py and submit_jobs.py may need to be modified based on the user's specific batch system.

</pre>

## Bug report <br />
* The number of iterations in ExtractImage.cxx needs to be changed manually if using a different value than the default (20). Specifically, this is at lines 8 and 10. For x iterations: 20 --> x and 22 --> x+2. This will be automated soon.  
