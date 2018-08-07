

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

brojJedinki=100
brojCiklusa=100
poeni=[]
koeficijentMutacije=0.05
koeficijentRekombinacije=0.05
brojGeneracija=1000
cc=3
cd=0
dc=5
dd=1
razliciteStrategije=64
def generisiStrategiju():
    strategija=[]
    for x in range(6):
        strategija.append(random.randint(0,1))
    return strategija
    
def kreirajPopulaciju():
    populacija=[]
    for x in range(brojJedinki):
        populacija.append(generisiStrategiju())
    return populacija

def napraviPoene(brj):
    global poeni
    poeni=[0]*brj
    return poeni


def birajClan(niz, peti, sesti):
    if peti==0:
        if sesti==0:
            clan=niz[0]
        else:
            clan=niz[1]
    else:
        if sesti==0:
            clan=niz[2]
        else:
            clan=niz[3]
    return clan

    
def pokreniSukobeUGeneraciji():
    brojJedinki=len(populacija)
    #print(brojJedinki)
    napraviPoene(brojJedinki)
    istorijaSukoba = numpy.zeros([brojJedinki,brojJedinki], dtype=int)
    for j1 in range(brojJedinki):
        for j2 in range(j1, brojJedinki):
            if j1!=j2:
                for x in range(brojCiklusa):
                    if x==0:
                        petij1=populacija[j1][4]
                        sestij1=populacija[j1][5]
                        petij2=populacija[j2][4]
                        sestij2=populacija[j2][5]
                    else:
                        petij1=istorijaSukoba[j1][j2]
                        petij2=istorijaSukoba[j2][j1]
                        sestij1=petij2
                        sestij2=petij1
                    clan1=birajClan(populacija[j1], petij1, sestij1)
                    clan2=birajClan(populacija[j2], petij2, sestij2)
                    istorijaSukoba[j1][j2]=clan1
                    istorijaSukoba[j2][j1]=clan2
                    if clan1==1:
                        if clan2==1:
                            poeni[j1]=poeni[j1]+cc
                            poeni[j2]=poeni[j2]+cc
                        else:
                            poeni[j1]=poeni[j1]+cd
                            poeni[j2]=poeni[j2]+dc
                    else:
                        if clan2==1:
                            poeni[j1]=poeni[j1]+dc
                            poeni[j2]=poeni[j2]+cd
                        else:
                            poeni[j1]=poeni[j1]+dd
                            poeni[j2]=poeni[j2]+dd


def srednjaVrednost(p): #srednja vrednost
    brojJedinki=len(populacija)    
    M=sum(p)
    M=M/brojJedinki
    return M
            
            
def standardnaDevijacija(p): #standardna devijacija
    dev=0
    s=0
    brojJedinki=len(populacija)
    for x in range(brojJedinki):
        s=s+((p[x]-srednjaVrednost(p))**2)/(brojJedinki-1)
    dev=math.sqrt(s)
    return dev


def razmnozavanje():
    #print(standardnaDevijacija(poeni))
    global populacija
    brojJedinki=len(populacija)   
    populacija1=[]
    
    for k in range (brojJedinki-1):
        if poeni[k]<=srednjaVrednost(poeni)+standardnaDevijacija(poeni) and poeni[k]>srednjaVrednost(poeni)-standardnaDevijacija(poeni):
            populacija1.append(populacija[k])
        elif poeni[k]>=srednjaVrednost(poeni)+standardnaDevijacija(poeni):
            for i in range (2):
                populacija1.append(populacija[k])
    populacija=deepcopy(populacija1)
    print('BrojJedinki:', brojJedinki)
    #brojJedinki=len(populacija)
    return (populacija)


def mutacije():
    global populacija
    brojJedinki=len(populacija)
    
    ('BrojJedinki:', brojJedinki)
    for f in range(0,int(len(populacija)*koeficijentMutacije)):  
        a=random.randint(0,brojJedinki-1)#random indeks
        b=random.randint(0,5)#random prelomno mesto
        c=populacija[a][b]#karakter koji se na tom mestu nalazi
        if b==0:
            left=[]
            right=populacija[a][1:]
        elif b==5:
            left=populacija[a][:5]
            right=[]
        else:
            left=populacija[a][:(b)]
            right=populacija[a][(b+1):]
        if c==0:
            s=[1]
            d=left+s+right
        else:
            s=[0]
            d=left+s+right
        populacija[a]=d
    

        
def rekombinacije():
    global populacija
    brojJedinki=len(populacija)

    t=0
    for f in range(0,int(len(populacija)*koeficijentRekombinacije)):
        a=random.randint(0,brojJedinki-1)  
        b=random.randint(0,brojJedinki-1)  #biramo neka 2 random indeksa   
        c=random.randint(0,5)  #biramo mesto od koje se lome strategije
        
        if c==0:
            populacija[a]=populacija[a] #sve ostaje isto
            populacija[b]=populacija[b]
            
        elif c==5:
            t=populacija[a] #menjamo mesta ovim strategijama
            populacija[a]=populacija[b]
            populacija[b]=t
            
        else:
            d=(populacija[a])[:c]+(populacija[b])[c:] 
            e=(populacija[b])[:c]+(populacija[a])[c:]#uvodimo neke 2 nove promenljive koje predstavljaju rekombinovane strategije
            populacija[a]=d #povratak na pocetne nazive
            populacija[b]=e
        #print(d)
        #print(e)
        
def prebacivanjeUDek(niz):
    dekadni=0
    for i in range (6):
        if niz[-i-1]==1:
            dekadni=dekadni+2**i
    return (dekadni)
def column(matrix, i):
    return [row[i] for row in matrix]


def genetskiAlgoritam(): 
    vreme=[]
    vreme = list(range(0,brojGeneracija))
    matrica= numpy.zeros([brojGeneracija,64], dtype=int)
    for t in range (brojGeneracija):
        dekadno=[]
        pokreniSukobeUGeneraciji()
        razmnozavanje()
        mutacije()
        rekombinacije()
        brojJedinki=len(populacija)
        for i in range (brojJedinki):
            dekadno.append(prebacivanjeUDek(populacija[i]))
        for k in range (brojJedinki):
            for i in range (0,63):
                if dekadno[k]==i:
                    matrica[t][i]=matrica[t][i]+1
    for i in range(razliciteStrategije):
        for k in range (brojGeneracija): 
            a=column(matrica,i)
            #reme[k]
        print (a)
        plt.plot(vreme, a)
        axes = plt.gca()
        axes.set_xlim([0,1000])
        axes.set_ylim([0,64])
        plt.ylabel('Broj strategije u generaciji')
        plt.xlabel('Generacija')
        plt.show()
        plt.savefig("grafik")
    return (matrica)
    

populacija=kreirajPopulaciju()
napraviPoene(brojJedinki)

#def plotovanje(m):    
#    a=[]
#    vreme=[]
#    for i in range(64):
#        for k in range (brojGeneracija): 
#            a=column(m,i)
#            vreme.append(k)
#        plt.plot(a, vreme)
#    return (a)
#


