import random
from time import time
import pandas as pd
from statistics import pstdev

def Instanciando(indexPath):
    PATH = ["Djibouti", "Qatar", "Uruguay", "Western Sahara", "Zimbabwe"]
    with open("Docs/" + PATH[indexPath] + ".txt", "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].split()
        for j in range(len(lines[i])):
            lines[i][j] = float(lines[i][j])
    return lines


def Work_opt2(arr, a: int, b: int):
    newArr = arr.copy()
    while(a < b):
        aux = newArr[a]
        newArr[a] = newArr[b]
        newArr[b] = aux
        a += 1
        b -= 1
    return newArr


def BLPM2opt(temp_Initial, temp_Limit, matrizDistancias, nCidades):

    solution = [x for x in range(nCidades)]
    random.shuffle(solution)

    first_Quality = 0
    for i in range(len(solution) - 1):
        first_Quality += matrizDistancias[solution[i]][solution[i+1]]

    first_Quality += matrizDistancias[solution[-1]][solution[0]]
    
    tam = len(solution)
   
    for x in range(tam):
  
        y = x + 1
        while(y < tam) and (time() - temp_Initial < temp_Limit):
            if x == y:
                y += 1
                continue

            newSolution = Work_opt2(solution, x, y)

            newQuality = 0
            for i in range(len(solution) - 1):
                newQuality += matrizDistancias[solution[i]][solution[i+1]]
            newQuality += matrizDistancias[solution[-1]][solution[0]]
            
            if(newQuality < first_Quality):

                first_Quality = newQuality
                solution = newSolution
                x = 0
                y = 0

            y += 1

        x += 1

    return first_Quality, temp_Initial

def tempo_medio(values_times):
    hora = 0
    for up in values_times: 
        hora += up

    hora = hora / len(values_times)
    times.append(round(hora))
    return times
    

#================================== MAIN PRINCIPAL ======================================
PATH = ["Djibouti", "Qatar", "Uruguay", "Western Sahara", "Zimbabwe"]
media , desvio , times = [] , [] ,[]

for i in range(len(PATH)):
   
    matrizDistancias = Instanciando(i)
    nCidades = len(matrizDistancias)
    temp_Limit =  60 * nCidades / 1000

    qualities , values_times = [] , []

    for i in range(10):
       
        first_Quality, temp_Initial = BLPM2opt(
            time(), temp_Limit, matrizDistancias, nCidades)

        qualities.append(first_Quality)
        values_times.append(time() - temp_Initial)
        
    media.append(round(sum(qualities) / len(qualities))) 
    time_final = tempo_medio(values_times) #t_medio
    
    desvio.append(round(pstdev(qualities),1))

headers = ["instancia", "autoria", "algoritmo","q-medio", "q-desvio", "t-medio"]

df = pd.DataFrame({"instancia": PATH, "autoria": "Rafaelle",
                       "algoritmo": "BT2opt", "q-medio": media,
                       "q-desvio": desvio, "t-medio": time_final})
df.to_csv("./resultados.csv", header=headers, index=False)