# Overview
This is a repository for an interactive fitting graphic for galactic rotation curves.

# Abstract
*The following abstract was written for a presentation which focused on the interactive fitting tool.*

“The orbital velocities of matter in galaxies clearly signal the existence of dark matter.” This is the stance of a large portion of the scientific community, but how can we really appreciate the reasons behind this statement and its implications? Our research focuses on understanding the mathematical modeling behind the orbital velocities of galactic matter.  By comparing our models to real galactic data, we can visualize both how a model using only luminous matter falls short and how including dark matter might bring our estimations of the galactic orbital velocities into alignment with measured values. We make our results accessible through a computer application that allows people to observe this modeling firsthand regardless of their own math or physics background. Tools like the one we present can help the general public understand and appreciate the concepts behind dark matter and reduce the barrier to entry for early-career scientists trying to learn more about dark matter.

# Instructions
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/villano-lab/galactic-spin/master?filepath=binder%2FRotation_Curve_Sliders.ipynb)
<br /> To run the interactive fitting tool, click on the binder button above. Please be patient when waiting for the environment to load; **note that it may take about 10 minutes to load**. Once the notebook is open, in the top bar, select `Cell`, then choose `Run All`. When both cells are finished running, a plot with sliders will appear beneath the visible code. Enjoy!

The above link is to a version of the notebook made specifically to be run on binder with minimal code visible.
For those interested, [here](https://mybinder.org/v2/gh/villano-lab/galactic-spin/master?filepath=binder%2FRotation_Curve_Sliders-With-Code.ipynb)
is a version with the full code visible. You can also run either version locally by cloning the repository and running one of the notebooks in the `binder` directory.

## Working Browsers
The following browsers have been tested with our notebook in binder.  
Please note that, unfortunately, the sliders do not appear to work in any mobile browser.
| Browser | Date Checked | Status |
|:--------|:------------:|--------|
|         | **Desktop Browsers** ||
| Firefox | 23/04/2020   | Working|
| Safari  | 16/04/2020   | Working|
| Chrome  | 23/04/2020   | Working|
| Edge    | 17/04/2020   | Working|
| Internet Explorer | 17/04/2020 | Page did not load within 10 minutes. |
|         | **Mobile Browsers** | |
|Firefox Mobile | 17/04/2020 | Sliders could not be used. |
|Safari Mobile  | 22/04/2020 | Sliders could not be used. |
|Chrome Mobile  | 17/04/2020 | Sliders could not be used. |

# References
All of our data and the equations used in most of our calculations comes from Noordermeer (2008). We also used Casertano 1983 for the disk component equations and Karukes, et al., for the halo component.

Casertano, Stefano. “Rotation Curve of the Edge-on Spiral Galaxy NGC 5907: Disc and Halo Masses.” Mon. Not. R. Astr. Soc. 203 (August 17, 1983): 735–47. [https://doi.org/10.1093/mnras/203.3.735](https://doi.org/10.1093/mnras/203.3.735). 

Karukes, E. V., P. Salucci, and Gianfranco Gentile. "The dark matter distribution in the spiral NGC 3198 out to 0.22 Rvir." Astronomy & Astrophysics 578 (2015): A13. https://doi.org/10.1051/0004-6361/201425339

Noordermeer, Edo. “The Rotation Curves of Flattened Sersic Bulges.” Mon. Not. R. Astron. Soc., April 2008. [https://doi.org/10.1111/j.1365-2966.2008.12837.x](https://doi.org/10.1111/j.1365-2966.2008.12837.x).

# Contributors
Judit Bergfalk  
Kitty Harris  
Raphael Hatami  
Anthony Villano, Ph.D.
