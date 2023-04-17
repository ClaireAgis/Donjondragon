
from tkinter import *
import tkinter.font
import keyboard
import time
import random
import sys

#CLASSES
class Object:  # object dans le jeu
    def __init__(self, Nomobject, effet):
        self.Nomobject = Nomobject
        self.effet = effet

class Ennemi:  # classe mechant
    def __init__(self, Type, degat):
        self.Type = Type
        self.degat = degat

class Enigme:  # tenigme
    def __init__(self, enigme, reponse, bonus, malus):
        self.enigme = enigme
        self.reponse = reponse
        self.bonus = bonus
        self.malus = malus


    def chargement_enigme(self,joueur):
        global saisie
        saisie = False
        saisi = StringVar()
        # creation d'une Entry pour la saisi de l'utilisateur
        barre = Entry(game, width=50, textvariable=saisi)
        boutonVal = Button(game, text="Valider", command=recupSaisie, height=5, width=20)

        while saisie != True:  # tant qu'on appui pas sur le bouton valider
            print("On atend la saisie")
            canvas.itemconfigure('txtpiece', text="\tENIGME \n"+ self.enigme+"\n\n\n\n\n\n\n")
            canvas.update()
            barre.place(x=550, y=400)
            boutonVal.place(x=620, y=550)

        boutonVal.destroy()
        barre.destroy()

        if (saisi.get() == self.reponse):
            print("bonne reponse")
            if self.bonus.Nomobject == "keur" :  # si objt bonus de heal
                # on ajoute le bonus au joueur
                canvas.itemconfigure('txtpiece', text="Bonne réponse \n       +1 vie\n\n")
                joueur.vie += self.bonus.effet
                if joueur.vie > 3 :
                    joueur.vie = 3  # vie max du perso
            if self.bonus.Nomobject.find("tresor") != -1:  # objt rapporte des points de score
                canvas.itemconfigure('txtpiece',text="Bonne réponse \n     +"+ str(self.bonus.effet) +" points\n\n")
                joueur.score += self.bonus.effet
            else :
                canvas.itemconfigure('txtpiece',text="Bonne réponse \n\n   0bjet trouvé\n\n")
                joueur.inventaire.append(self.bonus)
        else :
            print("mauvaise reponse")
            canvas.itemconfigure('txtpiece', text="Mauvaise réponse\n\n\n\n        -1 vie \n\n")
            joueur.vie += self.malus

        canvas.update()

class Joueur:  # classe joueur
    def __init__(self, pseudo):  # pseudo du joueur, pdv,positions,score,inventaire
        self.pseudo = pseudo
        self.vie = 3 #Init a 3 au debut
        self.posx = 0 #init a l'entree du lab en fct du type de difficulté
        self.posy = 0  #init a l'entree du lab en fct du type de difficulté
        self.score = 0
        #self.niveau = "FACILE" #difficulté du lab actuel du joeur
        self.niveau = "FACILE"  # difficulté du lab actuel du joeur
        self.inventaire = []
        self.imx = 428
        self.imy = 240

class Chambre:  # classe chambre
    def __init__(self, portes, etat, evenement):
        self.portes = portes  #si porte ou mur
        self.etat = etat  #si piece visitée ou bloquée ou  libre
        self.evenement = evenement

#########################
#SAUVEGARDE DE LA PARTIE#
#########################

#Sauvegarde des données du joueur a chaque fois qu'on est a un niveau supp
def SauvegardeJoueur(joueur,nfichier):
    #sauvegarde des données du joueur pour mode diffi et moyen
    fichier = open(nfichier, "w")

    fichier.write(joueur.pseudo + "\n") #pseudo du joueur
    fichier.write(str(joueur.vie)+ "\n") #nbr de pv
    fichier.write(str(joueur.score)+ "\n") #score du joueur
    fichier.write(str(joueur.niveau)+ "\n")  #mode facile moyen ou difficile
    fichier.write(str(joueur.posx) + "\n")  # score du joueur
    fichier.write(str(joueur.posy) + "\n")  # mode facile moyen ou difficile
    fichier.write(str(joueur.imx) + "\n")  # score du joueur
    fichier.write(str(joueur.imy) + "\n")  # mode facile moyen ou difficile
    for object in joueur.inventaire :
        #on sauvegarde les effets et le nom de l'objet pour pouvoir les recréer
        fichier.write(object.Nomobject+ "\n") #inventaire
        fichier.write(str(object.effet)+ "\n")

    fichier.close()
#lecture donnée du joueur
def LectureJoueur(joueur,nfichier) :
    i = 8
    inv = []
    contenu = []
    # Lecture fichier
    with open(nfichier, 'r') as fichier:  # on lit le fichier ligne par ligne
        lecture = fichier.readlines()

    for ligne in lecture:  # on supprime les caractere de saut de ligne
        temp = ligne.strip()
        contenu.append(temp)

    joueur.pseudo = contenu[0]
    joueur.vie = int(contenu[1])
    joueur.score = int(contenu[2])
    joueur.niveau = contenu[3]
    joueur.posx = int(contenu[4])
    joueur.posy = int(contenu[5])
    joueur.imx = int(contenu[6])
    joueur.imy = int(contenu[7])
    while i < len(contenu) :
        inv.append(Object(contenu[i],int(contenu[i+1])))
        i+=2
    joueur.inventaire = inv.copy()
    fichier.close()

    return joueur
#sauvegarde du labyrinthe
def SauvegardeLab(lab) :
    fichier = open("labyrinthe.txt", "w")
    #On sauvegarde en premier la taille du labyrinthe (Facile =5x5 moyen=5x6 difficile=6x6)
    fichier.write(str(len(lab)) + "\n")
    fichier.write(str(len(lab[0])) + "\n")
    for ligne in lab :
        for chambre in ligne : #on parcourt chaque chambre du labyrinthe pour sauvegarder les données
            i = 0
            while i < 4 : #on sauve le tableau de porte
                fichier.write(str(chambre.portes[i]) + "\n")  # 1 ou 0
                i += 1
            #sauvegarde etat de la piece
            fichier.write(chambre.etat + "\n")
            # sauvegarde de l'evenement
            if type(chambre.evenement) == str :
                fichier.write(chambre.evenement + "\n")
            if type(chambre.evenement) == Object : #il faut sauvegarder toutes les données de l'objet
                fichier.write(chambre.evenement.Nomobject + "\n")
                if chambre.evenement.Nomobject != "portailS" and chambre.evenement.Nomobject != "portailE" :
                    fichier.write(str(chambre.evenement.effet) + "\n")
                else : #cas ou l'objet est un portail et ou il faut sauvegarder une lmiste pour les effets
                    i = 0
                    while i < len(chambre.evenement.effet) :
                        fichier.write(str(chambre.evenement.effet[i]) + "\n")
                        i += 1
            if type(chambre.evenement) == Ennemi : #il faut sauvegarder toutes les données de l'ennemi
                fichier.write(chambre.evenement.Type + "\n")
                fichier.write(str(chambre.evenement.degat) + "\n")
            if type(chambre.evenement) == Enigme : #il faut sauvegarder toutes les données de l'enigme
                fichier.write(chambre.evenement.enigme + "\n")
                fichier.write(chambre.evenement.reponse + "\n")
                fichier.write(chambre.evenement.bonus.Nomobject + "\n")
                fichier.write(str(chambre.evenement.bonus.effet) + "\n")
                fichier.write(str(chambre.evenement.malus) + "\n")
#return lab
def LectureLab() : #Pour lire le labyrinthe du fichier.txt
    listeCh = [0, 0, 0, 0, 0]
    lab = [[], [], [], [], []]
    contenu = []
    portes = [0,0,0,0]
    listeS = [0,0]
    listeE = [0,0,0,0]

    # Lecture fichier
    with open('labyrinthe.txt', 'r') as fichier:  # on lit le fichier ligne par ligne
        lecture = fichier.readlines()

    for ligne in lecture:  # on supprime les caractere de saut de ligne
        temp = ligne.strip()
        contenu.append(temp)

    line = int(contenu[0])
    ch = int(contenu[1])

    if line == 5 :
        lab = [[], [], [], [], []]
    if line == 6 :
        lab = [[], [], [], [], [], []]
    if ch == 5 :
        listeCh = [0, 0, 0, 0, 0]
        tp = [0, 0, 0, 0, 0]
    if ch == 6 :
        listeCh = [0, 0, 0, 0, 0, 0]
        tp = [0, 0, 0, 0, 0,0]
    i = 2
    tmp=2
    y = 0 #num de la ligne
    while i < len(contenu) : #on parcourt notre liste de chaine et on rempli le lab
        y = 0
        while y < line :
            x = 0
            while x < ch :
                portes[0] = int(contenu[i])
                i+=1
                portes[1] = int(contenu[i])
                i += 1
                portes[2] = int(contenu[i])
                i += 1
                portes[3] = int(contenu[i])
                i += 1
                # lit etat de la piece
                etat=contenu[i]
                i += 1
                # lit de l'evenement
                if contenu[i] == "rien" or contenu[i] == "depart":
                    listeCh[x] = Chambre(portes.copy(),etat,contenu[i]) #on crée la chambre
                    i += 1
                    x += 1
                    if x == ch:
                        break
                #OBJET
                elif contenu[i] == "potion" or contenu[i] == "aile" or contenu[i] == "potion" or contenu[i] == "aile" or contenu[i] == "rubis" or contenu[i] == "epee" or contenu[i] == "keur" or contenu[i] == "bbtresor" or contenu[i] == "midtresor" or contenu[i] == "grostresor":  # il faut lire toutes les données de l'objet
                    Nom = contenu[i]
                    i+=1
                    listeCh[x] = Chambre(portes.copy(),etat,Object(Nom,int(contenu[i])))
                    i += 1
                    x+=1
                    if x == ch:
                        break
                elif contenu[i] ==  "portailS" :
                    Nom = contenu[i]
                    i += 1
                    listeS[0] = int(contenu[i])
                    i += 1
                    listeS[1] = int(contenu[i])
                    i += 1
                    listeCh[x] = Chambre(portes.copy(), etat, Object(Nom, listeS))
                    x += 1
                    if x == ch:
                        break
                elif contenu[i] == "portailE":
                    Nom = contenu[i]
                    i += 1
                    listeE[0] = int(contenu[i])
                    i += 1
                    listeE[1] = int(contenu[i])
                    i += 1
                    listeE[2] = int(contenu[i])
                    i += 1
                    listeE[3] = int(contenu[i])
                    i += 1
                    listeCh[x] = Chambre(portes.copy(), etat, Object(Nom, listeE))
                    x += 1
                    if x == ch:
                        break
                #ENNEMI
                elif contenu[i] == "dragon" or contenu[i] == "gobelin" or contenu[i] == "boss" :
                    Nom = contenu[i]
                    i += 1
                    listeCh[x] = Chambre(portes.copy(), etat, Ennemi(Nom,int(contenu[i])))
                    i += 1
                    x += 1
                    if x == ch:
                        break
                #ENIGME
                elif contenu[i] == "qu'est ce qui traverse les fenêtres sans les casser?" or contenu[i] == "Aussitôt que l'on me nomme, je n'existe plus. Qui suis-je?" or contenu[i] == "Qui tombe sans se faire mal ?" or contenu[i] == "Qu'est-ce qui peut être dans la mer et dans le ciel ?" :
                    quest = contenu[i]
                    i += 1
                    rep = contenu[i]
                    i += 1
                    #objet
                    if contenu[i] == "potion" or contenu[i] == "aile" or contenu[i] == "potion" or contenu[i] == "aile" or contenu[i] == "rubis" or contenu[i] == "epee" or contenu[i] == "keur" or contenu[i] == "bbtresor" or contenu[i] == "midtresor" or contenu[i] == "grostresor":  # il faut lire toutes les données de l'objet
                        Nom = contenu[i]
                        i += 1
                        tmp=i+1
                        listeCh[x] = Chambre(portes.copy(), etat, Enigme(quest,rep,Object(Nom,int(contenu[i])),int(contenu[tmp])))
                        i = tmp + 1
                        x+=1
                        if x == ch:
                            break
                print("i = ", i)
            lab[y] = listeCh.copy()
            listeCh = tp.copy()
            y+=1
            print("nouvelle ligne")
            print("i = ", i)
            print("contenu", len(contenu))
        print("i = ", i)
        break
    print("affichage des portes\n")
    for ligne in lab:
        for chambre in ligne:
            print(chambre.portes)
    return lab
#sspgrm pour sauvegarder l'ensemble de la partie (appel sauveJ et sauveLab)
def Save(joueur,lab) :
    global reprendre
    global pause
    global canvas
    SauvegardeJoueur(joueur, "savejoueur.txt")#on sauvegarde le joueur
    SauvegardeLab(lab) #on sauvegarde le labyrinthe
    pause.destroy()
    canvas.delete('joueur')
    reprendre = True
    Partie(joueur, lab)

def Liresauvegarde(joueur,lab) : #on lit la sauvegarde
    global save
    save = True #on met save a True et dans Partie() on a va init le joueur et oe lab en lisant le fichier de sauvegarde
    Partie(joueur,lab)  #on lance une partie en sauvegardant ca

###CHARGEMENT RECUP SAISIE
def recupSaisie() : #permet d'obtenir la saisie pour les Entry() (enigme saisi pseudo etc..)
    global saisie
    saisie = True

#########################
##CREATION DE LA PARTIE##
#########################

###CHARGEMENT CREATION JOUEUR
def CreationJoueur() :
    global saisie
    global canvas
    global game
    saisie = False
    saisi = StringVar()
    #creation d'une Entry pour la saisi de l'utilisateur
    barre = Entry(game,width = 50,textvariable=saisi)
    boutonVal = Button(game,text="Valider",command = recupSaisie,height=5,width=20)

    while saisie != True : #tant qu'on appui pas sur le bouton valider
        print("On atend la saisie")
        canvas.itemconfigure('text', text="Saisir le pseudo : ")
        canvas.update()
        barre.place(x=550, y=500)
        boutonVal.place(x=620, y=650)
    canvas.itemconfigure('text', text = "")
    boutonVal.destroy()
    barre.destroy()
    j1 = Joueur(saisi.get()) #on créé un nouveau joueur
    return j1
#affichage des données du joueurs
def AffichageJoueur(joueur):
    #AFFICHAGE DES INFOS DU JOUEUR A L'ECRAN
    print("Joueur : ", joueur.pseudo)
    print("PDV : ", joueur.vie)
    print("Score : ", joueur.score)
    print("Inventaire : ", joueur.inventaire)
    print("posx : ", joueur.posx)
    print("posy : ", joueur.posy)
#affichage d'une chambre contenu dans le labyrinthe
def AffichageChambre(chambre,nb):
    print("Chambre n° ",nb)
    i = 0
    #Affichage des cotés ou on peut aller
    while i<len(chambre.portes):
        if i==0 : #Porte de DROITE
            if(chambre.portes[i]==1) : #On peut aller a droite
                print("On peut aller a droite")
            if (chambre.portes[i] == 0):  # On ne peut pas aller a droite
                print("On ne peut pas aller a droite")
        if i == 1:  # Porte de HAUT
            if (chambre.portes[i] == 1):  # On peut aller en haut
                print("On peut aller en haut")
            if (chambre.portes[i] == 0):  # On ne peut pas aller en haut
                print("On ne peut pas aller en haut")
        if i == 2:  # Porte de GAUCHE
            if (chambre.portes[i] == 1):  # On peut aller a gauche
                print("On peut aller a gauche")
            if (chambre.portes[i] == 0):  # On ne peut pas aller a gauche
                print("On ne peut pas aller a gauche")
        if i == 3:  # Porte de BAS
            if (chambre.portes[i] == 1):  # On peut aller en bas
                print("On peut aller en bas")
            if (chambre.portes[i] == 0):  # On ne peut pas aller en bas
                print("On ne peut pas aller en bas")
        i = i + 1
    #Etat de la piece
    print("etat :",chambre.etat)
    #Evenement dans la piece
    if type(chambre.evenement) == str: #cas l'evenement est une chaine
        print("Chaine")
        if(chambre.evenement=="rien") : #pas d'evenement
            print("Rien dans la piece")
    if type(chambre.evenement) == Object:#cas l'evenement est un objet
        print("object")
    if type(chambre.evenement) == Ennemi: #cas l'evenement est un ennemi
        print("ennemi")
    if type(chambre.evenement) == Enigme: #cas l'evenement est une enigme
        print("enigme")
def CreationLabyrinthe(mode):
    listeCh = [0,0,0,0,0]
    labyrinthe = [[],[],[],[],[]]

    #creation des diff typ d'objet
    epee = Object("epee",0) #boss final askip
    #autre objets a ajouter :
    Potion = Object("potion",1) #permet de regarder un coeur quand on l'active
    Aile = Object("aile",0) #permet de sauter une case
    Rubis = Object("rubis",0) #invisibilite face au prochain monstre
    keur = Object("keur",1)
    bbtresor = Object("bbtresor",100)
    tresormid = Object("midtresor", 200)
    Grostresor = Object("grostresor", 300)
    portail1 = Object("portailS", [4,0]) #E pour l'entree du portail, S pour la sortie
    portail2 = Object("portailE", [0,5,470,-340])
    portail3 = Object("portailE", [5,5,390,86])
    portail4 = Object("portailS", [4,1])
    #creation ennemi
    dragon = Ennemi("dragon",1)
    gobelin = Ennemi("gobelin",1)
    boss = Ennemi("boss",3)
    #creation enigme
    E1 = Enigme("qu'est ce qui traverse les fenêtres sans les casser?", "la lumière", tresormid, -1)
    E2 = Enigme("Aussitôt que l'on me nomme, je n'existe plus. Qui suis-je?", "Le silence", Aile, -1)
    E3 = Enigme("Qui tombe sans se faire mal ?", "La nuit", bbtresor, -1)
    E4 = Enigme("Qu'est-ce qui peut être dans la mer et dans le ciel ?", "Une étoile", keur, -1)

    if(mode == "FACILE") : #mode facile
        #creation labyrinthe de 5X5

        #premiere ligne labyrinthe 1
        listeCh[0] = Chambre([1,0,0,1],"visitee","depart")
        listeCh[1] = Chambre([1,0,1,1],"libre","rien")
        listeCh[2] = Chambre([1, 0, 1, 1], "libre", keur)
        listeCh[3] = Chambre([1, 0, 1, 1], "libre", "rien")
        listeCh[4] = Chambre([0, 0, 1, 1], "bloque", "rien")
        labyrinthe[0]=listeCh[:]
        listeCh[:] = [0,0,0,0,0]
        #2nd ligne lab 1
        listeCh[0] = Chambre([1, 1, 0, 1], "libre", "rien")
        listeCh[1] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[2] = Chambre([1, 1, 1, 1], "libre", E1)
        listeCh[3] = Chambre([1, 1, 1, 1], "libre", epee)
        listeCh[4] =  Chambre([0, 1, 1, 1], "libre", keur)
        labyrinthe[1] = listeCh[:]
        listeCh[:] = [0,0,0,0,0]
        # 3nd ligne lab 1
        listeCh[0] = Chambre([1, 1, 0, 1], "libre", dragon)
        listeCh[1] = Chambre([1, 1, 1, 1], "libre", bbtresor)
        listeCh[2] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[3] = Chambre([1, 1, 1, 1], "libre", gobelin)
        listeCh[4] = Chambre([0, 1, 1, 1], "libre", "rien")
        labyrinthe[2] = listeCh[:]
        listeCh[:] =[0,0,0,0,0]
        # 4nd ligne lab 1
        listeCh[0] = Chambre([1, 1, 0, 1], "bloque", "rien")
        listeCh[1] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[2] = Chambre([1, 1, 1, 1], "libre", dragon)
        listeCh[3] = Chambre([1, 1, 1, 1], "libre", boss)
        listeCh[4] = Chambre([0, 1, 1, 1], "libre", "rien")
        labyrinthe[3] = listeCh[:]
        listeCh[:] = [0,0,0,0,0]
        # 5nd ligne lab 1
        listeCh[0] = Chambre([1, 1, 0, 0], "libre", keur)
        listeCh[1] = Chambre([1, 1, 1, 0], "libre", "rien")
        listeCh[2] = Chambre([1, 1, 1, 0], "libre", "rien")
        listeCh[3] = Chambre([1, 1, 1, 0], "libre", "rien")
        listeCh[4] = Chambre([0, 1, 1, 0], "libre", Grostresor)
        labyrinthe[4] = listeCh[:]

        listeCh[:] = []

    if (mode == "MOYEN"): #mode moyen
        print("Niveau 2")
        listeCh[:] = [0, 0, 0, 0, 0, 0]
        # creation lab de 5X6

        # premiere ligne labyrinthe 2
        listeCh[0] = Chambre([1, 0, 0, 1], "visitee", "depart")
        listeCh[1] = Chambre([1, 0, 1, 1], "libre", "rien")
        listeCh[2] = Chambre([1, 0, 1, 1], "libre", dragon)
        listeCh[3] = Chambre([1, 0, 1, 1], "libre", keur)
        listeCh[4] = Chambre([1, 0, 1, 1], "libre", Potion)
        listeCh[5] = Chambre([0, 0, 1, 1], "libre", portail1)

        labyrinthe[0] = listeCh[:]
        listeCh[:] = [0, 0, 0, 0, 0, 0]
        # 2nd ligne lab 2
        listeCh[0] = Chambre([1, 1, 0, 1], "libre", gobelin)
        listeCh[1] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[2] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[3] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[4] = Chambre([1, 1, 1, 1], "libre", E2)
        listeCh[5] = Chambre([0, 1, 1, 1], "libre", "rien")
        labyrinthe[1] = listeCh[:]
        listeCh[:] = [0, 0, 0, 0, 0, 0]
        # 3nd ligne lab 2
        listeCh[0] = Chambre([1, 1, 0, 1], "bloque", "rien")
        listeCh[1] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[2] = Chambre([1, 1, 1, 1], "bloque", "rien")
        listeCh[3] = Chambre([1, 1, 1, 1], "libre", gobelin)
        listeCh[4] = Chambre([1, 1, 1, 1], "libre", dragon)
        listeCh[5] = Chambre([0, 1, 1, 1], "libre", dragon)
        labyrinthe[2] = listeCh[:]
        listeCh[:] = [0, 0, 0, 0, 0, 0]
        # 4nd ligne lab 2
        listeCh[0] = Chambre([1, 1, 0, 1], "libre", Grostresor)
        listeCh[1] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[2] = Chambre([1, 1, 1, 1], "libre", keur)
        listeCh[3] = Chambre([1, 1, 1, 1], "libre", gobelin)
        listeCh[4] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[5] = Chambre([0, 1, 1, 1], "libre", boss)
        labyrinthe[3] = listeCh[:]
        listeCh[:] = [0, 0, 0, 0, 0, 0]
        # 5nd ligne lab 2
        listeCh[0] = Chambre([1, 1, 0, 0], "libre", portail2)
        listeCh[1] = Chambre([1, 1, 1, 0], "libre", E3)
        listeCh[2] = Chambre([1, 1, 1, 0], "libre", "rien")
        listeCh[3] = Chambre([1, 1, 1, 0], "libre", "rien")
        listeCh[4] = Chambre([1, 1, 1, 0], "bloque", "rien")
        listeCh[5] = Chambre([0, 1, 1, 0], "libre", "rien")
        labyrinthe[4] = listeCh[:]

        listeCh[:] = []

    if (mode == "DIFFICILE"): #mode diff
        print("Niveau 3")
        # creation lab de 6X6
        listeCh[:] = [0, 0, 0, 0, 0, 0]
        labyrinthe[:] = [[], [], [], [], [], []]

        # création de la première ligne
        listeCh[0] = Chambre([1, 0, 0, 1], "visitee", "depart")
        listeCh[1] = Chambre([1, 0, 1, 1], "libre", keur)
        listeCh[2] = Chambre([1, 0, 1, 1], "libre", dragon)
        listeCh[3] = Chambre([1, 0, 1, 1], "bloque", "rien")
        listeCh[4] = Chambre([1, 0, 1, 1], "libre", gobelin)
        listeCh[5] = Chambre([0, 0, 1, 1], "libre", boss)
        labyrinthe[0] = listeCh[:]
        listeCh[:] = [0, 0, 0, 0, 0, 0]

        # création de la deuxième ligne
        listeCh[0] = Chambre([1, 1, 0, 1], "libre", keur)
        listeCh[1] = Chambre([1, 1, 1, 1], "libre", gobelin)
        listeCh[2] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[3] = Chambre([1, 1, 1, 1], "bloque", "rien")
        listeCh[4] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[5] = Chambre([0, 1, 1, 1], "libre", dragon)
        labyrinthe[1] = listeCh[:]
        listeCh[:] = [0, 0, 0, 0, 0, 0]

        # création de la troisième ligne
        listeCh[0] = Chambre([1, 1, 0, 1], "libre", "rien")
        listeCh[1] = Chambre([1, 1, 1, 1], "libre", gobelin)
        listeCh[2] = Chambre([1, 1, 1, 1], "libre", Grostresor)
        listeCh[3] = Chambre([1, 1, 1, 1], "bloque", "rien")
        listeCh[4] = Chambre([1, 1, 1, 1], "libre", E4)
        listeCh[5] = Chambre([0, 1, 1, 1], "libre", "rien")
        labyrinthe[2] = listeCh[:]
        listeCh[:] = [0, 0, 0, 0, 0, 0]

        # création de la quatrième ligne
        listeCh[0] = Chambre([1, 1, 0, 1], "libre", gobelin)
        listeCh[1] = Chambre([1, 1, 1, 1], "libre", Rubis)
        listeCh[2] = Chambre([1, 1, 1, 1], "libre", dragon)
        listeCh[3] = Chambre([1, 1, 1, 1], "bloque", "rien")
        listeCh[4] = Chambre([1, 1, 1, 1], "libre", dragon)
        listeCh[5] = Chambre([0, 1, 1, 1], "libre", keur)
        labyrinthe[3] = listeCh[:]
        listeCh[:] = [0, 0, 0, 0, 0, 0]

        # création de la cinquième ligne
        listeCh[0] = Chambre([1, 1, 0, 1], "libre", "rien")
        listeCh[1] = Chambre([1, 1, 1, 1], "libre", portail3)
        listeCh[2] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[3] = Chambre([1, 1, 1, 1], "bloque", "rien")
        listeCh[4] = Chambre([1, 1, 1, 1], "libre", "rien")
        listeCh[5] = Chambre([0, 1, 1, 1], "libre", "rien")
        labyrinthe[4] = listeCh[:]
        listeCh[:] = [0, 0, 0, 0, 0, 0]

        # création de la sixième ligne
        listeCh[0] = Chambre([1, 1, 0, 0], "libre", keur)
        listeCh[1] = Chambre([1, 1, 1, 0], "libre", "rien")
        listeCh[2] = Chambre([1, 1, 1, 0], "libre", gobelin)
        listeCh[3] = Chambre([1, 1, 1, 0], "bloque", "rien")
        listeCh[4] = Chambre([1, 1, 1, 0], "libre", dragon)
        listeCh[5] = Chambre([0, 1, 1, 0], "libre", portail4)
        labyrinthe[5] = listeCh[:]

        listeCh[:] = []

    print("Fin creation labyrinthe")
    return labyrinthe

#########################
###DEROULEMENT DE JEU###
#########################

#Deroulement du jeu Action qui se passe en fct de ce qu'il y a dans la piece
def ActionChambre(chambre,joueur):
    global btnPause
    global canvas
    police2 = tkinter.font.Font(family="Time", size=30, weight="bold")
    btnPause.destroy()
    print("Action de la piece")
    #Def des Images
    IMG_vie = PhotoImage(file=r'objtVie.png')
    IMG_epee = PhotoImage(file=r'epee.png')
    IMG_piece = PhotoImage(file=r'piece.png')
    IMG_bbtresor = PhotoImage(file=r'bbtresor.png')
    IMG_midtresor = PhotoImage(file=r'midtresor.png')
    IMG_grostresor = PhotoImage(file=r'grostresor.png')
    IMG_Vortex = PhotoImage(file=r'portail.png')
    IMG_BOSS = PhotoImage(file=r'boss.png')
    IMG_dragon = PhotoImage(file=r'dragon.png')
    IMG_pot = PhotoImage(file=r'PotionI.png')
    IMG_rubis = PhotoImage(file=r'RubisI.png')

    # affichage d'entree dans la piece
    if chambre.etat != "visitee": #si on a pas visite la piece on affiche ce qu'il se passe
        canvas.create_image(0, 0, anchor='nw', tag='piece', image=IMG_piece)
        canvas.create_image(560, 340, anchor='nw', tag='evenement', image="")
        canvas.create_image(470, 220, anchor='nw', tag='ennemi', image="")
        canvas.create_text(690, 440, text="", font=police2, tag='txtpiece', fill="white")

    print("etat :", chambre.etat) #visitée libre ou bloquée

    # Evenement dans la piece
    if type(chambre.evenement) == str and chambre.etat != "visitee":  # cas l'evenement est une chaine
        # pas d'evenement dans cette piece
        print("Rien dans la piece")
        canvas.itemconfigure('txtpiece', text="Rien dans la pièce")

    if type(chambre.evenement) == Object :  # cas l'evenement est un objet
        print("OBJET TROUVE : ",chambre.evenement.Nomobject)
        #action de l'objet
        if chambre.evenement.Nomobject == "keur": #si objt bonus de heal
            #on ajoute le bonus au joueur
            joueur.vie += chambre.evenement.effet
            canvas.itemconfigure('evenement', image=IMG_vie)
            if joueur.vie > 3 :
                canvas.itemconfigure('txtpiece', text="  OBJET TROUVE\n\n\n\n\n\n\n\n\n       VIE MAX")
                joueur.vie = 3 #vie max du perso
            else :
                canvas.itemconfigure('txtpiece', text="OBJET TROUVE\n\n\n\n\n\n\n\n + 1 point de vie")
        if  chambre.evenement.Nomobject.find("tresor") != -1 : #objt rapporte des points
            joueur.score += chambre.evenement.effet
            if chambre.evenement.Nomobject == "bbtresor":
                canvas.itemconfigure('evenement', image=IMG_bbtresor)
            if chambre.evenement.Nomobject == "midtresor":
                canvas.itemconfigure('evenement', image=IMG_midtresor)
            if chambre.evenement.Nomobject == "grostresor":
                canvas.itemconfigure('evenement', image=IMG_grostresor)
            canvas.itemconfigure('txtpiece', text="   OBJET TROUVE\n\n\n\n\n\n\n\n\n      + " + str(chambre.evenement.effet) + " points")
        if chambre.evenement.Nomobject=="epee" : #objet inventaire
            joueur.inventaire.append(chambre.evenement)
            canvas.itemconfigure('evenement', image=IMG_epee)
            canvas.itemconfigure('txtpiece', text="\nOBJET TROUVE\n\n\n\n\n\n\n\n\n        EPEE")
        if chambre.evenement.Nomobject == "portailE" : #si c'est l'entree d'un portail
            canvas.itemconfigure('evenement', image=IMG_Vortex)
            canvas.itemconfigure('txtpiece', text="\nVORTEX\n\n\n\n\n\n\n\n\n ")
            x = joueur.imx
            y = joueur.imy
            joueur.posx = chambre.evenement.effet[0]
            joueur.posy = chambre.evenement.effet[1]
            joueur.imx = chambre.evenement.effet[2]
            joueur.imy = chambre.evenement.effet[3]
            canvas.move('joueur', joueur.imx, joueur.imy)
        if chambre.evenement.Nomobject == "portailS" : #si c'est la sortie d'un portail
            print("Rien dans la piece")
            canvas.itemconfigure('txtpiece', text="Rien dans la pièce")
        #objet de l'inventaire
        if chambre.evenement.Nomobject == "rubis": #objet inventaire
            canvas.itemconfigure('evenement', image=IMG_rubis)
            canvas.itemconfigure('txtpiece', text="\nOBJET TROUVE\n\n\n\n\n\n\n\n\n        RUBIS")
            joueur.inventaire.append(chambre.evenement)
        if chambre.evenement.Nomobject == "potion": #objet inventaire
            canvas.itemconfigure('evenement', image=IMG_pot)
            canvas.itemconfigure('txtpiece', text="\nOBJET TROUVE\n\n\n\n\n\n\n\n\n        POTION")
            joueur.inventaire.append(chambre.evenement)
    canvas.update()
    if type(chambre.evenement) == Ennemi:  # cas l'evenement est un ennemi
        print("Ennemi :", chambre.evenement.Type)
        if chambre.evenement.Type != "boss" :
            canvas.itemconfigure('txtpiece', text="   ENNEMI\n\n\n\n\n\n\n\n\n  DRAGON\n\n")
            canvas.itemconfigure('ennemi', image=IMG_dragon)
            joueur.vie -= chambre.evenement.degat
            canvas.update()
        else : #cas boss final
            print("QTE a faire pour battre boss final")
            canvas.itemconfigure('txtpiece', text="        ENNEMI\n\n\n\n\n\n\n\n\n\n BOSS DU NIVEAU\n")
            canvas.itemconfigure('ennemi', image=IMG_BOSS)
            canvas.update()
            time.sleep(1)
            cpt = QTE(joueur) #si cpt >= 5 on passe au niveau suivant sinon on recommence
            canvas.delete('piece')
            canvas.delete('txtpiece')
            canvas.delete('evenement')
            if cpt >= 5 and joueur.niveau == "FACILE":
                joueur.score += 300
                return 2 #fin recoit 2 et on passe au niveau d'au dessus
            if cpt >= 7 and joueur.niveau == "MOYEN":
                joueur.score += 300
                return 2 #fin recoit 2 et on passe au niveau d'au dessus
            if cpt >= 8 and joueur.niveau == "DIFFICILE":
                joueur.score += 300
                return 2 #fin recoit 2 et on passe au niveau d'au dessus
            else :
                return 1 #fin recoit 1 et recommence ce niveau
        if joueur.vie <= 0 :
            time.sleep(1)
            joueur.vie=0
            canvas.delete('piece')
            canvas.delete('txtpiece')
            canvas.delete('evenement')
            return 1  #fin recoit 1 et recommence ce niveau
    if type(chambre.evenement) == Enigme:  # cas l'evenement est une enigme
        print("enigme")
        chambre.evenement.chargement_enigme(joueur) #on lit l'enigme
        if joueur.vie <= 0 :
            time.sleep(1)
            joueur.vie=0
            canvas.delete('piece')
            canvas.delete('txtpiece')
            canvas.delete('evenement')
            return 1 #fin recoit 1 et recommence ce niveau

    time.sleep(1)
    chambre.etat = "visitee"
    canvas.delete('piece')
    canvas.delete('txtpiece')
    canvas.delete('evenement')

    canvas.update()
    return 0

#Deplacement du joueur dans le labyrinthe return l'image de la direction du perso
def Bas(joueur1,lab) :
    global canvas
    IMG_joueurB = PhotoImage(file=r'joueurB.png')
    if joueur1.posx + 1 < len(lab) :
        if lab[joueur1.posx][joueur1.posy].portes[3]==1 and  lab[joueur1.posx+1][joueur1.posy].etat != "bloque" : #la piece dans laquelle on est a une porte vers le bas et la porte n'est pas bloqué
            joueur1.posx += 1 #On augmente x de 1
            canvas.move('joueur', 0, 86) #Ob bouge l'image du joueur
            canvas.itemconfigure('joueur', image=IMG_joueurB)
        elif lab[joueur1.posx+1][joueur1.posy].etat == "bloque" : #si chambre bloque on ne peut pas y aller
            canvas.itemconfigure('joueur', image=IMG_joueurB)
            canvas.itemconfigure('text3', text=" Chambre Bloquée")
    else :
        print("impossible d'aller en bas")
        canvas.itemconfigure('joueur', image=IMG_joueurB)
    canvas.update()
    time.sleep(0.5)
    canvas.itemconfigure('text3', text="")
    return IMG_joueurB #on return la direction
def Droite(joueur1,lab) :
    global canvas
    IMG_joueurD = PhotoImage(file=r'joueurD.png')
    if joueur1.posy + 1 < len(lab[joueur1.posx]) : # impossible d'etre au dessus de taille lab
        if lab[joueur1.posx][joueur1.posy].portes[0] == 1 and lab[joueur1.posx][joueur1.posy+1].etat != "bloque": #la piece dans laquelle on est a une porte vers la droite et la porte n'est pas bloqué
            joueur1.posy += 1
            canvas.move('joueur', 90,0)
            canvas.itemconfigure('joueur', image=IMG_joueurD)
        elif lab[joueur1.posx][joueur1.posy+1].etat == "bloque":
            canvas.itemconfigure('joueur', image=IMG_joueurD)
            canvas.itemconfigure('text3', text=" Chambre Bloquée")
    else :
        print("impossible d'aller a droite")
        canvas.itemconfigure('joueur', image=IMG_joueurD)
    canvas.update()
    time.sleep(0.5)
    canvas.itemconfigure('text3', text="")
    return IMG_joueurD
def Gauche(joueur1,lab) :
    global canvas
    IMG_joueurG = PhotoImage(file=r'joueurG.png')

    if joueur1.posy - 1 >= 0 : # impossible d'etre en dessous de 0
        if lab[joueur1.posx][joueur1.posy].portes[2] == 1 and lab[joueur1.posx][joueur1.posy - 1].etat != "bloque":#la piece dans laquelle on est a une porte vers la gauche et la porte n'est pas bloqué
            joueur1.posy -= 1
            canvas.move('joueur', -90, 0)
            canvas.itemconfigure('joueur', image=IMG_joueurG)
        elif lab[joueur1.posx][joueur1.posy-1].etat == "bloque" :
            canvas.itemconfigure('joueur', image=IMG_joueurG)
            canvas.itemconfigure('text3', text=" Chambre Bloquée")
    else :
        print("impossible d'aller a gauche")
        canvas.itemconfigure('joueur', image=IMG_joueurG)
    canvas.update()
    time.sleep(0.5)
    canvas.itemconfigure('text3', text="")
    return IMG_joueurG
def Haut(joueur1,lab) :
    global canvas
    IMG_joueurH = PhotoImage(file=r'joueurH.png')

    if joueur1.posx - 1 >= 0 : # impossible d'etre en dessous de 0
        print("inf")
        if lab[joueur1.posx][joueur1.posy].portes[1] == 1 and lab[joueur1.posx - 1][joueur1.posy].etat != "bloque":   # la piece dans laquelle on est a une porte vers le bas et la porte n'est pas bloqué
            joueur1.posx -= 1
            canvas.move('joueur', 0, -86) #on deplace l'image du joueur
            canvas.itemconfigure('joueur', image=IMG_joueurH)
        elif lab[joueur1.posx-1][joueur1.posy].etat == "bloque" :
            canvas.itemconfigure('joueur', image=IMG_joueurH)
            canvas.itemconfigure('text3', text=" Chambre Bloquée")
    else :
        print("impossible d'aller en haut")
        canvas.itemconfigure('joueur', image=IMG_joueurH)
    print(joueur1.posx, joueur1.posy)
    canvas.update()
    time.sleep(0.5)
    canvas.itemconfigure('text3', text="")
    return IMG_joueurH
#combat contre le boss a la fin du lab
def QTE(joueur) :
    global canvas
    police2 = tkinter.font.Font(family="Time", size=30, weight="bold")
    if joueur.niveau == "FACILE" :
        chrono = 1.75
    if joueur.niveau == "MOYEN" :
        chrono = 1.5
    if joueur.niveau == "DIFFICILE" :
        chrono = 1.25
    i = 0
    temp = 0
    tp =- 1
    impre =- 1
    cpt = 0 #Compteur du nombre de touche qui ont bien été effectué
    #CHARGEMENT DES IMAGES
    IMG_fond = PhotoImage(file=r'fondQTE.png')
    #image animation dragon
    IMG_dragon1 = PhotoImage(file=r'QTEDrag1.png')
    IMG_dragon2 = PhotoImage(file=r'QTEDrag2.png')
    IMG_dragon3 = PhotoImage(file=r'QTEDrag3.png')
    IMG_dragon4 = PhotoImage(file=r'QTEDrag4.png')
    #image animation perso
    IMG_perso1 = PhotoImage(file=r'QTE0.png')
    IMG_perso2 = PhotoImage(file=r'QTE1.png')
    IMG_perso3 = PhotoImage(file=r'QTE2.png')
    IMG_perso4 = PhotoImage(file=r'QTE3.png')
    IMG_perso5 = PhotoImage(file=r'QTE4.png')
    IMG_winner =  PhotoImage(file=r'winner.png')
    IMG_lose =  PhotoImage(file=r'game_over.png')
    IMG_fight = PhotoImage(file=r'fight.png')

    IMG_touche = PhotoImage(file=r'touche.png')

    listQTE = [chr(random.randint(ord('a'), ord('z'))) for x in range(10)] #génération de 10 lettres aléatoire dans l'alphabet qui vont former la QTE

    listImJ = [IMG_perso2,IMG_perso3,IMG_perso4,IMG_perso5]

    canvas.create_image(0, 0, anchor='nw', tag='Fond', image=IMG_fond)
    canvas.create_image(660, 280, anchor='nw', tag='touche', image=IMG_touche)
    canvas.create_image(260, 605, anchor='nw', tag='perso', image=IMG_perso1)
    canvas.create_image(680, 505, anchor='nw', tag='dragon', image=IMG_dragon1)
    canvas.create_image(20, 300, anchor='nw', tag='dragonattack', image="")
    canvas.create_text(700, 235, text="Appuyez sur espace pour commencer",font=police2, tag='text', fill="white")
    canvas.create_text(698, 316, text="spc", font=police2, tag='lettre',fill="white")
    canvas.create_image(505, 200, anchor='nw', tag='win', image="")
    canvas.create_image(512, 100, anchor='nw', tag='lose', image="")
    canvas.create_image(570, 50, anchor='nw', tag='fight', image=IMG_fight)

    while keyboard.is_pressed('space') != True :
        print("on attend")
        canvas.update()
    while i != 10 : #Tant qu'on a pas fait les 10 touches pour la QTE
        canvas.itemconfigure('text', text="Saisir la touche ci-dessous")
        canvas.itemconfigure('lettre', text=str(listQTE[i]))
        canvas.update()
        if tp != i:
            print("nouvelle touche")
            temp=time.gmtime(time.time()).tm_sec #retourne le nombre de seconde
            tp += 1
        try  : #si on appuie sur la bonne touche
            if keyboard.is_pressed(listQTE[i]) == True and time.gmtime(time.time()).tm_sec - temp <= chrono  : #cas ou on appuie sur la touche bien
                imcourante = random.randint(0, 3)
                while imcourante == impre : #on modifie l'attaque et on verif que ce soit une differente de celle d'avant
                    imcourante = random.randint(0, 3)
                impre=imcourante
                canvas.itemconfigure('perso', image=listImJ[imcourante]) #on modifie l'image du joueur par une attaque alea
                canvas.itemconfigure('dragon',image=IMG_dragon4) #le boss subi une attaque
                canvas.update()
                time.sleep(1)
                canvas.itemconfigure('perso', image=IMG_perso1)
                canvas.itemconfigure('dragon', image=IMG_dragon1)
                canvas.update()
                i += 1
                cpt += 1

        except : #si c'est une autre touche
            # animation attaque du boss
            canvas.itemconfigure('dragon', image=IMG_dragon2)
            canvas.update()
            time.sleep(0.75)
            canvas.itemconfigure('dragon', image="")
            canvas.itemconfigure('dragonattack', image=IMG_dragon3)
            canvas.update()
            time.sleep(1)
            canvas.itemconfigure('dragon', image=IMG_dragon1)
            canvas.itemconfigure('dragonattack', image="")
            canvas.update()
            i += 1

        if time.gmtime(time.time()).tm_sec - temp >  chrono and tp == i: #on a appuyé trop tard
            #animation attaque du boss
            canvas.itemconfigure('dragon', image=IMG_dragon2)
            canvas.update()
            time.sleep(0.75)
            canvas.itemconfigure('dragon', image="")
            canvas.itemconfigure('dragonattack', image=IMG_dragon3)
            canvas.update()
            time.sleep(1)
            canvas.itemconfigure('dragon', image=IMG_dragon1)
            canvas.itemconfigure('dragonattack', image="")
            canvas.update()
            i += 1

    canvas.itemconfigure('touche',image ="")
    canvas.itemconfigure('fight', image="")
    canvas.itemconfigure('lettre', text="")
    canvas.itemconfigure('text', text="")

    if joueur.niveau == "FACILE":
        if cpt >= 5 :   #le personnage a reussi a battre le boss
            canvas.itemconfigure('win', image=IMG_winner)
        else :
            canvas.itemconfigure('lose', image=IMG_lose)
    if joueur.niveau == "MOYEN":
        if cpt >= 7 :   #le personnage a reussi a battre le boss
            canvas.itemconfigure('win', image=IMG_winner)
        else :
            canvas.itemconfigure('lose', image=IMG_lose)
    if joueur.niveau == "DIFFICILE":
        if cpt >= 8 :   #le personnage a reussi a battre le boss
            canvas.itemconfigure('win', image=IMG_winner)
        else :
            canvas.itemconfigure('lose', image=IMG_lose)
    canvas.update()
    time.sleep(4)
    return cpt

#########################
#######MENU DU JEU#######
#########################
def Menu() :
    global game
    global canvas
    global save
    global reprendre
    global btnSave
    global btnPlay
    global btnQuitter
    reprendre = False
    save = False
    # PARTIE GRAPHIQUE TKINTER
    game = Tk()
    print("debut game")
    # fenetre1 = game.attributes('-fullscreen',True) #creation fenetre 1 pour menu
    canvas = Canvas(game, width=1400, height=840)
    # chagement des images
    IMG_Menu = PhotoImage(file=r'menu.png')
    IMG_Quit = PhotoImage(file=r'quit.png')
    IMG_Play = PhotoImage(file=r'play.png')
    IMG_Save = PhotoImage(file=r'save.png')

    police1 = tkinter.font.Font(family="Time", size=60, weight="bold")  # creation de la police pour le projet
    police2 = tkinter.font.Font(family="Time", size=30, weight="bold")
    police3 = tkinter.font.Font(family="Time", size=30, weight="bold")
    fond = canvas.create_image(0, 0, anchor='nw', tag='image')  # image de fond du menu
    text = canvas.create_text(720, 300, text=' ', font=police1, tag='text',fill="white")  # texte qui s'affiche sur le canvas
    canvas.itemconfigure('image', image=IMG_Menu)
    canvas.pack()

    # creation des boutons
    btnPlay = Button(game, command=lambda: Chargement("", [], "partie"), image=IMG_Play, bd=0, height=47, width=183)
    # Button(fenetre1, command=Partie, image=IMG_Play, bd=0, height=52,width=183)\
    btnPlay.place(x=580, y=300)
    btnSave = Button(game, command=lambda: Chargement("", [], "sauvegarde"), image=IMG_Save, bd=0, height=47, width=183)
    # Button(fenetre1, command=Save, image=IMG_Save, bd=0, height=50,width=183)\
    btnSave.place(x=580, y=400)
    btnQuitter = Button(game, command=game.destroy, image=IMG_Quit, bd=0, height=47, width=183)
    # Button(fenetre1, command=fenetre1.destroy, image=IMG_Quit, bd=0, height=52,width=183)
    btnQuitter.place(x=580, y=500)
    canvas.update()

    game.mainloop() #on attend l'appui d'un des boutons

def Aide(joueur,lab) :
    global btnPause
    global canvas
    btnPause.destroy()
    global canvas
    global pause
    global reprendre
    print("AIDE MAIS JSP C QUOI")
    pause.destroy()
    canvas.delete('joueur')
    #Pour reprendre la partie
    reprendre = True
    Partie(joueur,lab)

def Reprendre(joueur,lab) :
    global btnPause
    global canvas
    btnPause.destroy()
    global canvas
    global pause
    global reprendre
    print("On reprend la partie la ou on en etait")
    pause.destroy()
    canvas.delete('joueur')
    reprendre = True
    Partie(joueur, lab)
def Pause(joueur,lab) :
    global canvas
    global pause
    global reprendre
    global btnPause

    btnPause.destroy()
    reprendre = False
    # PARTIE GRAPHIQUE TKINTER
    pause = Toplevel(canvas)
    canvas.itemconfigure('joueur', image="")
    # fenetre1 = game.attributes('-fullscreen',True) #creation fenetre 1 pour menu
    mPause = Canvas(pause, width=350, height=400)

    police1 = tkinter.font.Font(family="Time", size=60, weight="bold")  # creation de la police pour le projet
    fond = mPause.create_image(0, 0, anchor='nw', tag='menuP')  # image de fond du menu

    # Add text
    # label2 = Label(game, text=" ",bg="#88cffa")
    # label2.pack(pady=50)

    # creation des boutons
    btnPlay = Button(pause, command=lambda:Reprendre(joueur,lab), text = "Continuer", bd=3) #on reprend le niveau
    # Button(fenetre1, command=Partie, image=IMG_Play, bd=0, height=52,width=183)\
    btnPlay.pack()
    btnAide = Button(pause, command=lambda:Aide(joueur,lab), text = "Afficher l'aide", bd=3)
    # Button(fenetre1, command=Save, image=IMG_Save, bd=0, height=50,width=183)\
    btnAide.pack()
    btnSave = Button(pause, command=lambda: Save(joueur,lab),  text = "Sauvegarder", bd=3)
    # Button(fenetre1, command=fenetre1.destroy, image=IMG_Quit, bd=0, height=52,width=183)
    btnSave.pack()

    while  True :
        mPause.update()

def Chargement(joueur,lab, Type) : #save var pour savoir si c'est une sauvegarde ou celle de base
    #destruction du menu
    global canvas
    global btnSave
    global btnPlay
    global btnQuitter
    btnSave.destroy()
    btnPlay.destroy()
    btnQuitter.destroy()
    IMG_saisi = PhotoImage(file=r'Donjon.png')
    canvas.itemconfigure('image', image=IMG_saisi)
    canvas.itemconfigure('text', text="Saisir le pseudo : ")
    canvas.update()
    if Type == "partie" :
        Partie(joueur,lab)
    if Type == "sauvegarde" :
        Liresauvegarde(joueur,lab)

#Gere le deroulement de la partie en cours
def Partie(joueur1,lab) :
    global canvas
    global game
    global btnPause
    global save
    global reprendre
    FIN_PARTIE = False
    i = 0
    #CHARGEMENT DES IMAGES
    police2 = tkinter.font.Font(family="Time", size=30, weight="bold")
    police3 = tkinter.font.Font(family="Time", size=30, weight="bold")
    #chargement image
    IMG_vie2 = PhotoImage(file=r'coeurV.png')
    IMG_vie1 = PhotoImage(file=r'coeurP.png')
    IMG_labFACILE = PhotoImage(file=r'labfacile.png') #labyrinthe
    IMG_labmoyen = PhotoImage(file=r'labmoyen.png')
    IMG_labdifficile = PhotoImage(file=r'labdifficile.png')
    IMG_joueur = PhotoImage(file=r'joueurD.png')
    IMG_inventaire = PhotoImage(file=r'inventaire.png')
    IMG_pseudo = PhotoImage(file=r'pseudo.png')
    #Image objt dans l'inventaire
    IMG_IEpee = PhotoImage(file=r'IEpee.png')
    IMG_IPot = PhotoImage(file=r'potion.png')
    IMG_IAile = PhotoImage(file=r'aile.png')
    IMG_IRubis = PhotoImage(file=r'rubis.png')
    #Image etoile
    IMG_etoileP = PhotoImage(file=r'etoile.png')
    IMG_etoileV = PhotoImage(file=r'etoileVide.png')

    IMG_btnPause = PhotoImage(file=r'pause.png')
    IMG_Victoire = PhotoImage(file=r'victoirefond.png')
    if save != True and reprendre != True: #si ce n'est pas une sauvegarde on ne recreer pas un joueur
        print("crea nv joueur (pas save ni reprendre true")
        joueur1 = CreationJoueur()
        AffichageJoueur(joueur1)
    elif reprendre == True :
        print("reprendre true")
        # on ne change pas le joueur ni le lab
        AffichageJoueur(joueur1)
    elif save ==  True : #on lit le dossier de fichier
        print("save = true")
        joueur1 = Joueur("")
        SauvegardeJoueur(joueur1, "Joueur.txt")
        joueur1 = LectureJoueur(joueur1,"savejoueur.txt")
        AffichageJoueur(joueur1)

    #partie graphique affichage donnees J
    canvas.itemconfigure('text',text = "")
    canvas.create_text(650, 140, text="Trouvez la sortie et tuez le boss !\n       Choississez la direction :\n", font=police2, tag='text2',fill="white")
    canvas.create_text(310, 900, text="", font=police2, tag='choix',fill="white")
    #Info joueur
    canvas.create_image(920, 230, anchor='nw', tag='pseudo', image=IMG_pseudo)
    canvas.create_text(1100, 370, text="Joueur : " + joueur1.pseudo + "\n\nVie :\n\nScore : " + str(joueur1.score),font=police3, tag='InfoJ', fill="white")
    canvas.create_text(610, 30, text="",font=police3, tag='text3', fill="white")
    #image coeur du joueur
    canvas.create_image(1080, 350, anchor='nw', tag='vie1', image=IMG_vie1)
    canvas.create_image(1160, 350, anchor='nw', tag='vie2', image=IMG_vie1)
    canvas.create_image(1240, 350, anchor='nw', tag='vie3', image=IMG_vie1)

    canvas.create_image(430, 700, anchor='nw', tag='inventaire',image=IMG_inventaire)  # affichage barre inventaire sous le lab
    # image obj inventaire
    canvas.create_image(460, 720, anchor='nw', tag='obj1', image="")
    canvas.create_image(560, 720, anchor='nw', tag='obj2', image="")
    canvas.create_image(660, 720, anchor='nw', tag='obj3', image="")
    canvas.create_image(760, 720, anchor='nw', tag='obj4', image="")
    #etoile
    canvas.create_image(630, 370, anchor='nw', tag='et1', image="")
    canvas.create_image(690, 370, anchor='nw', tag='et2', image="")
    canvas.create_image(750, 370, anchor='nw', tag='et3', image="")
    nb=0
    while FIN_PARTIE != True : #FIN DEFINITIF DU JEU
        if save != True and reprendre != True :  # si ce n'est pas une sauvegarde on ne recreer pas un joueur
            print("pas save ni reprendre")
            lab = CreationLabyrinthe(joueur1.niveau)
            joueur1.posx = 0
            joueur1.posy = 0
        elif save == True :  # on lit le dossier de fichier
            lab = LectureLab()
        #SINON ON GARDE LE MM LAB POUR REPRENDRE

        #actualisation des positions du joueur en fonction du labyrinthe
        if joueur1.niveau == "FACILE" and save != True and reprendre != True:
            print("pas save")
            canvas.itemconfigure('text3', text="Niveau 1 :")
            canvas.itemconfigure('image', image=IMG_labFACILE)
            joueur1.imx = 428
            joueur1.imy = 240
            joueur1.inventaire.clear()
            joueur1.vie = 3
            joueur1.score = 0
            canvas.itemconfigure('lab')
        if joueur1.niveau == "MOYEN" and save != True and reprendre != True :
            print("pas save")
            joueur1 = LectureJoueur(joueur1,"Joueur.txt")
            canvas.itemconfigure('image', image=IMG_labmoyen)
            canvas.itemconfigure('text3', text="Niveau 2 :")
            joueur1.imx = 375
            joueur1.imy = 240
            joueur1.posx = 0
            joueur1.posy = 0
        if joueur1.niveau == "DIFFICILE" and save != True and reprendre != True :
            joueur1 = LectureJoueur(joueur1,"Joueur.txt")
            canvas.itemconfigure('text3', text="Niveau 3 :")
            canvas.itemconfigure('image', image=IMG_labdifficile)
            joueur1.imx = 370
            joueur1.imy = 190
            joueur1.posx = 0
            joueur1.posy = 0
        if save == True or reprendre == True :
            SauvegardeJoueur(joueur1, "Joueur.txt")
        #on ne change pas le joueur ni le lab : #on charge la pos du joueur
            if joueur1.niveau == "FACILE" :
                canvas.itemconfigure('text3', text = "Niveau 1 :")
                canvas.itemconfigure('image', image=IMG_labFACILE)
                joueur1.imx = 428 + joueur1.posy * 90
                joueur1.imy = 240 + joueur1.posx * 86
            if joueur1.niveau == "MOYEN" :
                canvas.itemconfigure('image', image=IMG_labmoyen)
                canvas.itemconfigure('text3', text="Niveau 2 :")
                joueur1.imx = 375 + joueur1.posy * 90
                joueur1.imy = 240 + joueur1.posx * 86
            if joueur1.niveau == "DIFFICILE" :
                canvas.itemconfigure('image', image=IMG_labdifficile)
                canvas.itemconfigure('text3', text="Niveau 3 :")
                joueur1.imx = 370 + joueur1.posy * 92
                joueur1.imy = 190 + joueur1.posx * 86

        print("imx =",joueur1.imx)
        print("imy =", joueur1.imy)

        btnPause = Button(game, command=lambda: Pause(joueur1, lab), image=IMG_btnPause, bd=0, height=78, width=78)
        btnPause.place(x=100, y=150)
        canvas.itemconfigure('obj1', image="")
        canvas.itemconfigure('obj2', image="")
        canvas.itemconfigure('obj3', image="")
        canvas.itemconfigure('obj4', image="")
        IMG_joueur = PhotoImage(file=r'joueurD.png')
        canvas.create_image(joueur1.imx, joueur1.imy, anchor='nw', tag='joueur', image=IMG_joueur)  # image joueur
        canvas.update()
        fin = 0 #Fin prend 0 pour lab en cours, 1 pour perdu et 2 pour victoire du lab en cours
        reprendre = False
        save = False
        #affichage du labyrinthe
        for ligne in lab :
            for chambre in ligne :
                AffichageChambre(chambre,nb)
                nb+=1
            print("\n\n\n")

        while fin != 1 and fin != 2: #tant que le joueur n'a pas perdu ou gagné
            #on actualise les données du joueur
            AffichageJoueur(joueur1)
            fin = ActionChambre(lab[joueur1.posx][joueur1.posy],joueur1) #fin recoit 1 si le j a perdu pendant l'action de la piece

            btnPause = Button(game, command=lambda : Pause(joueur1,lab), image=IMG_btnPause, bd=0, height=78, width=78)
            btnPause.place(x=100, y=150)
            canvas.itemconfigure('text2', text="Trouvez la sortie et tuez le boss !\n       Choississez la direction :\n")
            canvas.itemconfigure('InfoJ', text="Joueur : " + joueur1.pseudo + "\n\nVie :\n\nScore : " + str(joueur1.score))
            #AFFICHAGE GRAPHIQUE VIE DU PEROSO (0 1 OU 2 COUEUR)
            if joueur1.vie == 3:
                canvas.itemconfigure('vie1', image=IMG_vie1)
                canvas.itemconfigure('vie2', image=IMG_vie1)
                canvas.itemconfigure('vie3', image=IMG_vie1)
            if joueur1.vie == 2:
                canvas.itemconfigure('vie1', image=IMG_vie1)
                canvas.itemconfigure('vie2', image=IMG_vie1)
                canvas.itemconfigure('vie3', image=IMG_vie2)
            if joueur1.vie == 1:
                canvas.itemconfigure('vie1', image=IMG_vie1)
                canvas.itemconfigure('vie2', image=IMG_vie2)
                canvas.itemconfigure('vie3', image=IMG_vie2)
            if joueur1.vie == 0:
                canvas.itemconfigure('vie1', image=IMG_vie2)
                canvas.itemconfigure('vie2', image=IMG_vie2)
                canvas.itemconfigure('vie3', image=IMG_vie2)

            i = 0
            #AFFICHAGE GRAPHIQUE DE L'INVENTAIRE
            while i < len(joueur1.inventaire):
                if joueur1.inventaire[i].Nomobject == "epee":
                    canvas.itemconfigure('obj' + str(i + 1), image=IMG_IEpee)
                if joueur1.inventaire[i].Nomobject== "rubis":
                    canvas.itemconfigure('obj' + str(i + 1), image=IMG_IRubis)
                if joueur1.inventaire[i].Nomobject== "aile":
                    canvas.itemconfigure('obj' + str(i + 1), image=IMG_IAile)
                if joueur1.inventaire[i].Nomobject == "potion":
                    canvas.itemconfigure('obj' + str(i + 1), image=IMG_IPot)
                i = i + 1

            canvas.update()
            #APPUIS DES TOUCHES POUR ITEM ET DEPLACEMENT
            while lab[joueur1.posx][joueur1.posy].etat == "visitee" and fin != 1 and fin != 2 :

                #EN FCT DE LA TOUCHE QUI EST APPUYE, ON VA DANS UNE DIRECTION EN APPELANT LE SSPGRM
                if keyboard.is_pressed('up') == True :
                    IMG_joueur=Haut(joueur1,lab) #appel du sous programmes pour aller en haut
                if keyboard.is_pressed('down') == True :
                    IMG_joueur=Bas(joueur1,lab)   #appel du sous programmes pour aller en bas
                if keyboard.is_pressed('left') == True :
                    IMG_joueur=Gauche(joueur1,lab)   #appel du sous programmes pour aller en gauche
                if keyboard.is_pressed('right') == True :
                    IMG_joueur=Droite(joueur1,lab)   #appel du sous programmes pour aller en droite

                #Utilisation des objets de l'inventaire TOUCHE 1 2 3 4
                if keyboard.is_pressed('1') == True : #touche 1
                    if len(joueur1.inventaire) > 0 :
                        if joueur1.inventaire[0].Nomobject == "epee":
                            print("objet pour battre le boss")
                        if joueur1.inventaire[0].Nomobject == "rubis":
                            print("rubis")
                        if joueur1.inventaire[0].Nomobject == "aile":
                            print("aile")
                        if joueur1.inventaire[0].Nomobject == "potion": #potion permet de gagner de la vie
                            joueur1.vie += 1
                            if joueur1.vie > 3:
                                joueur1.vie = 3
                        joueur1.inventaire[0] = Object("",0)
                if keyboard.is_pressed('2') == True : #touche 2
                    if len(joueur1.inventaire) > 1 :
                        if joueur1.inventaire[1].Nomobject == "epee":
                            print("objet pour battre le boss")
                        if joueur1.inventaire[1].Nomobject == "rubis":
                            print("rubis")
                        if joueur1.inventaire[1].Nomobject == "aile":
                            print("aile")
                        if joueur1.inventaire[1].Nomobject == "potion":  # potion permet de gagner de la vie
                            print("pot")
                            joueur1.vie += 1
                            if joueur1.vie > 3:
                                joueur1.vie = 3
                        joueur1.inventaire[1] = Object("",0)
                if keyboard.is_pressed('3') == True : #touche 3
                    if len(joueur1.inventaire) > 2:
                        if joueur1.inventaire[2].Nomobject == "epee":
                            print("objet pour battre le boss")
                        if joueur1.inventaire[2].Nomobject == "rubis":
                            print("rubis")
                        if joueur1.inventaire[2].Nomobject == "aile":
                            print("aile")
                        if joueur1.inventaire[2].Nomobject == "potion":  # potion permet de gagner de la vie
                            joueur1.vie += 1
                            if joueur1.vie > 3:
                                joueur1.vie = 3
                        joueur1.inventaire[2] = Object("",0)
                if keyboard.is_pressed('4') == True : #touche 4
                    if len(joueur1.inventaire) > 3:
                        if joueur1.inventaire[3].Nomobject == "epee":
                            print("objet pour battre le boss")
                        if joueur1.inventaire[3].Nomobject == "rubis":
                            print("rubis")
                        if joueur1.inventaire[3].Nomobject == "aile":
                            print("aile")
                        if joueur1.inventaire[3].Nomobject == "potion":  # potion permet de gagner de la vie
                            joueur1.vie += 1
                            if joueur1.vie > 3:
                                joueur1.vie = 3
                        joueur1.inventaire[3] = Object("",0)

                canvas.itemconfigure('joueur', image=IMG_joueur)

        canvas.delete('joueur')
        btnPause.destroy()
        if joueur1.niveau == "FACILE" and fin == 2:
            joueur1.niveau = "MOYEN"
            SauvegardeJoueur(joueur1,"Joueur.txt")
            fin = 0
        if joueur1.niveau == "MOYEN" and fin == 2:
            joueur1.niveau = "DIFFICILE"
            SauvegardeJoueur(joueur1,"Joueur.txt")
            fin = 0
        if joueur1.niveau == "DIFFICILE" and fin == 2: #On a gagné le jeu
            print("fin du jeu")
            FIN_PARTIE = True
    canvas.delete('obj1')
    canvas.delete('obj2')
    canvas.delete('obj3')
    canvas.delete('obj4')
    canvas.delete('vie1')
    canvas.delete('vie2')
    canvas.delete('vie3')
    canvas.delete('pseudo')
    canvas.delete('inventaire')
    canvas.delete('InfoJ')
    canvas.delete('text')
    canvas.delete('text2')
    canvas.delete('text3')
    canvas.delete('text3')
    canvas.itemconfigure('image', image=IMG_Victoire)
    pourcent = joueur1.score / 1300 * 100
    print(pourcent)
    if pourcent <= 25 : #0 etoile
        canvas.itemconfigure('et1',image=IMG_etoileV)
        canvas.itemconfigure('et2', image=IMG_etoileV)
        canvas.itemconfigure('et3', image=IMG_etoileV)
    if pourcent > 25 and pourcent <= 50: #1 etoile
        canvas.itemconfigure('et1',image=IMG_etoileP)
        canvas.itemconfigure('et2', image=IMG_etoileV)
        canvas.itemconfigure('et3', image=IMG_etoileV)
    if pourcent > 50 and pourcent <= 75: #2 etoile
        canvas.itemconfigure('et1',image=IMG_etoileP)
        canvas.itemconfigure('et2', image=IMG_etoileP)
        canvas.itemconfigure('et3', image=IMG_etoileV)
    if pourcent > 75 : #3 etoile
        canvas.itemconfigure('et1',image=IMG_etoileP)
        canvas.itemconfigure('et2', image=IMG_etoileP)
        canvas.itemconfigure('et3', image=IMG_etoileP)

    canvas.create_text(700, 400, text="     "+joueur1.pseudo +"\n\n\n     "+str(int(pourcent))+"%",font=police2, tag='fin', fill="white")
    canvas.update()
    time.sleep(5)
    sys.exit()

if __name__ == '__main__':
    Menu()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
