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
        grid.append([0, 0, 0, 0])
    return grid


def initialisation():
    grid = datacreate()
    compteur = 0
    while compteur < 2:
        i = rdm.randint(0, 3)
        j = rdm.randint(0, 3)
        grid[i][j] = 2
        for elem in grid:
            compteur += elem.count(2)
    return grid


def loseDetect(gridNouveau: list, gridAncien: list):
    """
    Fonction qui permet de vérifier si le joueur a perdu, c'est à dire si il
    n'y a plus de cases vides et que le mouvement ne change pas la grille.
    C'est à dire que la grille avant le mouvement est la même
    que la grille après le mouvement.
    """
    for elem in gridNouveau:
        if elem.count(0) != 0:
            return False
    for i in range(4):
        for j in range(4):
            if gridAncien[i][j] != gridNouveau[i][j]:
                return False
    return True


def move(grid: list, direction: str):
    """
    Fonction qui fait le déplacement de la grille, elle sauvegarde d'abord
    la configuration précédente pour pouvoir vérifier si le joueur a perdu.
    """
    gridOld = grid
    if direction == "down":
        for i in range(3, 0, -1):
            for j in range(0, 4):
                # On apelle la fonction collision avec comme case immobile
                # la case de la ligne du dessous et la case mobile la case
                # de la ligne du dessus.
                # On va ensuite réinsérer le résultat de la collision
                # dans les cases.
                grid[i][j], grid[i-1][j] = collision(
                    caseImmobile=grid[i][j],
                    caseMobile=grid[i-1][j])
    if direction == "up":
        for i in range(0, 3):
            for j in range(0, 4):
                # On appelle la fonction collision avec comme case immobile
                # la case de la ligne du dessus et la case mobile la case
                # de la ligne du dessous.
                # On va ensuite réinsérer le résultat de la collision
                # dans les cases.
                grid[i][j], grid[i+1][j] = collision(
                    caseImmobile=grid[i][j],
                    caseMobile=grid[i+1][j])
    if direction == "right":
        for i in range(0, 4):
            for j in range(3, 0, -1):
                # On appelle la fonction collision avec comme case immobile
                # la case de la colonne de droite et la case mobile la case
                # de la colonne de gauche.
                # On va ensuite réinsérer le résultat de la collision
                # dans les cases.
                grid[i][j], grid[i][j-1] = collision(
                    caseImmobile=grid[i][j],
                    caseMobile=grid[i][j-1])
    if direction == "left":
        for i in range(0, 4):
            for j in range(0, 3):
                # On appelle la fonction collision avec comme case immobile
                # la case de la colonne de gauche et la case mobile la case
                # de la colonne de droite.
                # On va ensuite réinsérer le résultat de la collision
                # dans les cases.
                grid[i][j], grid[i][j+1] = collision(
                    caseImmobile=grid[i][j],
                    caseMobile=grid[i][j+1])
    lose = loseDetect(grid, gridOld)
    return grid, lose


def collision(caseImmobile, caseMobile):
    """
    Fonction qui fait la cohésion de deux case si possible.
    """
    if caseImmobile == caseMobile:
        caseImmobile += caseMobile
        caseMobile = 0
    elif caseImmobile == 0:
        caseImmobile = caseMobile
        caseMobile = 0
    return caseImmobile, caseMobile
