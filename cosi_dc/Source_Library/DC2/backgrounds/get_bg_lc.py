import os

bg_list = ['AtmosphericNeutrons','AlbedoPhotons','PrimaryAlphas','PrimaryElectrons','PrimaryPositrons','PrimaryProtons','SecondaryPositrons','SecondaryProtonsDownward','SecondaryElectrons','SecondaryProtonsUpward']
for each in bg_list:
    os.system("AWS_ACCESS_KEY_ID=GBAL6XATQZNRV3GFH9Y4 AWS_SECRET_ACCESS_KEY=GToOczY5hGX3sketNO2fUwiq4DJoewzIgvTCHoOv aws s3api get-object  --bucket cosi-pipeline-public --key COSI-SMEX/DC2/Data/Background_LCs/%s_LightCurve_SameOriTime_3months.dat --endpoint-url=https://s3.us-west-1.wasabisys.com %s_LightCurve_SameOriTime_3months.dat" %(each,each))
