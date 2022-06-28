# reveja esta video aqui < https://www.youtube.com/watch?v=qMELaoBnMyY >
# Cálculo Numérico - Interpolação Polinomial 

import numpy as np 
import matplotlib.pylab as plt


def poly(x,y):
    n = len(x) -1
    A =[]
    B =[]
    for xi in x:
        row =[1]
        for j in range(1,n+1):
            row.append(xi**j)
        A.append(row)
    return np.linalg.solve(A,y)

def func_poly(x,coefientes):
    first = coefientes[0]
    return first + sum ([ai * x ** j for j, ai in enumerate(coefientes[1:],1)])



if __name__ == '__main__':

    #exemplos de dados
    #x = [-2,0,1,2]
    #y = [-47,3,4,41]
    #x = [1,2,3]
    #y =[1,4,1]
    #final de exemplos de dados
   
    #exemplo de PI
    x = [0,np.pi /2, np.pi]
    y = [0,1,0]


    coefientes = poly(x,y)
    print(coefientes)

    def p(x):
        print("caiu aqui no def p")
        return func_poly(x, coefientes)

    t =np.linspace(min(x),max(x),200)
    pt =[p(ti) for ti in t]
    #exemplo funcao do seno
    st =np.sin(t) #seno

    plt.plot(t,st)#seno
    plt.plot(t,pt)


    plt.savefig('interp.png')

    plt.scatter(x,y)