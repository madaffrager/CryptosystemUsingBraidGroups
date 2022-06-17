# Mon TIPE consiste à étudier le groupe des tresses d'Artin et ses propriétés afin de pouvoir en déduire un système de cryptographie utilisant des tresses au lieu des nombres, et de voir la viabilité de ce système. 
# Pour cela, je m'intéresse au problème du mot dans le groupe des tresses, mais aussi au problème de conjugaison qui est plus compliqué à résoudre.  
# Par définition, le groupe des tresses à n brins est un groupe engendré par n-1 générateurs et leurs inverses dans ce groupe et qui entretiennent des relations entre eux. 
# Ce sont ces relations qui donnent sa particularité au groupe. On peut représenter les éléments de ce groupe par des tresses, d'où son nom, mais aussi par des mots sur l'alphabet des générateurs du groupe. 
# Je me suis intéressé dans ce groupe à plusieurs de ses propriétés utiles pour les algorithmes qui me servent à la cryptographie à base de tresses, comme la forme normale des tresses ou l'ordre total de Dehornoy sur ce groupe. 
# Afin de résoudre le problème du mot, c'est-à-dire de savoir si deux tresses sont les mêmes dans deux représentations différentes, j'ai utilisé l'algorithme de retournement. 
# En appliquant deux fois cet algorithme à la différence de deux tresses, il permet de vérifier si cette différence est la tresse nulle et donc de savoir si les tresses sont équivalentes. 
# L'algorithme de retournement permet aussi de trouver une forme unique pour une tresse, en imposant en plus quelques conditions sur l'ordre des facteurs dans les sous-tresses positives et négatives. 
# En ce qui concerne la cryptographie, j'ai adapté des protocoles de cryptographie à clé publique aux groupes des tresses en me ramenant au cas de sous-groupes commutatifs. 
# Je n'ai malheureusement pas eu le temps de m'intéresser aux différentes attaques cryptographiques sur le groupe des tresses, comme la résolution du problème de conjugaison ou des attaques spécifiques sur la forme normale.

## opération sur les tresses (le sens positif des tresses est de gauche à droite) : une tresse est représentée par sous forme de liste, ou chaque élément est un doublet où le premier élément est le sens de la tresse, et le second le numéro le numéro du générateur. 

def somme_tresses(T1,T2):
    return T1 + T2
    
def miroir_tresses(T1): ## renvoie l'inverse d'une tresse pour la loi de groupe, qui est la réflexion dans un miroir de cette tresse
    T2 = []
    n = len(T1)
    for i in range(1,n+1) :
        if T1[n-i][0] == 'h':
            T2.append(('b',T1[n-i][1]))
        else :
            T2.append(('h',T1[n-i][1]))
    return T2
    
def echange(L,i,j):
    a = L[i]
    L[i] = L[j]
    L[j] = a
    
def tri_tresses(T1):
    bol = True
    bol2 = False
    n = len(T1)
    while bol :
        bol = False
        for i in range(n-1):
            if (T1[i][1]>T1[i+1][1])and(abs(T1[i][1]-T1[i+1][1])>1) :
                echange(T1,i,i+1)
                bol = True
                bol2 = True
    return bol2
    
def reduction_tresses(T1):
    n = len(T1)
    bol = True
    bol2 = False
    while bol :
        bol = False
        i = 0
        while i<n-1 :
            if (T1[i][0] != T1[i+1][0])and(T1[i][1] == T1[i+1][1]):
                del T1[i+1]
                del T1[i]
                n -= 2
                bol = True
                bol2 = True
            i += 1
    
def reduction_trivial(T1):
    bol1 = True 
    bol2 = True 
    while bol1 or bol2 :
        bol1 = (tri_tresses(T1))
        bol2 = (reduction_tresses(T1))
    return T1
    
def decalage_tresses(T,p,n):
    for i in range(len(T)):
        T[i] = (T[i][0],(T[i][1]+p)%(n-1)+1)
        return T

def tresse_normale(n):
    T = []
    L = []
    for i in range(1,n):
        L.insert(0,('h',i))
        T = T + L
    return T

## forme normale

def insert_liste(L,l,p):
    for i in range(len(l)):
        L.insert(p+i,l[i])
    
def maP(f,L):
    for i in range(len(L)):
        L[i] = f(L[i])

def reduction_normale(n,k):
    T = tresse_normale(n) + [('b',k)]
    j = len(T) - 1
    L = []
    i = -1
    while j != 0 :
        if abs(T[j-1][1] - T[j][1]) > 1:
            echange(T,j-1,j)
            j -= 1
        elif T[j-1][1] == T[j][1]:
            del(T[j])
            del(T[j-1])
            def a(x):
                    return x-2
            maP(a,L)
            if i != -1:
                j = L[i]
                del(L[i])
                i -= 1
            else :
                j = 0
        elif abs(T[j-1][1] - T[j][1]) == 1:
            T.insert(j-1,('h',T[j][1]))
            T.insert(j-1,('b',T[j][1]))
            T.insert(j-1,T[j+2])
            del(T[j+3])
            def b(x):
                return x+2
            maP(b,L)
            j -= 1
            L.append(j+1)
            i += 1
    return T
    
def forme_normale(T,n):
    T.insert(0,('delta',0))
    m = len(T)
    i = 1 
    while i < m :
        if T[i][0] == 'b':
            T[0] = (T[0][0],T[0][1] - 1)
            D = reduction_normale(n,T[i][1])
            d = len(D)
            del(T[i])
            insert_liste(T,D,i)
            m += d - 1
            i += d
        else :
            i += 1
    return T
    
def forme_normale_degeu(T,n):
    T = forme_normale(T,n)
    D = miroir_tresses(tresse_normale(n))
    r = abs(T[0][1])
    del(T[0])
    for i in range(r):
        T = D + T
    return T
    
def forme_normale_bien(T,n):
    T = forme_normale(T,n)
    

    
## algorithme de retournement de mot

def retournement(T): ## pas retournement opti
    T1 = T.copy()
    n = len(T1)
    i = 0
    while (i<n-1):
        if (T1[i][0] != T1[i+1][0])and(T1[i][1] == T1[i+1][1]):
            del T1[i+1]
            del T1[i]
            n -= 2
            if i>0:
                i -= 1
        elif (T1[i][0] == 'b')and(T1[i+1][0] == 'h')and(abs(T1[i][1]-T1[i+1][1])>1) :
            echange(T1,i,i+1)
            if i>0:
                i -= 1
        elif (abs(T1[i][1]-T1[i+1][1])==1)and(T1[i][0] == 'b')and(T1[i+1][0] == 'h'):
            a = T1[i][1]
            del T1[i]
            T1.insert(i+1,('b',a))
            T1.insert(i+1,('b',T1[i][1]))
            T1.insert(i+1,('h',a))
            n +=2
            if i>0:
                i -= 1
        elif (T1[i][0] == 'h')and(T1[i+1][0] == 'h')and(T1[i][1]>1+T1[i+1][1]):
            echange(T1,i,i+1)
            if i>0:
                i -= 1
        elif (T1[i][0] == 'b')and(T1[i+1][0] == 'b')and(T1[i][1]+1<T1[i+1][1]):
            echange(T1,i,i+1)
            if i>0:
                i -= 1
        else:
             i += 1
    return T1
    
def comparaison(T1,T2): 
    T = retournement(T1 + miroir_tresses(T2))
    print(tresses_retournee(T))
    i = 0
    while T[i][0] == 'h':
        i += 1
    L = []
    n = len(T)
    for j in range(n):
        L.append(T[(j+i)%n])
    return retournement(L)
    
def tresses_retournee(T):
    boll = True
    bol = True
    i = 0 
    n = len(T)
    while (i < n)and(bol):
        if (T[i][0] == 'b')and(boll):
            boll = False
        elif (T[i][0] == 'h')and(not(boll)):
            bol = False
        i += 1
    return bol


## cryptographie avec tresses

import random
def tresses_hasard(m,n,q):
    T = []
    for i in range(q):
        a = random.randint(0,1)
        b = random.randint(m,n)
        if a == 0:
            T.append(('h',b))
        else:
            T.append(('b',b))
    return T
    
def base_q_to_nb(L,q):
    n = 0
    for i in range(len(L)):
        n += L[i]*(q**i)
    return n
    
def nb_to_base_q(n,q):
    L = []
    while n != 0:
        L.append(n%q)
        n = (n - (n%q))//q
    return L
    
def prehash_tresses(T):
    s = ""
    for i in range(len(T)):
        s += T[i][0] + str(T[i][1])
    return s

def somme_mod_2(n,m):
    i = 1
    code = 0
    while (n != 0)or(m != 0):
        code += i*((n + m)%2)
        n = n//2
        m = m//2
        i = i*2
    return (code)
    
def liste_to_mot(L):
    s = ""
    for i in range(len(L)):
        if L[i] == 0:
            s += " "
        else:
            s += chr(L[i]+96)
    return s
    
def mot_to_liste(mot):
    L = []
    for i in range(len(mot)):
        if mot[i] == ' ':
            L.append(0)
        else:
            L.append(ord(mot[i])-96)
    return L
    
def cryptage_tresses(mot,T1,T2,nb_indice,num,long):
    L = mot_to_liste(mot)
    n = base_q_to_nb(L,27)
    print("Transformation de mot "+ s + " en Liste à base "+str(nb)+". n = "+str(n))
    R = tresses_hasard(num,nb_indice+num-1,long)
    print("Tresse de cryptage :",R)
    R2 = miroir_tresses(R)
    X = R + T1 + R2
    print("X = R + P1 + R-1 = ",X)
    Y = R + T2 + R2
    print("Y = R + P2 + R-1 = ",Y)

    m = abs(hash(prehash_tresses(retournement(Y))))
    print("Hachage du retournement de mot Y, m = ",m)
    
    return(X,somme_mod_2(n,m))
        
def dechiffrer_tresses(X,m,S):
    X2 = S + X + miroir_tresses(S)
    x2 = abs(hash(prehash_tresses(retournement(X2))))
    print("Hachage du retournement de mot S+X+S-1 :",x2)
    L = nb_to_base_q(somme_mod_2(x2,m),27)
    return liste_to_mot(L)
    
## test

s = "anwar"
print("message à crypté par les tresses :",s)
long = 10
print("longueur de tresses : ",long)
nb = 10 
print("indice de tresses : ",long)

S = tresses_hasard(1,nb,long)
print("Tresse privée S : ",S)

P1 = tresses_hasard(1,2*nb+1,long)
print("Tresse Publique P1 : ",P1)
P2 = S + P1 + miroir_tresses(S)
print("P2 = S + P1 + S-1 : ",P2)
print("\n############################ CHIFFREMENT ############################\n")
(X,M) = cryptage_tresses(s,P1,P2,nb,nb+2,long)
print("Tresse X = ",X)
print("la somme modulo 2 de(n,m) = ",M)
print("############################ DECHIFFREMENT ############################")
print("Mot déchiffré :",dechiffrer_tresses(X,M,S))


## illustration des tresses

import matplotlib.pyplot as plt

def graphe_perm(e,i,dec,prof):
    if e == 'h':
        plt.plot([dec+i,dec+i+1],[prof,prof-1],'k')
        plt.plot([dec+i+1,dec+i+2/3],[prof,prof-1/3],'k')
        plt.plot([dec+i+1/3,dec+i],[prof-2/3,prof-1],'k')
    else:
        plt.plot([dec+i+1,dec+i],[prof,prof-1],'k')
        plt.plot([dec+i+1,dec+i+2/3],[prof-1,prof-2/3],'k')
        plt.plot([dec+i+1/3,dec+i],[prof-1/3,prof],'k')

def graphe_droit(i,dec,prof):
    plt.plot([dec+i,dec+i],[prof,prof-1],'k')
    
def graphe_portion(l,m,dec,prof):
    for i in range(1,m+1):
        if i == l[1]:
            graphe_perm(l[0],l[1],dec,prof)
        elif i != (l[1]+1):
            graphe_droit(i,dec,prof)
            
def graphe_tresse(T,n,dec=0):
    for i in range(len(T)):
        graphe_portion(T[i],n,dec,-i)
    
def graphe_liste_tresses(L,n):
    for i in range(len(L)):
        graphe_tresse(L[i],n,i*(n+1))
    plt.show()


    




















  