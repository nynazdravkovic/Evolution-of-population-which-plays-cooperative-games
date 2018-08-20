

# -*- coding: utf-8 -*-
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
brojCiklusa=200
#koeficijentMutacije=0.02
koeficijentKrosovera=0.05
brojGeneracija=5000
cc=1
cd=0
dc=5
dd=3
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
        matrica[t][0]+=matrica[t][1]+matrica[t][2]+matrica[t][3]+matrica[t][4]+matrica[t][5]+matrica[t][6]+matrica[t][8]+matrica[t][9]+matrica[t][11]+matrica[t][12]+matrica[t][13]
        #matrica[t][0]=matrica[t][0]/12
        #grupa1
        matrica[t][16]=(matrica[t][16]+matrica[t][18]+matrica[t][19])#/3
        matrica[t][58]=(matrica[t][58]+matrica[t][57]+matrica[t][56])#/3
        #grupa2
        matrica[t][15]=(matrica[t][15]+matrica[t][14])#/2
        #tft
        matrica[t][21]=(matrica[t][21]+matrica[t][23])#/2
        matrica[t][41]=(matrica[t][41]+matrica[t][43])#/2
        #gtft
        matrica[t][52]=(matrica[t][52]+matrica[t][53]+matrica[t][55])#/3
        matrica[t][33]=(matrica[t][34]+matrica[t][35]+matrica[t][33])#/3
        #grupa3
        matrica[t][20]=(matrica[t][20]+matrica[t][22])#/2
        matrica[t][59]=(matrica[t][59]+matrica[t][40])#/2
        #grupa5
        matrica[t][24]=(matrica[t][24]+matrica[t][27])#/2
        matrica[t][42]=(matrica[t][42]+matrica[t][26])#/2
        #grupa4
        #pavlov
        matrica[t][36]=(matrica[t][36]+matrica[t][39]+matrica[t][26])#/3
        matrica[t][25]=(matrica[t][25]+matrica[t][37]+matrica[t][38])#/3
        #flipflop
        matrica[t][48]=(matrica[t][48]+matrica[t][49])#/2
        matrica[t][50]=(matrica[t][50]+matrica[t][51])#/2
        matrica[t][63]=(matrica[t][63]+matrica[t][15]+matrica[t][62]+matrica[t][30]+matrica[t][31]+matrica[t][61]+matrica[t][29]+matrica[t][60]+matrica[t][44]+matrica[t][46]+matrica[t][47]+matrica[t][14])#/12
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
        matrica[t][14]=0
        matrica[t][15]=0
        matrica[t][19]=0
        matrica[t][18]=0
        matrica[t][22]=0
        matrica[t][23]=0
        matrica[t][27]=0
        matrica[t][29]=0
        matrica[t][30]=0
        matrica[t][31]=0
        matrica[t][34]=0
        matrica[t][35]=0
        matrica[t][37]=0
        matrica[t][38]=0
        matrica[t][39]=0
        matrica[t][42]=0
        matrica[t][43]=0
        matrica[t][44]=0
        matrica[t][46]=0
        matrica[t][47]=0
        matrica[t][49]=0
        matrica[t][51]=0
        matrica[t][53]=0
        matrica[t][55]=0
        matrica[t][57]=0
        matrica[t][58]=0
        matrica[t][60]=0
        matrica[t][61]=0
        matrica[t][62]=0
        matricap[t][0]+=matricap[t][1]+matricap[t][2]+matricap[t][3]+matricap[t][4]+matricap[t][5]+matricap[t][6]+matricap[t][8]+matricap[t][9]+matricap[t][11]+matricap[t][12]+matricap[t][13]
        #matricap[t][0]=matricap[t][0]/12
        #grupa1
        matricap[t][16]=(matricap[t][16]+matricap[t][18]+matricap[t][19])#/3
        matricap[t][58]=(matricap[t][58]+matricap[t][57]+matricap[t][56])#/3
        #grupa2
        matricap[t][15]=(matricap[t][15]+matricap[t][14])#/2
        #tft
        matricap[t][21]=(matricap[t][21]+matricap[t][23])#/2
        matricap[t][41]=(matricap[t][41]+matricap[t][43])#/2
        #gtft
        matricap[t][52]=(matricap[t][52]+matricap[t][53]+matricap[t][55])#/3
        matricap[t][33]=(matricap[t][34]+matricap[t][35]+matricap[t][33])#/3
        #grupa3
        matricap[t][20]=(matricap[t][20]+matricap[t][22])#/2
        matricap[t][59]=(matricap[t][59]+matricap[t][40])#/2
        #grupa5
        matricap[t][24]=(matricap[t][24]+matricap[t][27])#/2
        matricap[t][42]=(matricap[t][42]+matricap[t][26])#/2
        #grupa4
        #pavlov
        matricap[t][36]=(matricap[t][36]+matricap[t][39]+matricap[t][26])#/3
        matricap[t][25]=(matricap[t][25]+matricap[t][37]+matricap[t][38])#/3
        #flipflop
        matricap[t][48]=(matricap[t][48]+matricap[t][49])#/2
        matricap[t][50]=(matricap[t][50]+matricap[t][51])#/2
        matricap[t][63]=(matricap[t][63]+matricap[t][15]+matricap[t][62]+matricap[t][30]+matricap[t][31]+matricap[t][61]+matricap[t][29]+matricap[t][60]+matricap[t][44]+matricap[t][46]+matricap[t][47]+matricap[t][14])#/12
        matricap[t][1]=0
        matricap[t][2]=0   
        matricap[t][3]=0
        matricap[t][4]=0
        matricap[t][5]=0
        matricap[t][6]=0
        matricap[t][8]=0
        matricap[t][9]=0
        matricap[t][11]=0
        matricap[t][12]=0
        matricap[t][13]=0
        matricap[t][14]=0
        matricap[t][15]=0
        matricap[t][19]=0
        matricap[t][18]=0
        matricap[t][22]=0
        matricap[t][23]=0
        matricap[t][27]=0
        matricap[t][29]=0
        matricap[t][30]=0
        matricap[t][31]=0
        matricap[t][34]=0
        matricap[t][35]=0
        matricap[t][37]=0
        matricap[t][38]=0
        matricap[t][39]=0
        matricap[t][42]=0
        matricap[t][43]=0
        matricap[t][44]=0
        matricap[t][46]=0
        matricap[t][47]=0
        matricap[t][49]=0
        matricap[t][51]=0
        matricap[t][53]=0
        matricap[t][55]=0
        matricap[t][57]=0
        matricap[t][58]=0
        matricap[t][60]=0
        matricap[t][61]=0
        matricap[t][62]=0
    plt.hist(poeni/(99*brojCiklusa))
    plt.ylabel('Broj jedinki')
    plt.xlabel('Poeni')
    plt.title('Zastupljenost poena u generaciji')
    plt.show()
    for i in range (64):
        plt.plot(vreme,column(matrica,[i]))
        putanja=(r'C:\Users\nina\Desktop\projekat2018\svaka1\grafik')
        b=putanja + str(i) + '.jpg'
        ''.join(b)
        plt.ylabel('zastupljenst u drustvu [%]')
        plt.xlabel('t [generacija]')
        plt.title('Zastupljenost srategija po generaciji')
        plt.savefig(b)
        plt.clf()
    for i in range (64):
        plt.plot(vreme,column(matricap,[i]))
        putanja=(r'C:\Users\nina\Desktop\projekat2018\poeni_svake1\grafik')
        b=putanja + str(i) + '.jpg'
        ''.join(b)
        plt.ylabel('srednji poeni startegije')
        plt.xlabel('t [generacija]')
        plt.title('Srednji poeni srategije po generaciji')
        plt.savefig(b)
        plt.clf()
#        srednja=numpy.n.mean(1) #ako obrnemo ose onda je 0, a ne 1
#        odstupanje=numpy.n.std(1)
#        minimalno=odstupanje[0]
#        for i in range(brojGeneracija):
#            if(odstupanje[i]<minimalno):
#                minimalno=odstupanje[i]
#                pamtiIndex=1
#        procenat=(minimalno/srednja[pamtiIndex])*100
    
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
#        A = numpy.asarray(matrica).reshape(-1)
#        with open('test1.txt', 'w') as f:
#            f.write(json.dumps(A))
#        f.close()
#        putanja1=(r'C:\Users\nina\Desktop\projekat2018\txt\matrica')
#        b=putanja1 +str(i)+ '.txt'
        srednjaVrednost=g[0]
        srednja.append(srednjaVrednost)
        matricaPo=g[2]
#        A = numpy.asarray(matricaPo).reshape(-1)
#        with open('test1.txt', 'w') as f:
#            f.write(json.dumps(A))
#        f.close()
#        putanja=(r'C:\Users\nina\Desktop\projekat2018\txt\matricaPo')
#        b=putanja +str(i)+ '.txt'

#        if (g[2]<=):
#            if (prviMinimum==-1):
#                prviMinimum=x
        plt.plot(vreme,srednjaVrednost)
        axes = plt.gca()
        axes.set_ylim([0,5])
        plt.ylabel('srednji poeni')
        plt.xlabel('generacija')
        plt.title('Srednji poeni po generaciji')
        putanja=(r'C:\Users\nina\Desktop\projekat2018\srednji_poeni1\grafik')
        b=putanja + str(x) + '.jpg'
        ''.join(b)
        plt.savefig(b)
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
