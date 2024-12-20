from .f_gdl_efectivos import*

def restricciones(Nodos,Elems,dx,dz):
    [gdl_n,gdl_e]=f_gdl_efectivos(Nodos,Elems,dx,dz)
    return gdl_n,gdl_e