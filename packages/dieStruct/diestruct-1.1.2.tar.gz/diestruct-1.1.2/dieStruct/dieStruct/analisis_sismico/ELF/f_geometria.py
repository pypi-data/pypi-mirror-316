# -*- coding: utf-8 -*-
import numpy as np # type: ignore
def f_geometria(dx,dz):
    dx = dx.split("-")     
    dx =[float(dx[0]) for di in dx] 
    dx.insert(0,0) 

    dz = dz.split("-") 
    dz =[float(di) for di in dz]  
    dz.insert(0,0) 

    return [dx,dz]