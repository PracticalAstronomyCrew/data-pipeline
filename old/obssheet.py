import os
import sys
import pyfits

root='/net/vega/data/users/observatory/images/'+str(sys.argv[1])+'/'

f = open("OBSSHEET_"+str(sys.argv[1])+".txt","w+")

f.write('BLAAUW OBSERVATORY OBSSHEET FOR '+str(sys.argv[1])+'\n')
f.write('--------------------------------------------------------------------------------------------'+'\n')
f.write('STL-6303E IMAGER ('+str(len(os.listdir(root+'/STL-6303E/i/')))+' frames)\n')
f.write('--------------------------------------------------------------------------------------------'+'\n')
f.write("{:28s} {:24s} {:15s} {:6s} {:5s} {:4s} {:4s}".format('FILENAME','DATE-OBS','IMAGETYP','FILTER','EXPT','XBIN','YBIN')+'\n')
f.write('--------------------------------------------------------------------------------------------'+'\n')

for filename in sorted(os.listdir(root+'/STL-6303E/i/')):
    if filename.endswith(".FIT") or filename.endswith(".fits"):
        hdu = pyfits.open(root+'/STL-6303E/i/'+filename)
        f.write("{:28s} {:24s} {:15s} {:6s} {:5.1f} {:4d} {:4d}".format(filename,hdu[0].header['DATE-OBS'],hdu[0].header['IMAGETYP'],hdu[0].header['FILTER'],hdu[0].header['EXPTIME'],hdu[0].header['CCDXBIN'],hdu[0].header['CCDYBIN'])+'\n')
        continue
    else:
        continue
f.write('--------------------------------------------------------------------------------------------'+'\n')
f.write('--------------------------------------------------------------------------------------------'+'\n')
f.write('STL-6303E GUIDER ('+str(len(os.listdir(root+'/STL-6303E/g/')))+' frames)\n')
f.write('--------------------------------------------------------------------------------------------'+'\n')
f.write("{:28s} {:24s} {:15s} {:6s} {:5s} {:4s} {:4s}".format('FILENAME','DATE-OBS','IMAGETYP','FILTER','EXPT','XBIN','YBIN')+'\n')
f.write('--------------------------------------------------------------------------------------------'+'\n')

for filename in sorted(os.listdir(root+'/STL-6303E/g/')):
    if filename.endswith(".FIT") or filename.endswith(".fits"):
        hdu = pyfits.open(root+'/STL-6303E/g/'+filename)
        f.write("{:28s} {:24s} {:15s} {:6s} {:5.1f} {:4d} {:4d}".format(filename,hdu[0].header['DATE-OBS'],hdu[0].header['IMAGETYP'],hdu[0].header['FILTER'],hdu[0].header['EXPTIME'],hdu[0].header['CCDXBIN'],hdu[0].header['CCDYBIN'])+'\n')
        continue
    else:
        continue
f.write('--------------------------------------------------------------------------------------------'+'\n')
f.write('--------------------------------------------------------------------------------------------'+'\n')
f.write('ST-7 IMAGER ('+str(len(os.listdir(root+'/ST-7/i/')))+' frames)\n')
f.write('--------------------------------------------------------------------------------------------'+'\n')
f.write("{:28s} {:24s} {:15s} {:6s} {:5s} {:4s} {:4s}".format('FILENAME','DATE-OBS','IMAGETYP','FILTER','EXPT','XBIN','YBIN')+'\n')
f.write('--------------------------------------------------------------------------------------------'+'\n')

for filename in sorted(os.listdir(root+'/ST-7/i/')):
    if filename.endswith(".FIT") or filename.endswith(".fits"):
        hdu = pyfits.open(root+'/ST-7/i/'+filename)
        f.write("{:28s} {:24s} {:15s} {:6s} {:5.1f} {:4d} {:4d}".format(filename,hdu[0].header['DATE-OBS'],hdu[0].header['IMAGETYP'],hdu[0].header['FILTER'],hdu[0].header['EXPTIME'],hdu[0].header['CCDXBIN'],hdu[0].header['CCDYBIN'])+'\n')
        continue
    else:
        continue
f.write('--------------------------------------------------------------------------------------------'+'\n')
f.write('--------------------------------------------------------------------------------------------'+'\n')
f.write('ST-7 GUIDER ('+str(len(os.listdir(root+'/ST-7/g/')))+' frames)\n')
f.write('--------------------------------------------------------------------------------------------'+'\n')
f.write("{:28s} {:24s} {:15s} {:6s} {:5s} {:4s} {:4s}".format('FILENAME','DATE-OBS','IMAGETYP','FILTER','EXPT','XBIN','YBIN')+'\n')
f.write('--------------------------------------------------------------------------------------------'+'\n')

for filename in sorted(os.listdir(root+'/ST-7/g/')):
    if filename.endswith(".FIT") or filename.endswith(".fits"):
        hdu = pyfits.open(root+'/ST-7/g/'+filename)
        f.write("{:28s} {:24s} {:15s} {:6s} {:5.1f} {:4d} {:4d}".format(filename,hdu[0].header['DATE-OBS'],hdu[0].header['IMAGETYP'],hdu[0].header['FILTER'],hdu[0].header['EXPTIME'],hdu[0].header['CCDXBIN'],hdu[0].header['CCDYBIN'])+'\n')
        continue
    else:
        continue
f.write('--------------------------------------------------------------------------------------------'+'\n')

f.close()
