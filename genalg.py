

# -*- coding: utf-8 -*-
"""
Created on Thu May 10 23:41:01 2018

@author: nina
"""

import random
import numpy
import math
from copy import copy, deepcopy
import matplotlib.pyplot as plt
import os
from numba import jit

brojJedinki=100
brojCiklusa=100
poeni=[]
koeficijentMutacije=0.005
koeficijentRekombinacije=0.05
brojGeneracija=100
cc=3
cd=0
dc=5
dd=1
razliciteStrategije=64


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


def napraviPoene(brj):
    global poeni
    poeni=numpy.zeros(brj)
    return poeni


def dodavanjePoena(matrica):
    brojJedinki=len(populacija)
    napraviPoene(brojJedinki)
    for i1 in range (brojJedinki):
        for i2 in range (i1, brojJedinki):
            a = populacija[i1]
            b = populacija[i2]
            poeni[i1]=poeni[i1] + matrica[a][b]
            poeni[i2]=poeni[i2] + matrica[b][a]


def razmnozavanje():
    global populacija
    
    brojJedinki=len(populacija)   
    populacija2=deepcopy(populacija) 
    sv=numpy.mean(poeni)
    print(sv)
    std=numpy.std(poeni)
    print(std)
    while len(populacija)<=len(populacija2):
        for k in range (brojJedinki):
            if poeni[k]>=sv+std:
                for p in range (2):
                    populacija2.append(populacija[k])
            elif poeni[k]<sv+std and poeni[k]>=sv-std:
                populacija2.append(populacija[k])
    populacija=deepcopy(populacija2)
    brojJedinki=len(populacija)
    print('BrojJedinki:', brojJedinki)
    return (populacija)


def mutacije():
    brojJedniki=len(populacija)
    for f in range (int(len(populacija)*koeficijentMutacije)):
        a=random.randint(0,brojJedinki)#random indeks
        #print(populacija[a])
        b=random.randint(0,5)#random prelomno mesto
        populacija[a]=populacija[a]^(1<<b)


#def krosover():
#    global populacija
#    brojJedniki=len(populacija)
#    for f in range(int(brojJedinki*koeficijentRekombinacije)):
#        a=random.randint(0,brojJedinki)  
#        b=random.randint(0,brojJedinki)
#        c=random.randint(0,6)  #biramo mesto na kome se lome strategije  
#        mask=(1<<(c+1))-1
#        donji1=populacija[a] & mask
#        donji2=populacija[b] & mask
#        gornji1=populacija[a]-donji1
#        gornji2=populacija[b]-donji2
#        populacija[a]=gornji1+donji2
#        populacija[b]=gornji2+donji1


def column(matrix, i):
    return [row[i] for row in matrix]

def genetskiAlgoritam(): 
    vreme=[]
    vreme = list(range(0,brojGeneracija))
    matrica= numpy.zeros([brojGeneracija,64], dtype=int)
#    for n in range (10):
#        populacija=kreirajPopulaciju()
    brojJedniki=len(populacija)
    for t in range (brojGeneracija):
        dodavanjePoena(matricaPoena)
        razmnozavanje()
        mutacije()
        #krosover()
        #prebacujem populaciju u deekadni niz
        for k in range (brojJedinki):
            for i in range (0,63):
                if populacija[k]==i:
                    matrica[t][i]=matrica[t][i]+1
        plt.scatter(t, numpy.mean(poeni)/10000/brojJedinki)
    plt.show()
    #ovde krece plotovanje
    for i in range(razliciteStrategije):
        for k in range (brojGeneracija): 
            a=column(matrica,i)
        plt.plot(vreme, a)
        axes = plt.gca()
        axes.set_xlim([0,brojGeneracija])
        #axes.set_ylim([0,64])
        plt.ylabel('Broj strategije u generaciji')
        plt.xlabel('Generacija')
        putanja=(r'C:\Users\nina\Desktop\projekat2018\optimizovano\grafik')
        b=putanja + str(i) + '.pdf'
        ''.join(b)
        plt.savefig(b)
        plt.show()

         

    

populacija=kreirajPopulaciju()
napraviPoene(brojJedinki)
matricaPoena=svakaSaSvakom()
#os.makedirs(r'C:\Users\nina\Desktop\projekat2018\optimizovano')
plt.ioff()



