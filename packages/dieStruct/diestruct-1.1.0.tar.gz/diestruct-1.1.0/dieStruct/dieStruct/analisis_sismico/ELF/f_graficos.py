# -*- coding: utf-8 -*-
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

def f_graficar_estructura(nodos,x,y,elems,ni,nj,gdl_n,views): 
      
    plt.figure(figsize=(6,6))
    brx=0.1*max(x)
    bry=0.1*max(y)
       
    '''---------------------------------------- Grafica elementos---------------------------------------------'''
    L=[]
    c=[]
    s=[]
    ne=len(elems)
    for i in range(ne):
        x1=x[int(ni[i])]
        x2=x[int(nj[i])]
        
        y1=y[int(ni[i])]
        y2=y[int(nj[i])]
        
        Li=((x2-x1)**2+(y2-y1)**2)**0.5
        ci=(x2-x1)/Li
        c.append(ci)
        
        si=(y2-y1)/Li
        s.append(si)
        
        L.append(Li)
        
        xt=(x1+x2)/2
        yt=(y1+y2)/2
        
        plt.plot([x1,x2],[y1,y2],color='blue',alpha=0.25,linewidth=4)
        plt.text(xt,yt,'e'+str(int(elems[i])),color='blue',fontsize=6) 
        
    '''---------------------------------------- Grafica nodos ------------------------------------------------'''
    
    nn=len(nodos)
    for i in range(nn):
        plt.plot(x[i],y[i],marker='o',markersize=2,color='green')
        plt.text(x[i]+0.1*brx,y[i]+0.1*bry,'n'+str(int(nodos[i])),fontsize=6,color='green')           
            
    
   
    '''---------------------------------------- Grafica gdl ------------------------------------------------'''
    
        
    if views==True:
        lf=0.1*max(L)
        lc=lf/2

        for i in range(nn):
            flecha_horizontal(x[i],y[i],max(L)*0.1,'black') 
            flecha_vertical(x[i],y[i],max(L)*0.1,'black') 
            dibujo_giro(x[i]+lc*0.7071,y[i]-lc*0.7071,0.1*lf,'black')
            
            h=x[i];k=y[i];r=lc
            t=np.linspace(135*np.pi/180,315*np.pi/180,100)

            x1=r*np.cos(t)+h
            y1=r*np.sin(t)+k
            plt.plot(x1,y1,color='black')
            
            plt.text(x[i]+0.1*max(L),y[i],str(int(gdl_n[i,1])),fontsize=8,color='black')
            plt.text(x[i],y[i]+0.1*max(L),str(int(gdl_n[i,2])),fontsize=8,color='black')
            plt.text(x[i]+lc,y[i]-lc,str(int(gdl_n[i,3])),fontsize=8,color='black')
            
    '''---------------------------------------------- show()---------------------------------------------'''
    plt.xlabel('Longitud [m]')
    plt.ylabel('Alturas [m]')
    #plt.xlim(min(x)-brx,max(x)+brx)
    #plt.ylim(min(y)-bry,max(y)+bry)
    plt.grid(alpha=0.25)
    plt.axis('equal')
    plt.show()   
    
    return [L,c,s]


def graficar_elementos(ne,ni,nj,x,y,names_e,cr,lw,af,ls):    
    L=[];c=[]; s=[]   
    for i in range(ne):
        
        x1=x[int(ni[i]-1)]
        x2=x[int(nj[i]-1)]
        
        y1=y[int(ni[i]-1)]
        y2=y[int(nj[i]-1)]
        
        Li=((x2-x1)**2+(y2-y1)**2)**0.5
        ci=(x2-x1)/Li
        c.append(ci)
        
        si=(y2-y1)/Li
        s.append(si)
        
        L.append(Li)
        
        xt=x1+0.4*Li*ci
        yt=y1+0.4*Li*si
        
        plt.plot([x1,x2],[y1,y2],color=cr,alpha=af,linewidth=lw,linestyle=ls)
        plt.text(xt,yt,names_e[i],color='blue',fontsize=10)
        
    return L,c,s

def dibujo_giro(xo,yo,lf,cl):
    
    coordp=np.array([  [xo,yo],
                       [xo+lf*0.7071,yo+lf*0.7071],
                       [xo+lf*0.7071,yo-lf*0.7071],
                       [xo-lf*0.7071,yo+lf*0.7071],         

                    ])

    conecp=np.array([   [1,2],
                        [2,3],
                        [2,4],
                        [3,4]         

                    ])

    nep=len(conecp)
    nip=conecp[:,0]
    njp=conecp[:,1]

    xp=coordp[:,0]
    yp=coordp[:,1]

    names_ep=['','','','']    
  
    graficar_elementos(nep,nip,njp,xp,yp,names_ep,cl,1.5,1,'-')
    
def flecha_horizontal(xo,yo,lf,cl):
    
    coordp=np.array([[xo,yo],
                        [xo+lf,yo],
                        [xo+0.9*lf,yo+0.1*lf],
                        [xo+0.9*lf,yo-0.1*lf]          

                    ])

    conecp=np.array([[1,2],
                        [3,4],
                        [3,2],
                        [4,2]         

                    ])

    nep=len(conecp)
    nip=conecp[:,0]
    njp=conecp[:,1]

    xp=coordp[:,0]
    yp=coordp[:,1]

    names_ep=['','','','']    
  
    graficar_elementos(nep,nip,njp,xp,yp,names_ep,cl,1.5,1,'-')
    
def flecha_vertical(xo,yo,lf,cl):
    
    coordp=np.array([[xo,yo],
                     [xo,yo+lf],
                     [xo+0.1*lf,yo+0.9*lf],
                     [xo-0.1*lf,yo+0.9*lf]          

                    ])

    conecp=np.array([[1,2],
                     [3,4],
                     [3,2],
                     [4,2]         

                    ])

    nep=len(conecp)
    nip=conecp[:,0]
    njp=conecp[:,1]

    xp=coordp[:,0]
    yp=coordp[:,1]

    names_ep=['','','','']    
  
    graficar_elementos(nep,nip,njp,xp,yp,names_ep,cl,1.5,1,'-')






