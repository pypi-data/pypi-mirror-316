# -*- coding: utf-8 -*-
from .f_geometria import*


def peso_reactivo(CM_losa,CL_losa,coef_cl,wcol,wvig):
    
    n=len(CM_losa)
    wr=[]
    for i in range(n):
        a=CM_losa[i]
        b=wcol[i]
        c=wvig[i]

        d=coef_cl*CL_losa[i]
        wr.append(a+b+c+d)

    return wr


