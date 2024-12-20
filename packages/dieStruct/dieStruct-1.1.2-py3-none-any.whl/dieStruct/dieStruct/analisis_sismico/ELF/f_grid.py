# -*- coding: utf-8 -*-
import numpy as np # type: ignore

def f_grid(dx,dz):#--------------------------------------------------------------------- Grid 

    npx=len(dx) ; npz=len(dz)
    nn   = npx*npz                       
    ncol = npx*(npz-1)                   
    nvig = (npx-1)*(npz-1) 
    nelm =ncol+nvig          

    Nodos=np.zeros((nn,4)) # [name,x,y,z]
    i=0
    lz=0
    for zi in range(npz):
        lz=lz+dz[zi]    ;  ly=0
        lx=0
        for xi in range(npx):   
            lx=lx+dx[xi]             
            # Numero de nodos 
            Nodos[i,0:4]=i,lx,ly,lz               
            i=i+1

    Elems=np.zeros((nelm,4))
    # Conectividad Columnas 
    c = 0
    for i in range(npz-1):
        for k in range(npx):
            Elems[c] = [c,c,c+npx,1]
            c = c + 1
    # Conectividad vigas paralelas a X
    m = npx
    for i in range(npz-1):        
        for k in range(npx-1):
            Elems[c] = [c,m,m+1,2]
            m = m + 1
            c = c + 1
        m = m + 1

    return [Nodos,Elems]
