import numpy as np # type: ignore
import math
from scipy import linalg as LA

pi=math.pi

def f_matriz_masas(Mi):
    n=len(Mi)
    M=np.eye(n)
    np.fill_diagonal(M, Mi)
    return M/9.806


def f_periodos(w2):
    T=np.zeros([len(w2),1])
    for i in range(len(w2)):
        T[i]=2*pi/w2[i]**0.5
    return T

def periodos_estructura(Mi,KL):
    M=f_matriz_masas(Mi)
    w2,fi=LA.eigh(KL,M)
    T=f_periodos(w2)
    return T ,max(T[0])