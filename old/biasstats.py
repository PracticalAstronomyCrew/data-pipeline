import sys
import pyfits
import numpy as np
import subprocess
from scipy.stats import skew
from scipy.stats import kurtosis
from scipy.stats import mode

subprocess.call("ls /net/vega/data/users/observatory/images/"+str(sys.argv[1])+"/STL-6303E/i/*BIAS* > /Users/users/noelstorr/rough/bias.list",shell=True)

subprocess.call("ls /net/vega/data/users/observatory/images/"+str(sys.argv[1])+"/STL-6303E/i/*Li* > /Users/users/noelstorr/rough/file.list",shell=True)

biasfiles = [line.rstrip('\n') for line in open("/Users/users/noelstorr/rough/bias.list")]

allfiles = [line.rstrip('\n') for line in open("/Users/users/noelstorr/rough/file.list")]

hdu = pyfits.open(allfiles[0])
datetoday = hdu[0].header['DATE-OBS'][0:10] 
timestart = float(hdu[0].header['DATE-OBS'][11:13]) + float(hdu[0].header['DATE-OBS'][14:16])/60.0
if timestart < 12.0: timestart = timestart + 24.0

for file in biasfiles:
    hdu = pyfits.open(file)
    nighttime = float(hdu[0].header['DATE-OBS'][11:13]) + float(hdu[0].header['DATE-OBS'][14:16])/60.0
    if nighttime < 12.0: nighttime = nighttime + 24.0
    obstime = nighttime - timestart
    expcount = allfiles.index(file)
    data = hdu[0].data
    oned = data.flatten()

    print("{:11s} , {:4.2f} , {:4d} , {:4.2f} , {:6.2f} , {:4.2f} , {:6.2f} , {:6.2f} , {:5.4f} , {:6.2f}".format(datetoday,nighttime,expcount,obstime,np.mean(data),np.std(data),float(mode(oned)[0]),float(np.median(oned)),skew(oned),kurtosis(oned)))
