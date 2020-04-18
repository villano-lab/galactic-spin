################################
########### Imports ############
################################

import sys
sys.path.append('../../python/')          # Defining path

import numpy as np                        
import matplotlib.pyplot as plt

import NGC5533_functions as nf            # Components
import noordermeer as noord               # Traced data of Galaxy NGC 5533
import fitting_NGC5533 as fitting         # Fitting parameters for best fit values

from ipywidgets import interactive, fixed, FloatSlider, HBox, Layout, Button, Label, Output, VBox
from IPython.display import display

import warnings
warnings.filterwarnings("ignore")         #ignore warnings

################################
############ Data ##############
################################

data = noord.data
data_total = noord.data_total
r_dat = noord.r_dat
v_dat = noord.v_dat
v_err0 = noord.v_err0
v_err1 = noord.v_err1

################################
######### Components ###########
################################

def blackhole(r,M):
    return nf.bh_v(r,M,load=False)

def bulge(r,bpref):
    return bpref*nf.b_v(r,load=True)

def disk(r,dpref):
    return dpref*nf.d_thief(r)

def halo(r,rc,rho00):
    return nf.h_v(r,rc,rho00,load=False)

def gas(r,gpref):
    return gpref*nf.g_thief(r)

def totalcurve(r,M,bpref,dpref,rc,rho00,gpref):
    total = np.sqrt(blackhole(r,M)**2 
                    + bulge(r,bpref)**2 
                    + disk(r,dpref)**2
                    + halo(r,rc,rho00)**2
                    + gas(r,gpref)**2)
    return total

################################
###### Fitting Parameters ######
################################

best_M = fitting.f_M
best_bpref = fitting.f_c
best_dpref = fitting.f_pref
best_rc = fitting.f_rc
best_rho00 = fitting.f_hrho00
best_gpref = fitting.f_gpref
#delf = fitting.delf

################################
###### Plotting Function #######
################################

# Define plotting function
def f(M,bpref,dpref,rc,rho00,gpref):
    
    # Define r
    r = np.linspace(0.1,100,1000)
    
    # Plot
    plt.figure(figsize=(9,7))
    plt.xlim(0,100)
    plt.ylim(0,360)
    
    plt.errorbar(r_dat,v_dat,yerr=v_err1,fmt='bo',label='Data')
    plt.plot(r,blackhole(r,M),label=("Black Hole"),color='black')
    plt.plot(r,bulge(r,bpref),label=("Bulge"),color='orange')
    plt.plot(r,disk(r,dpref),label=("Disk"),color='purple')
    plt.plot(r,halo(r,rc,rho00),label=("Halo"),color='green')
    plt.plot(r,gas(r,gpref),label=("Gas"),color='blue')
    plt.plot(r,totalcurve(r,M,bpref,dpref,rc,rho00,gpref),label=("Total Curve"),color='red')
    plt.fill_between(r,
                     noord.greyb_bottom(r),noord.greyb_top(r),
                     color='#dddddd')
    plt.title("Interactive Rotation Curve - Galaxy: NGC 5533")
    plt.xlabel("Radius (kpc)")
    plt.ylabel("Velocity (km/s)")
    
    # Chi squared and reduced chi squared
    # Residuals
    r = np.linspace(0.1,100,69)
    residuals = v_dat - totalcurve(r_dat,M,bpref,dpref,rc,rho00,gpref)
    # Determining errors
    errors = np.sqrt(v_err1**2 + noord.band**2) #second term is inclination uncertainty
    # Chi squared
    chisquared = np.sum(residuals**2/errors**2)
    #chisquared = stats.chisquare(v_dat,totalcurve(r,M,bpref,dpref,rc,rho00,gpref))
    reducedchisquared = chisquared * (1/(len(r_dat)-6))
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    plt.text(80,170,r"$\chi^2$: {:.5f}".format(chisquared)+'\n'+r"Reduced: {:.5f}".format(reducedchisquared),bbox=props)
    #plt.text(80,150,,bbox=props)
    
    plt.legend(loc='upper right')
    plt.annotate('Can you get the Reduced $\chi^2$ to zero?',
            xy=(0, 0), xytext=(510, 430),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=22, ha='left')
    textt= 'In a strictly statistical sense,  a Reduced $\chi^2$ of zero indicates \na perfect fit. However, such a fit may be artificial and bear no \nphysical meaning. In this fit, the Reduced $\chi^2$ is around 1 due \nprimarily to the gas component, which is actually fixed \n(according to the physical characteristics of the Hydrogen gas it \nrepresents, see our video for more details). Though here we allow \nyou to break the laws of nature and move each component around \nas you please. See how "good" of a fit you can get!'
    plt.annotate(textt,
            xy=(0, 0), xytext=(510, 280),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=14, ha='left')
    plt.annotate('source: E.  Noordermeer.The  rotation  curves  of  flattened  sérsic  bulges.MNRAS,385(3):1359–1364, Apr 2008',
            xy=(0, 0), xytext=(0,0),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=10, ha='left', va='bottom')
    
    plt.show()

###############################
######### Appearance ##########
###############################

style = {'description_width': 'initial'}
layout = {'width':'600px'}

################################
######## Define Sliders ########
################################

M = FloatSlider(min=0, max=5e9, step=1e8, 
                value=best_M, 
                description='Black Hole Mass [$M_{\odot}$]', 
                readout_format='.2e', 
                orientation='horizontal', 
                style=style, layout=layout)

bpref = FloatSlider(min=0, max=5, step=0.1, 
                    value=best_bpref, 
                    description='Bulge Prefactor', 
                    readout_format='.2f', 
                    orientation='horizontal', 
                    style=style, layout=layout)

dpref = FloatSlider(min=0, max=5, step=0.1, 
                    value=best_dpref, 
                    description='Disk Prefactor', 
                    readout_format='.2f', 
                    orientation='horizontal', 
                    style=style, layout=layout)

#rc = FloatSlider(min=0, max=5, step=0.1, value=best_rc, description='Halo Core Radius [kpc]', readout_format='.2f', orientation='horizontal', style=style, layout=layout)
rc = fixed(best_rc)

rho00 = FloatSlider(min=0, max=1e9, step=1e7, 
                    value=best_rho00, 
                    description='Halo Surface Density [$M_{\odot} / pc^3$]', 
                    readout_format='.2e', 
                    orientation='horizontal', 
                    style=style, layout=layout)

gpref = FloatSlider(min=0, max=5, step=0.1, 
                    value=best_gpref, 
                    description='Gas Prefactor', 
                    readout_format='.2f', 
                    orientation='horizontal', 
                    style=style, layout=layout)

################################
######### Interactive ##########
################################

def interactive_plot(f):
    interact = interactive(f, M = M, 
                               bpref = bpref, 
                               dpref = dpref, 
                               rc = rc,
                               rho00 = rho00,
                               gpref = gpref,
                               continuous_update=False)
    return interact

################################
########### Button #############
################################

button = Button(
    description="Best Fit",
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    icon='check')
out = Output()

def on_button_clicked(_):
    M.value = best_M
    bpref.value = best_bpref
    dpref.value = best_dpref
    rho00.value = best_rho00
    gpref.value = best_gpref

button.on_click(on_button_clicked)