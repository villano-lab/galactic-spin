###############
### Imports ###
###############

#from sympy.utilities.lambdify import lambdify
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interactive, fixed, FloatSlider, HBox, Layout, Button, Label, Output, VBox
from IPython.display import display
import code7814_clean as wi7814
import matplotlib.image as mpimg
import sys
sys.path.append('../../python/')          # Defining path
import dataPython as dp
import scipy.integrate as si

# Note: getting so that the halo component/total RC curve updates as bh widgets update

####################
### Galaxy image ###
####################

# Import galaxy image
img = plt.imread("A_spiral_snowflake.jpg") # import special snowflake ngc 6814, 
                                           # which has visual diameter about 27.6 kpc
    
# Find the center by eye from the image
c_x = 1960
c_y = 1800

# Kpc limits, visual guess based on the galaxy in the image chosen:
minkpc = 0
maxkpc = 25

#############################
### Parameters for slider ###
#############################

# Visual scaling
scale = .2e9           # the number of theoretical black holes each graphed dot actually presents, 
                       # somewhat arbitrary but should be a number that does't require the plotting 
                       # too many or too few dots representing bh's
        
# units: scale = [#number of actual black holes / plotted dot]
kpctopixels = 50       # visual scaling, varies depending on size of galaxy image (and actual size of galaxy)
r1 = minkpc*kpctopixels
r2 = maxkpc*kpctopixels

# For number of black holes slider
minnumberBH = 1                       # min number of black holes
maxnumberBH = 100                     # max number of black holes
defaultnumber = 0.5 * maxnumberBH     # default number of bh's for slider
stepN = 0.1 * maxnumberBH             # step of # of bh's for slider

# For mass of black hole slider:
minmassBH = 0.1                 # solar masses, arbitrary
maxmassBH = 3.7                 # solar masses, just smaller then the smallest black hole ever discovered according to
                                # https://www.scientificamerican.com/gallery/the-smallest-known-black-hole/
defaultmass = 0.5 * maxmassBH   # default mass value for slider

# Generate random positions for the donut
rand_radius = np.random.uniform(r1,r2,int(maxnumberBH))
rand_angle = np.random.uniform(0,2*np.pi,int(maxnumberBH))  # angle 0 to 360 degrees for full circle (donut) for each bracket


def f(arraysize,Mbh):
        
    # Fractions: now changing the number of dots plotted within each bracket, 
    # which changes as the slider variable ("arraysize") changes
    
    # Change input to an integer
    arraysize = int(arraysize)     # units: dot
    
    # Trim to the first x elements (arraysize) of the pre-calculated radius arrays for each bracket
    radius_trim = rand_radius[:arraysize]
    angle_trim = rand_angle[:arraysize]
    
    # Plot for each bracket, two equations for each bracket
    x = c_x + radius_trim*np.cos(angle_trim)     # x coordinates
    y = c_y + radius_trim*np.sin(angle_trim)     # y coordinates
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
    f.set_figheight(15)
    f.set_figwidth(30)
    
    # Below: changing the physical size of the plotted dots as the BH mass slider changes. 
    # Note: the if else statement is fancy but not necessary 
    
    # WIP: getting so that the halo component/total RC curve updates as BH widgets update
   
    Me = Mbh*arraysize*scale*M/max(M)    # units: Msun/bh * dot *bh/dot = Msun
    velocity = np.sqrt(Me*G/rcut)               # is it rc or just r???? units: km/s
     
    Mbh = 1.5*Mbh                        # judging by eye
    if .1 <= Mbh<1:
        Mbh = Mbh**1.5
    elif 1 <= Mbh<2:
        Mbh = Mbh**2
    else:
        Mbh = Mbh**3                     # display size of each marker
        
    # First plot - image with black holes
    ax1.scatter(x,y,color="r",marker='o',s=Mbh)
    ax1.imshow(img)
    ax1.axis('off')
    
    # Second plot - rotation curve   
    ax2.plot(r,h(r,Mbh,arraysize),label=("Dark Matter Halo"),color='green')
    ax2.errorbar(r,wi7814.v_dat,yerr=wi7814.v_err1,fmt='bo',label='Data')
    ax2.plot(r,wi7814.bulge_fitted,label=("Bulge"),color='orange')
    ax2.plot(r,wi7814.disk_fitted,label=("Disk"),color='purple')
    ax2.plot(r,wi7814.gas_fitted,label=("Gas"),color='blue')
    ax2.plot(r,wi7814.totalvelocity(r,Mbh,arraysize),label=("Total Curve"),color='red')
    ax2.set_xlim([minkpc, 19])
    ax2.set_ylim([0, 400])
    ax2.set_title('NGC 7814',fontsize = 40)
    ax2.set_ylabel('Velocity [km/s]',fontsize = 30)
    ax2.set_xlabel('radius [kpc]',fontsize = 30)
    ax2.legend(loc='upper right',prop={'size': 20},ncol=3)
   
    residuals = wi7814.v_dat - wi7814.totalvelocity(wi7814.radius,Mbh,arraysize)
 
    # Determining errors
    errors = wi7814.v_err1**2 #second term is inclination uncertainty
    # Chi squared
    chisquared = np.sum(residuals**2/errors**2)
    #chisquared = stats.chisquare(v_dat,totalcurve(r,M,bpref,dpref,rc,rho00,gpref))
    reducedchisquared = chisquared * (1/(len(wi7814.radius)-6))
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax2.text(0.4,360,r"Reduced $\chi^2$:"+'\n'+"{:.2f}".format(reducedchisquared),bbox=props,size=30)
       
style = {'description_width': 'initial'}
layout = {'width':'600px'}

################################
######## Define Sliders ########
################################

# Mass of each black hole
Mbh = FloatSlider(min=minmassBH, max=maxmassBH, step=minmassBH, 
                value=defaultmass,
                description='Mass of each lil black holes [$M_{\odot}$]', 
                readout=True,
                readout_format='.1f', 
                orientation='horizontal', 
                style=style, layout=layout)

# Number of projected black dots slider
arraysize = FloatSlider(min=minBH, max=maxBH, step=stepN, 
                value=defaultnumber, 
                description='Number of lil black holes multiplied by scale %.0e'%scale, 
                readout=True,
                readout_format='.2d', 
                orientation='horizontal', 
                style=style, layout=layout)

def interactive_plot(f):
    interact = interactive(f, arraysize=arraysize, Mbh=Mbh, continuous_update=False)
    return interact

################################
########### Button #############
################################

# Button to revert back to Best Fit
button = Button(
    description="Best Fit",
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    icon='check')
out = Output()

def on_button_clicked(_):
    Mbh.value = defaultmass
    arraysize.value = defaultnumber
button.on_click(on_button_clicked)