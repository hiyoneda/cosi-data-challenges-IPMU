# COSI Data Challenge

## Required Software <br />
The data challenge module requires the MEGAlib code, available [here](http://megalibtoolkit.com/home.html). Among other things, MEGAlib simulates the emission from any (MeV) gamma-ray source, simulates the instrument response, performs the event reconstruction, and performs the high-level data analysis. See the above link for more details regarding the MEGAlib package.   

## Getting Help <br />
For any help/problems with running the data challenge module please contact Chris Karwin at: ckarwin@clemson.edu. 

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
vela <br /> 
cenA <br />
cygX1 <br />

**Diffuse:**  <br />
Al26 <br />
Al26_10xFlux <br />
GC511A (based on Knoedlseder+05) <br />
GC511A_10xFlux <br />
GC511B (based on Skinner+14) <br />
GalBrem <br />
GalIC

**Background:**  <br />
LingBG <br />

## Quickstart Guide <br /> 
<pre>
1. Download cosi-data-challenges directory:
  - git clone https://github.com/ckarwin/COSI.git
  - It's advised to add the Run_Data_Challenge directory to your python path.
  - Note: This repository does not include the geometery file. 

2. For any new analysis (assuming you added your path), copy the following files to a new analysis directory: inputs.yaml, run_setup.py
     
3. Specify inputs in inputs.yaml </b>
  - Note: The pipeline supports the use of mcosima with multiple cores. This can be specified in the yaml file.    

4. Run setup script: python run_setup.py
  - This will setup the source directory and copy all needed files for running the code.
  
5. To run the code:  </b>
  - Uncomment the functions inside the client code that you want to run.
  - The code can be ran directly from the terminal or submitted to a batch system.
  - To run from the terminal use python run_sims.py.
  - To run parallel jobs in cosima with numerous time bins use python run_parallel_sims.py. 
  - To run a single job in cosima with one time bin use python submit_jobs.py. 

6. If running parallel jobs:
  - In the client code uncomment all functions except mimrec.
  - Run: python run_parallel_sims.py.  
  - After all the jobs finish, uncomment just the mimrec function in the client code, then run: python submit_jobs.py.

7. Note that the submission commands in run_parallel_sims.py and submit_jobs.py may need to be modified based on the user's batch system.

</pre>

## Best Practices for Adding New Sources <br />
* New sources should be added to Source_Library. <br />
* Use Source_Library/crab as a template to follow. See the MEGAlib cosima documentation for more details regarding the inputs. <br />
* Define a directory for the source using its simple name (i.e. src_name). The same name must be used for all files in the directory. <br />
* At minimum the source directory needs to contain a source file (src_name.source) and a spectral file (src_name.dat). In the future it may also include a light curve file and a polarization file. <br />
* The source also needs to be added to master_source_list.txt in Source_Library.
* Alternatively, send me the source name, position, and spectra, and I can add it to the library.

## Data Challenge Notes <br />
**Data Challenge 1:** A brief summary of the first data challenge is available [here](https://drive.google.com/file/d/1F4p6Mq6Lg26Cqx8vgu4I_64cIKz3JhV4/view?usp=sharing) (please request access if needed).
