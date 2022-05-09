# 2048Project
###
Ce projet a été fait par JACQUIN Valentin, VINCENS Arthur et PREHAUD Benjamin, tous étudiants de LDDBI
dans le cadre du projet de fin de 2nd semestre d'IN200N.

Lien du dépot github: https://github.com/uvsq22102587/2048project

## Notice
###
Lors du lancement du programme, une grille vide de 2048 apparaît. Pour lancer la partie, il faut cliquer sur cette matrice.
Le jeu est par défaut en mode 1D, il faut appuyer sur le bouton 4D mode pour passer en mode 4D. Comme dit dans l'énoncé, le mode 4D crée 4 grilles de 2x2 qui vont sé déplacer en même temps. Lorsque le mode 4D est activé, le jeu ne crée pas 2 nouvel case dans chaque grille par déplacement, mais une seule.
Le mode de jeu actuel est écrit dans le titre de la fenêtre.

Pour faire bouger les élements de la grille, nous avons décidé de bind les flèches directionnelles plutôt que des boutons car elles sont beaucoup plus pratique.

Le jeu s'arrête soit quand le joueur a perdu, soit quand il a atteint 2048.

La grille peut être sauvegardé à tous moments, sauf quand le joueur a déjà perdu/gagné. Elle est stockée dans un fichier texte appellée "save.txt".
On pourra donc naturellement charger cette configuration avec le bouton "Charger Config".

Le score du joueur est actualisé à chaque fois que le joueur fais un mouvement, il est affiché au dessus de la grille. Lors de la fin de la partie, le score est stocké dans un fichier texte "score.txt". Ce qui permet de créer un panneau des score à gauche de la grille.
Tant que le fichier "score.txt" est vide, ce panneau des score ne s'affichera pas.
Un bouton est dédié à la rénitialisation de ce tableau des score.

Le bouton "Recommencer" permet naturellement de recommencer la partie en cours, dans ce cas le score actuel ne sera pas sauvegardé dans le tableau des scores.
