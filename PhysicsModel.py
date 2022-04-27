import numpy as np
import pandas as pd
# input: données météo, localisation,  L, l, alpha, beta,

# output: energie produite par jour
radiation_Energy = pd.read_csv (r'C:\Users\jgerm\Documents\EPFL\MA2\05_SHS\Proto\Igl_h.csv')
lat = 46        #function parameter
phi = lat/180*np.pi

hoursTot = np.arange(0,365*24-1)
hours = hoursTot%24
days = hoursTot//24

deltas = 23.45* np.sin(2*np.pi*((days-81)/365))/180*np.pi







i=0