###############
### Imports ###
###############

import numpy as np
import sys
sys.path.append('../../python/')
import dataPython as dp
import scipy.integrate as si
from scipy.interpolate import InterpolatedUnivariateSpline

import NGC5533_functions as nf            # Components
import noordermeer as noord               # Traced data of Galaxy NGC 5533
import fitting_NGC5533 as fitting         # Fitting parameters for best fit values

################################
############ Data ##############
################################

data = noord.data
data_total = noord.data_total
r_dat = noord.r_dat
v_dat = noord.v_dat
v_err0 = noord.v_err0
v_err1 = noord.v_err1

#####################
### Interpolation ###
#####################

def interpd(x,y):
    return InterpolatedUnivariateSpline(x,y,k=4)

################################
######### Components ###########
################################

def blackhole(r,M):
    x = np.sort(r)
    y = nf.bh_v(r,M,load=False)
    polynomial = interpd(x,y)
    return polynomial(r)

def bulge(r,bpref):
    x = np.sort(r)
    y = bpref*nf.b_v(r,load=True)
    polynomial = interpd(x,y)
    return polynomial(r)

def disk(r,dpref):
    x = np.sort(r)
    y = dpref*nf.d_thief(r)
    polynomial = interpd(x,y)
    return polynomial(r)

def gas(r,gpref):
    x = np.sort(r)
    y = gpref*nf.g_thief(r)
    polynomial = interpd(x,y)
    return polynomial(r)

################################
###### Fitting Parameters ######
################################

best_M = fitting.f_M
best_bpref = fitting.f_c
best_dpref = fitting.f_pref
rcut = fitting.f_rc
rho0 = fitting.f_hrho00
best_gpref = fitting.f_gpref

# Constants
G = 4.30091e-6            # gravitational constant (kpc/solar mass*(km/s)^2)

#################################
### Calculating enclosed mass ### 
#################################

# NFW (dark halo) density profile
rho_NFW = lambda r: rho0 / ((r/rcut)*(1+r/rcut)**2)

# Isothermal (dark halo) density profile
rho_ISO = lambda r: rho0 / (1+(r/rcut)**2)

# Inner function
#mass_inner = lambda r: rho_NFW(r) * 4 * np.pi * r**2
mass_inner = lambda r: rho_ISO(r) * 4 * np.pi * r**2

# Mass integral: total mass at radius r (kpc)
#mass_r = lambda r: si.quad(mass_inner, 0, r)   
# Integral keeps giving me errors, so I used Mathematica to do the integral for me, this is the result:
def mass_r(r):
    return 4 * rcut**3 * np.pi * rho0 * (-1 + rcut/(rcut+r) - np.log(rcut) + np.log(rcut+r))

########################################################
### Calculating halo velocity using only black holes ###
########################################################

def halo_BH(r,mBH): 
    x = np.sort(r)
    y = mBH * np.sqrt(G * mass_r(r)/r)
    polynomial = interpd(x,y)
    return polynomial(r)

##################################
### Calculating total velocity ###
##################################

def totalvelocity(r,mBH,M,bpref,dpref,gpref):
    total = np.sqrt(blackhole(r,M)**2 
                    + bulge(r,bpref)**2 
                    + disk(r,dpref)**2
                    + halo_BH(r,mBH)**2
                    + gas(r,gpref)**2)
    return total