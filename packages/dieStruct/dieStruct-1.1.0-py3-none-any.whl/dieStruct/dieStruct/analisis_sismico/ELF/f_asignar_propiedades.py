# -*- coding: utf-8 -*-
import numpy as np # type: ignore

def asignar_propiedades(Elems,L,ac,ic,av,iv,Ec):
    propi=np.zeros([len(Elems),5])
    for i in range(len(Elems)):
        
        propi[i,0]=Elems[i,3]# type
        propi[i,1]=L[i]
        if propi[i,0]==1: # columna 
            propi[i,2]=ac
            propi[i,3]=ic
        else:
            propi[i,2]=av
            propi[i,3]=iv
        propi[i,4]=Ec        

    return propi

