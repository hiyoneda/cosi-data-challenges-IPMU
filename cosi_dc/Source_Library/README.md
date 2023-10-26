# Source Library <br />
All sources from COSI's data challenges are available here. Sources must be specified in the input yaml file just as given below, i.e. including the relative path from the Source_Library directory. 

## Data Challenge 1 (DC1) <br /> 
DC1/crab <br />
DC1/crab_10xFlux <br />
DC1/cenA <br />
DC1/cenA_10xFlux <br />
DC1/vela <br />
DC1/vela_10xFlux <br />
DC1/cygX1 <br />
DC1/cygX1_10xFlux <br />
DC1/LingBG <br />
DC1/Al26 <br />
DC1/Al26_10xFlux <br /> 
DC1/GC511A <br />
DC1/GC511A_10xFlux <br />
DC1/GC511B <br />
DC1/OrthoPs <br />

## Data Challenge 2 (DC2) <br />
DC2/proto_dc2/gruber99 <br />
DC2/proto_dc2/gruber99_LEO <br />
DC2/backgrounds/PrimaryProtons <br />
DC2/backgrounds/PrimaryAlphas <br />
DC2/backgrounds/CosmicPhotons <br />
DC2/backgrounds/AtmosphericNeutrons <br />
DC2/backgrounds/PrimaryElectrons <br />
DC2/backgrounds/AlbedoPhotons <br />
DC2/backgrounds/PrimaryPositrons <br />
DC2/backgrounds/SecondaryProtons <br />

## Galactic Diffuse (Galdiff) <br />
Galdiff/GalIC <br />
Galdiff/GalBrem <br />
Galdiff/GalTotal_SA100_F98 <br />
Galdiff/GalTS_Baseline <br />
Galdiff/GalTS_BestMatch <br />

## Using your own sources:
To use your own sources specifiy 'other' in the input yaml source list.  <br />
The source files must still be copied to the source directory of the run, and all corresponding paths need to be correct. <br />
When running define_sim (in run_sims.py) you need to pass 'external_src=True'.
