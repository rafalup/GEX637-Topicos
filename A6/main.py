from unittest import result
from random import randrange, sample, choice
from math import floor, sqrt, ceil
from time import clock_getres, time
import pandas as pd
from statistics import pstdev


def HGreX(inst, father, mother, tam):
    son = [-1 for _ in range(tam)]
    unvisited = set()
    for i in range(tam):
        unvisited.add(i)

    for i in range(2):
        son[i] = father[i]
        unvisited.remove(father[i])

    parents = [father, mother]

    for i in range(2, tam):
        a = (parents[1].index(son[i-1]) + 1) % tam
        b = (parents[0].index(son[i-1]) + 1) % tam

        menor = a
        if inst[son[i - 1]][b] < inst[son[i - 1]][menor]:
            menor = b

        son[i] = menor

        if son[i] not in unvisited:
            son[i] = choice(list(unvisited))

        unvisited.remove(son[i])

        parents.reverse()

    return son


def SOVAI_AGHGreX(initialTime, timeLimit, distances, ncidades):

    noSolutions = ceil(sqrt(ncidades))
    if(noSolutions % 2):
        noSolutions += 1

    aux = [i for i in range(ncidades)]
    population = []
    for i in range(noSolutions):
        population.append(sample(aux, ncidades))

    MelhorQualidade = -1

    while(time() - initialTime < timeLimit):

        toReproduce = sample(population, len(population))
        track_pull = []

        for i in range(0, len(toReproduce), 2):
            mae = toReproduce[i]
            pai = toReproduce[i+1]

            track_pull.append(HGreX(distances, mae, pai, ncidades))
            track_pull.append(HGreX(distances, pai, mae, ncidades))

        for Sotrack in track_pull[:int(len(track_pull)*.2)]:
            cities = [randrange(ncidades), randrange(ncidades)]
            Sotrack[cities[0]], Sotrack[cities[1]
                                        ] = Sotrack[cities[1]], Sotrack[cities[0]]

        population.sort(key=lambda x: qualidade(x, distances))
        track_pull.sort(key=lambda x: qualidade(x, distances))
        bestPull = track_pull[:ceil(len(population)*.8)]
        population = population[:floor(len(population) * .2)] + bestPull

        best = qualidade(track_pull[0], distances)
        if best < MelhorQualidade or MelhorQualidade == -1:
            MelhorQualidade = best

    return MelhorQualidade, initialTime


def qualidade(solution, distanceTable):
    totalDistance = 0
    for i in range(len(solution) - 1):
        totalDistance += distanceTable[solution[i]][solution[i+1]]
    totalDistance += distanceTable[solution[-1]][solution[0]]
    return totalDistance


# --------------------------- MAIN INITIAL ---------------------------
PATH = ["Djibouti", "Qatar",  "Western Sahara"]
media, desvio, times = [], [], []
for i in range(3):  # 0 1 2 3
    # distanceTable = Instanciando(i)
    PATH = ["Djibouti", "Qatar", "Western Sahara"]
    with open("Docs/" + PATH[i] + ".txt", "r") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split()
        for j in range(len(lines[i])):
            lines[i][j] = float(lines[i][j])

    ncidades = len(lines)
    tempo_Limite = 180 * ncidades / 1000
    nqualidade, localTime = [], []

    for _ in range(10):
        print('iter', _)
        MelhorQualidade, tempInitial = SOVAI_AGHGreX(
            time(), tempo_Limite, lines, ncidades)

        nqualidade.append(MelhorQualidade)
        localTime.append(time() - tempInitial)
    print("---- ACABOUUU CONTAGEM\n")
    # media da qualidade
    media.append(round(sum(nqualidade) / len(nqualidade)))
    # media do tempo de execucao
    helper = sum(localTime) / len(localTime)
    times.append(round(helper))
    # desvio padrão da qualidade
    desvio.append(round(pstdev(nqualidade), 1))

headers = ["instancia", "autoria", "algoritmo",
           "q-medio", "q-desvio", "t-medio"]
df = pd.DataFrame({"instancia": PATH, "autoria": "Rafaelle", "algoritmo": "AGHGreX",
                   "q-medio": media, "q-desvio": desvio, "t-medio": times})
df.to_csv("./resultados.csv", header=headers, index=False)