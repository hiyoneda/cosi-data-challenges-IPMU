# COSI Data Challenge

## Required Software <br />
The data challenge module requires the MEGAlib code, available [here](http://megalibtoolkit.com/home.html). Among other things, MEGAlib simulates the emission from any (MeV) gamma-ray source, simulates the instrument response, performs the event reconstruction, and performs the high-level data analysis. See the above link for more details regarding the MEGAlib package.   

## Getting Help <br />
For any help/problems with running the data challenge module please contact Chris Karwin at: christopher.m.karwin@nasa.gov. 

## Data Challenge Releases <br />
* March 2023: The first data challenge is now available! It can be found [here](https://github.com/cositools/cosi-data-challenge-1.git).

## Purpose <br />
The main purpose of this repository is to simulate the all-sky data that will be observed by COSI. The primary code is **run_dc.py**, which can be called with **run_sims.py**, with the main input parameters passed via **inputs.yaml**. Additionally, parallel simulations with multiple time bins can be ran using **run_parallel_sims.py**, which distributes the time bins to seperate compute nodes. The pipeline also supports the use of mcosima with numerous cores per compute node. The modules can be ran directly from the command line, or submitted to a batch system, which allows them to be easily employed for generating multiple/long simulations. 

## Available Sources for Simulations <br />
See Source_Library for available sources. Let us know if you want any specific source added!

## Quickstart Guide <br /> 
<pre>
1. Download cosi-data-challenges directory:
  $ git clone https://github.com/cositools/cosi-data-challenges.git

2. Install with pip:
  $ cd cosi-data-challenges
  $ pip install -e .

3. Start a new analysis directory, and enter the commmand-line prompt:
  $ make_sim
   
4. Specify inputs in inputs.yaml </b>
     
5. Run setup script: 
  $ python run_sim_setup.py
  - This will setup the source directory and copy all needed files for running the code.
  
6. To run the code:  </b>
  - Uncomment the functions inside run_sims.py that you want to run.
  - The code can be ran directly from the terminal or submitted to a batch system.
  - The code supports both PBS and Slurm.
  - To run from the terminal use python run_sims.py.
  - To run parallel jobs in cosima with numerous time bins use python run_parallel_sims.py. 
  - To submit a single job use 'python submit_jobs.py' for PBS and 'sbatch slurm_single.sh' for Slurm. 

7. If running parallel jobs:
  - In run_sims.py uncomment all functions except mimrec.
  - Run: python run_parallel_sims.py.  
  - This will setup all the scripts needed for running parallel jobs, depending on the run type specified in the inputs yaml file. 

8. Note that the batch submission commands may need to be modified based on the user's specific batch system.
  - The batch system is specified via the run_type parameter. 
  - The example directory contains different batch scripts. 

</pre>

## Bug report <br />
* The number of iterations in ExtractImage.cxx needs to be changed manually if using a different value than the default (20). Specifically, this is at lines 8 and 10. For x iterations: 20 --> x and 22 --> x+2. This will be automated soon.  
