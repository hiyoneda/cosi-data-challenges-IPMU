The official ori file for DC2 is 20280301_3_month.ori, 
which defines a low Earth equatorial orbit (550 km and 0 deg inclination) with zenith pointing for 3 months. 
The file is too large for github (777 MB) but is available on wasabi.
The time binning is 1 sec. 
For the background simulations we used a 15 s time binning, also available on wasabi: 20280301_3month_15sbin_bkg.ori

It can be downloaded from the command line as follows:

You'll need awscli:
pip install awscli 

To download: 
AWS_ACCESS_KEY_ID=GBAL6XATQZNRV3GFH9Y4 AWS_SECRET_ACCESS_KEY=GToOczY5hGX3sketNO2fUwiq4DJoewzIgvTCHoOv aws s3api get-object  --bucket cosi-pipeline-public --key COSI-SMEX/DC2/Data/Orientation/20280301_3_month.ori --endpoint-url=https://s3.us-west-1.wasabisys.com 20280301_3_month.ori
