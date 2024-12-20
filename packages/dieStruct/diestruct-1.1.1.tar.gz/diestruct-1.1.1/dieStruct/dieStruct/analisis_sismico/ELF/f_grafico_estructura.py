# -*- coding: utf-8 -*-
import numpy as np # type: ignore

from .f_gdl_totales import*
from .f_graficos import*

def grafico_estructura(Nodos,Elems,gdl_n,ver_gdl=False):
    nodos=Nodos[:,0]; x=Nodos[:,1] ; z=Nodos[:,3]
    elems=Elems[:,0] ; ni=Elems[:,1]; nj=Elems[:,2]   
    ht=max(z) 
    
    [L,c,s]=f_graficar_estructura(nodos,x,z,elems,ni,nj,gdl_n,ver_gdl)

    return L,c,s,ht

