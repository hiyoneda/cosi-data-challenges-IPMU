We used a total exposure time of 3 months, i.e this is the time that was used in step 1 of the simulations.
For the irradiation time in step 2 of the simulations we used 1 year.
Thus, our background estimates correspond to 3 months of exposure, and then scaled to a rate for an irradiation time of 1 year.

The background simulations include the time variation from the changing geomagnetic cutoff within the orbit. To accomplish this, the simulations are ran using a light curve, which modifies the normalization of the flux accordingly (for each respective component). In order to get the correct time dependence, an orientation file is also used. These files are available on wasabi, and they can be downloaded as follows:

You'll need awscli:
pip install awscli 

To download orientation file: 
AWS_ACCESS_KEY_ID=GBAL6XATQZNRV3GFH9Y4 AWS_SECRET_ACCESS_KEY=GToOczY5hGX3sketNO2fUwiq4DJoewzIgvTCHoOv aws s3api get-object  --bucket cosi-pipeline-public --key COSI-SMEX/DC2/Data/Orientation/20280301_3month_15sbin_bkg.ori --endpoint-url=https://s3.us-west-1.wasabisys.com 20280301_3month_15sbin_bkg.ori

To download light curve files run:
python get_bg_lc.py

