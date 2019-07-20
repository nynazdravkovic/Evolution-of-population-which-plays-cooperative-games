# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 23:56:09 2019

@author: nina
"""

import pandas as pd
import numpy
import matplotlib.pyplot as plt

g = (pd.read_excel (r"C:\Users\nina\Desktop\greske_harmony_mut.xlsx"))
m = (pd.read_excel (r"C:\Users\nina\Desktop\harmony_mut.xlsx"))
koeficijentMutacije = list(range(20))

def column(matrix, k):
    return [row[k] for row in matrix]


plt.plot(koeficijentMutacije,column(m,[0]))
plt.errorbar(koeficijentMutacije,column(m,[0]),column(g,[0]),label='uvek izdaj',marker = "*")
plt.plot(koeficijentMutacije,column(m,[21]))    
plt.errorbar(koeficijentMutacije,column(m,[21]),column(g,[21]), label='TFT', marker="X")
plt.plot(koeficijentMutacije,column(m,[25]))
plt.errorbar(koeficijentMutacije,column(m,[25]),column(g,[25]), label='Pavlov', marker="s")
#plt.plot(koeficijentMutacije,column(m,[36])
#plt.errorbar(koeficijentMutacije,column(m,[36]),column(g,[36]), label='Pavlov k', marker='p')
plt.plot(koeficijentMutacije,column(m,[41]))
plt.errorbar(koeficijentMutacije,column(m,[41]),column(g,[41]),label='TFT k',marker = "o")
plt.plot(koeficijentMutacije,column(m,[50]))
plt.errorbar(koeficijentMutacije,column(m,[50]),column(g,[50]),label='flip flop k',marker = "x")
plt.plot(koeficijentMutacije,column(m,[52]))    
plt.errorbar(koeficijentMutacije,column(m,[52]),column(g,[52]),label='GTFT k',marker = "v")
plt.plot(koeficijentMutacije,column(m,[63]))    
plt.errorbar(koeficijentMutacije,column(m,[63]),column(g,[63]),label='uvek saradjuj',marker =  "p")

plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.ylabel('zastupljenost jedinke [%]')
plt.xlabel('koeficijent mutacije')
plt.title('Grafik zavisnosti zastupljenosti jedinke u poslednjoj generaciji od koeficijenta mutacije')
putanja=(r'C:Users\nina\Desktop\Grafici\mut_cg.eps')
plt.savefig(putanja)
plt.show()