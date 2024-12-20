# -*- coding: utf-8 -*-
import numpy as np # type: ignore
from .f_geometria import*

def f_rigidez_local(Ei,Ai,Ii,Li): 
    a=Ei*Ai/Li
    b=12*Ei*Ii/Li**3
    c=6*Ei*Ii/Li**2
    d=4*Ei*Ii/Li
    e=2*Ei*Ii/Li


    kei=np.array([  [ a,  0,  0, -a,  0,  0],
                    [ 0,  b,  c,  0, -b,  c],
                    [ 0,  c,  d,  0, -c,  e],
                    [-a,  0,  0,  a,  0,  0],
                    [ 0, -b, -c,  0,  b, -c],
                    [ 0,  c,  e,  0, -c,  d]   
    ])
    return kei

def f_rigidez_global(kei,ci,si):
    
    Tei=np.array([ [ci, si,  0,  0,  0,  0], 
  [-si, ci,  0,  0,  0,  0],
   [0,  0,  1,  0,  0,  0],
   [0,  0,  0,  ci, si,  0],
   [0,  0,  0, -si,  ci, 0],
   [0,  0,  0,  0,  0,  1]    
    ])
    
    KEi=np.transpose(Tei)@kei@Tei    
    return KEi

def f_ens(KEi,gdli,K):
    dim=2 # dimensión 
    gdn=3 # grados de libertad por nodo
    
    for i in range(dim*gdn):
        f=gdli[i]-1
        for j in range(dim*gdn):
            c=gdli[j]-1
            if f<0 or c<0:
                continue 
            else: 
                K[f,c]=K[f,c]+KEi[i,j]
                
    return K

def rigidez_estructura(gdl_e,propi,c,s):
    n_gdl=int(np.max(gdl_e[:,1:7]))
    K=np.zeros([n_gdl,n_gdl])

    for i in range(len(c)):
        Li,Ai,Ii,Ei=propi[i,1],propi[i,2],propi[i,3],propi[i,4]
        kei=f_rigidez_local(Ei,Ai,Ii,Li)

        ci,si=c[i],s[i]
        KEi=f_rigidez_global(kei,ci,si)

        gdli=gdl_e[i,1:7]
        K=f_ens(KEi,gdli,K)

    return K


def rigidez_lateral(K,gdl_e,dy,dz):
    [dy,dz]=f_geometria(dy,dz)
    nc=len(dz)-1
    npy=len(dy)
    n_gdl=int(np.max(gdl_e[:,1:7]))
    
    kaa=K[0:nc,0:nc]
    kab=K[0:nc,nc+1:n_gdl]
    kba=kab.T
    kbb=K[nc+1:n_gdl,nc+1:n_gdl]
    KL=kaa-kab@np.linalg.inv(kbb)@kba

    return KL,npy
