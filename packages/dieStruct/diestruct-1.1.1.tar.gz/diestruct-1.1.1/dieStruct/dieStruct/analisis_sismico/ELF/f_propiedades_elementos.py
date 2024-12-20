# -*- coding: utf-8 -*-

def propiedades_elementos(b,h,agr):
    area   =b*h
    inercia=b*h**3/12*agr
    return area,inercia