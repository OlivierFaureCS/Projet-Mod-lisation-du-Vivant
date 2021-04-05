from tkinter import *
import random as rd
import numpy.random as nprd
import matplotlib.pyplot as plt
import numpy as np

pd = 1
duree_vie_min = 7
duree_vie_max = 14
apoptose = True  # mettre False si on ne veut pas de phénomène d'apoptose, True sinon
ecart_temps = 10


def damier():  # fonction dessinant le tableau
    ligne_vert()
    ligne_hor()


def ligne_vert():
    c_x = 0
    while c_x != width:
        can1.create_line(c_x, 0, c_x, height, width=1, fill='black')
        c_x += c


def ligne_hor():
    c_y = 0
    while c_y != height:
        can1.create_line(0, c_y, width, c_y, width=1, fill='black')
        c_y += c


def click_gauche(event):  # fonction rendant vivante la cellule cliquée donc met la valeur 1 pour la cellule cliquée au dico_case
    x = event.x - (event.x % c)
    y = event.y - (event.y % c)
    can1.create_rectangle(x, y, x+c, y+c, fill='black')
    dico_case[x, y] = 1


def click_droit(event):  # fonction tuant la cellule cliquée donc met la valeur 0 pour la cellule cliquée au dico_case
    x = event.x - (event.x % c)
    y = event.y - (event.y % c)
    can1.create_rectangle(x, y, x+c, y+c, fill='white')
    dico_case[x, y] = 0


def change_vit(event):  # fonction pour changer la ecart_temps(l'attente entre chaque étape), ne fonctionne pas très bien
    global ecart_temps
    ecart_temps = int(eval(entree.get()))
    print(ecart_temps)


def go():
    "démarrage de l'animation"
    global flag
    if flag == 0:
        flag = 1
        play()


def stop():
    "arrêt de l'animation"
    global flag
    flag = 0


def play():  # fonction comptant le nombre de cellules vivantes autour de chaque cellule
    global flag, ecart_temps, dico_case, vie_cellule, cellule_vivante
    dico_case = tour(dico_case)
    if apoptose:  # ici on traite le cas de l'apoptose: si une cellule vivante atteint sa durée de vie, elle meurt
        for cell in dico_case:
            x, y = cell[0], cell[1]
            if not(x < 0 or y < 0 or x >= width or y >= height) and dico_case[cell] == 1:
                if vie_cellule[cell] == [0, 0]:
                    duree_vie = rd.randint(duree_vie_min, duree_vie_max)
                    vie_cellule[cell] = [1, duree_vie]
                elif vie_cellule[cell][0] == vie_cellule[cell][1]:
                    dico_case[cell] = 0
                    vie_cellule[cell] = [0, 0]
                else:
                    vie_cellule[cell][0] += 1

    cell_vivante = 0  # compteur du nombre de cellules vivantes
    for cell in dico_case:
        x, y = cell[0], cell[1]
        if not(x < 0 or y < 0 or x >= width or y >= height) and dico_case[cell] == 1:
            cell_vivante += 1
    cellule_vivante.append(cell_vivante)
    redessiner()
    if flag > 0:
        fen1.after(ecart_temps, play)


def redessiner():  # fonction redessinant le tableau à partir de dico_etat
    can1.delete(ALL)
    damier()
    t = 0
    while t != width/c:
        u = 0
        while u != height/c:
            x = t*c
            y = u*c
            if dico_case[x, y] == 1:
                can1.create_rectangle(x, y, x+c, y+c, fill='black')
            else:
                can1.create_rectangle(x, y, x+c, y+c, fill='white')
            u += 1
        t += 1


def tour(dico):
    global height, width
    newdico = dico.copy()
    cles = list(newdico.keys())
    rd.shuffle(cles)  # on choisit de traiter les cellules vivantes dans un ordre aléatoire popur ne pas privilégier une certaine géométrie (ex traiter les cellules de gauche à droite)
    for cell in cles:
        x, y = cell[0], cell[1]
        # = la cellule n'est pas sur la bordure fictive et est vivante.
        if not(x < 0 or y < 0 or x >= width or y >= height) and dico[cell] == 1:
            division(newdico, cell)
    return newdico


def division(newdico, cell):
    # on obtient la liste des cases voisines de notre cellule avec pour chacune d'elles la probabilité que notre cellule se divise sur cette case.
    voisins_vide = get_empty_neighbors(newdico, cell)
    if voisins_vide != []:
        fille = choisir_fille(voisins_vide)
        if fille != []:  # si la cellule se divise, on rend sa fille vivante
            x, y = fille[0], fille[1]
            newdico[x, y] = 1


def get_empty_neighbors(dico, cell):
    voisins_vides = []
    x, y = cell[0], cell[1]
    for i in range(3):
        for j in range(3):
            # ie si la case n'est pas celle de notre cellule et qu'elle est vide
            if (x-c+i*c, y-c+j*c) != (x, y) and dico[(x-c+i*c, y-c+j*c)] == 0:
                if (i+j) % 2 == 0:  # permet de savoir si la case est en diagonale par rapport à notre cellule
                    voisins_vides.append((x-c+i*c, y-c+j*c, pd))
                else:
                    voisins_vides.append((x-c+i*c, y-c+j*c, 1))
    return voisins_vides


def choisir_fille(voisins_vide):
    somme_proba = 0
    for cell in voisins_vide:
        somme_proba += cell[2]
    if somme_proba < 1:  # Dans ce cas, seules des cellules en diagonales sont accessibles
        nb = rd.randint(0, len(voisins_vide)-1)  # on en choisit une au hasard
        # on fait un tirage probabiliste de Bernoulli pour déterminer si notre cellule s'y divisera
        bol = nprd.binomial(1, pd) == 0
        if bol:
            return voisins_vide[nb]  # si le tirage vaut 0 on renvoie la fille
        return []  # sinon elle ne se divise pas
    else:
        # cas où seule une cellule au N/S/E/W est libre.
        if len(voisins_vide) == 1:
            return voisins_vide[0]
        poids = [voisins_vide[i][2] /
                 somme_proba for i in range(len(voisins_vide))]  # cas où plusieurs case sont libres dont des cellules N/S/E/W, on choisit une fille en pondérant par les probabilités les voisines libres.
        [fille] = rd.choices(voisins_vide, weights=poids)
        return fille


# les différentes variables:
# taille de la grille
global height, width
height = 600
width = 600

# taille des cellules
c = 5

flag = 0

# liste contenant à le nombre de cellules vivantes à chaque tour.
cellule_vivante = []
# dictionnaire qui pour chaque cellule contient sa durée de vie et sa durée de vie maximale.
vie_cellule = {}
dico_case = {}  # dictionnaire contenant les coordonnées de chaques cellules et une valeur 0 ou 1 si elles sont respectivement mortes ou vivantes
i = -1
# assigne une valeur 0(morte) a chaque coordonnées(cellules), pour ne pas se préoccuper des cas particuliers aux bords, on ajoute une "bordure" fictive autour de la grille affichée où toutes les cellules restent mortes.
while i != width/c+1:
    j = -1
    while j != height/c+1:
        x = i*c
        y = j*c
        if i < 0 or j < 0 or i >= width/c or j > height/c:
            vie_cellule[x, y] = [0, 0]
            dico_case[x, y] = 1
        else:
            dico_case[x, y] = 0
            vie_cellule[x, y] = [0, 0]
        j += 1
    i += 1

# programme "principal"
fen1 = Tk()

can1 = Canvas(fen1, width=width, height=height, bg='white')
can1.bind("<Button-1>", click_gauche)
can1.bind("<Button-3>", click_droit)
can1.pack(side=TOP, padx=5, pady=5)

damier()

b1 = Button(fen1, text='Go!', command=go)
b2 = Button(fen1, text='Stop', command=stop)
b1.pack(side=LEFT, padx=3, pady=3)
b2.pack(side=LEFT, padx=3, pady=3)


entree = Entry(fen1)
entree.bind("<Return>", change_vit)
entree.pack(side=RIGHT)
chaine = Label(fen1)
chaine.configure(text="Attente entre chaque étape (ms) :")
chaine.pack(side=RIGHT)


def tracer():
    liste = [i for i in range(len(cellule_vivante))]
    plt.plot(liste, cellule_vivante)
    plt.xlabel("temps")
    plt.ylabel("Nombre de cellules")
    plt.title("Nombre de cellules en fonction du temps")
    plt.show()


b4 = Button(fen1, text='Graphe', command=tracer)
b4.pack(side=LEFT, padx=3, pady=3)
fen1.mainloop()
