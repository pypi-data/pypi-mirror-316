# -*- coding: utf-8 -*-

import numpy as np # type: ignore
from .f_geometria import*
from .f_mallado import*

def peso_estructura(Wd,Wl,den,dx,dy,dz,ac,av):
    [_,Elemsx,_]=mallado(dx,dz)
    [_,Elemsy,_]=mallado(dy,dz)

    [dx,_]=f_geometria(dx,dz)
    [dy,dz]=f_geometria(dy,dz)

   
    
    Lx=sum(dx) 
    Ly=sum(dy) 
    area=Lx*Ly
    n=len(dz)-1
    CMi=[]
    CLi=[]

    # Carga de la losa

    for i in range(n):
        CMi.append(area*Wd[i])
        CLi.append(area*Wl[i])

    # Carga de los elementos vigas columnas 
    
    type_ex=Elemsx[:,3]
    nvigx=np.sum(type_ex == 2)
    ncol=np.sum(type_ex == 1)

    type_ey=Elemsy[:,3]
    nvigy=np.sum(type_ey == 2)
    

    wcol=[]
    wvig=[]
    
    for i in range(n):
        if i==n-1:
            Lc=dz[n]/2
        else:
            Li=dz[i+1]/2
            Ls=dz[i+2]/2
            Lc=Li+Ls
        
        wcol.append(Lc*ac*den*ncol/n*(len(dy)))
        wvig.append(Lx*av*den*(len(dy))+Ly*av*den*(len(dx)))
        

   



    return CMi,CLi, wcol , wvig


