from random import sample
import pandas as pd 
import numpy as np
import time


def VerificaPath(path, matrix):
    cost = 0
    print(cost)
    for p in range(len(path)):
        print(p)
        if p == (len(path) - 1) :
            cost += matrix [ path[p] ] [ path [0] ]
        else:
            cost += matrix[path[p]] [path[p+1]]
        
    return cost


resultsFinal = pd.DataFrame()




#matrix = pd.read_csv(f'Docs/matrixwi29.csv', header=None)
matrix = open('Docs/matrixwi29.txt',"r+")
#matrix = matrix.to_numpy()
timeInst = len(matrix) * 60/100
print(timeInst)
cidades = len (matrix)

results = pd.DataFrame()
bestPath =[]
minCost = 999999999999
   
for i in range(10):
    start = time.time()
    while True:
        path = sample(range(cidades), cidades)
        currentCost = VerificaPath(path, matrix)

        if currentCost < minCost:
            minCost = currentCost
            bestPath = path
        end = time.time()
        t = end - start
        print(t)

        if t > timeInst:
            break
        
        
        results = results.append({'tempo': t ,'custo':minCost, 'path': " ".join(str(w) for w in bestPath)}, ignore_index= True)
    resultsFinal = resultsFinal.append(

        {
            'instancia': 'opa',
            'autoria': 'op',
            'algoritmo': 'ad',
            'q-custo': int(results.custo.mean()),
            'q-desvio':round(results.custo.std(),2),
            'q-medio':int(results.tempo.mean())}, ignore_index= True)
resultsFinal.to_csv('resultados.csv')