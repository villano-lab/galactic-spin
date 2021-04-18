###############
### Imports ###
###############

import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interactive, fixed, FloatSlider, HBox, Layout, Button, Label, Output, VBox
from IPython.display import display
import code5533_clean as wi5533
import sys
sys.path.append('../../python/')          # Defining path
import dataPython as dp

####################
### Galaxy image ###
####################

# Import galaxy image
img = plt.imread("NGC_5533/pictures/A_spiral_snowflake.jpg") # import special snowflake ngc 6814, 
                                                             # which has visual diameter about 27.6 kpc
    
# Find the center by eye from the image
c_x = 1960
c_y = 1800

# Kpc limits, visual guess based on the galaxy in the image chosen:
minkpc = 0
maxkpc = 100

#############################
### Parameters for slider ###
#############################
      
# units: scale = [#number of actual black holes / plotted dot]
kpctopixels = 20       # visual scaling, varies depending on size of galaxy image (and actual size of galaxy)
r1 = minkpc*kpctopixels
r2 = maxkpc*kpctopixels

# For number of black holes slider
minnumberBH = 10                      # min number of black holes
maxnumberBH = 1000                    # max number of black holes
defaultnumber = 510                   # default number of bh's for slider
stepN = minnumberBH                   # step of # of bh's for slider

# For mass of black hole slider:
minmassBH = 0.1                 # solar masses, arbitrary
maxmassBH = 3.8                 # solar masses, just smaller then the smallest black hole ever discovered according to
                                # https://www.scientificamerican.com/gallery/the-smallest-known-black-hole/
defaultmass = 1.5               # default mass value for slider
stepM = minmassBH               # step of mass of bh's

# For number of black holes at the center slider
minrhoBH = 1e4                  # min number of black holes at the center
maxrhoBH = 1.5e6                # max number of black holes at the center
defaultrho = 4.2e5              # default number of bh's at the center for slider
stepRHO = minrhoBH              # step of # of bh's at the center for slider

# Generate random positions for the donut
rand_radius = lambda rad1,rad2: np.random.uniform(rad1,rad2,int(maxnumberBH))
rand_angle = np.random.uniform(0,2*np.pi,int(maxnumberBH))  # angle 0 to 360 degrees for full circle (donut) for each bracket


####################################
### Plotting function for widget ###
####################################

def f(rho0,arraysize,mBH):
        
     # Change input to an integer
    arraysize = int(arraysize)     # units: dot
    
    # Random radii for the galaxy image
    # Trim to the first x elements (arraysize) of the pre-calculated radius arrays for each bracket
    radius_trim = rand_radius(r1,r2)[:arraysize]
    angle_trim = rand_angle[:arraysize]
    
    # x and y coordinates for plotting
    x = c_x + radius_trim*np.cos(angle_trim)     # x coordinates
    y = c_y + radius_trim*np.sin(angle_trim)     # y coordinates
    
    # Random radii for the plot
    radius_plot = rand_radius(minkpc,maxkpc)[:arraysize]
    radius_plot = np.sort(radius_plot)           # sort array
    radius_plot[0] = 0.2    # first element of the radius should be close to zero because spline function won't plot up to zero
      
    # Set up two plots next to each other
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
    f.set_figheight(10)
    f.set_figwidth(32)
    
    # First plot - image with black holes
    ax1.scatter(x,y,color="orangered",marker='o',s=mBH*10)      # s changes the size of the dots on the plot
    ax1.scatter(c_x,c_y,color="orangered",marker='o',s=rho0/1e3)
    ax1.imshow(img)
    ax1.set_title("Arbitrary face-on galaxy for visual representation")
    ax1.set_xlim(0,3970)
    ax1.set_ylim(0,3970)
    ax1.axis('off')
    
    # Second plot - rotation curve   
    ax2.plot(radius_plot,wi5533.halo_BH(radius_plot,mBH,arraysize,rho0),label=("Dark Matter Halo - Tiny Black Holes"),color='green')
    ax2.errorbar(wi5533.r_dat,wi5533.v_dat,yerr=wi5533.v_err1,fmt='bo',label='Data')
    ax2.plot(radius_plot,wi5533.blackhole(radius_plot,wi5533.best_M),label=("Central Black Hole"),color='black')
    ax2.plot(radius_plot,wi5533.bulge(radius_plot,wi5533.best_bpref),label=("Bulge"),color='orange')
    ax2.plot(radius_plot,wi5533.disk(radius_plot,wi5533.best_dpref),label=("Disk"),color='purple')
    ax2.plot(radius_plot,wi5533.gas(radius_plot,wi5533.best_gpref),label=("Gas"),color='blue')
    ax2.plot(radius_plot,
             wi5533.totalvelocity(radius_plot,mBH,arraysize,rho0,wi5533.best_M,wi5533.best_bpref,wi5533.best_dpref,wi5533.best_gpref),
                                  label=("Total Curve"),color='red')
    ax2.set_title('NGC 5533',fontsize = 40)
    ax2.set_ylabel('Velocity [km/s]',fontsize = 25)
    ax2.set_xlabel('radius [kpc]',fontsize = 25)
    ax2.tick_params(axis='x', labelsize=16)
    ax2.tick_params(axis='y', labelsize=16)
    ax2.set_xlim(0,100)
    ax2.set_ylim(0,400)
    ax2.legend(loc='upper center',prop={'size': 16},ncol=3)
   
    # Residuals
    residuals = wi5533.v_dat - wi5533.totalvelocity(wi5533.r_dat,mBH,arraysize,rho0,wi5533.best_M,wi5533.best_bpref,wi5533.best_dpref,wi5533.best_gpref)
 
    # Determining errors
    errors = wi5533.v_err1**2 #second term is inclination uncertainty
    # Chi squared
    chisquared = np.sum(residuals**2/errors**2)
    reducedchisquared = chisquared * (1/(len(wi5533.r_dat)-6))
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax2.text(73,330,r"Reduced $\chi^2$:"+'\n'+"{:.2f}".format(reducedchisquared),ha='left',va='top',bbox=props,size=20)
       
style = {'description_width': 'initial'}
layout = {'width':'800px'}

################################
######## Define Sliders ########
################################

# Number of projected black dots slider
rho0 = FloatSlider(min=minrhoBH, max=maxrhoBH, step=stepRHO, 
                value=defaultrho, 
                description='Number of tiny black holes at the center dense region (increasing by {:.0f})'.format(stepRHO), 
                readout=True,
                readout_format='.1d', 
                orientation='horizontal', 
                style=style, layout=layout)


# Number of projected black dots slider
arraysize = FloatSlider(min=minnumberBH, max=maxnumberBH, step=stepN, 
                value=defaultnumber, 
                description='Number of tiny black holes in the outer region (increasing by {:.0f})'.format(stepN), 
                readout=True,
                readout_format='.2d', 
                orientation='horizontal', 
                style=style, layout=layout)

# Mass of each black hole
mBH = FloatSlider(min=minmassBH, max=maxmassBH, step=stepM, 
                value=defaultmass,
                description='Mass of each tiny black hole (in solar masses, increasing by {:.1f})'.format(stepM), 
                readout=True,
                readout_format='.1f',
                orientation='horizontal', 
                style=style, layout=layout)



def interactive_plot(f):
    interact = interactive(f, rho0=rho0, arraysize=arraysize, mBH=mBH, continuous_update=False)
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
    mBH.value = defaultmass
    arraysize.value = defaultnumber
    rho0.value = defaultrho
button.on_click(on_button_clicked)