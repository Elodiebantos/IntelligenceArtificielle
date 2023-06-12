#coding:utf-8
#Ebauche d'un jeu sympa

import tkinter
import openai
from base64 import b64decode
from tkinter import *
from PIL import ImageTk,Image 
from tkinter import messagebox

#ATTENTION cette clé est la mienne donc à consommer avec modération
openai.api_key = ""

"""
StringVar()
IntVar()
BooleanVar()
"""

###########################################################################################
## Fonctions diverses
###########################################################################################

#Utilisation d'un Observable pour connecter les valeurs
def observable(*args):
    value.set(entree.get())

def gagner(*args):
    if (var_gagne.get()==0) :
        messagebox.showinfo("Fin du jeu", "Bravo, vous avez gagné !")
    elif (var_gagne.get()==1) :
        messagebox.showinfo("Fin du jeu", "Pas de chance, vous avez perdu !")

def regles():
    regles_fenetre = tkinter.Toplevel(fenetre)
    regles_fenetre.title("Règles du jeu")
    label = tkinter.Label(regles_fenetre, text="Amusez-vous en faisant deviner à votre auditoire quel prompt vous avez écrit pour générer vos images. \n Si l'auditoire réussit à deviner l'intitulé de votre prompt, vous aurez gagné et remporterez des points ! \n Sinon, vous aurez perdu et les points reviendront à votre auditoire !")
    label.pack()
    regles_fenetre.minsize("100x100")
    regles_fenetre.maxsize("400x400")
    regles_fenetre.geometry("300x300")

    
def jouer():
    messagebox.showinfo("Début du jeu", "Le jeu va se lancer, les scores vont donc être remis à zéro")
#Les scores n'ont pas pu être implémentés par manque de temps


def nuit():
    fenetre.config(bg='#030303')
    label_Bienvenue.config(background='#030303', foreground='#FFFFFF')
    cadreprincipal.config(background='#030303', foreground='#FFFFFF')
    cadrebas.config(background='#030303')
    message_prompt.config(background='#030303', foreground='#FFFFFF')
    message_prompt2.config(background='#030303', foreground='#FFFFFF')
    label_gagne.config(background='#030303', foreground='#FFFFFF')
    check_valide.config(background='#030303', foreground='#FFFFFF')
    check_nonvalide.config(background='#030303', foreground='#FFFFFF')
    message_intermediaire.config(background='#030303', foreground='#FFFFFF')

    
def jour():
    fenetre.config(bg='#FFFFFF')
    label_Bienvenue.config(background='#FFFFFF', foreground='#030303')
    cadreprincipal.config(background='#FFFFFF', foreground='#030303')
    cadrebas.config(background='#FFFFFF')
    message_prompt.config(background='#FFFFFF', foreground='#030303')
    message_prompt2.config(background='#FFFFFF', foreground='#030303')
    label_gagne.config(background='#FFFFFF', foreground='#030303')
    check_valide.config(background='#FFFFFF', foreground='#030303')
    check_nonvalide.config(background='#FFFFFF', foreground='#030303')
    message_intermediaire.config(background='#FFFFFF', foreground='#030303')
    

#Permet de générer des exemples d'images avant de générer les vraies images afin de "chauffer la salle"
def recupere_clair(): 
    image = entree.get()
    list = []
    print(image)
    fenetre_image = tkinter.Toplevel(fenetre)
    response = openai.Image.create(
        prompt=image,
        n=1,
        size = "256x256",
        response_format="b64_json",
    )
    for index, image_dict in enumerate(response["data"]):

        # Pour chaque image, on décode le contenu de l'image
        image_data = b64decode(image_dict["b64_json"])
        image_file = f"test-image-{index}.png"
        # On sauvegarde l'image dans un fichier
        # L'utilisation de "with" permet de fermer le fichier automatiquement
        with open(image_file, mode="wb") as png:
            image_file = f"test-image-{index}.png"
            print(image_file)
            png.write(image_data)
            label = tkinter.Label(fenetre_image, text="image_simple")
            label.image = tkinter.PhotoImage(file = image_file)
            label.configure(image=label.image)
            label.grid()

#Vrai jeu 
def recupere_cache(): 
    image = entree_secrete.get()
    print(image)
    fenetre_image = tkinter.Toplevel(fenetre)
    response = openai.Image.create(
        prompt=image,
        n=1,
        size = "256x256",
        response_format="b64_json",
    )
    for index, image_dict in enumerate(response["data"]):

        # Pour chaque image, on décode le contenu de l'image
        image_data = b64decode(image_dict["b64_json"])
        image_file = f"test-image-{index}.png"
        # On sauvegarde l'image dans un fichier
        # L'utilisation de "with" permet de fermer le fichier automatiquement
        with open(image_file, mode="wb") as png:
            image_file = f"test-image-{index}.png"
            print(image_file)
            png.write(image_data)
            label = tkinter.Label(fenetre_image, text="image_simple")
            label.image = tkinter.PhotoImage(file = image_file)
            label.configure(image=label.image)
            label.grid()

###########################################################################################
## Organisation graphique
###########################################################################################

#Configuration de la fenêtre
fenetre = Tk()
cadreprincipal = tkinter.LabelFrame(fenetre, text="Bienvenue", width=500, height=300)
cadreprincipal.grid(row=0, column=2, columnspan=3, padx=15, pady=15)

cadrebas = tkinter.LabelFrame(fenetre, text="A propos")
cadrebas.grid(row=55, column=2, columnspan=15)
###########################################################################################
## Fenêtre tkinter
###########################################################################################

fenetre.title("Site de génération d'images")
fenetre.minsize(450,500)
fenetre.maxsize(2000,2000)
fenetre.geometry("450x500")

label_Bienvenue = tkinter.Label(cadreprincipal, text="Faîtes deviner à vos amis quelle image vous avez générée dans le prompt.")
label_Bienvenue.grid(padx=15, pady=10, row = 1, column=2)

# changement_mode_jeu = tkinter.Listbox(fenetre)
# changement_mode_jeu.insert(1, "Choisissez une image à générer")
# changement_mode_jeu.insert(2, "Faites deviner ce que vous avez tapé")
# changement_mode_jeu.grid()

message_prompt = tkinter.Label(fenetre, text="Choisissez une image à générer en clair")
message_prompt.grid(row=1, column=2)
#AJOUTER UN RADIOBUTTON
#Créer un input pour demander un prompt
value = tkinter.StringVar() 
value.trace("w", observable)
entree = Entry(fenetre, textvariable=value, width=30, exportselection=0)
entree.grid(row=3, column=2)
prompt = ""

#Créer un bouton pour valider
bouton_clair = Button(fenetre, text="Valider", command=recupere_clair)
bouton_clair.grid(row=5, column= 2, padx=15, pady=15)

message_intermediaire = tkinter.Label(fenetre, text="ou...")
message_intermediaire.grid(row=6, column=2, padx=5, pady=5)


#Création d'un prompt avec les caractères cachés
message_prompt2 = tkinter.Label(fenetre, text="Faites deviner ce que vous avez tapé dans le prompt !")
message_prompt2.grid(padx=15, pady=12, row=7, column=2)
secret_value = tkinter.StringVar() 
entree_secrete = Entry(fenetre, textvariable=secret_value, width=30, show='*', exportselection=0)
entree_secrete.grid(row=8, column=2)

#Créer un bouton pour valider
bouton_clair = Button(fenetre, text="Valider", command=recupere_cache)
bouton_clair.grid(row=9, column= 2, padx=15, pady=15)

# Valider si l'auditoire a trouvé la bonne réponse ou non
var_gagne = tkinter.IntVar()
var_gagne.trace("w", gagner)

label_gagne = tkinter.Label(fenetre, text="L'auditoire a-t-il trouvé l'intitulé de votre prompt ?")
label_gagne.grid(row=10, column=2)
check_valide = tkinter.Radiobutton(fenetre, text="Oui", value=0, variable=var_gagne)
check_valide.grid(row=11, column=2)
check_nonvalide = tkinter.Radiobutton(fenetre, text="Non", value=1, variable=var_gagne)
check_nonvalide.grid(row=12, column=2)

#Créer un message d'erreur ou d'information
# A mettre dans une fonction
# info_fin_jeu = messagebox.showinfo("Fin du jeu", "Le temps est écoulé !")
# info_fin_jeu = messagebox.showwarning("", "")
# info_fin_jeu = messagebox.showerror("", "")
# info_fin_jeu = messagebox.askquestion("", "")
# info_fin_jeu = messagebox.askretrycancel("", "")

#Permettre de quitter le jeu
bouton=Button(fenetre, text="Fermer", width=25, command=fenetre.quit)
bouton.grid(row=13, column= 2, padx=15, pady=15)

menuprincipal = tkinter.Menu(fenetre)

menu1 = tkinter.Menu(menuprincipal, tearoff=0)
menu1.add_command(label="Règles", command=regles)
menu1.add_command(label="Jouer", command=jouer)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menuprincipal.add_cascade(label="Jeu", menu=menu1)

menu2 = Menu(menuprincipal, tearoff=0)
menu2.add_command(label="Sombre", command=nuit)
menu2.add_command(label="Clair", command=jour)
menuprincipal.add_cascade(label="Modes de jeu", menu=menu2)

# dimensions = tkinter.StringVar()
# dimensions.trace("rw", choix_dimensions)
# menu3 = Menu(menuprincipal, tearoff=0)
# taillepetite = menu3.add_command(label="256x256", command=choix_dimensions)
# taillemoyenne = menu3.add_command(label="512x512", command=choix_dimensions)
# taillegrande = menu3.add_command(label="1024x1024", command=choix_dimensions)
# menuprincipal.add_cascade(label="Taille d'affichage", menu=menu3)

# #Pour faire tourner la fenêtre Tkinter en continu
fenetre.config(menu=menuprincipal)
fenetre.mainloop()
