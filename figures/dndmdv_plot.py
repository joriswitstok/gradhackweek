import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import glob
import re
import os
pwd = os.getcwd()
import itertools

# some functions for making custom colourmaps and plotting background slopes
def plotBackground(ax, x0, y0, colour, zorder0):
    cmap=makeCmap('#011627','backgroundColour')
    yMin=y0*np.power(x0/1e20,2)
    yMax=y0*np.power(x0/1e-20,2)
    nColours=25
    change=0.01
    for i in range(nColours-1):
        ax.fill([1e-20,1e-20,1e20],[yMax*change**(i),yMin*change**(i),yMin*change**(i)],c=cmap((i+1)/nColours),zorder=(i+1)+zorder0)
    newZord = i+1+zorder0
    return ax, newZord

def makeCmap(hexColour, name, zeroColour='#FFFFFF'):
    r0,g0,b0=mpl.colors.hex2color(zeroColour)
    r,g,b=mpl.colors.hex2color(hexColour)
    cdict = {'red':   ((0.0, r0, r0),
                   (1.0, r, r)),
         'green': ((0.0, g0, g0),
                   (1.0, g, g)),
         'blue':  ((0.0, b0, b0),
                   (1.0, b, b))
        }
    cmap = mpl.colors.LinearSegmentedColormap(name, cdict)
    return cmap

'''
sPlot.grid('off')
sPlot.axis('off')
sPlot.set_xlim(0,1)
sPlot.set_ylim(0,1)

nFile=0
for fileName in glob.glob('data/*.txt'):
    print(fileName)
    with open(fileName, 'r') as f:
        footer = f.readlines()[-1]
    _,name,colour,linestyle,_=re.split(r'/+', footer)
    data=np.atleast_2d(np.genfromtxt(fileName))
    data=data[data[:,1]>0,:]
    nPlot.plot(data[:,0],data[:,1],zorder=zord,c=colour,ls=linestyle)
    zord+=1
    #nPlot.text(textPos[index][0],textPos[index][1],text[index],color=colours[index])
    if np.shape(data)[1] > 2: #if uncertainty columns are included
        xs = np.concatenate((data[:,0],data[:,0][::-1]))
        ys = np.concatenate(((data[:,1]+data[:,2]),(data[:,1]-data[:,3])[::-1]))
        nPlot.fill(xs, ys, alpha=0.25,zorder=zord,c=colour)
        zord+=1

    xText=0.03+0.25*(nFile % 4)
    yText=0.9-0.15*int(nFile/4)
    sPlot.scatter(xText-0.015,yText+0.03,s=100,c=colour)
    sPlot.text(xText,yText,name,fontsize=14)
    nFile+=1
'''

gs = GridSpec(1, 1, bottom=.12, top=.95, left=.1, right=.98, hspace=0)
fig = plt.figure()
ax1 = fig.add_subplot(gs[0])
#nGrid = mpl.gridspec.GridSpec(5,1)
#nPlot = plt.subplot(nGrid[0:4,0])
#sPlot = plt.subplot(nGrid[4,0])

zord = -100 # for the background gradients
xlo, xhi = 1e-8, 1e16
ylo, yhi = 1e-40, 1e5
M_all = np.array([xlo, xhi])
#M_all = np.logspace(xlo, xhi, 500)

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlim(xlo, xhi)
ax1.set_ylim(ylo, yhi)
ax1.set_xlabel(r'Mass [M$_\odot]$')
ax1.set_ylabel(r'Number density, $dN / (dM dV)$ [M$_\odot^{-1}$ pc$^{-3}]$')

plotBackground(ax1, xhi*1e2, ylo, 'k', zorder0=zord)


## Planck cosmology
Omh2 = 0.143
Och2 = 0.012
Obh2 = 0.00237
H0 = 67.27
Ostar = 0.003

mass_density_gcm3 = 9.9e-30
mass_density_Mspc3 = mass_density_gcm3 * (100*3e16)**3 / (1000*2e30)

matter = (mass_density_Mspc3 * Omh2 / (H0*0.01)**2) / M_all**2
baryons = (mass_density_Mspc3 * Obh2 / (H0*0.01)**2) / M_all**2
cdm = (mass_density_Mspc3 * Och2 / (H0*0.01)**2) / M_all**2


## Obs: planets
mplan, ndplan = np.genfromtxt(pwd + '/../data/planets_obs.txt').T
ndplan *= Ostar
ax1.plot(mplan, ndplan, c='#F0E054', ls='-', label='Planets')


## Obs: galaxies
mgal_exp, ndgal = np.genfromtxt(pwd + '/../data/galaxies_obs.txt').T
mgal = 10**mgal_exp

idxs = np.nonzero(ndgal)
mgal_new = mgal[idxs]
ndgal_new = ndgal[idxs]

ax1.plot(mgal_new, ndgal_new, c='#CC2EC7', ls='-', label='Galaxies, SDSS')


#ax1.plot(1, 1, c='#FFFFFF', ls='-', label=' ') # dummy legend entry
#ax1.plot(1, 1, c='#FFFFFF', ls='-', label=' ') # dummy legend entry


## Simulations: galaxies -- Illustris TNG300
mgal_tng = np.genfromtxt(pwd + '/../data/illustris/mbins.txt').T

ndgal_tng3 = np.genfromtxt(pwd + '/../data/illustris/dNbydMdV_Mstar_TNG300.txt').T
idxs = np.nonzero(ndgal_tng3)
mgal_tng3 = mgal_tng[idxs]
ndgal_tng3_new = ndgal_tng3[idxs]

ax1.plot(mgal_tng3, ndgal_tng3_new, c='#EA5B42', ls='-', label='Galaxies, Illustris TNG300')

ndgal_tng3_vir = np.genfromtxt(pwd + '/../data/illustris/dNbydMdV_Mvir_TNG300.txt').T
idxs = np.nonzero(ndgal_tng3_vir)
mgal_tng3_vir = mgal_tng[idxs]
ndgal_tng3_vir_new = ndgal_tng3_vir[idxs]

ax1.plot(mgal_tng3_vir, ndgal_tng3_vir_new, c='#802313', ls='-', label=r'TNG300, M$_{\rm vir}$')

## Illustris TNG100
ndgal_tng1 = np.genfromtxt(pwd + '/../data/illustris/dNbydMdV_Mstar_TNG100.txt').T
idxs = np.nonzero(ndgal_tng1)
mgal_tng1 = mgal_tng[idxs]
ndgal_tng1_new = ndgal_tng1[idxs]

ax1.plot(mgal_tng1, ndgal_tng1_new, c='#4284EA', ls='-', label='Galaxies, Illustris TNG100')

ndgal_tng1_vir = np.genfromtxt(pwd + '/../data/illustris/dNbydMdV_Mvir_TNG100.txt').T
idxs = np.nonzero(ndgal_tng1_vir)
mgal_tng1_vir = mgal_tng[idxs]
ndgal_tng1_vir_new = ndgal_tng1_vir[idxs]

ax1.plot(mgal_tng1_vir, ndgal_tng1_vir_new, c='#274B83', ls='-', label=r'TNG100, M$_{\rm vir}$')


## Simulations: galaxies -- Eagle
ndgal_eag = np.genfromtxt(pwd + '/../data/eagle/dNbydMdV_Mstar_EAGLE.txt').T
idxs = np.nonzero(ndgal_eag)
mgal_eag = mgal_tng[idxs]
ndgal_eag_new = ndgal_eag[idxs]

ax1.plot(mgal_eag, ndgal_eag_new, c='#69FF02', ls='-', label='Galaxies, Eagle')


#ax1.plot(1, 1, c='#FFFFFF', ls='-', label=' ') # dummy legend entry


## Planck cosmology
ax1.plot(M_all, baryons, c='#8E44AD', ls='--', label='Baryons')
ax1.plot(M_all, cdm,  c='#2ECC71', ls='--', label='Dark matter')
ax1.plot(M_all, matter, c='#3498DB', ls='--', label='Baryons + DM')


#ax1.plot(1, 1, c='#FFFFFF', ls='-', label=' ') # dummy legend entry


## Theory: stellar initial mass function
Mbins = np.array([0.01, 0.08, 0.5, 100])
alpha = np.array([0.3, 1.3, 2.3])

Total = Ostar * mass_density_Mspc3

Norms = np.zeros(len(alpha))
Norms[-1] = 1.
for i in range(2):
    Norms[-(i+2)] = Norms[-(i+1)] * Mbins[-(i+2)]**(-alpha[-(i+1)]+alpha[-(i+2)])

Norm = Total / np.sum(Norms * (Mbins[1:]**(-alpha+2) - Mbins[:-1]**(-alpha+2))/(-alpha+2))
Norms *= Norm

imf = np.zeros(2)
for ii in range(3):
    imf = Norms[ii] * alpha[ii] * Mbins[ii:ii+2]**(-(alpha[ii] +1))
    if ii < 2:
        ax1.plot(Mbins[ii:ii+2], imf, c='#54F0F0', ls='-')
    else:
        ax1.plot(Mbins[ii:ii+2], imf, c='#54F0F0', ls='-', label='Stellar IMF')


## Theory: limits

nmin = 1e-32
ns = 2.6e38 / M_all**3
nobs = 6.0953e-81 * M_all**(-1.5)

plt.plot(M_all, nmin / M_all, ls='--', c='#F39C12', label='Minimum')
#plt.plot(M_all, ns / M_all, ls='--', c='#CF2419', label='Maximum')


#ax1.plot(1, 1, c='#FFFFFF', ls='-', label=' ') # dummy legend entry


#ax1.text(.2, .95, 'Observations', transform=ax1.transAxes, fontsize=8, color='k')
#ax1.text(.39, .95, 'Simulations', transform=ax1.transAxes, fontsize=8, color='k')
#ax1.text(.66, .95, 'Planck cosmology', transform=ax1.transAxes, fontsize=8, color='k')
#ax1.text(.83, .95, 'Theory', transform=ax1.transAxes, fontsize=8, color='k')
handles, labels = ax1.get_legend_handles_labels()
print('labels',labels)
#labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
plt.legend(handles, labels, loc=[.1,.8], bbox_transform=ax1.transAxes, ncol=4, fontsize=8)
#plt.tight_layout()
plt.show()
plt.savefig(pwd + '/dndmdv.png')

# TODO: plot total mass of universe (number density of that mass over the size of the universe) and see if it agrees w/ where the 'Minimum' theory line and Baryons+DM line meet
