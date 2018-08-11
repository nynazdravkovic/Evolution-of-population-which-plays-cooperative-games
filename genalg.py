

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
brojCiklusa=200
poeni=[]
koeficijentMutacije=0.05
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
    napraviPoene(brojJedinki)
    for i1 in range (brojJedinki):
        for i2 in range (i1, brojJedinki):
            a = populacija[i1]
            b = populacija[i2]
            poeni[i1]=poeni[i1] + matrica[a][b]
            poeni[i2]=poeni[i2] + matrica[b][a]



def razmnozavanje():
    global populacija
    populacija2=deepcopy(populacija) 
    sv=numpy.mean(poeni)
    std=numpy.std(poeni)
    for k in range (brojJedinki):
        if poeni[k]<sv-std:
            populacija2.remove(populacija[k])
        l=len(populacija)-len(populacija2)
    populacija2=[x for _, x in sorted(zip(poeni,populacija2))]
    for n in range (l):
        if populacija[n]>=sv+std:
            for i in range (2):
                populacija2.append(populacija[n])
        else:
            populacija2.append(populacija[n])
    populacija=deepcopy(populacija2)
    return (populacija)


def mutacije():
    global populacija
    a=random.uniform(0,1)
    pop=deepcopy(populacija)
    if a<=koeficijentMutacije:
        for f in range (int(len(pop)*a)):
            shuffle(pop)
            a=random.randint(0,brojJedinki-1)#random indeks
            #print(populacija[a])
            b=random.randint(0,5)#random prelomno mesto
            pop[a]=pop[a]^(1<<b)
    populacija=deepcopy(pop)
#def mutacije():
#    for k in range (int(len(populacija)*koeficijentMutacije)):
#        shuffle(populacija)
#        a=random.randint(0,brojJedinki-1)#random indeks
#        b=random.randint(0,5)#random prelomno mesto
#        populacija[a]=populacija[a]^(1<<b)
#        



def krosover():
    global populacija
    for f in range(int(brojJedinki*koeficijentRekombinacije)):
        a=random.randint(0,brojJedinki-1)  
        b=random.randint(0,brojJedinki-1)
        c=random.randint(0,6)  #biramo mesto na kome se lome strategije  
        mask=(1<<(c+1))-1
        donji1=populacija[a] & mask
        donji2=populacija[b] & mask
        gornji1=populacija[a]-donji1
        gornji2=populacija[b]-donji2
        populacija[a]=gornji1+donji2
        populacija[b]=gornji2+donji1


def column(matrix, k):
    return [row[k] for row in matrix]

def genetskiAlgoritam(): 
    vreme=list(range(brojGeneracija))
    matrica= numpy.zeros([brojGeneracija,64], dtype=int)
    nizSrednjihPoena=[]
    for t in range (brojGeneracija):
        dodavanjePoena(matricaPoena)
        razmnozavanje()
        mutacije()
        krosover()
        nizSrednjihPoena.append(numpy.mean(poeni)/99/brojCiklusa)
        #plt.scatter(t, numpy.mean(poeni)/brojCiklusa/brojJedinki)
        for k in range (brojJedinki):
            for i in range (0,64):
                if populacija[k]==i:
                    matrica[t][i]=matrica[t][i]+1
    #putanja=(r'C:\Users\nina\Desktop\projekat2018\aaa\grafik')
    #b=putanja + str(i) + '.jpg'
    #''.join(b)
    #plt.savefig(b)
    #plt.show()
    return matrica, nizSrednjihPoena
         

def sve():
    matrica1=numpy.zeros([10,64])
    for x in range (10):
        populacija=kreirajPopulaciju()
        #print(populacija)
        k=[]
        s=[]
        vreme=list(range(brojGeneracija))
        srednja=[]
        matrica=genetskiAlgoritam()[0]
        for i in range (brojGeneracija):
            for k in range (0, 64):        
                matrica1[x][k]+=matrica[i][k]
        srednjaVrednost=genetskiAlgoritam()[1]
        srednja.append(srednjaVrednost)
        plt.plot(vreme, srednjaVrednost)        
        #axes = plt.gca()
        #axes.set_ylim([0,5])
        plt.show()    
    for x in range (brojGeneracija):
        n=column(srednja,x)
        m=numpy.mean(n)
        s.append(numpy.std(n))
        plt.scatter(x,m)
    print(numpy.mean(s))
    plt.show()
    
#    for i in range (63):
#        
#        a=column(matrica1,i)
#        print(a)
#        plt.plot(vreme,a)
#        axes = plt.gca()
#        axes.set_xlim([0,brojGeneracija])
#        plt.ylabel('Broj strategije u generaciji')
#        plt.xlabel('Generacija')
#        putanja=(r'C:\Users\nina\Desktop\projekat2018\optimizovano\grafik')
#        b=putanja + str(i) + '.jpg'
#        ''.join(b)
#        plt.savefig(b)
#        plt.show()


#
populacija=kreirajPopulaciju()
napraviPoene(brojJedinki)
matricaPoena=svakaSaSvakom()
#os.makedirs(r'C:\Users\nina\Desktop\projekat2018\optimizovano')
plt.ioff()
#def cuvanje(pop, h):
#    populacija2=deepcopy(pop)
#    for i in range (len(pop)):
#        str(populacija2[i]).join(', ')
#    populacija2= map(str, pop)   
#    h=map(str,h)
#    text_file = open("Output8.txt", "w")
#    text_file1 = open("Output81.txt", "w")
#    text_file.write(''.join(populacija2))
#    text_file.close()
#    text_file1.write(''.join(h))
#    text_file1.close()
#    putanja=(r'C:\Users\nina\Desktop\projekat2018\txt\grafik')
#    b=putanja + '.txt'


#            poeni2=deepcopy(poeni)
#            poeni2=map(str,poeni2)
#            text_file1 = open("poeni.txt", "w")
#            text_file1.write(''.join(poeni2))
#            text_file1.close()
#            putanja=(r'C:\Users\nina\Desktop\projekat2018\txt\grafik')