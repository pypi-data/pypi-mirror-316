from .f_geometria import*
from .f_grid import*
from .f_gdl_totales import*


def mallado(dx,dz):
    [dx,dz]=f_geometria(dx,dz)
    [Nodos,Elems]=f_grid(dx,dz)
    gdl_n=f_gdl_totales(Nodos,Elems)
       
    return Nodos,Elems,gdl_n