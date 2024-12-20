# -*- coding: utf-8 -*-
import numpy as np # type: ignore

def f_gdl_totales(Nodos,Elems):
    ni=Elems[:,1]; nj=Elems[:,2] 
    nn=len(Nodos)
    ne=len(Elems)

    gdl_n=np.zeros([nn,4],dtype=int)
    for i in range(nn):
        gdl_n[i,0]=i
        gdl_n[i,1]=(i+1)*3-2
        gdl_n[i,2]=(i+1)*3-1
        gdl_n[i,3]=(i+1)*3


        
    return gdl_n