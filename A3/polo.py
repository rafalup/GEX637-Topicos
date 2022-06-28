'''
# -*- coding: utf-8 -*-
'''
import math
import numpy as np

#----------------------------------------------------------------------
#FUNCÇÃO OPCIONAL PARA COMPARAR COM A INTERPOLAÇÃO (OPCIONAL)
def f(x):
    return math.tan(x)

#----------------------------------------------------------------------
#LISTA DE PONTOS
'''
Pontos baseados no exercicio 6a da lista 10
(fechou com as respostas do autor)
'''
# pontos_x = [0,0.25,0.50,0.75]
# pontos_y = [1,1.64872,2.71828,4.48169]

pontos_x = [-2,0,1,2]
pontos_y = [-47,3,4,41]

# pontos_x = [0.84,3.46,6,9,13]
# pontos_y = [0.64,3.2,-1,4,2.2]


#----------------------------------------------------------------------
#LEITURA MANUAL DOS DADOS (OPCINAL)
'''
#GERA Y EM FUNÇÃO DE X (OPCIONAL)
for x in pontos_x:
    pontos_y.append(f(x))    
#INSERE PONTOS MANUALMENTE (OPCIONAL)
qtd_pontos = input("Quantidade de pontos para interpolação: ")
for i in range(0,qtd_pontos):
    x = input("x{} = ".format(i))
    y = input("y{} = ".format(i))
    pontos_x.append(x)
    pontos_y.append(y)
    
'''

#----------------------------------------------------------------------
#GRAU MÁXIMO DE INTERPOLAÇÃO
print ("POLINOMIO INTERPOLADOR DE LAGRANGE \n")
grau = int(input("Grau maximo de interpolação(1 <= int <= {}): ".format(len(pontos_x)-1))) + 1
print ("x: ", pontos_x)
print ("y: ", pontos_y)

#----------------------------------------------------------------------
#PONTO DE ANÁLISE
#x0 = input("Ponto de análise: ") #declaração manual (opcional)
#x0 = 0.43
x0= 4
print ('x0 = {}'.format(x0))
#----------------------------------------------------------------------
#CÁLCULO DE Li
L = []
result = 1 #para o produtório
for i in range(0, grau): 
    print ('--------')
    for j in range(0, grau):
        if (i != j):
            print (x0,'-',pontos_x[j],'/',pontos_x[i],'-',pontos_x[j],'=',((x0 - pontos_x[j])/(pontos_x[i] - pontos_x[j])))
            result = result * ((x0 - pontos_x[j])/(pontos_x[i] - pontos_x[j]))
    L.append(result)
    result = 1

#----------------------------------------------------------------------
#Li * Yi
print ('\nL*y')
for i in range(0, grau):
    print ('--------')
    print (L[i],'*',pontos_y[i],'=',L[i]*pontos_y[i])
    L[i] = L[i]*pontos_y[i]

#----------------------------------------------------------------------
#SOMATÓRIO
P = sum(L)

#--------------------------------------------------------------------------
print('\nPolinomio:')
'''
Para graus menores que o grau máximo
a função polyfit retorna o polinomio mediano
entre todos os pontos.
'''
p  =  np.polyfit (pontos_x, pontos_y, grau-1)

casas_decimais = 5 #para os prints
j = (len(p)-1)
for i in range(0, len(p)):
    print (round(p[i],casas_decimais),'x^{}'.format(j))
    j -= 1

#print 'f({}) = {}'.format(x0, round(f(x0),casas_decimais)) #caso comparação com função real (OPCIONAL)
print ('\nP({}) = {}'.format(x0, round(P,casas_decimais)))
#print 'Erro Abs: {}'.format(round(math.fabs(f(x0) - P),casas_decimais)) #para saber o erro abs da função real (OPCIONAL)

