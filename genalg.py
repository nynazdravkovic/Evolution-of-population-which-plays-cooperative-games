# -*- coding: utf-8 -*-
"""
Created on Thu May 10 23:41:01 2018

@author: nina
"""
import random
import numpy
from copy import copy, deepcopy
import matplotlib.pyplot as plt
from math import sqrt

brojJedinki=100
brojCiklusa=100
koeficijentKrosovera=0.05
brojGeneracija=1000
cc=3
cd=0
dc=5
dd=1
razliciteStrategije=64
matrica= numpy.zeros([brojGeneracija,64], dtype=int)
strategije=list(range(0,63))


    

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
    for x in range(37):
        strategije.append(random.choice(strategije))
    return (strategije)

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
    #lpoeni=list(poeni)
    populacija2=deepcopy(pop)
    populacija2=[x for _, x in sorted(zip(poeni,populacija2))]
    populacija2=populacija2[::-1]
    poeni=sorted(poeni)
    lpoeni=poeni[::-1]
    for n in range (5):
        populacija2.append(populacija2[n])
        lpoeni.append(poeni[-n])
    populacija2=[x for _, x in sorted(zip(lpoeni,populacija2))]
    populacija2=populacija2[5:]
    pop=deepcopy(populacija2)
    return (pop)


def mutacije(pop,koef):
    for i in range (brojJedinki):
        a=random.uniform(0,1)
        if a<=koef:
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


def genetskiAlgoritam(koef): 
    vreme=list(range(0,brojGeneracija))
    populacija=kreirajPopulaciju()
    nizSrednjihPoena=[]
    for t in range (brojGeneracija):
        poeni=dodavanjePoena(populacija)
        populacija=razmnozavanje(poeni,populacija)
        populacija=mutacije(populacija,koef)
        populacija=krosover(populacija)
        nizSrednjihPoena.append (numpy.mean(poeni)/(99*brojCiklusa))
##ovde se plotuje histogram poena 
#    plt.hist(poeni/ (99*brojCiklusa))
#    plt.ylabel('Broj jedinki')
#    plt.xlabel('Poeni')
#    plt.title('Grafik zastupljenosti poena u generaciji')
#    plt.show()
    #k=numpy.rot90(matrica)
    return nizSrednjihPoena



def sve(koeficijentMutacije):
    srednja=[]
    stabilizacija=[]
    o=list(range(64))
    vreme=list(range(brojGeneracija))
    for x in range (10):
        k=x
        s=[]
        s1=[]
        srednjaVrednost=genetskiAlgoritam(koeficijentMutacije)
        srednja.append(srednjaVrednost)
    numpy.rot90(srednja,3)
    for x in range (brojGeneracija):
        n=column(srednja,x)
        m=numpy.mean(n)
        m1=numpy.std(n)/sqrt(10)
        s.append(m)
        s1.append(m1)
#    plt.plot(vreme,s)
#    plt.errorbar(vreme, s, s1)
#    axes = plt.gca()
#    axes.set_ylim([0,5])
#    plt.ylabel('Srednji poeni')
#    plt.xlabel('Generacija')
#    plt.title('Grafik srednjih poena po generaciji')
#    plt.show()
    return s, s1

def svesve():
    c=[]
    d=[]
    koeficijentMutacije=numpy.zeros(10, dtype=float)
    for i in range (10):    
        koeficijentMutacije[i]=(i+1)/100
        print (koeficijentMutacije[i])
        stab=sve(koeficijentMutacije[i])
        a=stab[0]
        b=stab[1]
        e=0
        for i in range (brojGeneracija):
            if a[i]>2.9:
                e=i
                k=numpy.mean(a[i:])
                g=numpy.std(a[i:])/sqrt(10)
                break
            c.append(k)
            d.append(g)
    plt.plot(koeficijentMutacije, c)
    plt.errorbar(koeficijentMutacije, c, d)
    plt.ylabel('Srednji broj poena posle stabilizacije')
    plt.xlabel('Koeficijent mutacije')
    plt.show()
#        c.append(e)
#    plt.plot(koeficijentMutacije, c)
#    plt.errorbar(koeficijentMutacije, c, d)
#    plt.ylabel('Generacija u kojoj se populacija stabilizovala')
#    plt.xlabel('Koeficijent mutacije')
#    plt.title('Grafik stabilacije poena u zavisnosti od koeficijenta mutacije')
    
matricaPoena=svakaSaSvakom()    
svesve()
