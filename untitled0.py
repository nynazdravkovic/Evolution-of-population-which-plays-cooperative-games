Stari deo koda koji se ponavljao stalno i koji radi
def pokreniSukobeUGeneraciji():
    brojJedinki=len(populacija) 
    #print(brojJedinki)
    napraviPoene(brojJedinki)
    istorijaSukoba = numpy.zeros([brojJedinki,brojJedinki], dtype=int)
    for j1 in range(brojJedinki):
        for j2 in range(j1, brojJedinki):
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

