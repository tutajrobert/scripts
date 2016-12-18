# -*- coding: utf-8 -*-
#
###############################################################################
#
# UWAGA: Skrypt napisany w Pythonie 3.x
#
# Wcięcia realizowane są czterema spacjami.
#
# Doczytanie bibliotek numpy i matplotlib:
# pip install numpy
# pip install matplotlib
#
# Uruchamianie skryptu:
# python dane.py
#
###############################################################################
#
# Plik dane.csv zawiera dane zbierane na węźle ciepłowniczym przez 
# przedsiębiorstwo dostarczające ciepło do budynku (patrz opisy kolumn w pliku). 
# Celem ćwiczenia jest wstępna analiza tych danych.
#
# A.
# Wczytać wszystkie zmienne (kolumny) i wszystkie wiersze (obserwacje) z pliku dane.csv do listy t.
# Do poszczególnych list t_* wczytać obserwacje dla wybranych zmiennych.
# Opuścić pierwszy wiersz z opisem danych.
#
# B.
# Sprawdzić podstawowe statystyki poszczególnych zmiennych.
# Wykreślić histogramy danych dla poszczególnych zmiennych.
#
# C.
# Na podstawie statystyk, histogramu i ew. innych testów zidentyfikować zmienne, 
# w których występują potencjalnie błędne dane (obserwacje) lub braki danych.
# Opracować kryterium, które pozwoli na określenie błędnych danych 
# dla zidentyfikowanych zmiennych i określić metodę ich naprawy / usunięcia
# (obliczenie prawidłowej wartości / wstawienie wartości średniej / 
# wstawienie mediany / wstawienie wartości z poprzedniej obserwacji / 
# usunięcie obserwacji).
# Poprawić/usunąć błędne dane na podstawie opracowanej metody.
#
# D.
# Obliczyć unormowane korelacje pomiędzy poszczególnymi zmiennymi.
# Sprawdzić wizualnie poprawność wyliczeń (narysować odpowiednie wykresy liniowe).
# Między jakimi zmiennymi jest największa korelacja, a między jakimi - najmniejsza?
# Czy są to wyniki intuicyjne, czy też nie?
# Wykorzystując wyliczone korelacje opracować kryterium wyszukiwania anomalii.
#
# E.
# Przeprowadzić regresję liniową dla wybranych zmiennych. W razie potrzeby podzielić
# dane na podzakresy i przeprowadzić regresję dla każdego z podzakresów osobno.
# Narysować odpowiednie wykresy.
#
###############################################################################

import csv
import numpy as np
import matplotlib.pyplot as plt

#print("Hello World!")
#input()

print()

t_przeplyw = []
t_temp_zas = []
t_temp_wyj = []
t_roznica_temp = []
t_moc = []

plik = open("dane.csv", "rt")
dane = csv.reader(plik)
next(dane)

for obserwacja in dane:
    t_przeplyw.append(float(obserwacja[6]))
    t_temp_zas.append(float(obserwacja[7]))
    t_temp_wyj.append(float(obserwacja[8]))
    t_roznica_temp.append(float(obserwacja[9]))
    t_moc.append(float(obserwacja[12]))

listy = [t_przeplyw, t_moc, t_roznica_temp, t_temp_wyj, t_temp_zas]
naglowki = ["PRZEPLYW", "MOC", "ROZNICA_TEMP", "TEMP_WYJ", "TEMP_ZAS"]
for index, x in enumerate(t_moc):
    if x > 100:
        for lista in listy:
             del lista[index]
			 
for index, x in enumerate(t_roznica_temp):
    if x > 100000:
        for lista in listy:
             del lista[index]
			 
for index, x in enumerate(t_przeplyw):
    if x > 100000:
        for lista in listy:
             del lista[index]


			 
plt.plot(t_przeplyw, t_moc, ".")
a, b, c, d = np.polyfit(t_przeplyw, t_moc, 3)
yreg = [(a * i)**3 + (b * i)**2 + (c * i)**1 + (d * i)**0 for i in t_przeplyw]
plt.plot(t_przeplyw, yreg)
plt.show()


def ncorrelate(a, b):
    a1 = ((a - np.mean(a)) / (np.std(a) * len(a)))
    b1 = ((b - np.mean(b)) / np.std(b))
    return np.correlate(a1, b1)
wsp_korelacji = []
naglowki_lista = []
for i in range(len(listy)):
    for j in range(len(listy)):
        if (i != j) and (i < j):
            korelacja = ncorrelate(listy[i], listy[j])
            wsp_korelacji.append(korelacja)
            naglowki_lista.append([naglowki[i], naglowki[j]])
            print("Wsp. korelacji dla", naglowki[i], "i", naglowki[j], ":", round(korelacja[0], 3))
		
abs_wsp = [abs(i) for i in wsp_korelacji]
min_index = abs_wsp.index(min(abs_wsp))
print()
print("Najsłabsza korelacja wynosi:", round(abs_wsp[min_index][0], 3), "dla", naglowki_lista[min_index][0], "i", naglowki_lista[min_index][1])

wpr = input("Podaj wartość przepływu w l/min: ")
wpr = float(wpr)
print("Przewidywana moc:", (a * wpr)**3 + (b * wpr)**2 + (c * wpr)**1 + (d * wpr)**0)