# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
def mostrar_tabla(data,nombre):
    
    if nombre=="Propiedades":
        nombre_col=["Tipo","L[m]","A[m2]","I(m4)","Ec[T/m2]"]
        etiquetas = [f'elem {i}' for i in range(len(data))]

    if nombre=="M_Rigidez":
        nombre_col=[f'u {i+1}' for i in range(len(data))]
        etiquetas =[f'f {i+1}' for i in range(len(data))]

    if nombre=="M_Rigidez_Lateral":
        nombre_col=[f'u {i+1}' for i in range(len(data))]
        etiquetas =[f'f {i+1}' for i in range(len(data))]

    if nombre=="ELF":
        nombre_col = ['H (m)', 'W (tonf)',' F (tonf)','V (tonf)']

        etiquetas = [f'Piso {len(data)-i-1}' for i in range(len(data))] 

    if nombre=="Desplazamientos":
        data=data[::-1]
        nombre_col = ['ue [m]'] 

        etiquetas = [f'Piso {len(data)-i-1}' for i in range(len(data))] 

    if nombre=="Derivas":
        
        nombre_col = ['Drift [ ]'] 

        etiquetas = [f'Piso {len(data)-i-1}' for i in range(len(data))] 

    if nombre=="Periodos":
        
        nombre_col = ['T [s]'] 

        etiquetas =[f'T{i+1}' for i in range(len(data))] 
         
    df1 = pd.DataFrame(data,columns=nombre_col,index=etiquetas).round(3)

    return display(df1) # type: ignore