from random import random
from math_braid import Braid

# n: braid width (number of strands)
# p: power of fundamental element D in left canonical form
# k: number of canonical factors (implemented via a getter)
# a: list of canonical factors
N=8
l=4
x=Braid.random(N,l)
print("La tresse publique x =",x)
a=Braid.random(N,1)
print("A’s private key a =",a)
b=Braid.random(N,l)
print("B’s private key b =",b)

pa=Braid.random(N,1)
pa=a.__invert__()
pa=pa.__mul__(x)
pa=pa.__mul__(a)
print("A’s public key y_A = a^-1 * x * a =",pa)
pb=Braid.random(N,1)
pb=b.__invert__()
pb=pb.__mul__(x)
pb=pb.__mul__(b)
print("B’s public key y_B = b^-1 * x * b =",pb)
print(" Alice reçoit la clé publique de Bob et calcule la clé K partagée :")
K=Braid.random(N,1)
K=a.__invert__()
K=K.__mul__(pb)
K=K.__mul__(a)
print(K)
print(" Bob reçoit la clé publique de Alice et calcule la clé K partagée :")
K=Braid.random(N,1)
K=b.__invert__()
K=K.__mul__(pa)
K=K.__mul__(b)
print(K)
print("Nous voyons que A et B calculent la même clé K, comme prévu.")