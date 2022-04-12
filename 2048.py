###############################################################################
# Etudiants: JACQUIN Valentin, VINCENS Arthur, PREHAUD Benjamin
###############################################################################
# Importation des libraires
import tkinter as tk
import random as rdm
###############################################################################
# Définition des fonctions
def datacreate():
    grid = []
    for i in range(4):
        grid.append([0,0,0,0])
    return grid


def initialisation(grid):
    compteur = 0
    while compteur < 2:
        i = rdm.randint(0,3)
        j = rdm.randint(0,3)
        grid[i][j] = 2
        for elem in grid:
            compteur += elem.count(2)
    return grid

