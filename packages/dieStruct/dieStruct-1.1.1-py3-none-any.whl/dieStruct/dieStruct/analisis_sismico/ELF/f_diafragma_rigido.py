# -*- coding: utf-8 -*-
import numpy as np # type: ignore
from .f_geometria import*

def diafragma_rigido(Nodos,Elems,dx,dz):
    [dx,dz]=f_geometria(dx,dz)

    ni=Elems[:,1]; nj=Elems[:,2] 

    nn=len(Nodos)
    ne=len(Elems)

    gdl_n=np.zeros([nn,4],dtype=int)

    for i in range(len(dz)):
        gdl_n[len(dx)*i:len(dx)*(i+1),1]=i

    j=0
    for i in range(nn):
        gdl_n[i,0]=i
        if i>len(dx)-1:

            gdl_n[i,2]=len(dz)+j
            gdl_n[i,3]=len(dz)+j+1
            j=j+2
        else:
            gdl_n[i,1]=0
            gdl_n[i,2]=0
            gdl_n[i,3]=0


    gdl_e=np.zeros([ne,7],dtype=int)
    for i in range(ne):
        gdl_e[i,0]=i
        gdl_e[i,1:4]=gdl_n[int(ni[i]),1:4]
        gdl_e[i,4:7]=gdl_n[int(nj[i]),1:4]

    gdl_e=np.zeros([ne,7],dtype=int)
    for i in range(ne):
        gdl_e[i,0]=i
        gdl_e[i,1:4]=gdl_n[int(ni[i]),1:4]
        gdl_e[i,4:7]=gdl_n[int(nj[i]),1:4]
    return [gdl_n,gdl_e]
