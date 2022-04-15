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
###############################################################################
# Définition des fonctions gestion données



def datacreate():
    """
    Fonction qui créée une matrice de 4x4.
    """
    global data
    data = []
    for i in range(4):
        data.append([0, 0, 0, 0])
    return data


def initialisation():
    """"
    Fonction qui ajoute 2 dans deux cases de la matrice au hasard au début du jeu.
    """
    global matrice
    matrice = datacreate()
    compteur = 0
    while compteur < 2:
        compteur = 0
        i = rdm.randint(0, 3)
        j = rdm.randint(0, 3)
        matrice[i][j] = 2
        for elem in matrice:
            compteur += elem.count(2)


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


def move(direction: str):
    """
    Fonction qui fait le déplacement de la grille, elle sauvegarde d'abord
    la configuration précédente pour pouvoir vérifier si le joueur a perdu.
    """
    global matrice
    gridOld = matrice
    grid = matrice
    finish = False
    if direction == "down":
        for i in range(3, 0, -1):
            while finish is not True:
                for j in range(0, 4):
                    # On apelle la fonction collision avec comme case immobile
                    # la case de la ligne du dessous et la case mobile la case
                    # de la ligne du dessus.
                    # On va ensuite réinsérer le résultat de la collision
                    # dans les cases.
                    grid[i][j], grid[i-1][j], finish = collision(
                        caseImmobile=grid[i][j],
                        caseMobile=grid[i-1][j])
    if direction == "up":
        for i in range(0, 3):
            while finish is not True:
                for j in range(0, 4):
                    # On appelle la fonction collision avec comme case immobile
                    # la case de la ligne du dessus et la case mobile la case
                    # de la ligne du dessous.
                    # On va ensuite réinsérer le résultat de la collision
                    # dans les cases.
                    grid[i][j], grid[i+1][j], finish = collision(
                        caseImmobile=grid[i][j],
                        caseMobile=grid[i+1][j])
    if direction == "right":
        for i in range(0, 4):
            while finish is not True:
                for j in range(3, 0, -1):
                    # On appelle la fonction collision avec comme case immobile
                    # la case de la colonne de droite et la case mobile la case
                    # de la colonne de gauche.
                    # On va ensuite réinsérer le résultat de la collision
                    # dans les cases.
                    grid[i][j], grid[i][j-1], finish = collision(
                        caseImmobile=grid[i][j],
                        caseMobile=grid[i][j-1])
    if direction == "left":
        for i in range(0, 4):
            while finish is not True:
                for j in range(0, 3):
                    # On appelle la fonction collision avec comme case immobile
                    # la case de la colonne de gauche et la case mobile la case
                    # de la colonne de droite.
                    # On va ensuite réinsérer le résultat de la collision
                    # dans les cases.
                    grid[i][j], grid[i][j+1], finish = collision(
                        caseImmobile=grid[i][j],
                        caseMobile=grid[i][j+1])
    lose = loseDetect(grid, gridOld)
    matrice = grid
    return lose


def collision(caseImmobile, caseMobile):
    """
    Fonction qui fait la cohésion de deux case si possible.
    """
    if caseImmobile == caseMobile:
        caseImmobile += caseMobile
        caseMobile = 0
        finish = False
    elif caseImmobile == 0:
        caseImmobile = caseMobile
        caseMobile = 0
        finish = False
    else:
        finish = True
    return caseImmobile, caseMobile, finish


def save():
    """
    Fonction qui sauvegarde la grille dans un fichier texte.
    """
    global matrice
    fichier = open("save.txt", "w")
    for elem in matrice:
        fichier.write(str(elem) + "\n")
    fichier.close()


def restart():
    """
    Fonction qui permet de recommencer le jeu.
    """
    global matrice
    matrice = datacreate()
    initialisation()
    affichage()


###############################################################################
# Création de l'interface graphique
racine = tk.Tk()
racine.title("2048")

cMatrice = tk.Canvas(racine, width=500, height=500)
cMatrice.grid(row=1, column=1, columnspan=4)

lTitreJeu = tk.Label(text="2048", font=("Arial", 21))
lTitreJeu.grid(row=0, column=1)

bRestart = tk.Button(text="Recommencer", command=restart)
bRestart.grid(column=0, row=1)

bSave = tk.Button(text="Sauvegarder", command=save)
bSave.grid(column=0, row=2)


###############################################################################
# Définition des fonctions graphiques
def creer_case():
    """
    Fonction qui crée les cases de la grille.
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
            guiText.append(cMatrice.create_text(x, y, text=""))
            guiCase.append(case)
            


def affichage():
    """
    Fonction qui actualise les carrées en fonction des données stockées dans
    matrice
    """
    global guiCase, matrice, guiText
    print(matrice)
    compteurCase = 0
    for elem in matrice:
        for case in elem:
            compteur = 0
            while case >= 2:
                case = case // 2
                compteur += 1
            if case == 0:
                cMatrice.itemconfig(
                    guiCase[compteurCase],
                    fill="white",
                )
            else:
                cMatrice.itemconfig(
                    guiCase[compteurCase],
                    fill=couleur[compteur]
                )
            compteurCase += 1


###############################################################################
# Initialisation du jeu
def lancement():
    """
    Fonction qui lance le jeu.
    """
    initialisation()
    creer_case()
    affichage()


###############################################################################
# Lancement du jeu
lancement()
racine.mainloop()