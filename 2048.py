###############################################################################
# Etudiants: JACQUIN Valentin, VINCENS Arthur, PREHAUD Benjamin
###############################################################################
# Importation des libraires
import tkinter as tk
import random as rdm
import copy as cp
###############################################################################
# Définition des variables
couleur = open("couleur.txt", "r")
couleur = couleur.readline()
couleur = couleur.split()
score = 0
stockageLscoreboardData = []
###############################################################################
# Définition des fonctions gestion données


def matriceCreate():
    """
    Fonction qui crée la matrice de jeu de 4x4.
    """
    global matrice
    matrice = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    return None


def initialisation():
    """"
    Fonction qui ajoute 2 ou 4 dans deux cases de la matrice au hasard
    au début du jeu.
    """
    global stop
    print("Initialisation")
    global matrice
    matriceCreate()
    nombre0 = compte0(matrice)
    while nombre0 > 14:
        nouvelCase()
        nombre0 = compte0(matrice)
    stop = False
    return None


def nouvelCase():
    """
    Fonction qui ajoute une case de valeur 2 ou 4 au hasard dans une case vide.
    """
    print("Nouvel case")
    global matrice
    nombre0 = compte0(matrice)
    if nombre0 == 0:
        return None
    elif nombre0 == 16:
        x = rdm.randint(0, 3)
        y = rdm.randint(0, 3)
        matrice[y][x] = rdm.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
    else:
        x = rdm.randint(0, 3)
        y = rdm.randint(0, 3)
        if matrice[y][x] != 0:
            while matrice[y][x] != 0:
                x = rdm.randint(0, 3)
                y = rdm.randint(0, 3)
        matrice[y][x] = rdm.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
    print(matrice)
    return None


def compte0(matrice):
    """
    Fonction qui compte le nombre de cases vides dans la grille.
    """
    print("Compte 0")
    nombre0 = 0
    for i in range(0, len(matrice)):
        for j in range(0, len(matrice[i])):
            if matrice[i][j] == 0:
                nombre0 += 1
    return nombre0


def statusGame(grid):
    """
    Fonction qui permet de vérifier si le joueur a perdu ou gagné,
    c'est à dire si il n'y a plus de cases vides.
    Et que le mouvement est impossible.
    Retourne vrai si le joueur a perdu, faux sinon.
    """
    print("status Game")
    """
    On vérifie d'abord si le joueur n'a pas gagné.
    """
    for elem in grid:
        if elem.count(2048) != 0:
            return "win"
    """
    On vérifie d'abord si il y a des cases vides.
    """
    if compte0(grid) != 0:
        return "continue"
    """
    On vérifie ensuite qu'il n'y a pas deux cases qui ont la même valeur
    cote à cote. D'abord dans le sens horizontale, puis dans le sens vertical.
    """
    for i in range(0, len(grid)):
        for j in range(1, len(grid[i])):
            if grid[i][j - 1] == grid[i][j]:
                return "continue"
    for i in range(1, len(grid)):
        for j in range(0, len(grid[i])):
            if grid[i - 1][j] == grid[i][j]:
                return "continue"
    return "lose"


def move(direction: str):
    """
    Fonction qui fait le déplacement de la grille, elle sauvegarde d'abord
    la configuration précédente pour pouvoir vérifier si le joueur a perdu.
    """
    print("Move")
    global matrice
    changement = False
    grid = cp.deepcopy(matrice)
    if direction == "down":
        for j in range(0, 4):
            colonne = [grid[i][j] for i in range(0, len(grid))]
            colonne = collision(colonne)
            for i in range(0, 4):
                if grid[i][j] != colonne[i]:
                    grid[i][j] = colonne[i]
                    changement = True
    if direction == "up":
        for j in range(0, 4):
            colonne = [grid[i][j] for i in range(0, len(grid))]
            colonne.reverse()
            colonne = collision(colonne)
            colonne.reverse()
            for i in range(0, 4):
                if grid[i][j] != colonne[i]:
                    grid[i][j] = colonne[i]
                    changement = True
    if direction == "right":
        for i in range(0, 4):
            ligne = [grid[i][j] for j in range(0, len(grid))]
            ligne = collision(ligne)
            for j in range(0, 4):
                if grid[i][j] != ligne[j]:
                    grid[i][j] = ligne[j]
                    changement = True
    if direction == "left":
        for i in range(0, 4):
            ligne = [grid[i][j] for j in range(0, len(grid))]
            ligne.reverse()
            ligne = collision(ligne)
            ligne.reverse()
            for j in range(0, 4):
                if grid[i][j] != ligne[j]:
                    grid[i][j] = ligne[j]
                    changement = True
    matrice = cp.deepcopy(grid)
    affichage()
    lose = statusGame(matrice)
    if changement and lose == "continue":
        nouvelCase()
    affichage()
    return lose


def collision(liste):
    """
    Fonction qui permet de faire la collision des cases dans une ligne ou
    une colonne.
    """
    print("Collision")
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
    print("Save")
    global matrice
    fichier = open("save.txt", "w")
    compteur = 0
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
    Fonction qui charge la grille sauvegarder dans le fichier texte save.txt.
    """
    print("Charger")
    global matrice
    matrice = []
    fichier = open("save.txt", "r")
    config = fichier.readlines()
    for ligne in config:
        ligne = ligne.split()
        ligne = list(ligne)
        for i in range(0, 4):
            ligne[i] = int(ligne[i])
        matrice.append(ligne)
    fichier.close()
    affichage()
    lEnd.grid_forget()
    return None


def restart():
    """
    Fonction qui permet de recommencer le jeu.
    """
    print("Restart")
    global matrice, lEnd, stop
    stop = False
    lEnd.grid_forget()
    initialisation()
    affichage()
    return None


def resetScoreBoard():
    """
    Fonction qui permet de réinitialiser le scoreBoard.
    """
    print("Reset ScoreBoard")
    fic = open("score.txt", "w")
    fic.write("")
    fic.close()
    afficheScoreBoard()
    return None


def CalculeScore():
    """
    Fonction qui calcule le score du joueur.
    """
    print("Score")
    global matrice
    score = 0
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            score += matrice[i][j]
    score = str(score)
    return score


###############################################################################
# Création de l'interface graphique
racine = tk.Tk()
racine.title("2048")

cMatrice = tk.Canvas(racine, width=500, height=500)
cMatrice.grid(row=1, column=1, rowspan=10, columnspan=4)

lEnd = tk.Label(text="Ceci est un secret", font=("Arial", 28))

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


###############################################################################
# Définition des fonctions graphiques
def creer_case():
    """
    Fonction qui crée les cases de la grille.
    """
    print("Creer_case")
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
                text="1",
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
    print("ScoreBoard")
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
    print(lScore)
    lScore = lScore[:10]
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
    print("Affichage")
    global guiCase, matrice, guiText
    compteurCase = 0
    for elem in matrice:
        for case in elem:
            compteur = 0
            case2 = case
            while case2 >= 2:
                case2 = case2 // 2
                compteur += 1
            if case == 0:
                cMatrice.itemconfig(
                    guiCase[compteurCase],
                    fill="white",
                )
                affiche_nombre(compteurCase, "")
            else:
                cMatrice.itemconfig(
                    guiCase[compteurCase],
                    fill=couleur[compteur]
                )
                affiche_nombre(compteurCase, str(case))
            compteurCase += 1
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
    print("End")
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
    global stop
    if not stop:
        status = move("up")
        if status == "lose":
            print("You lose")
            endGame(False)
        elif status == "win":
            print("You win")
            endGame(True)


def bas(event):
    """
    Fonction qui agit sur la matrice si le jeu n'est pas stop.
    """
    global stop
    if not stop:
        status = move("down")
        if status == "lose":
            print("You lose")
            endGame(False)
        elif status == "win":
            print("You win")
            endGame(True)


def gauche(event):
    """
    Fonction qui agit sur la matrice si le jeu n'est pas stop.
    """
    global stop
    if not stop:
        status = move("left")
        if status == "lose":
            print("You lose")
            endGame(False)
        elif status == "win":
            print("You win")
            endGame(True)


def droite(event):
    """
    Fonction qui agit sur la matrice si le jeu n'est pas stop.
    """
    global stop
    if not stop:
        status = move("right")
        if status == "lose":
            print("You lose")
            endGame(False)
        elif status == "win":
            print("You win")
            endGame(True)


racine.bind("<KeyPress-Up>", haut)
racine.bind("<KeyPress-Down>", bas)
racine.bind("<KeyPress-Left>", gauche)
racine.bind("<KeyPress-Right>", droite)

###############################################################################
# Initialisation du jeu


def lancement():
    """
    Fonction qui lance le jeu.
    """
    print("Lancement")
    initialisation()
    creer_case()
    affichage()
    afficheScoreBoard()
    return None


###############################################################################
# Lancement du jeu
lancement()
racine.mainloop()
