import sys
import pyfits
import numpy as np
import subprocess
from scipy import stats

f = open("ROUGHSTATS_"+str(sys.argv[1])+".txt","w+")

subprocess.call("ls /net/vega/data/users/observatory/images/"+str(sys.argv[1])+"/STL-6303E/i/*BIAS* > /Users/users/noelstorr/rough/bias.list",shell=True)

subprocess.call("ls /net/vega/data/users/observatory/images/"+str(sys.argv[1])+"/STL-6303E/i/*DARK* > /Users/users/noelstorr/rough/dark.list",shell=True)

subprocess.call("ls /net/vega/data/users/observatory/images/"+str(sys.argv[1])+"/STL-6303E/i/*FLAT* > /Users/users/noelstorr/rough/flat.list",shell=True)

subprocess.call("ls /net/vega/data/users/observatory/images/"+str(sys.argv[1])+"/STL-6303E/i/*Li* > /Users/users/noelstorr/rough/file.list",shell=True)

print('Stripping')
biasfiles = [line.rstrip('\n') for line in open("/Users/users/noelstorr/rough/bias.list")]

darkfiles = [line.rstrip('\n') for line in open("/Users/users/noelstorr/rough/dark.list")]

flatfiles = [line.rstrip('\n') for line in open("/Users/users/noelstorr/rough/flat.list")]

allfiles = [line.rstrip('\n') for line in open("/Users/users/noelstorr/rough/file.list")]

try:
    print('Stacking Biases')
    data_stack = []
    bias_list = []
    std_list = []
    biascount = 0
    for file in biasfiles:
        hdu = pyfits.open(file)
        data_stack.append(pyfits.getdata(file))
        # print('Bias:',np.mean(pyfits.getdata(file)),np.std(pyfits.getdata(file)),'TEMP SET-ACT:',hdu[0].header['SET-TEMP'] - hdu[0].header['CCD-TEMP'])
        bias_list.append(np.mean(pyfits.getdata(file)))
        std_list.append(np.std(pyfits.getdata(file)))
        biascount = biascount + 1
    
    print('Calculating Bias')
    medianBias = np.median(data_stack,axis=0)
    earlyBias = np.median(data_stack[1:5],axis=0)
    lateBias = np.median(data_stack[-5:-1],axis=0)

    pyfits.writeto('/Users/users/noelstorr/rough/earlyBias'+str(sys.argv[1])+'.fits',earlyBias)
    pyfits.writeto('/Users/users/noelstorr/rough/lateBias'+str(sys.argv[1])+'.fits',lateBias)
except:
    print('Bias Missing or Bias Error')

try:
    print('Stacking and Bias Subtracting Darks')
    data_stack = []
    temp_stack = []
    darktime = 0.0
    for file in darkfiles:
        debias = pyfits.getdata(file) - medianBias
        hdu = pyfits.open(file)
        exptime = hdu[0].header['EXPTIME']
        darktime = darktime + exptime
        persec = np.array(debias).astype('float64') / exptime
        #    print('Dark:',np.mean(persec),exptime,np.mean(pyfits.getdata(file)),np.mean(debias),np.std(pyfits.getdata(file)),np.std(debias),np.mean(pyfits.getdata(file))-np.mean(medianBias),hdu[0].header['CCD-TEMP'])
        data_stack.append(persec)
        temp_stack.append(hdu[0].header['CCD-TEMP'])

    print('Calculating Dark')
    medianDark = np.median(data_stack,axis=0)
except:
    print('Dark Error or Missing')

try:
    print('Flat Statistics')
    flatsdone = []
    for file in flatfiles:
        hdu = pyfits.open(file)
        counts = np.average(pyfits.getdata(file)) - np.average(medianBias)
        flatsdone.append((hdu[0].header['FILTER'],counts))
except:
    print('Flats Missing or Flat Error')

print('Total Exposure')
tot_exp = 0.0
expfilts = []
for file in allfiles:
    hdu = pyfits.open(file)
    imtype = hdu[0].header['IMAGETYP']
    exptime = hdu[0].header['EXPTIME']
    if imtype == 'Light Frame': 
        tot_exp = tot_exp + exptime
        expfilts.append(hdu[0].header['FILTER'])
        continue  

f.write('Rough-cut Summary Data for '+str(sys.argv[1])+'\n')
f.write('\n')
try: 
    f.write("{:17s} {:5.0f} {:s} {:3d} {:s}".format('Mean Bias Level:',np.mean(medianBias),'counts/pix based on',biascount,'frames')+'\n')
except:
    print('Bias Troubles')
try: 
    f.write("{:17s} {:5.0f} {:3s} {:3.0f}".format('Early Bias:',np.mean(bias_list[:5]),'+/-',np.mean(std_list[:5]))+'\n')
except: 
    print('Early Bias Troubles')

try: 
    f.write("{:17s} {:5.0f} {:3s} {:3.0f}".format('Late Bias:',np.mean(bias_list[-5:]),'+/-',np.mean(std_list[-5:]))+'\n')
except:
    print('Late Bias Troubles')

try: 
    f.write("{:17s} {:5.0f}".format('Bias Shift:',np.mean(bias_list[:5])-np.mean(bias_list[-5:]))+'\n')
except:
    print('Bias Troubles')

f.write('\n')

try: 
    f.write("{:17s} {:5.3f} {:s} {:3.1f} {:s} {:6.2f} {:s}".format('Mean Dark Level:',np.mean(medianDark),'counts/pix/sec at',np.mean(temp_stack),'Celsius from',darktime,'sec of Darks')+'\n')
except:
    print('Dark Tourbles')

try:
    filters = set([item[0] for item in flatsdone])
    f.write('\n')
    hdu = pyfits.open(flatfiles[0])
    flate = hdu[0].header['DATE-OBS']
    hdu = pyfits.open(flatfiles[-1])
    flatm = hdu[0].header['DATE-OBS']

    if float(flate[11:13]) > 14.0: 
        if float(flatm[11:13]) < 10.0: 
            f.write('Evening and Morning Flats Obtained\n') 
        else:
            f.write('Evening Flats Obtained\n')
    elif float(flatm[11:13]) < 10.0:
        f.write('Morning Flats Obtained\n')
    else:
        f.write('No Flats Obtained\n')

    for filter in filters:
        f.write("{:2d} {:s} {:7s} {:s} {:6.0f}".format(len([item[1] for item in flatsdone if item[0] == filter]),'flats taken in',filter,'average counts =',np.mean([item[1] for item in flatsdone if item[0] == filter]))+'\n')
except:
    print('Flat Troubles')

f.write('\n')

try: 
    f.write("{:17s} {:7.2f} {:s}".format('Total Light Frame Time',tot_exp,'seconds')+'\n')
except:
    print('Total Light Time Troubles')

try:
    exf = set(expfilts)
    for filter in exf:
        f.write("{:5d} {:s} {:s}".format(expfilts.count(filter),'exposures in',filter)+'\n')
except:
    print('Per-Filter Light Time Troubles')

    f.write('\n')

hdu = pyfits.open(allfiles[0])
timerf = hdu[0].header['DATE-OBS']
f.write("{:22s} {:s}".format('First Exposure (UTC): ',timerf+'\n'))
hdu = pyfits.open(allfiles[-1])
timerl = hdu[0].header['DATE-OBS']
f.write("{:22s} {:s}".format('Last Exposure (UTC): ',timerl+'\n'))

fhr = float(timerf[11:13]) + (float(timerf[14:16])/60.)
lhr = float(timerl[11:13]) + (float(timerl[14:16])/60.)

if lhr < 12.0: lhr = lhr + 24.0

expo = lhr - fhr

f.write("{:22s} {:4.2f} {:s}".format('Observing period:',expo,'hours\n'))

f.write('\n')
f.write('Exposure List at: http://www.astro.rug.nl/~noelstorr/obs/sheets/OBSSHEET_'+str(sys.argv[1])+'.txt'+'\n')

f.close() 

