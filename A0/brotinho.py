#forca bruta 
import random

def main():
    data_table = open("Docs/be_someone.txt") 
    vetor , vector_pull = [] ,[]

    n = 0
    while(n < 29):
        vetor.append(n)
        n = n + 1

    random.shuffle(vetor)

    lines = data_table.readlines()
    for up in lines:
        vector_pull.append(up.split(' '))
        
main()