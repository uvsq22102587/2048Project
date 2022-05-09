###############################################################################
# Etudiants: JACQUIN Valentin, VINCENS Arthur, PREHAUD Benjamin
###############################################################################
# Importation des libraires
from logging import root
import tkinter as tk
import random as rdm
import copy as cp
###############################################################################
# Définition des variables
couleur = open("couleur.txt", "r")
couleur = couleur.readline()
couleur = couleur.split()
score = 0
fourD = False
listeLigneNoire = []
stockageLscoreboardData = []
###############################################################################
# Définition des fonctions gestion données


def lancement(event):
    """
    Fonction qui lance le jeu.
    """
    global listeMatrice
    # Grid des boutons
    listeMatrice = initialisation()
    creer_case()
    affichage()
    afficheScoreBoard()
    cMatrice.unbind("<Button-1>")
    return None


def matriceCreate(mode="1D"):
    """
    Fonction qui crée la matrice de jeu de 4x4 ou 4x2x2 si mode 4D.
    """
    if mode == "4D":
        matrice = [[[0, 0], [0, 0]] for i in range(0, 4)]
    else:
        matrice = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
    return matrice


def fourDmode():
    """
    Fonction qui permet de changer le mode de jeu en 4D.
    Ou de le repasser en 1D.
    """
    global fourD, listeLigneNoire, listeMatrice
    lEnd.grid_forget()
    if fourD:
        racine.title("2048 - 1D")
        fourD = False
        b1Dmode.grid_forget()
        b4Dmode.grid(row=6, column=0)
        for elem in listeLigneNoire:
            cMatrice.delete(elem)
        listeLigneNoire = []
    else:
        racine.title("2048 - 4D")
        fourD = True
        b4Dmode.grid_forget()
        b1Dmode.grid(row=6, column=0)
        listeLigneNoire = []
        ligne1 = cMatrice.create_line(0, 202, 402, 202, fill="black", width=3)
        ligne2 = cMatrice.create_line(202, 0, 202, 402, fill="black", width=3)
        listeLigneNoire = [ligne1, ligne2]
    listeMatrice = initialisation()
    affichage()
    return None


def initialisation():
    """"
    Fonction qui ajoute 2 ou 4 dans deux cases de la grille si mode 1D.
    Sinon une case de 2 ou 4 dans une case par grille.
    """
    global stop, fourD, listeMatrice
    if fourD:
        matrice = matriceCreate("4D")
        nombre0Necessaire = 3
    else:
        nombre0Necessaire = 14
        matrice = matriceCreate()
    for elem in matrice:
        nombre0 = compte0(elem)
        while nombre0 > nombre0Necessaire:
            elem = nouvelCase(elem)
            nombre0 = compte0(elem)
    stop = False
    listeMatrice = matrice
    return matrice


def nouvelCase(matrice):
    """
    Fonction qui ajoute une case de valeur 2 ou 4 au hasard dans une case vide
    de la grille.
    """
    global fourD
    nombre0 = compte0(matrice)
    if fourD:
        nbrCase = 2
    else:
        nbrCase = 4
    if nombre0 == 0:
        return matrice
    else:
        x = rdm.randint(0, nbrCase - 1)
        y = rdm.randint(0, nbrCase - 1)
        if matrice[y][x] != 0:
            while matrice[y][x] != 0:
                x = rdm.randint(0, nbrCase - 1)
                y = rdm.randint(0, nbrCase - 1)
        matrice[y][x] = rdm.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
    return matrice


def compte0(matrice):
    """
    Fonction qui compte le nombre de cases vides dans une grille.
    """
    nombre0 = 0
    for i in range(0, len(matrice)):
        for j in range(0, len(matrice[i])):
            if matrice[i][j] == 0:
                nombre0 += 1
    return nombre0


def statusGame(listeDeGrilles):
    """
    Fonction qui permet de vérifier si le joueur a perdu ou gagné,
    c'est à dire si il n'y a plus de cases vides.
    Et que le mouvement est impossible.
    Retourne le status de la partie en str.
    (Pour le mode 4D, c'est lorsque toutes les grilles
    sont perdues que la partie est perdue.)
    """
    # On vérifie d'abord si le joueur n'a pas gagné.
    for grid in listeDeGrilles:
        for elem in grid:
            if elem.count(2048) != 0:
                return "win"
    # On vérifie d'abord si il y a des cases vides.
        if compte0(grid) != 0:
            return "continue"
    # On vérifie ensuite qu'il n'y a pas deux cases qui ont la même valeur
    # côte à côte. D'abord dans le sens horizontale, puis dans le sens
    # vertical.
        for i in range(0, len(grid)):
            for j in range(1, len(grid[i])):
                if grid[i][j - 1] == grid[i][j]:
                    return "continue"
        for i in range(1, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i - 1][j] == grid[i][j]:
                    return "continue"
    return "lose"


def move(matrice: list, direction: str):
    """
    Fonction qui fait le déplacement de la grille, elle sauvegarde d'abord
    la configuration précédente pour pouvoir vérifier si le déplacement
    a eu une conséquence sur la grille.
    """
    changement = False
    grid = cp.deepcopy(matrice)
    if direction == "down":
        for j in range(0, len(grid)):
            colonne = [grid[i][j] for i in range(0, len(grid))]
            colonne = collision(colonne)
            for i in range(0, len(grid)):
                if grid[i][j] != colonne[i]:
                    grid[i][j] = colonne[i]
                    changement = True
    if direction == "up":
        for j in range(0, len(grid)):
            colonne = [grid[i][j] for i in range(0, len(grid))]
            colonne.reverse()
            colonne = collision(colonne)
            colonne.reverse()
            for i in range(0, len(grid)):
                if grid[i][j] != colonne[i]:
                    grid[i][j] = colonne[i]
                    changement = True
    if direction == "right":
        for i in range(0, len(grid)):
            ligne = [grid[i][j] for j in range(0, len(grid))]
            ligne = collision(ligne)
            for j in range(0, len(grid)):
                if grid[i][j] != ligne[j]:
                    grid[i][j] = ligne[j]
                    changement = True
    if direction == "left":
        for i in range(0, len(grid)):
            ligne = [grid[i][j] for j in range(0, len(grid))]
            ligne.reverse()
            ligne = collision(ligne)
            ligne.reverse()
            for j in range(0, len(grid)):
                if grid[i][j] != ligne[j]:
                    grid[i][j] = ligne[j]
                    changement = True
    matrice = cp.deepcopy(grid)
    return changement, matrice


def collision(liste):
    """
    Fonction qui permet de faire la collision des cases dans une ligne ou
    une colonne.
    """
    lenListeini = len(liste)
    liste = [elem for elem in liste if elem != 0]
    while len(liste) < 4:
        liste.insert(0, 0)
    for i in range(len(liste) - 1, 0, -1):
        if liste[i] == liste[i - 1]:
            liste[i] = liste[i] * 2
            liste[i - 1] = 0
    liste = [elem for elem in liste if elem != 0]
    while len(liste) < lenListeini:
        liste.insert(0, 0)
    return liste


def save():
    """
    Fonction qui sauvegarde la grille dans un fichier texte.
    """
    global listeMatrice, stop
    assert stop is not True, "La partie est terminée."
    fichier = open("save.txt", "w")
    compteur = 0
    for matrice in listeMatrice:
        for elem in matrice:
            for case in elem:
                fichier.write(str(case) + " ")
                compteur += 1
                if compteur == 4:
                    fichier.write("\n")
                    compteur = 0
    fichier.close()
    return None


def charger():
    """
    Fonction qui charge la grille sauvegardée dans le fichier texte save.txt.
    """
    global listeMatrice
    listeMatrice = []
    fichier = open("save.txt", "r")
    config = fichier.readlines()
    for ligne in config:
        ligne = ligne.split()
        ligne = list(ligne)
        for i in range(0, 4):
            ligne[i] = int(ligne[i])
        listeMatrice.append(ligne)
    fichier.close()
    listeMatrice = [listeMatrice]
    affichage()
    lEnd.grid_forget()
    return None


def restart():
    """
    Fonction qui permet de recommencer le jeu.
    """
    global listeMatrice, lEnd, stop
    stop = False
    lEnd.grid_forget()
    listeMatrice = initialisation()
    affichage()
    return None


def resetScoreBoard():
    """
    Fonction qui permet de réinitialiser le scoreBoard.
    """
    fic = open("score.txt", "w")
    fic.write("")
    fic.close()
    afficheScoreBoard()
    return None


def CalculeScore():
    """
    Fonction qui calcule le score du joueur.
    """
    global listeMatrice
    score = 0
    for matrice in listeMatrice:
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                score += matrice[i][j]
    score = str(score)
    return score


###############################################################################
# Création de l'interface graphique
racine = tk.Tk()
racine.title("2048- 1D")

cMatrice = tk.Canvas(racine, width=500, height=500)
cMatrice.grid(row=1, column=1, rowspan=10, columnspan=4)

lEnd = tk.Label(text="Ceci est un easter egg", font=("Arial", 28))

lScore = tk.Label(text="Score : 0", font=("Arial", 15))
lScore.grid(row=0, column=2)

lScoreBoard = tk.Label(text="Scoreboard", font=("Arial", 15))

lScoreBoardData = tk.Label(text="", font=("Arial", 15))

bRestart = tk.Button(text="Recommencer", command=restart)
bRestart.grid(column=0, row=2)

bSave = tk.Button(text="Sauvegarder", command=save)
bSave.grid(column=0, row=3)

bCharger = tk.Button(text="Charger Config", command=charger)
bCharger.grid(column=0, row=4)

bResetScoreboard = tk.Button(text="Reset Scoreboard", command=resetScoreBoard)
bResetScoreboard.grid(column=0, row=5)

b4Dmode = tk.Button(text="4D Mode", command=fourDmode)
b4Dmode.grid(column=0, row=6)

b1Dmode = tk.Button(text="1D Mode", command=fourDmode)


###############################################################################
# Définition des fonctions graphiques
def creer_case():
    """
    Fonction qui crée les cases de la grille. C'est en
    quelque sorte l'initialisation de la partie graphique.
    """
    global guiCase, guiText
    guiCase, guiText = [], []
    for i in range(4):
        for j in range(4):
            case = cMatrice.create_rectangle(
                (j*100+5, i*100+5),
                (j*100+100, i*100+100),
                fill="white",
                outline="grey"
                )
            coord = cMatrice.coords(case)
            x = (coord[0] + coord[2]) // 2
            y = (coord[1] + coord[3]) // 2
            guiText.append(cMatrice.create_text(
                x, y,
                text="",
                font=("E", 25)))
            guiCase.append(case)
    return None


def affiche_score():
    """
    Fonction qui actualise le score.
    """
    lScore.config(text="Score: " + CalculeScore())
    return None


def afficheScoreBoard():
    """
    Fonction qui affiche le score board.
    """
    global stockageLscoreboardData
    for elem in stockageLscoreboardData:
        elem.grid_forget()
    stockageLscoreboardData = []
    lScoreBoard.grid(row=0, column=5)
    fScore = open("score.txt", "r")
    lScore = fScore.read()
    lScore = lScore.split("\n")
    while lScore.count('') > 0:
        lScore.remove('')
    for i in range(0, len(lScore)):
        lScore[i] = int(lScore[i])
    fScore.close()
    lScore.sort(reverse=True)
    lScore = lScore[:5]
    for i in range(0, len(lScore)):
        lScoreBoardData = tk.Label(
            text=str(i+1) + " : " + str(lScore[i])
            )
        lScoreBoardData.grid(row=i+1, column=5)
        stockageLscoreboardData.append(lScoreBoardData)
    return None


def affichage():
    """
    Fonction qui actualise les carrées en fonction des données stockées dans
    matrice
    """
    global guiCase, guiText, listeMatrice, fourD
    # On a besoin de gérer le choix des carré lorsque le jeu est
    # en mode 4D ou non, c'est pour cela qu'on utilise la variable compteurCase
    # et la variable indexCompteurCase
    if fourD:
        compteurCase = [0, 1, 4, 5, 2, 3, 6, 7, 8, 9, 12, 13, 10, 11, 14, 15]
    else:
        compteurCase = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    indexCompteurCase = 0
    for element in listeMatrice:
        for elem in element:
            for case in elem:
                compteur = 0
                case2 = case
                while case2 >= 2:
                    case2 = case2 // 2
                    compteur += 1
                if case == 0:
                    cMatrice.itemconfig(
                        guiCase[compteurCase[indexCompteurCase]],
                        fill="white",
                    )
                    affiche_nombre(compteurCase[indexCompteurCase], "")
                else:
                    cMatrice.itemconfig(
                        guiCase[compteurCase[indexCompteurCase]],
                        fill=couleur[compteur]
                    )
                    affiche_nombre(compteurCase[indexCompteurCase], str(case))
                indexCompteurCase += 1
    return None


def affiche_nombre(numerocase: int, valeurCase: str):
    """
    Fonction qui configure le label associé à la case
    avec le nombre stocké dans matrice.
    """
    global guiText
    cMatrice.itemconfig(guiText[numerocase], text=valeurCase)
    return None


def endGame(condition: bool):
    """
    Fonction qui stop le jeu si le joueur perd ou gagne.
    """
    global lEnd, stop
    stop = True
    if not condition:
        lEnd.config(text="Perdu !")
    else:
        lEnd.config(text="Gagné !")
    lEnd.grid(row=1, column=0)
    score = open("score.txt", "a")
    score.write(CalculeScore() + "\n")
    score.close()
    affiche_score()
    afficheScoreBoard()


def haut(event):
    """
    Fonction qui agit sur la matrice si le jeu n'est pas stop.
    """
    global stop, listeMatrice
    if stop:
        return None
    if not stop:
        for i in range(0, len(listeMatrice)):
            status, listeMatrice[i] = move(listeMatrice[i], "up")
            if status:
                listeMatrice[i] = nouvelCase(listeMatrice[i])
        affichage()
    if statusGame(listeMatrice) == "lose":
        endGame(False)
        print("You lose")
    return None


def bas(event):
    """
    Fonction qui agit sur la matrice si le jeu n'est pas stop.
    """
    global stop, listeMatrice
    if stop:
        return None
    if not stop:
        for i in range(0, len(listeMatrice)):
            status, listeMatrice[i] = move(listeMatrice[i], "down")
            if status:
                listeMatrice[i] = nouvelCase(listeMatrice[i])
        affichage()
    if statusGame(listeMatrice) == "lose":
        print("You lose")
        endGame(False)
    return None


def gauche(event):
    """
    Fonction qui agit sur la matrice si le jeu n'est pas stop.
    """
    global stop, listeMatrice
    if stop:
        return None
    if not stop:
        for i in range(0, len(listeMatrice)):
            status, listeMatrice[i] = move(listeMatrice[i], "left")
            if status:
                listeMatrice[i] = nouvelCase(listeMatrice[i])
        affichage()
    if statusGame(listeMatrice) == "lose":
        print("You lose")
        endGame(False)
    return None


def droite(event):
    """
    Fonction qui agit sur la matrice si le jeu n'est pas stop.
    """
    global stop, listeMatrice
    if stop:
        return None
    if not stop:
        for i in range(0, len(listeMatrice)):
            status, listeMatrice[i] = move(listeMatrice[i], "right")
            if status:
                listeMatrice[i] = nouvelCase(listeMatrice[i])
        affichage()
    if statusGame(listeMatrice) == "lose":
        print("You lose")
        endGame(False)
    return None


racine.bind("<KeyPress-Up>", haut)
racine.bind("<KeyPress-Down>", bas)
racine.bind("<KeyPress-Left>", gauche)
racine.bind("<KeyPress-Right>", droite)
cMatrice.bind("<Button-1>", lancement)

#########################################################################
# Lancement du jeu
creer_case()
racine.mainloop()
