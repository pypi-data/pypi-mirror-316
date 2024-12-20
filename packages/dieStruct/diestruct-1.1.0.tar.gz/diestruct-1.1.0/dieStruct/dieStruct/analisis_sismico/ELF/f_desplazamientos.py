
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt # type: ignore

import numpy as np # type: ignore

from .f_geometria import*

def desplazamientos_e(KLX,ELF):
    F=ELF[0:-1,2]
    F=F[::-1]
    ue=np.linalg.inv(KLX)@F
    

    return np.insert(ue, 0, 0)


def deriva(ue,dz):
    [_,dz]=f_geometria('0',dz) 
    n=len(ue)

    ue=np.flip(ue)
    dz=np.flip(dz)
    der=np.zeros([n,1])
    for i in range(len(ue)-1):        
        if i==len(ue)-1:
            der[i]=(ue[i])/dz[i]
        else:
            der[i]=(ue[i]-ue[i+1])/dz[i]

    return der


def derivas_nec15(der,R):
    return 0.75*R*der   

def derivas_nec24(der,Ie,cd):
    return cd*der/Ie


def grafico_derivas(Dxi,ELF,dmax):
    Niveles=ELF[:,0]
    xmax=max(int(max(Dxi)),dmax)
    
    fig2,ax2 = plt.subplots()

    ax2.plot(Dxi,Niveles, color='blue',ls = "-.",lw=1,label=str(max(max(Dxi.round(1)))) +' %')
    ax2.scatter(Dxi,Niveles, marker='o',color='blue')


    ax2.axvline(x=dmax, ymin=0, ymax=1,color='black',ls = "--",lw=1)

    ax2.set_title(f'Deriva Inelástica', color='black', fontsize=12)
    ax2.set_ylabel('Altura [m]', color='black', fontsize=10)
    ax2.set_xlabel('Drift[%]', color='black', fontsize=10)
    ax2.legend()
    ax2.set_xlim(0, xmax+0.5) 
    ax2.grid(alpha=0.5)