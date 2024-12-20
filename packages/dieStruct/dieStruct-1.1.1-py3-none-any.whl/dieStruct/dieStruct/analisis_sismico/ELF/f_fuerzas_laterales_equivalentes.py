# -*- coding: utf-8 -*-
import numpy as np # type: ignore

import matplotlib.pyplot as plt



from .f_geometria import*


def fuerzas_laterales_equivalentes(Wr,k,v,dx,dz):
    pi=Wr
    [_,dz]=f_geometria(dx,dz)

    hi=np.zeros((len(dz)-1))
    suma=0            
    for i in range(len(dz)-1):
        hi[i]=dz[1+i]+suma
        suma=suma+dz[1+i]
    hi=hi.tolist()

    af=f_factor_aft(pi,hi,k)
 
    Fi=np.array(af)*v

    Fi=np.insert(Fi, 0, 0)
    hi=np.insert(hi, 0, 0)
    pi=np.insert(pi, 0, 0)

    ELF=np.zeros((len(hi),4))

    for i in range(len(hi)):
        ii=len(hi)-i-1
        ELF[i,0]=hi[ii]
        ELF[i,1]=pi[ii]
        ELF[i,2]=Fi[ii]
        if i==0:
            ELF[i,3]=ELF[i,2]
        else:
            ELF[i,3]=ELF[i,2]+ELF[i-1,3]


    
    fig1,ax1 = plt.subplots() 
    
    ax1.scatter(0,0, marker='s',color='blue',s=200)# pendulo 
    ax1.axvline(x=0, ymin=0.05, ymax=0.95,color='blue',ls = "-",lw=3) # pendulo
    ax1.scatter([0]*len(ELF[:,2]),ELF[:,0], marker='o',color='blue',s=200) # pendulo 


    ax1.plot(-ELF[:,2],ELF[:,0], color='blue',ls = "-.",lw=0.5,label='Fi') # Inclinada 

    for i in range(len(hi)-1):
        ax1.hlines(y=ELF[i,0], xmin=-ELF[i,2], xmax=-0.1*ELF[-2,2], color='r') # fecha roja 
        ax1.scatter(-0.1*ELF[-2,2],ELF[i,0], marker='>',color='red',s=100)# fecha 
        
        ax1.text(-ELF[-2,2],ELF[i,0],f'{round(ELF[i,2],2)}')# texto 
        


    ax1.set_title('Fuerzas Laterales    equivalentes', color='black', fontsize=12)
    ax1.set_ylabel('Altura (m)', color='black', fontsize=10)
    ax1.set_xlabel('F (tonf)', color='black', fontsize=10)
    ax1.legend()
    ax1.grid(alpha=0.5)


    return ELF




def f_factor_afi(pi,P,H,k):
    suma=0
    for i in range(len(H)):
        suma=suma+P[i]*H[i]**k
    return P[pi]*H[pi]**k/suma

def f_factor_aft(p,h,k):
    af=[]
    for i in range(len(h)):
        afi=f_factor_afi(i,p,h,k)
        af.append(afi)    
    return af