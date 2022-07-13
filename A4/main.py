from random import sample
import pandas as pd
import numpy as np
import time
import random

from scipy import rand

def calculateCost(path, matrix):
   
    cost = 0
    for p in range(len(path)):
        if p == len(path) - 1:
            cost += matrix[ path[p] ][ path[0] ] 
        else:
        
            cost += matrix[ path[p] ][ path[p+1] ] 
    return cost

#retorna o vizinho entre os 30% melhores
def getVizinho(pathCsv):
    pathCsv = pd.DataFrame(pathCsv)
    pathCsv.sort_values(by = ['custo'], inplace = True, ascending= True)
    pathCsv.index = [i for i in range(pathCsv.shape[0])]

    #print(pathCsv.head(10))

    size = int(pathCsv.shape[0] * 0.3)
    vizinho = random.randint(0, size)
    vizinho = pathCsv.iloc[vizinho].vizinho

    #print(f"Vizinho escolhido é {vizinho}")

    return int(vizinho)



def vizinhoPerto(path, matrix, inicial):

    if len(path) == len(matrix):
        #print(path)
        return path 
    while len(path) != len(matrix):
       
        lastNode = path[-1]
        #print('LastNode ', lastNode)
        vizinhos = matrix[:, lastNode]

        pathCsv = {'vizinho': [], 'custo': []}
        for idx, v in enumerate(vizinhos):
            if idx != lastNode:
                pathCsv['vizinho'].append(idx)
                pathCsv['custo'].append(v)

        vizinhoProximo = getVizinho(pathCsv)

        path.append(vizinhoProximo)

    return path
   
    
        
files = ['Djibouti', 'Qatar', 'Uruguay','Western Sahara', 'Zimbabwe']
resultsFinal = pd.DataFrame()
for file in files:
   # print(f'Calculando {file}')
    matrix = pd.read_csv(f'matrizes/matrix{file}.csv', header= None)
    matrix = matrix.to_numpy()
    timeInst = len(matrix) * 60 / 1000
    cidades = len(matrix)
   # print(f'Calculando {file}, tempo cada iteração {timeInst}, cidades {cidades}')
    results = pd.DataFrame()
    allPaths = {}

    #print('caminho inicial', path)
    minCost = 999999999999
    iniciais = []
    inicial = 0
    for i in range(10):
        start = time.time()
        print('iter', i)
        while True:
            path = []
            while inicial in iniciais:
                if  len(iniciais) >= len(matrix):
                    break 
                inicial = random.randint(0, cidades-1)
            iniciais.append(inicial)
            path.append(inicial)

            path = vizinhoPerto(path, matrix, inicial)
            #print('caminho', path)
            #print(f'Caminho... {path[i]} x {path[j]}', path)
            currentCost = calculateCost(path, matrix)
            if currentCost < minCost:
                minCost = currentCost
            allPaths[" ".join(str(s) for s in path)] = currentCost
            
            end = time.time()
            t = end - start
            if t > timeInst:
                done = True
                break
            
        results = results.append({
            'tempo': t,
            'custo': minCost, 
            'path': " ".join(str(w) for w in path)
        }, ignore_index = True)


    resultsFinal = resultsFinal.append(
        {
        'instancia': file,
        'autoria': 'Rafaelle',
        'algoritmo': 'BCGα',
        'q-medio': int(results.custo.mean()),
        'q-desvio': round(results.custo.std(),2),
        't-medio': int(results.tempo.mean())}, ignore_index = True)
    #print(f"Menor custo {minCost} \n Melhor caminho: {bestPath} \n")
resultsFinal.to_csv("resultados.csv")

