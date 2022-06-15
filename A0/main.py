from math import sqrt
from unittest import result


def main():
    file = open('Docs/wi29.txt') 
    graphs_matriz = open("Docs/be_someone.txt", 'w') 
    lines = file.readlines()
    vector, process_matriz = [],[]

    
    for line in lines:
       line = line.split(' ')
       line[2] = line[2].replace('\n','')
       vector.append(line)
       #print(line)

   
    for i in vector:
        temp =[]
        for j in vector:
            result = sqrt((float(i[1])-float(j[1]))**2 + (float(i[2]) - float(j[2]))**2)
            temp.append(int(round(result)))
        process_matriz.append(temp)

    for line in process_matriz:
        for k in line:
            graphs_matriz.write(str(k) )
            graphs_matriz.write(' ')
        graphs_matriz.write("\n")

#CODIGO PRINCIPAL, chamando as função
if __name__ == '__main__':
	main()
