

# -*- coding: utf-8 -*-
"""
Created on Thu May 10 23:41:01 2018

@author: nina
"""

import random
from random import shuffle
import numpy
import math
from copy import copy, deepcopy
import matplotlib.pyplot as plt
import os
from numba import jit

brojJedinki=100
brojCiklusa=100
koeficijentMutacije=0.01
koeficijentKrosovera=0.05
brojGeneracija=4000
cc=3
cd=0
dc=5
dd=1
razliciteStrategije=64
matrica= numpy.zeros([brojGeneracija,64], dtype=int)


    

def bit (broj, m):
    a=((1<<m) & broj)>>m
    return a



def birajClan(niz, peti, sesti):
    if peti==0:
        if sesti==0:
            clan=bit(niz,5)
        else:
            clan=bit(niz,4)
    else:
        if sesti==0:
            clan=bit(niz,3)
        else:
            clan=bit(niz,2)
    return clan



def svakaSaSvakom():#pravim praznu matricu poena
    populacija1=[]
    matricaPoena=numpy.zeros([64,64], dtype=int)
    for i in range (64): #pravim strategije
        populacija1.append(i)
    istorijaSukoba = numpy.zeros([64,64], dtype=int)
    for j1 in range(64):
        for j2 in range(j1, 64):
            for x in range(brojCiklusa):
                if x==0:
                    petij1=bit(populacija1[j1],1)
                    sestij1=bit(populacija1[j1],0)
                    petij2=bit(populacija1[j2],1)
                    sestij2=bit(populacija1[j2],0)
                    
                else:
                    petij1=istorijaSukoba[j1][j2]
                    petij2=istorijaSukoba[j2][j1]
                    sestij1=petij2
                    sestij2=petij1
                clan1=birajClan(populacija1[j1], petij1, sestij1)
                clan2=birajClan(populacija1[j2], petij2, sestij2)
                istorijaSukoba[j1][j2]=clan1
                istorijaSukoba[j2][j1]=clan2                
                
                if (clan1==1):
                    if (clan2==1):
                        if j1!=j2:
                            matricaPoena[j1][j2]=matricaPoena[j1][j2]+cc
                            matricaPoena[j2][j1]=matricaPoena[j2][j1]+cc
                        else:
                            matricaPoena[j2][j1]=matricaPoena[j2][j1]+cc
                        
                    else:
                        matricaPoena[j1][j2]=matricaPoena[j1][j2]+cd
                        matricaPoena[j2][j1]=matricaPoena[j2][j1]+dc

                else:
                    if (clan2==1):
                        matricaPoena[j1][j2]=matricaPoena[j1][j2]+dc
                        matricaPoena[j2][j1]=matricaPoena[j2][j1]+cd
                    else:
                        if j1!=j2:
                            matricaPoena[j1][j2]=matricaPoena[j1][j2]+dd
                            matricaPoena[j2][j1]=matricaPoena[j2][j1]+dd
                        else:
                            matricaPoena[j2][j1]=matricaPoena[j2][j1]+dd
    return (matricaPoena)
    


def kreirajPopulaciju():
    populacija=[]
    for x in range(brojJedinki):
        populacija.append(random.randint(0,63))
    return (populacija)


#def napraviPoene(brj):
#    global poeni
#    poeni=numpy.zeros(brj)
#    return poeni


def dodavanjePoena(pop):
    poeni=numpy.zeros(brojJedinki)
    for i1 in range (brojJedinki):
        for i2 in range (i1, brojJedinki):
            a = pop[i1]
            b = pop[i2]
            poeni[i1]=poeni[i1] + matricaPoena[a][b]
            poeni[i2]=poeni[i2] + matricaPoena[b][a]
    return(poeni)



def razmnozavanje(poeni,pop):
    lpoeni=list(poeni)
    populacija2=deepcopy(pop) 
    populacija2=[x for _, x in sorted(zip(poeni,populacija2))]
    for n in range (5):
        populacija2.append(populacija2[n])
        lpoeni.append(poeni[n])
    populacija2=[x for _, x in sorted(zip(lpoeni,populacija2))]
    populacija2=populacija2[::-1]
    populacija2=populacija2[5:]
    pop=deepcopy(populacija2)
    return (pop)


def mutacije(pop):
    for i in range (brojJedinki):
        a=random.uniform(0,1)
        if a<=koeficijentMutacije:
            b=random.randint(0,5)#random prelomno mesto
            pop[i]=pop[i]^(1<<b)
    return(pop)

def krosover(pop):
    for i in range (brojJedinki):
        g=random.uniform(0,1)
        if g<=koeficijentKrosovera:
                a=random.randint(0,brojJedinki-1)  
                b=random.randint(0,brojJedinki-1)
                c=random.randint(0,6)  #biramo mesto na kome se lome strategije  
                mask=(1<<(c+1))-1
                donji1=pop[a] & mask
                donji2=pop[b] & mask
                gornji1=pop[a]-donji1
                gornji2=pop[b]-donji2
                pop[a]=gornji1+donji2
                pop[b]=gornji2+donji1
    return(pop)

def column(matrix, k):
    return [row[k] for row in matrix]

matrica= numpy.zeros([brojGeneracija,64], dtype=int)

def genetskiAlgoritam(): 
    vreme=list(range(0,brojGeneracija))
    nizSrednjihPoena=[]
    populacija=kreirajPopulaciju()
    for t in range (brojGeneracija):
        poeni=dodavanjePoena(populacija)
        populacija=razmnozavanje(poeni,populacija)
        mutacije(populacija)
        krosover(populacija)
        nizSrednjihPoena.append (numpy.mean(poeni)/(99*brojCiklusa))
        for k in range (brojJedinki):
            for i in range (0,64):
                if populacija[k]==i:
                    matrica[t][i]=matrica[t][i]+1
        matrica[t][0]+=matrica[t][1]+matrica[t][2]+matrica[t][3]+matrica[t][4]+matrica[t][5]+matrica[t][6]+matrica[t][8]+matrica[t][9]+matrica[t][11]+matrica[t][12]+matrica[t][13]
        matrica[t][16]+=matrica[t][18]+matrica[t][19]
        matrica[t][20]+=matrica[t][22]
        matrica[t][21]+=matrica[t][23]
        matrica[t][52]+=matrica[t][53]+matrica[t][55]
        matrica[t][24]+=matrica[t][27]
        matrica[t][48]+=matrica[t][49]
        matrica[t][36]+=matrica[t][39]
        matrica[t][63]+=matrica[t][62]+matrica[t][61]+matrica[t][60]+matrica[t][59]+matrica[t][58]+matrica[t][57]+matrica[t][55]+matrica[t][54]+matrica[t][52]+matrica[t][51]+matrica[t][50]
        matrica[t][47]+=matrica[t][45]+matrica[t][44]
        matrica[t][43]+=matrica[t][41]
        matrica[t][42]+=matrica[t][40]
        matrica[t][11]+=matrica[t][10]+matrica[t][8]
        matrica[t][39]+=matrica[t][36]
        matrica[t][15]+=matrica[t][14]
        matrica[t][28]+=matrica[t][24]
        matrica[t][1]=0
        matrica[t][2]=0       
        matrica[t][3]=0
        matrica[t][4]=0
        matrica[t][5]=0
        matrica[t][6]=0
        matrica[t][8]=0
        matrica[t][9]=0
        matrica[t][11]=0
        matrica[t][12]=0
        matrica[t][13]=0
        matrica[t][18]=0
        matrica[t][19]=0
        matrica[t][22]=0
        matrica[t][23]=0
        matrica[t][53]=0
        matrica[t][55]=0
        matrica[t][27]=0
        matrica[t][49]=0
        matrica[t][39]=0
        matrica[t][24]=0
        matrica[t][14]=0
        matrica[t][36]=0
        matrica[t][10]=0
        matrica[t][40]=0
        matrica[t][62]=0
        matrica[t][61]=0
        matrica[t][60]=0
        matrica[t][59]=0
        matrica[t][58]=0
        matrica[t][57]=0
        matrica[t][55]=0
        matrica[t][54]=0
        matrica[t][53]=0
        matrica[t][52]=0
        matrica[t][51]=0
        matrica[t][50]=0
        matrica[t][41]=0
    putanja=(r'C:\Users\nina\Desktop\projekat2018\histogrami\histogram')
    b=putanja + str(t) + '.jpg'
    ''.join(b)
    plt.savefig(b)
    plt.hist(poeni/(99*brojCiklusa))  
    plt.show()
    m=matrica.transpose()
    for i in range (64):
        plt.plot(vreme,m[i])
        axes = plt.gca()
        axes.set_ylim([0,500])
        putanja=(r'C:\Users\nina\Desktop\projekat2018\svaka\grafik')
        b=putanja + str(i) + '.jpg'
        ''.join(b)
        plt.savefig(b)
    plt.show()
    return nizSrednjihPoena, matrica


def sve():
    o=list(range(0,64))
    for x in range (10):
        s=0
        k=[]
        vreme=[]
        vreme=list(range(brojGeneracija))
        srednja=[]
        g=genetskiAlgoritam() 
        matrica=g[1]
        srednjaVrednost=g[0]
        srednja.append(srednjaVrednost)
        plt.plot(vreme, srednjaVrednost)  
    plt.show()
    #m=matrica.transpose()
    for x in range (brojGeneracija):
        plt.bar(o,matrica[3999])
    plt.show()
    
    
    
matricaPoena=svakaSaSvakom()

        #plt.scatter(t,numpy.mean(poeni)/(99*brojCiklusa))
    #axes = plt.gca()
    #axes.set_ylim([0,5])
    #plt.show()
#    
#    for x in range (brojGeneracija):
#        n=column(srednja,x)
#        m=numpy.mean(n)
#        s=numpy.std(n)
#        plt.scatter(x,m)
#    plt.show()