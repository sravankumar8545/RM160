import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import pandas as pd
import glob
from astropy.time import Time

file_pattern = 'mrk142.*.scale.txt'
file_list = sorted(glob.glob(file_pattern))

data_list = []
z=0.0449

for filename in file_list:
    data = np.loadtxt(filename)
    wavelength = data[:, 0]/(1+z)
    flux = data[:, 1]/(1+z)**3
    flux_err = data[:, 2]/(1+z)
    
    # Define the wavelength ranges
    range1 = (wavelength >= 4792.3) & (wavelength <= 4933.4)
    range2 = (wavelength >= 5100) & (wavelength <= 5300)
    
    # Extract the data for each range
    data_range1 = np.array(list(zip(wavelength[range1], flux[range1], flux_err[range1])), 
                            dtype=[('wavelength', float), ('flux', float), ('flux_err', float)])
    #data_range2 = np.array(list(zip(wavelength[range2], flux[range2], flux_err[range2])), 
                            #dtype=[('wavelength', float), ('flux', float), ('flux_err', float)])
    
    # Append the data to the list
    data_list.append((data_range1))
"""
df3 = pd.read_csv('mrk142.scale.info.dat', sep='\s+')
HJD=np.array(df3['HJD'])
#HJD=HJD-2450000
hjd_time = Time(HJD, format='jd')

#Fbeta=Fbeta*0.01
mjd_time = hjd_time.mjd
time=hjd_time-4000
"""
# Save the data_list as a text file
with open('Hb.txt', 'w') as f:
    num_files = len(file_list)
    f.write(f"{num_files} {sum(len(data_range1)  for data_range1 in data_list)}\n")
    
    for i, (data_range1) in enumerate(data_list):
        #f.write(f"# {time[i]}\n")  # assuming mjd_time is a list of MJD times
        np.savetxt(f, data_range1, fmt='%10.4e %10.4e %10.4e')
        #np.savetxt(f, data_range2, fmt='%10.4e %10.4e %10.4e')
        f.write("\n")
