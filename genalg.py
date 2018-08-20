
#-*- coding: utf-8 -*-
"""
Created on Thu May 10 23:41:01 2018

@author: nina
"""

import random
import numpy
from copy import copy, deepcopy
import matplotlib.pyplot as plt
import json

brojJedinki=100
brojCiklusa=100
#koeficijentMutacije=0.02
koeficijentKrosovera=0.05
brojGeneracija=10
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



#def razmnozavanje(poeni,pop):
#    brojJedinki=len(pop)
#    lpoeni=list(poeni)
#    populacija2=deepcopy(pop)
#    sv=numpy.mean(poeni)
#    std=numpy.std(poeni)
#    for i in range (brojJedinki):
#        if poeni[i]<=sv-1.2*std:
#            populacija2.remove(pop[i])
#    l=len(pop)-len(populacija2)
##    print (l)
#    populacija2=[x for _, x in sorted(zip(poeni,populacija2))]
#    for i in range (l):
#        populacija2.append(pop[i])
#    pop=deepcopy(populacija2)
##    print(len(pop))
#    return pop

def razmnozavanje(poeni,pop):
    lpoeni=list(poeni)
    populacija2=deepcopy(pop)
    populacija2=[x for _, x in sorted(zip(poeni,populacija2))]
    for n in range (7):
        populacija2.append(populacija2[n])
        lpoeni.append(poeni[n])
    populacija2=[x for _, x in sorted(zip(lpoeni,populacija2))]
    populacija2=populacija2[::-1]
    populacija2=populacija2[7:]
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


def genetskiAlgoritam(koef, matrica, matricap): 
    vreme=list(range(0,brojGeneracija))
    populacija=kreirajPopulaciju()
    nizSrednjihPoena=[]
    #minOdstupanje=7000
    for t in range (brojGeneracija):
        poeni=dodavanjePoena(populacija)
        populacija=razmnozavanje(poeni,populacija)
        mutacije(populacija,koef)
#        print(populacija)
        krosover(populacija)
        nizSrednjihPoena.append (numpy.mean(poeni)/(99*brojCiklusa))
#        odstupanje=numpy.std(poeni)
#        if odstupanje<=minOdstupanje:
#            minOdstupanje=odstupanje
        for k in range (brojJedinki):
            for i in range (0,64):
                matricap[t][i]+=poeni[k]
        for k in range (brojJedinki):
            for i in range (0,64):
                matricap[t][i]=int(matricap[t][i]/(99*brojCiklusa))                
        for k in range (brojJedinki):
            for i in range (0,64):
                if populacija[k]==i:
                    matrica[t][i]=matrica[t][i]+1
                    

    plt.hist(poeni/ (99*brojCiklusa))
    plt.ylabel('Broj jedinki')
    plt.xlabel('Poeni')
    plt.title('Zastupljenost poena u generaciji')
    plt.show()
    for i in range (64):
        plt.plot(vreme,column(matrica,[i]))
#        putanja=(r'C:\Users\nina\Desktop\projekat2018\svaka1\grafik')
#        b=putanja + str(i) + '.jpg'
#        ''.join(b)
        plt.ylabel('zastupljenst u drustvu [%]')
        plt.xlabel('t [generacija]')
        plt.title('Zastupljenost srategija po generaciji')
    plt.show()
#        plt.savefig(b)
#        plt.clf()
    for i in range (64):
        plt.plot(vreme,column(matricap,[i]))
#        putanja=(r'C:\Users\nina\Desktop\projekat2018\poeni_svake1\grafik')
#        b=putanja + str(i) + '.jpg'
#        ''.join(b)
        plt.ylabel('srednji poeni startegije')
        plt.xlabel('t [generacija]')
        plt.title('Srednji poeni srategije po generaciji')
    plt.show()
#        plt.savefig(b)
#        plt.clf()

    return nizSrednjihPoena, matrica, matricap


def sve(koeficijentMutacije):
    srednja=[]
    o=list(range(0,64))  
    matricaZastupljenosti= numpy.zeros([brojGeneracija,64], dtype=int)
    matricaP= numpy.zeros([brojGeneracija,64], dtype=int)
    for x in range (10):
        print (x)
        s=[]
        vreme=list(range(brojGeneracija))
        g=genetskiAlgoritam(koeficijentMutacije, matricaZastupljenosti,matricaP) 
        #prviMinimum=-1
        matrica=g[1]
        srednjaVrednost=g[0]
        srednja.append(srednjaVrednost)
        matricaPo=g[2]
#        if (g[2]<=):
#            if (prviMinimum==-1):
#                prviMinimum=x
        plt.plot(vreme,srednjaVrednost)
        axes = plt.gca()
        axes.set_ylim([0,5])
        plt.ylabel('srednji poeni')
        plt.xlabel('generacija')
        plt.title('Srednji poeni po generaciji')
#        putanja=(r'C:\Users\nina\Desktop\projekat2018\srednji_poeni1\grafik')
#        b=putanja + str(x) + '.jpg'
#        ''.join(b)
#        plt.savefig(b)
        plt.show()
        plt.bar(o,matrica[brojGeneracija-1])
        plt.ylabel('Zastupljenost strategije')
        plt.xlabel('Različite stretgije')
        plt.title('Zastupljenost strategija u posledjoj generaciji')
        plt.show()
    numpy.rot90(srednja,3)
    for x in range (brojGeneracija):
        n=column(srednja,x)
        m=numpy.mean(n)
        s.append(m)
    plt.plot(vreme,s)
    axes = plt.gca()
    axes.set_ylim([0,5])
    plt.ylabel('Srednji poeni')
    plt.xlabel('Generacija')
    plt.title('Srednji poeni po generaciji')
    plt.show()
    return(matricaZastupljenosti, matricaPo)
    #return prviMinimum

#def svesve():
##    matricaNova=[64][10]
#    koeficijentMut=numpy.zeros(10, dtype=float)
#    matricaNova = []
#    for i in range(10):
#        koeficijentMut[i]=i/100
#        s=sve(koeficijentMut)
#        matricaNova.append(s[0])
#    for j in range(len(matricaNova[0])):
#        tempNiz = numpy.array([])
#        for i in matricaNova:
#            tempNiz = numpy.append(tempNiz, i[j])
#        plt.plot(koeficijentMut, tempNiz)
#        plt.ylabel('Populacija')
#        plt.xlabel('koeficijent mutacije')
#        plt.title('grafik zavisnosti')
#        plt.show()
                
    
#    plt.plot(prviMin,koeficijentMutacije)
#    plt.ylabel('Broj ranova')
#    plt.xlabel('koeficijent mutacije')
#    plt.title('Zavisnost broja ranova u kojima se društvo stabilizuje od parametra mutacije')
#    plt.show

matricaPoena=svakaSaSvakom()    






matricaPoena=svakaSaSvakom()

        #plt.scatter(t,numpy.mean(poeni)/(99*brojCiklusa))
    #axes = plt.gca()
    #axes.set_ylim([0,5])
    #plt.show()
#  