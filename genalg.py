

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
koeficijentMutacije=0.05
koeficijentRekombinacije=0.05
brojGeneracija=100
cc=3
cd=0
dc=5
dd=1
razliciteStrategije=64

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
    #print (clan)
    return clan


    
def svakaSaSvakom():#pravim praznu matricu poena
    populacija1=[]
    matricaPoena=numpy.zeros([64,64], dtype=int)
    for i in range (64): #pravim strategije
        strategija1=list(bin(i)[2:].zfill(6))
        strategija=''.join(strategija1)
        populacija1.append(strategija)
    istorijaSukoba = numpy.zeros([64,64], dtype=int)
    for j1 in range(64):
        for j2 in range(64):
            for x in range(brojCiklusa):
                if x==0:
                    petij1=populacija1[j1][4]
                    sestij1=populacija1[j1][5]
                    petij2=populacija1[j2][4]
                    sestij2=populacija1[j2][5]
                else:
                    petij1=istorijaSukoba[j1][j2]
                    petij2=istorijaSukoba[j2][j1]
                    sestij1=petij2
                    sestij2=petij1
                clan1=int(birajClan(populacija1[j1], petij1, sestij1))
                clan2=int(birajClan(populacija1[j2], petij2, sestij2))
                istorijaSukoba[j1][j2]=clan1
                istorijaSukoba[j2][j1]=clan2                
                if (clan1==1):
                    if (clan2==1):
                        matricaPoena[j1][j2]=matricaPoena[j1][j2]+cc
                        matricaPoena[j2][j1]=matricaPoena[j2][j1]+cc
                    else:
                        matricaPoena[j1][j2]=matricaPoena[j1][j2]+cd
                        matricaPoena[j2][j1]=matricaPoena[j2][j1]+dc
                else:
                    if (clan2==1):
                        matricaPoena[j1][j2]=matricaPoena[j1][j2]+dc
                        matricaPoena[j2][j1]=matricaPoena[j2][j1]+cd
                    else:
                        matricaPoena[j1][j2]=matricaPoena[j1][j2]+dd
                        matricaPoena[j2][j1]=matricaPoena[j2][j1]+dd
    return (matricaPoena)


def generisiStrategiju():
    strategija=[]
    for x in range(6):
        strategija.append(random.randint(0,1))
    return strategija

def kreirajPopulaciju():
    populacija=[]
    for i in range (64): #pravim strategije
        strategija1=list(str(bin(i)[2:].zfill(6)))
        strategija=''.join(strategija1)
        populacija.append(strategija)
    return (populacija)
#def kreirajPopulaciju():
#    populacija=[]
#    for x in range(brojJedinki):
#        populacija.append(generisiStrategiju())
#    return populacija


def napraviPoene(brj):
    global poeni
    poeni=[0]*brj
    return poeni


def prebacivanjeUDek(niz):
    dekadni=0
    for i in range (6):
        if int(niz[-i-1])==1:
            dekadni=dekadni+2**i
    return (dekadni)


def dodavanjePoena(matrica):
    brojJedinki=len(populacija)
    napraviPoene(brojJedinki)
    for i1 in range (brojJedinki):
        for i2 in range (i1, brojJedinki):

            a = prebacivanjeUDek(populacija[i1])
            b = prebacivanjeUDek(populacija[i2])
            poeni[i1]=poeni[i1] + matrica[a][b]
            poeni[i2]=poeni[i2] + matrica[b][a]

    
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
    global populacija
    brojJedinki=len(populacija)   
    populacija2=[]    
    for k in range (brojJedinki):
        if poeni[k]<=srednjaVrednost(poeni)+standardnaDevijacija(poeni) and poeni[k]>srednjaVrednost(poeni)-standardnaDevijacija(poeni):
            populacija2.append(populacija[k])
        elif poeni[k]>=srednjaVrednost(poeni)+standardnaDevijacija(poeni):
            for i in range (2):
                populacija2.append(populacija[k])
    populacija=deepcopy(populacija2)
    brojJedinki=len(populacija)
    print('BrojJedinki:', brojJedinki)
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
    brojJedinki=len(populacija)

        
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
        



def column(matrix, i):
    return [row[i] for row in matrix]

def genetskiAlgoritam(): 
    vreme=[]
    #k=[0,brojGeneracija]
    vreme = list(range(0,brojGeneracija))
    matrica= numpy.zeros([brojGeneracija,64], dtype=int)
    for t in range (brojGeneracija):
        print (t)
        brojJedinki=len(populacija)
        dekadnaPopulacija=[]
        dodavanjePoena(matricaPoena)
        print('standardna', standardnaDevijacija(poeni))
        print('srednja', srednjaVrednost(poeni))
        razmnozavanje()
        brojJedinki=len(populacija)
        mutacije()
        rekombinacije()
        brojJedinki=len(populacija)
        #prebacujem populaciju u deekadni niz
        for i in range (brojJedinki):
            dekadnaPopulacija.append(prebacivanjeUDek(populacija[i]))
        for k in range (brojJedinki):
            for i in range (0,63):
                if dekadnaPopulacija[k]==i:
                    matrica[t][i]=matrica[t][i]+1
        plt.scatter(t, srednjaVrednost(poeni))
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
        putanja=(r'C:\Users\nina\Desktop\projekat2018\optimizacija4\grafik')
        b=putanja + str(i) + '.pdf'
        ''.join(b)
        plt.savefig(b)
        plt.show()

         

    

populacija=kreirajPopulaciju()
napraviPoene(brojJedinki)
matricaPoena=svakaSaSvakom()
#os.makedirs(r'C:\Users\nina\Desktop\projekat2018\optimizacija')
plt.ioff()

##@jit(nopython=True)   


#Stari deo koda koji se ponavljao stalno i koji radi
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
                    clan1=int(birajClan(populacija[j1], petij1, sestij1))
                    clan2=int(birajClan(populacija[j2], petij2, sestij2))
                    istorijaSukoba[j1][j2]=clan1
                    istorijaSukoba[j2][j1]=clan2
                    #print(istorijaSukoba)
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
    return (poeni)

#
