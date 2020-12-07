#SDSSRM_11_Pix_Filter.py creates a median spectra (or flux error or S/N array, depending on the criteria desired) for comparison to the original spectra, in order to eliminate spikes (bad pixels) in the data. 

import math
import numpy as np
import scipy
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt

def pixel_filter(wavelength, flux, fluxerr, Cont_Type):

    filterval=5
    filterval2=6

    #Left/right side of interval - to be filled
    new_left_flux=np.zeros(filterval)
    new_right_flux=np.zeros(filterval)

    #Mask to be filled with non-nan indices         
    indices=[]

    for k in np.arange(0,len(flux),1):
        if (math.isnan(flux[k]) == False): #Get rid of nans so the medians are accurate/not crazy. 
           indices.append(k)

    #These next two blocks create mirrored versions of the ends of the spectra, so that median points can be determined for each point along the original spectra.


    #Define left/right sides of flux array (maybe -1 should be 0? [or something to get the last element :])
    if Cont_Type=="S/N":
       #Horizontally flip the fluxes: #Just replace this with fluxerr and see what happens?
       end=np.flipud(flux[indices][-filterval2:-1])/np.flipud(fluxerr[indices][-filterval2:-1])
       #end=fluxerr[indices][-filterval2:-1]
       end_wave=wavelength[indices][-filterval2:-1]
       #start=fluxerr[indices][0:filterval]
       start=(flux[indices][0:filterval])/(fluxerr[indices][0:filterval])
       start_wave=wavelength[indices][0:filterval]
    elif Cont_Type=="Fluxerrs":
       #Horizontally flip the fluxes: #Just replace this with fluxerr and see what happens?
       end=fluxerr[indices][-filterval2:-1]
       end_wave=wavelength[indices][-filterval2:-1]
       start=fluxerr[indices][0:filterval]
       start_wave=wavelength[indices][0:filterval]
    elif Cont_Type=="Fluxes":
       #Horizontally flip the fluxes: #Just replace this with fluxerr and see what happens?
       end=flux[indices][-filterval2:-1]
       end_wave=wavelength[indices][-filterval2:-1]
       start=flux[indices][0:filterval]
       start_wave=wavelength[indices][0:filterval]

    left_median=np.nanmedian(start)
    right_median=np.nanmedian(end)

    #Save absolute deivations - to be computed below:
    Flux_Devs_Left=np.zeros(filterval)
    Flux_Devs_Right=np.zeros(filterval)

    #Now flipping the mirrored spectra over the left and right medians:
    for k in np.arange(0,filterval,1):        
        Flux_Devs_Right[k]=(end[k]-right_median)
        Flux_Devs_Left[k]=(start[k]-left_median)
        
    for k in np.arange(0,filterval,1):
        new_right_flux[k]=(end[k] - Flux_Devs_Right[k])
        new_left_flux[k]=(start[k] - Flux_Devs_Left[k])

 
    if Cont_Type=="S/N":
       extended_flux_array=np.concatenate((new_left_flux,flux/fluxerr,new_right_flux),axis=0)
    elif Cont_Type=="Fluxerrs":
       extended_flux_array=np.concatenate((new_left_flux,fluxerr,new_right_flux),axis=0)
    elif Cont_Type=="Fluxes":
       extended_flux_array=np.concatenate((new_left_flux,flux,new_right_flux),axis=0)

    #extended_flux_array=np.concatenate((new_left_flux,flux/fluxerr,new_right_flux),axis=0)
    continuum = [np.nanmedian(extended_flux_array[l-filterval:l+filterval]) for l in np.arange(filterval,len(flux)+filterval,1)]
    continuum = np.asarray(continuum)


    return continuum
