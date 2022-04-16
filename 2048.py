###############################################################################
# Etudiants: JACQUIN Valentin, VINCENS Arthur, PREHAUD Benjamin
###############################################################################
# Importation des libraires
import tkinter as tk
import random as rdm
###############################################################################
# Définition des variables
couleur = open("couleur.txt", "r")
couleur = couleur.readline()
couleur = couleur.split()
score = 0
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
    print("Initialisation")
    global matrice
    matriceCreate()
    nombre0 = compte0()
    while nombre0 > 14:
        nouvelCase()
        nombre0 = compte0()
    return None


def nouvelCase():
    """
    Fonction qui ajoute une case de valeur 2 ou 4 au hasard dans une case vide.
    """
    print("Nouvel case")
    global matrice
    nombre0 = compte0()
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


def compte0():
    """
    Fonction qui compte le nombre de cases vides dans la grille.
    """
    print("Compte 0")
    global matrice
    nombre0 = 0
    for i in range(0, len(matrice)):
        for j in range(0, len(matrice[i])):
            if matrice[i][j] == 0:
                nombre0 += 1
    return nombre0


def loseDetect(gridNouveau: list, gridAncien: list):
    """
    Fonction qui permet de vérifier si le joueur a perdu, c'est à dire si il
    n'y a plus de cases vides et que le mouvement ne change pas la grille.
    C'est à dire que la grille avant le mouvement est la même
    que la grille après le mouvement.
    """
    print("Lose detect")
    for elem in gridNouveau:
        if elem.count(0) != 0:
            return False
    for i in range(4):
        for j in range(4):
            if gridAncien[i][j] != gridNouveau[i][j]:
                return False
    return True


def move(direction: str):
    """
    Fonction qui fait le déplacement de la grille, elle sauvegarde d'abord
    la configuration précédente pour pouvoir vérifier si le joueur a perdu.
    """
    print("Move")
    global matrice
    gridOld = matrice
    grid = matrice
    if direction == "down":
        for j in range(0, 4):
            colonne = [grid[i][j] for i in range(0, 4)]
            colonne = collision(colonne)
            for i in range(0, 4):
                grid[i][j] = colonne[i]
    if direction == "up":
        for j in range(0, 4):
            colonne = [grid[i][j] for i in range(0, 4)]
            colonne.reverse()
            colonne = collision(colonne)
            colonne.reverse()
            for i in range(0, 4):
                grid[i][j] = colonne[i]
    if direction == "right":
        for i in range(0, 4):
            ligne = [grid[i][j] for j in range(0, 4)]
            ligne = collision(ligne)
            for j in range(0, 4):
                grid[i][j] = ligne[j]
    if direction == "left":
        for i in range(0, 4):
            ligne = [grid[i][j] for j in range(0, 4)]
            ligne.reverse()
            ligne = collision(ligne)
            ligne.reverse()
            for j in range(0, 4):
                grid[i][j] = ligne[j]
    lose = loseDetect(grid, gridOld)
    matrice = grid
    affichage()
    nouvelCase()
    affichage()
    return lose


def collision(liste):
    """
    Fonction qui permet de faire la collision des cases dans une ligne ou
    une colonne.
    """
    print("Collision")
    liste = [elem for elem in liste if elem != 0]
    while len(liste) < 4:
        liste.insert(0, 0)
    for i in range(len(liste) - 1, 0, -1):
        if liste[i] == liste[i - 1]:
            liste[i] = liste[i] * 2
            liste[i - 1] = 0
    liste = [elem for elem in liste if elem != 0]
    while len(liste) < 4:
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
    return None


def restart():
    """
    Fonction qui permet de recommencer le jeu.
    """
    print("Restart")
    global matrice
    initialisation()
    affichage()
    return None


def score():
    """
    Fonction qui calcule le score du joueur.
    """
    print("Score")
    global matrice
    score = 0
    for i in range(4):
        for j in range(4):
            score += matrice[i][j]
    score = str(score)
    return score


###############################################################################
# Création de l'interface graphique
racine = tk.Tk()
racine.title("2048")

cMatrice = tk.Canvas(racine, width=500, height=500)
cMatrice.grid(row=1, column=1, columnspan=4)

lTitreJeu = tk.Label(text="2048", font=("Arial", 21))
lTitreJeu.grid(row=0, column=1)

lScore = tk.Label(text="Score : 0", font=("Arial", 15))
lScore.grid(row=0, column=2)

bRestart = tk.Button(text="Recommencer", command=restart)
bRestart.grid(column=0, row=1)

bSave = tk.Button(text="Sauvegarder", command=save)
bSave.grid(column=0, row=2)

bCharger = tk.Button(text="Charger Config", command=charger)
bCharger.grid(column=0, row=3)


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
    lScore.config(text="Score: " + score())
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
    affiche_score()
    return None


def affiche_nombre(numerocase: int, valeurCase: str):
    """
    Fonction qui configure le label associé à la case
    avec le nombre stocké dans matrice.
    """
    global guiText
    cMatrice.itemconfig(guiText[numerocase], text=valeurCase)
    return None


def haut(event):
    move("up")


def bas(event):
    move("down")


def gauche(event):
    move("left")


def droite(event):
    move("right")


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
    return None


###############################################################################
# Lancement du jeu
lancement()
racine.mainloop()
