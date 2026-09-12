# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 17:22:21 2026

@author: GracjanM
"""
from math import sin, cos, sqrt, exp
import matplotlib.pyplot as plt


def bisek(a, b, tol, f):
    while abs(b - a) > tol: # pętla wykonuje sie dopuki długosc przedzialu jest wieksza od tol, abs - daje wartosc bezwgledna
        c = (a + b) / 2 # wyznacza srodek przedizału

        if f(a) * f(c) < 0: #spradza zmiane znaku 
            b = c
        else:
            a = c

    return (a + b) / 2 #zwracam srodek ostatniego malego przedzialu - przyblizona wartosc m. zero

#parametry 
Vo = 0.58
a = 6.71
np = 1000

h = Vo / np #krok energi udo tablicowania fun do wykresu
dE = Vo / 100 #krok energii do przeszukiwnia m.zero
tol = Vo / 1000 #dokladnosc bisek

E1 = -Vo + 0.00001 * Vo #lewa strone szukania energii bierze minimlanie wiekszy od -V0
E2 = E1 + dE   #prawa granica 

#listy do wynikow
zero = []
zero_even = []
zero_odd = []

oddplot = []
evenplot = []
energies = []




#---------------------
#Definiuje funkcje psi. 
'''
if spradwza czy punkt lezy wewnatrz studni, jesli tak to psi ma postac cosinus dla parzystcyh i sinus dla nieparzystych.
Jesli jest poza studnia, funkcja znika wykladniczo - powli maleje --> slad tunelowania kwantowego.
W przypadku psi nieparzytsego jesli x jest poza studnia to trzeba sprawdzic po ktorej stronie studni jest. 
'''
#---------------------

def psi_even(x,E):
    k = sqrt(2* (Vo + E))
    kappa = sqrt(-2*E)
    
    if abs(x) <= a/2 :
        return cos(k*x)
    else:
        return cos(k*a/2)*exp(-kappa*(abs(x)-a/2))



def psi_odd(x, E):
    k = sqrt(2 * (Vo + E))
    kappa = sqrt(-2 * E)

    if abs(x) <= a / 2:
        return sin(k * x)
    else:
        if x > 0:               #najpierw spradza czy jest po prawej stronie studni jesli tak to fun zanika wykladniczo
            return sin(k * a / 2) * exp(-kappa * (x - a / 2))
        else:                   #analogiczne tylko ze po lewej stronie i ze znakiem minus by zachowac nieparzystosc psi(-x) = -psi(x)
            return -sin(k * a / 2) * exp(-kappa * (-x - a / 2))



# Funkcje do szukania energii
#----------------------------
        
def feven(E): 
    k = sqrt(2 * (Vo + E))
    return sin(k * a / 2) - cos(k * a / 2) * sqrt(-2 * E) / k


def fodd(E):
    k = sqrt(2 * (Vo + E))
    return sin(k * a / 2) + cos(k * a / 2) * k / sqrt(-2 * E)






# Przygotowanie danych do wykresu - tablicowanie funkcji
#-------------------------------------


for i in range(1, np - 1):
    E = -Vo + i * h # wyznacza energie dla i

    energies.append(E)
    oddplot.append(fodd(E))
    evenplot.append(feven(E))




# Szukanie miejsc zerowych, petla wykonuje sie dopuki prawa granica energii jest mnijesza od 0, jest tak bo szukam stnaów związancyh 
# -V0<E<0 wiec w skrocie szuka energii wlasnych 
#--------------------------------

while E2 < 0:
    if feven(E1) * feven(E2) < 0: #sparwdzam czy feven zmienia znak, jesli tak odpala bisek do szukania zero
        z = bisek(E1, E2, tol, feven)
        zero.append(z)
        zero_even.append(z)

    if fodd(E1) * fodd(E2) < 0:
        z = bisek(E1, E2, tol, fodd)
        zero.append(z)
        zero_odd.append(z)
    #przesuwamy granice w prawo
    E1 = E2
    E2 = E1 + dE




#Wypisanie wyników
print("Wszystkie poziomy energii:")
for z in sorted(zero):
    print(z)

print("\nStany parzyste:")
for z in zero_even:
    print(z)

print("\nStany nieparzyste:")
for z in zero_odd:
    print(z)




'''
    WYKRES funkcji cw 1: feven(E) i fodd(E) 
    *********************************
'''


plt.figure(figsize=(10, 6)) #towrzy figure 10x6
plt.plot(energies, evenplot, label='feven(E)', color='blue') #rysuje funkcje parzysta
plt.plot(energies, oddplot, label='fodd(E)', color='red') #rysuje funkcje nieparzysta
plt.axhline(0, linewidth=2, color='black' ) #rysuje linie na y = 0 by widac przeciecia 

# zaznaczenie miejsc zerowych 
for z in zero_even:
    # rysuje punkt na (z,0), 
    plt.plot(z, 0, 'o', color='purple')

for z in zero_odd:
    plt.plot(z, 0, 's', color='purple')

plt.xlabel('Energia E')
plt.ylabel('F(E)')
plt.title('Funkcje feven(E) i fodd(E)')
plt.legend()
plt.grid(True) #siatka pomocnicza


'''
    WYKRES 2: studnia potencjału i poziomy energii
    ************************************
'''


plt.figure(figsize=(8, 6))

# granice studni
x_left = -a / 2
x_right = a / 2

# rysowanie studni
plt.plot([-2, x_left], [0, 0], color='black') # rysuje poziomy odcinkek po lewej stronie, v = 0
plt.plot([x_left, x_left], [0, -Vo], color='black') #rysuje pionowa lewa sciane studni
plt.plot([x_left, x_right], [-Vo, -Vo], color='black' ) #rysuje dno studni
plt.plot([x_right, x_right], [-Vo, 0], color='black') #rysuje prawa pionowa sciane studni
plt.plot([x_right, 2], [0, 0], color='black')  #rysuuje prawa czesc potencjalu poza studnia


# rysowanie poziomow energii
for z in sorted(zero):
    plt.hlines(z, x_left, x_right, color='red') #hlines - poziome linie
    
    
    
plt.xlabel('x')
plt.ylabel('Energia / Potencjał')
plt.title('Studnia potencjału i poziomy energetyczne')
plt.grid(True)



# przygotowanie do wykresow psi. lista na x, zakresy do rysowania - tak by byly szersze od studni by widac "ogony" funkcji
   
x_values = []
x_min = -2*a
x_max = 2*a
nx = 1000
dx = (x_max-x_min)/ nx  #krok pomiedy kolejnym punktami


# tworzy siatke punktow

for i in range(nx + 1):
    x_values.append(x_min + i * dx)


'''
    Wykres funkcji własnych na tle studni
    ******************
'''

plt.figure(figsize=(10,6))

plt.plot([x_min,-a/2], [0,0], 'k--')
plt.plot([-a/2,-a/2], [0,-Vo], 'k--')
plt.plot([-a/2,a/2],[-Vo,-Vo], 'k--')
plt.plot([a/2, a/2],[-Vo,0], 'k--')
plt.plot([a/2, x_max],[0,0], 'k--')

#tworzy funkcje parzyste i nieparzyste
for E in zero_even:
    psi_vals = []
    for x in x_values:
        psi_vals.append(psi_even(x, E))
    plt.plot(x_values, [ y for y in psi_vals],label=f"psi_even, E={E:.3f}") #rysujemy funkcje nie wokol zera ale wokol swojego poziomu energetycznego 

for E in zero_odd:
    psi_vals = []
    for x in x_values:
        psi_vals.append(psi_odd(x, E))
    plt.plot(x_values, [y for y in psi_vals],label=f"psi_odd, E={E:.3f}")
    
plt.xlabel('X')
plt.ylabel('Energia + psi(x)')
plt.title('Funkcje własne na tle studni potencjału')
plt.grid(True)
plt.legend()

        
'''
    Wykres kwadratów modułu |psi(x)|^2
    ***************
'''

plt.figure(figsize=(10,6))

plt.plot([x_min,-a/2], [0,0], 'k--')
plt.plot([-a/2,-a/2], [0,-Vo], 'k--')
plt.plot([-a/2,a/2],[-Vo,-Vo], 'k--')
plt.plot([a/2, a/2],[-Vo,0], 'k--')
plt.plot([a/2, x_max],[0,0], 'k--')

#liczy funkcje falowa  a potem liczy jej kwadrat 

for E in zero_even:
    psi2_vals = []
    for x in x_values:
        val = psi_even(x, E)
        psi2_vals.append(val*val)
    plt.plot(x_values,[E+ y for y in psi2_vals],label=f"|psi_even|^2, E={E:.3f}")
    

for E in zero_odd:
    psi2_vals = []
    for x in x_values:
        val = psi_odd(x, E)
        psi2_vals.append(val*val)
    plt.plot(x_values, [E+ y for y in psi2_vals], label=f"|psi_odd|^2, E={E:.3f}")
    
plt.xlabel('X')
plt.ylabel('Energia + |psi(x)|^2')
plt.title('Kwadraty modułu funkcji własnych na tle studni')
plt.grid(True)
plt.legend()



plt.show()