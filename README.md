# Le Compte Est Bon : script python
## Principe du jeu
Le principe de ce jeu est bien connu et [Wikipedia](https://fr.wikipedia.org/wiki/Des_chiffres_et_des_lettres#Le_Compte_est_Bon) nous en donne la teneur :  
*Le but de cette épreuve est d'obtenir un nombre (de 101 à 999) à partir d'opérations élémentaires (Addition "+", Soustraction "−", Multiplication "×", Division "÷") sur des entiers naturels, en partant de nombres tirés au hasard (de 1 à 10, 25, 50, 75 et 100). Lorsque l'émission n'était pas informatisée, le jeu comportait vingt-quatre plaques : les nombres de 1 à 10 présents en double exemplaire et les nombres 25, 50, 75 et 100 présents en un seul exemplaire. Sont alors tirées 6 valeurs.  
À défaut de trouver le compte exact, il faut tenter de s'en approcher le plus près possible.*
## Algorithmes existants
Différentes algorithmes en python sont disponibles sur le web, par exemple :  
- [Le Compte Sera Bon de Janiko71](https://github.com/janiko71/le-compte-sera-bon)
- [Le Compte Est Bon de hbouia](https://codes-sources.commentcamarche.net/source/103323-le-compte-est-bon)  
- [Compte est bon Nombre.py de Python-2018](https://github.com/MarcPartensky/Python-2018/blob/master/Compte%20est%20bon%20Nombre.py)
- [le-compte-est-bon de SamuelDSR](https://github.com/SamuelDSR/le-compte-est-bon)
- [leComteEstBon de halftermeyer](https://github.com/halftermeyer/leCompteEstBon)
- [calculator.py de ychaouche](https://gist.github.com/ychaouche/2944228)
- [jupyter de n3times](https://github.com/n3times/jupyter/blob/master/Le%20compte%20est%20bon.ipynb)
- [Le Compte est bon en Python de Christophe Boilley](https://boilley.ovh/blog/bon-compte.html)

Également disponible, un solveur en ligne : [dCode](https://www.dcode.fr/compte-est-bon)
## Principe de l'Algorithme
- Tester toutes les solutions possibles pour un tirage donné
- Simplifier le test et augmenter la rapidité en éliminant les doublons
- Créer une classe Panel qui comporte deux variables d'instance : 
  * la variable numbers, collection de nombre
  * la variable way, string décrivant les différentes opérations pour calculer un nombre
- Utiliser une fonction récursive
- On peut décider des valeurs des plaques et de la cible ou les tirer de manière aléatoire
## Résultats
- Toutes les solutions possibles sont testées dans un délai de l'ordre de 3 secondes (dépendant de la vitesse du processeur)
- Le nombre de solutions testées est variable, dépendant du nombre de doublons, de l'ordre du million
- La première solution exacte, si elle existe, est, le plus souvent, trouvée en quelques millisecondes
- Une fonction printResults affiche le nombre de solutions testées, la première solution trouvée (solution exacte ou solution la plus proche).
- Notons que des valeurs supérieures à 1000 peuvent être cherchées.
- Notons également que l'on peut décider de tirer plus de plaques. Mais la durée de réponse sera considérablement augmentée : de l'ordre de 180 secondes si on tire 7 plaques et non 6 : le nombre de solutions testées passant de 1 à 70 millions !
## Exemple d'affichage
    valeur cible : 620 --- plaques : [1, 75, 3, 100, 2, 10]
    1224821 solutions testées en 3.272111415863037 secondes
    il existe au moins une solution exacte : 620
    3 + 75 = 78
    2 + 78 = 80
    10 - 1 = 9
    9 x 80 = 720
    720 - 100 = 620
    première solution exacte trouvée en 0.00000946688652038574 millisecondes
    nombre de solutions exactes testées : 199
## ToDo
- Fenêtre d'option : aléatoire ou non
- Alerte d'erreur si la cible choisie n'est pas un entier
- Alerte d'erreur si les plaques choisies ne respectent pas la règle du jeu
- Afficher plusieurs solutions exactes et non la première
- Version anglophone du ReadMe et des commentaires du script
