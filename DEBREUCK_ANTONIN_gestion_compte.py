# -*- coding: utf-8 -*-
"""
Account management

Created on Thuesday April 27 2023 at 15:51
"Finished" on Thuesday April 28 2023 at 23:59

Authors : 
Antonin De Breuck (BC info)
Website : https://antodb.be

Repository : https://github.com/AntoDB/gestion-compte
"""

#=========================================================================================================#

                        #-------------------- Modules imported --------------------#

#=========================================================================================================#

from tkinter import *
import datetime
import os
import platform
import json
import re # For Regex

#=========================================================================================================#

            #-------------------- Mofiable/Changeable variables | Options --------------------#

#=========================================================================================================#
            
#================================================== Parameters ==================================================#

frame_width = 1000
ratio = 16/9

version = '1.0.0'

# =============== Colors =============== #
bg_frame_color = 'black'
bg_button_color = 'gray11'

label_color = '#FFF'
label_button_color = '#FFF'

label_CorrectAswer_color = '#33FF33'
label_WrongAswer_color = '#F00'

label_error_color = '#CC0000'

# =============== Labels Displays =============== #

label_info_msg = {
    "loginSuccessfully" : "Vous êtes bien connecté !",
    "successfullyNewAccount" : "Compte créé !",
    "pswSuccessfullyUpdated" : "Votre mot de pase est bien mis à jour !",
    "accountSuccessfullyDelete" : "Votre compte est bien supprimé !",
    "connnectionRefused" : "Connexion refusée !",

    "noUsers" : "Il y a aucun utilisateur dans notre base de données actuellement.",
    "noUser" : "Cet utilisateur n'existe pas !",
    "userAllreadyExist" : "Cet utilisateur existe déjà !",
    "wrongPassword" : "Le mot de passe entré, n'est pas bon !",
    "emptyData" : "Merci de remplir tous les champs !\nIl manque votre pseudo et/ou votre mot de passe.",
    "sameUserPsw" : "Pour des raison de sécurité, nous n'autorisons pas un mot de passe identique à l'utilisateur.",
    "tooEasyPsw" : "Mot de passe trop connu et pas assez robuste.",
    "tooPoorPsw" : "Mot de passe pas assez robuste !\nIl doit contenir au moins 8 caractères dont 1 spécial, une minuscule et une majuscule.",
    "toManyTry" : "Vous avez essayer trop de fois des mots de passe incorrects !\nNous soupçonnons une tentative d'attaque brute force.",
    "illegalCharacter" : "Caractère non autorisée !\nNous soupçonnons une tentative d'injection de code.",

    "notSameNewPsw" : "Le nouveau mot de passe et la confirmation ne correspondent pas !"
}

# =============== Password =============== #

maxTryPsw = 3
regexPswPattern = r'[^\w\s]'

# =============== Files =============== #

cwd = str(os.getcwd())

files_folder = "/Documents/"

logs_folder = "/Documents/logs/"
saves_folder = "/Documents/"

logs_file = "logs"
data_file = "users"

#================================================== Don't touch ==================================================#

date = ""
users = {}
currentTryPsw = 0

#=========================================================================================================#

                        #-------------------- Homemade Function/Class --------------------#

#=========================================================================================================#

#================================================== Operations ==================================================#

def logs(info):
    """
    Description : S'assure la création des logs pour toutes les informations.
    Les logs contiendront toutes les informations qui pourraient aider à débloquer le jeu
    
    Input :
        info : string -> Message à mettre dans les logs
    Output : /
    """
    global date
    info = str(info)
    datenow = datetime.datetime.now()

    # To avoid 1 file per logs
    if date == "":
        date = f"{datenow.day}-{datenow.month}-{datenow.year}_{datenow.hour}-{datenow.minute}-{datenow.second}"

    if not os.path.exists(cwd + logs_folder + logs_file + " " + date + ".txt"):
        if not os.path.exists(cwd + files_folder):
            os.mkdir(cwd + files_folder)
        if not os.path.exists(cwd + logs_folder):
            os.mkdir(cwd + logs_folder)
            
    with open(cwd + logs_folder + logs_file + "_" + date + ".txt", 'a') as f:
        f.write('[' + str(datenow) + '] ' + info + '\n')

    print('[' + str(datenow) + '] ' + info)

# ===== JSON ===== #
def loadJson():
    """
    Description : Lit le fichier JSON pour récupérer tous les comptes des utilisateurs.
    
    Input : /
    Output :
        users : dict -> Dictionnaire du fichier JSON
    """
    with open(cwd + files_folder + data_file + ".json") as jf: # jf = Json file
        users = json.load(jf)
        return users

def createJson(users : dict):
    """
    Description : Écrit dans le fichier JSON les comptes des utilisateurs.
    
    Input :
        users : dict -> Dictionnaire à mettre dans le fichier JSON
    Output : /
    """
    with open(cwd + files_folder + data_file + ".json", "w") as fp:
        json.dump(users, fp)
    logs("[INFO] Crée ou écrit un fichier JSON avec les utilisateurs")

# ===== Users treatment ===== #
def userExist(logins: dict, username: str):
    """
    Description : Renvoie un booléen en fonction de si l'utilsateur existe
    
    Input :
        logins : dict -> Dictionnaire contenant les utilisateurs et leurs mots de passe
        username : str -> Le nom d'utilisateur
    Output :
        bool -> True si l'utilisateur existe dans la base de données, False dans le cas contraire
    """
    if username in logins.keys() :
        return True
    else :
        return False
    
def pswCorrect(logins: dict, username: str, password: str):
    """
    Description : Renvoie un booléen en fonction du mot de passe est bon pour l'utilsateur
    
    Input :
        logins : dict -> Dictionnaire contenant les utilisateurs et leurs mots de passe
        username : str -> Le nom d'utilisateur
        password : str -> Le mot de passe de l'utilisateur
    Output :
        bool -> True si l'utilisateur et le mot de passe correspond, False dans le cas contraire
    """
    if username in logins.keys() : # Sécurité
        if logins[username] == password :
            return True
        else:
            return False
        
def updateUser(logins: dict, username: str, password: str):
    """
    Description : Renvoie le dictionnaire des comptes mis à jour
    
    Input :
        logins : dict -> Dictionnaire contenant les utilisateurs et leurs mots de passe
        username : str -> Le nom d'utilisateur
        password : str -> Le mot de passe de l'utilisateur
    Output :
        logins : dict -> Dictionnaire contenant les utilisateurs et leurs mots de passe mis à jour
    """
    logins[username] = password
    createJson(logins)
    logs("[INFO] Utilisateur bien mis à jour !")
    return logins

def removeUser(logins: dict, username: str):
    """
    Description : Renvoie le dictionnaire des comptes mis à jour
    
    Input :
        logins : dict -> Dictionnaire contenant les utilisateurs et leurs mots de passe
        username : str -> Le nom d'utilisateur
    Output :
        logins : dict -> Dictionnaire contenant les utilisateurs et leurs mots de passe mis à jour
    """
    if username in logins.keys() : # Sécurité
        logins.pop(username, None)
        createJson(logins)
        logs("[INFO] Utilisateur supprimé !")
    return logins

# ===== Input & Psw treatment ===== #
def checkNoInjection(input: str):
    """
    Description : Renvoie un booléen en fonction de si le texte ne contient pas des caractères suspects
    
    Input :
        input : str -> La chaine de caractère à analyser
    Output :
        bool -> True si pas de caractères spéciaux sensible, False dans le cas contraire
    """
    if "#" in input or "\"" in input :
        logs("[WARN] Soupçon de tentative d'injection de code.")
        return False
    return True

def checkNoEasyPsw(input: str):
    """
    Description : Renvoie un booléen en fonction de si le texte n'est pas trop simple
    
    Input :
        input : str -> La chaine de caractère à analyser
    Output :
        bool -> True si le mot de passe n'est pas trop simple, False dans le cas contraire
    """
    if "1234" in input or "&é\"'" in input or "abc" in input.lower() or "azerty" in input.lower() or "qwerty" in input.lower() :
        return False
    return True

def checkNoPoorPsw(input: str):
    """
    Description : Renvoie un booléen en fonction de si le texte n'est pas trop pauvre en robustesse
    
    Input :
        input : str -> La chaine de caractère à analyser
    Output :
        bool -> True si le mot de passe n'est pas trop simple, False dans le cas contraire
    """
    if len(input) >= 8 and input != input.lower() and input != input.upper() and bool(re.search(regexPswPattern, input)) : # Dernier : Renvoie true si le regex est juste (s'il y a un caractère spécial de trouvé dans le str)
        return True
    return False

#================================================== Interfaces ==================================================#

class Interface(Tk):
    def __init__(self):
        """
        Description : Initialisation de tous les "écrans"
        
        Input :
            self
        Output : /
        """
        Tk.__init__(self)   
        """
        Description : Création du menu de lancement du jeu.
        Contient les catégories : Se connecter, Création de compte, Changer mot de passe, Supprimer un compte, Affichage des pseudos existants.
        
        Input : /
        Output : /
        """
        # MH = Menu Home
        self.frame_MH = Frame(self)
        self.canvas_mBG = Canvas(self.frame_MH, bg=bg_frame_color, width=frame_width, height=frame_width/ratio, highlightthickness = 0)
    
        self.label_MH_Title = Label(self.frame_MH, bg=bg_frame_color, fg=label_color, text="Gestionnaire de comptes", font =("Helvetica", 25))

        self.buttonMH1 = Button(self.frame_MH, bg=bg_button_color, fg=label_button_color, text="Se connecter", width = 25, height = 3, font =("Helvetica", 15), command=lambda: self.modifyScreenAfterLogin("login"))
        self.buttonMH2 = Button(self.frame_MH, bg=bg_button_color, fg=label_button_color, text="Créer un compte", width = 25, height = 3, font =("Helvetica", 15), command=lambda: self.screenChange(self.frame_Create))  
        self.buttonMH3 = Button(self.frame_MH, bg=bg_button_color, fg=label_button_color, text="Changer votre mot de passe", width = 25, height = 2, font =("Helvetica", 15), command=lambda: self.screenChange(self.frame_PSWMod))
        self.buttonMH4 = Button(self.frame_MH, bg=bg_button_color, fg=label_button_color, text="Supprimer votre compte", width = 25, height = 2, font =("Helvetica", 15), command=lambda: self.modifyScreenAfterLogin("delPsw"))
        self.buttonMH5 = Button(self.frame_MH, bg=bg_button_color, fg=label_button_color, text="Afficher les utilisateurs", width = 25, height = 2, font =("Helvetica", 15), command=lambda: self.modifyScreenAfterLogin("displayUsers"))

        Label(self.frame_MH, bg=bg_frame_color, fg=label_color, text="Python V : " + str(platform.python_version())).place(x = 10 , y = frame_width/ratio-65)
        Label(self.frame_MH, bg=bg_frame_color, fg=label_color, text="App V : " + version).place(x = 10 , y = frame_width/ratio-45)
        Button(self.frame_MH, bg=bg_button_color, fg=label_button_color, text="Quitter", width = 20, height = 2, font =("Helvetica", 15), command=self.destroy).grid(row = 5, column = 3)

        self.canvas_mBG.grid(row = 1, column = 1, rowspan = 5, columnspan = 5)
                                
        self.label_MH_Title.grid(row = 1, column = 1, columnspan = 5)

        self.buttonMH1.grid(row = 2, column = 2)
        self.buttonMH2.grid(row = 2, column = 4)
        self.buttonMH3.grid(row = 4, column = 2)
        self.buttonMH4.grid(row = 4, column = 3)
        self.buttonMH5.grid(row = 4, column = 4)

        logs("[INFO] Menu de démarrage fait")

        # Affichage premier écran & Prend quel écran c'est & Met le titre
            
        self.mesAutresFrames = {}
        self.mesAutresFrames["whichMenu"] = self.frame_MH
        self.mesAutresFrames["whichMenu"].grid()

        # =============== Création des autres fenêtres =============== #

        """
        Description : Création de l'écran de connexion
        
        Input : /
        Output : /
        """
        # Con = Connexion
        self.frame_Con = Frame(self)
        self.canvas_Con = Canvas(self.frame_Con, bg=bg_frame_color, width=frame_width, height=frame_width/ratio, highlightthickness = 0)
    
        Label(self.frame_Con, bg=bg_frame_color, fg=label_color, text="Se connecter", font =("Helvetica", 25)).grid(row = 1, column = 1)

        Label(self.frame_Con, bg=bg_frame_color, fg=label_color, text="Pseudo", font =("Helvetica", 25)).place(x=frame_width/2-220, y=frame_width/ratio/5*1.2)
        Label(self.frame_Con, bg=bg_frame_color, fg=label_color, text="Mot de passe", font =("Helvetica", 25)).place(x=frame_width/2-300, y=frame_width/ratio/5*2)

        self.entryUsr_Con = Entry(self.frame_Con, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))
        self.entryPsw_Con = Entry(self.frame_Con, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))

        self.buttonCon1 = Button(self.frame_Con, bg=bg_button_color, fg=label_button_color, text="Se connecter", width = 20, height = 2, font =("Helvetica", 15), command=lambda: self.connection("login"))
        self.buttonCon2 = Button(self.frame_Con, bg=bg_button_color, fg=label_button_color, text="Retour à l'accueil", width = 15, height = 2, font =("Helvetica", 15), command=lambda: self.screenChange(self.frame_MH))

        self.canvas_Con.grid(row = 1, column = 1, rowspan = 5)

        self.entryUsr_Con.grid(row = 2, column = 1)
        self.entryPsw_Con.grid(row = 3, column = 1)

        self.buttonCon1.grid(row = 4, column = 1)
        self.buttonCon2.grid(row = 5, column = 1)

        logs("[INFO] Menu de connexion fait")

        """
        Description : Création de l'écran de création de compte
        
        Input : /
        Output : /
        """
        # Create = Création (de compte)
        self.frame_Create = Frame(self)
        self.canvas_Create = Canvas(self.frame_Create, bg=bg_frame_color, width=frame_width, height=frame_width/ratio, highlightthickness = 0)
    
        Label(self.frame_Create, bg=bg_frame_color, fg=label_color, text="Créer votre compte", font =("Helvetica", 25)).grid(row = 1, column = 1)

        Label(self.frame_Create, bg=bg_frame_color, fg=label_color, text="Pseudo", font =("Helvetica", 25)).place(x=frame_width/2-220, y=frame_width/ratio/6*1.2)
        Label(self.frame_Create, bg=bg_frame_color, fg=label_color, text="Mot de passe", font =("Helvetica", 25)).place(x=frame_width/2-300, y=frame_width/ratio/6*2)
        Label(self.frame_Create, bg=bg_frame_color, fg=label_color, text="Confirmation du nouveau\nmot de passe", font =("Helvetica", 18)).place(x=frame_width/2-380, y=frame_width/ratio/6*2.8)

        self.entryUsr_Create = Entry(self.frame_Create, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))
        self.entryPsw_Create = Entry(self.frame_Create, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))
        self.entryConfPsw_Create = Entry(self.frame_Create, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))

        self.buttonCreate1 = Button(self.frame_Create, bg=bg_button_color, fg=label_button_color, text="Créer le compte", width = 15, height = 2, font =("Helvetica", 15), command=self.createAccount)
        self.buttonCreate2 = Button(self.frame_Create, bg=bg_button_color, fg=label_button_color, text="Retour à l'accueil", width = 15, height = 2, font =("Helvetica", 15), command=lambda: self.screenChange(self.frame_MH))

        self.canvas_Create.grid(row = 1, column = 1, rowspan = 6)

        self.entryUsr_Create.grid(row = 2, column = 1)
        self.entryPsw_Create.grid(row = 3, column = 1)
        self.entryConfPsw_Create.grid(row = 4, column = 1)

        self.buttonCreate1.grid(row = 5, column = 1)
        self.buttonCreate2.grid(row = 6, column = 1)

        logs("[INFO] Menu de création de compte fait")

        """
        Description : Création de l'écran d'information de connexion/modification/suppression
        
        Input : /
        Output : /
        """
        # IC = Info Connexion
        self.frame_IC = Frame(self)
        Canvas(self.frame_IC, bg=bg_frame_color, width=frame_width, height=frame_width/ratio, highlightthickness = 0).grid(row = 1, column = 1, rowspan = 2)
    
        self.label_IC = Label(self.frame_IC, bg=bg_frame_color, fg=label_color, text="Si vous lisez ceci, c'est une erreur.\nPrévenez le créateur en expliquant votre manipulation.", font =("Helvetica", 18), height=2)
        self.button_IC = Button(self.frame_IC, bg=bg_button_color, fg=label_button_color, text="Retour à l'accueil", width = 20, height = 2, font =("Helvetica", 15), command=lambda: self.screenChange(self.frame_MH))

        self.label_IC.grid(row = 1, column = 1)
        self.button_IC.grid(row = 2, column = 1)

        logs("[INFO] Écran d'affichage message de connexion/modification/suppression.")

        """
        Description : Création de l'écran de modification de mot de passe
        
        Input : /
        Output : /
        """
        # PSWMod = Password Modification = Modification de mot de passe
        self.frame_PSWMod = Frame(self)
        self.canvas_PSWMod = Canvas(self.frame_PSWMod, bg=bg_frame_color, width=frame_width, height=frame_width/ratio, highlightthickness = 0)
    
        Label(self.frame_PSWMod, bg=bg_frame_color, fg=label_color, text="Modifiez votre mot de passe", font =("Helvetica", 25)).grid(row = 1, column = 1)

        Label(self.frame_PSWMod, bg=bg_frame_color, fg=label_color, text="Pseudo", font =("Helvetica", 18)).place(x=frame_width/2-220, y=frame_width/ratio/8*1.2)
        Label(self.frame_PSWMod, bg=bg_frame_color, fg=label_color, text="Mot de passe\nactuel", font =("Helvetica", 18)).place(x=frame_width/2-280, y=frame_width/ratio/8*2)

        self.entryUsr_PSWMod = Entry(self.frame_PSWMod, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))
        self.entryPsw_PSWMod = Entry(self.frame_PSWMod, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))

        Label(self.frame_PSWMod, bg=bg_frame_color, fg=label_color, text="Nouveau\nmot de passe", font =("Helvetica", 18)).place(x=frame_width/2-280, y=frame_width/ratio/8*3.2)
        Label(self.frame_PSWMod, bg=bg_frame_color, fg=label_color, text="Confirmation du nouveau\nmot de passe", font =("Helvetica", 18)).place(x=frame_width/2-400, y=frame_width/ratio/8*4.2)

        self.entryNewPsw_PSWMod = Entry(self.frame_PSWMod, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))
        self.entryConfNewPsw_PSWMod = Entry(self.frame_PSWMod, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))

        self.buttonPSWMod1 = Button(self.frame_PSWMod, bg=bg_button_color, fg=label_button_color, text="Modifier le mot de passe", width = 20, height = 2, font =("Helvetica", 15), command=self.modifyAccountPsw)
        self.buttonPSWMod2 = Button(self.frame_PSWMod, bg=bg_button_color, fg=label_button_color, text="Retour à l'accueil", width = 15, height = 2, font =("Helvetica", 15), command=lambda: self.screenChange(self.frame_MH))

        self.canvas_PSWMod.grid(row = 1, column = 1, rowspan = 8)

        self.entryUsr_PSWMod.grid(row = 2, column = 1)
        self.entryPsw_PSWMod.grid(row = 3, column = 1)
        self.entryNewPsw_PSWMod.grid(row = 5, column = 1)
        self.entryConfNewPsw_PSWMod.grid(row = 6, column = 1)

        self.buttonPSWMod1.grid(row = 7, column = 1)
        self.buttonPSWMod2.grid(row = 8, column = 1)

        logs("[INFO] Menu de modification de mot de passe fait")

        """
        Description : Création du menu de statistique.
        Contient les catégories : Nom/Pseudo, Points, Nombres de parties (Dont réussie, Dont ratée), Nombres de pions placés, Temps joué
        
        Input : /
        Output : /
        """
        # DA = Display Account = Affiche compte
        self.frame_DA = Frame(self, bg=bg_frame_color)
        self.canvas_DA = Canvas(self.frame_DA, bg=bg_frame_color, width=frame_width, height=frame_width/ratio, highlightthickness = 0)
    
        Label(self.frame_DA, bg=bg_frame_color, fg=label_color, text="Comptes enregistrés", font = ("Helvetica", 25)).grid(row = 1, column = 1, columnspan= 2)

        Label(self.frame_DA, bg=bg_frame_color, fg=label_error_color, text="⚠ Nous considérons que tous les comptes sont des administrateurs.\nEn réalité, il faudrait chiffrer tous les mots de passe.\n\nEn effet afficher les mots de passe en clair pour tout les utilsateurs\nrelève d'une énorme faille de sécuritée.", font = ("Helvetica", 15)).grid(row = 2, column = 1, columnspan= 2)
    
        Label(self.frame_DA, bg=bg_frame_color, fg=label_color, text="Noms/Pseudos", font = ("Helvetica", 25)).grid(row = 3, column = 1)
        Label(self.frame_DA, bg=bg_frame_color, fg=label_color, text="Mots de passe", font = ("Helvetica", 25)).grid(row = 3, column = 2)
        
        self.text_DA = Text(self.frame_DA, font = ("Helvetica", 15), height=10)
        self.text_DA.grid(row = 4, column = 1, columnspan=2, sticky=EW)

        # create a scrollbar widget and set its command to the text widget
        scrollbar = Scrollbar(self.frame_DA, orient='vertical', command=self.text_DA.yview)
        scrollbar.grid(row=4, column=3, sticky=NS)

        #  communicate back to the scrollbar
        self.text_DA['yscrollcommand'] = scrollbar.set
        
        Button(self.frame_DA, bg=bg_button_color, fg=label_button_color, text="Retour à l'accueil", width = 15, height = 2, font =("Helvetica", 15), command=lambda: self.screenChange(self.frame_MH)).grid(row = 5, column = 1, columnspan= 2)

        self.canvas_DA.grid(row = 1, column = 1, rowspan=5, columnspan= 2)

        logs("[INFO] Écran d'affichage de comptes fait")

    # ===== Interface treatment ===== #

    def screenChange(self, arg : object):
        """
        Description : Affiche le menu demandé.
        Actions : Enlève le précédent écran, affiche celui demandé, set une variable sur cette écran
        
        Input :
            self
            arg = object -> Fenêtre à placer
        Output : /
        """
        #print(dir(arg)) # Possibilité d'opération sur l'object
        logs("[INFO] Changement fenêtre : " + str(self.mesAutresFrames["whichMenu"]) + " > " + str(arg))
        self.mesAutresFrames["whichMenu"].grid_remove()
        self.mesAutresFrames["whichMenu"] = arg
        self.mesAutresFrames["whichMenu"].grid()
    
    def modifyScreenAfterLogin(self, operation : str):
        """
        Description : Change le bouton de connexion Affiche le menu demandé.
        Actions : Enlève le précédent écran, affiche celui demandé, set une variable sur cette écran
        
        Input :
            self
            frame : object -> Fenêtre à placer
            operation : str -> Quel opération à faire et quelle frame a afficher si la connexion est réussie
        Output : /
        """
        if operation == "displayUsers":
            self.buttonCon1.configure(text= "Afficher les comptes", command= lambda: self.connection(operation))
        elif operation == "delPsw":
            self.buttonCon1.configure(text= "Suprimmer le compte", command= lambda: self.connection(operation))
        else:
            self.buttonCon1.configure(text= "Se connecter", command= lambda: self.connection(operation))
        self.entryUsr_Con.delete(0, 'end')
        self.entryPsw_Con.delete(0, 'end')
        self.screenChange(self.frame_Con)

    def connection(self, frame : str):
        """
        Description : Essaye de connecter l'utilsateur en fonction de s'il est dans la db et s'il a entré des bonne données
        
        Input :
            self
            frame : str -> Quel opération à faire et quelle frame a afficher si la connexion est réussie
        Output : /
        """ 
        users = loadJson() # Must update the variable in the code if account where created ou deleted

        username = self.entryUsr_Con.get()
        password = self.entryPsw_Con.get()
        if username != "" and password != "":
            if checkNoInjection(username) and checkNoInjection(password):
                if userExist(users, username):
                    if pswCorrect(users, username, password):
                        if frame == "displayUsers" :
                            self.label_IC.configure(text = label_info_msg["pswSuccessfullyUpdated"] + f"\nBonjour {username} !", fg = label_CorrectAswer_color)
                            self.button_IC.configure(text= "Retour à l'accueil", command= lambda: self.screenChange(self.frame_MH))
                            
                            #print(users)
                            #print(users.items())
                            #(list(enumerate(users.items())))
                            self.text_DA.configure(state=NORMAL)
                            self.text_DA.delete('1.0', END)
                            for index, (key, values) in enumerate(users.items()):
                                self.text_DA.insert(f'{index+1}.0', f'{key}\t\t')
                                self.text_DA.insert(f'{index+1}.100', f'{values}\n')
                                print(f"index : {index+1}, key : {key}, values : {values}")
                            self.text_DA.configure(state=DISABLED)

                            self.screenChange(self.frame_DA)
                        elif frame == "delPsw" :
                            self.label_IC.configure(text = label_info_msg["accountSuccessfullyDelete"], fg = label_CorrectAswer_color)
                            self.button_IC.configure(text= "Retour à l'accueil", command= lambda: self.screenChange(self.frame_MH))
                            removeUser(users, username)

                            self.screenChange(self.frame_IC)
                        else :
                            self.label_IC.configure(text = label_info_msg["loginSuccessfully"] + f"\nBonjour {username} !", fg = label_CorrectAswer_color)
                            self.button_IC.configure(text= "Retour à l'accueil", command= lambda: self.screenChange(self.frame_MH))
                            self.screenChange(self.frame_IC)

                    else: # Le mmot de passe est incorrect
                        global currentTryPsw
                        currentTryPsw += 1
                        if currentTryPsw >= maxTryPsw:
                            self.label_IC.configure(text = label_info_msg["toManyTry"], fg = label_WrongAswer_color)
                            self.button_IC.configure(text= "Retour à l'accueil", command= lambda: self.screenChange(self.frame_MH))
                            self.screenChange(self.frame_IC)

                            currentTryPsw = 0
                            self.entryUsr_Con.delete(0, 'end')
                        else:
                            self.label_IC.configure(text = label_info_msg["wrongPassword"] + f"\nIl vous reste {maxTryPsw - currentTryPsw} tentative(s)", fg = label_WrongAswer_color)
                            self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_Con))
                            self.screenChange(self.frame_IC)
                        self.entryPsw_Con.delete(0, 'end')

                else: # L'user n'existe pas
                    self.label_IC.configure(text = label_info_msg["noUser"], fg = label_WrongAswer_color)
                    self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_Con))
                    self.screenChange(self.frame_IC)
            else: # Illegal character
                self.label_IC.configure(text = label_info_msg["illegalCharacter"], fg = label_WrongAswer_color)
                self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_Con))
                self.screenChange(self.frame_IC)
        else: # Username or password empty
            self.label_IC.configure(text = label_info_msg["emptyData"], fg = label_WrongAswer_color)
            self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_Con))
            self.screenChange(self.frame_IC)
    
    def createAccount(self):
        """
        Description : Essaye de connecter l'utilsateur en fonction de s'il est dans la db et s'il a entré des bonne données
        
        Input :
            self
        Output : /
        """
        username = self.entryUsr_Create.get()
        password = self.entryPsw_Create.get()
        confPsw = self.entryConfPsw_Create.get()
        if username != "" and password != "" and confPsw != "" :
            if checkNoInjection(username) and checkNoInjection(password) and checkNoInjection(confPsw):
                if username != password:
                    if userExist(users, username): # L'user est déjà existant
                        self.label_IC.configure(text = label_info_msg["userAllreadyExist"], fg = label_WrongAswer_color)
                        self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_Create))
                        self.screenChange(self.frame_IC)
                    else: # L'user n'existe pas
                        if password == confPsw:
                            if checkNoEasyPsw(password): # Le mot de passe n'est pas trop simple (1234, salut, ...)
                                if checkNoPoorPsw(password): # Le mot de passe est assez robuste
                                    updateUser(users, username, password)

                                    self.label_IC.configure(text = label_info_msg["successfullyNewAccount"], fg = label_CorrectAswer_color)
                                    self.button_IC.configure(text= "Retour à l'accueil", command= lambda: self.screenChange(self.frame_MH))
                                    self.screenChange(self.frame_IC)

                                    self.entryUsr_Create.delete(0, 'end')
                                    self.entryPsw_Create.delete(0, 'end')
                                    self.entryConfPsw_Create.delete(0, 'end')

                                else: # Password too poor
                                    self.label_IC.configure(text = label_info_msg["tooPoorPsw"], fg = label_WrongAswer_color)
                                    self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_Create))
                                    self.screenChange(self.frame_IC)
                            else: # Password too easy
                                self.label_IC.configure(text = label_info_msg["tooEasyPsw"], fg = label_WrongAswer_color)
                                self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_Create))
                                self.screenChange(self.frame_IC)
                        else: # New psw and confirmation of new psw not the same
                            self.label_IC.configure(text = label_info_msg["notSameNewPsw"], fg = label_WrongAswer_color)
                            self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_Create))
                            self.screenChange(self.frame_IC)
                else: # Username et password identique
                    self.label_IC.configure(text = label_info_msg["sameUserPsw"], fg = label_WrongAswer_color)
                    self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_Create))
                    self.screenChange(self.frame_IC)
            else: # Illegal character
                self.label_IC.configure(text = label_info_msg["illegalCharacter"], fg = label_WrongAswer_color)
                self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_Create))
                self.screenChange(self.frame_IC)
        else: # Username or password empty
            self.label_IC.configure(text = label_info_msg["emptyData"], fg = label_WrongAswer_color)
            self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_Create))
            self.screenChange(self.frame_IC)
    
    def modifyAccountPsw(self):
        """
        Description : Change le mot de passe en fonction de s'il est dans la db et s'il a entré des bonne données
        
        Input :
            self
        Output : /
        """
        username = self.entryUsr_PSWMod.get()
        password = self.entryPsw_PSWMod.get()
        if username != "" and password != "":
            if checkNoInjection(username) and checkNoInjection(password):
                if userExist(users, username):
                    if pswCorrect(users, username, password): # LOGIN, now check new password
                        newPsw = self.entryNewPsw_PSWMod.get()
                        confNewPsw = self.entryConfNewPsw_PSWMod.get()

                        if newPsw != "" and confNewPsw != "":
                            if checkNoInjection(newPsw) and checkNoInjection(confNewPsw):
                                if newPsw == confNewPsw:
                                    if username != newPsw:
                                        if checkNoEasyPsw(newPsw): # Le mot de passe n'est pas trop simple
                                            if checkNoPoorPsw(newPsw): # Le mot de passe est assez robuste
                                                updateUser(users, username, newPsw)

                                                self.label_IC.configure(text = label_info_msg["pswSuccessfullyUpdated"], fg = label_CorrectAswer_color)
                                                self.button_IC.configure(text= "Retour à l'accueil", command= lambda: self.screenChange(self.frame_MH))
                                                self.screenChange(self.frame_IC)

                                                self.entryUsr_PSWMod.delete(0, 'end')
                                                self.entryPsw_PSWMod.delete(0, 'end')
                                                self.entryConfNewPsw_PSWMod.delete(0, 'end')

                                            else: # Password too poor
                                                self.label_IC.configure(text = label_info_msg["tooPoorPsw"], fg = label_WrongAswer_color)
                                                self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_PSWMod))
                                                self.screenChange(self.frame_IC)
                                        else: # Password too easy
                                            self.label_IC.configure(text = label_info_msg["tooEasyPsw"], fg = label_WrongAswer_color)
                                            self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_PSWMod))
                                            self.screenChange(self.frame_IC)
                                    else: # Username et password identique
                                        self.label_IC.configure(text = label_info_msg["sameUserPsw"], fg = label_WrongAswer_color)
                                        self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_PSWMod))
                                        self.screenChange(self.frame_IC)
                                else: # New psw and confirmation of new psw not the same
                                    self.label_IC.configure(text = label_info_msg["notSameNewPsw"], fg = label_WrongAswer_color)
                                    self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_PSWMod))
                                    self.screenChange(self.frame_IC)
                            else: # Illegal character
                                self.label_IC.configure(text = label_info_msg["illegalCharacter"], fg = label_WrongAswer_color)
                                self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_PSWMod))
                                self.screenChange(self.frame_IC)
                        else: # Username or password empty
                            self.label_IC.configure(text = label_info_msg["emptyData"], fg = label_WrongAswer_color)
                            self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_PSWMod))
                            self.screenChange(self.frame_IC)

                    else: # Le mmot de passe est incorrect
                        global currentTryPsw
                        currentTryPsw += 1
                        if currentTryPsw >= maxTryPsw:
                            self.label_IC.configure(text = label_info_msg["toManyTry"], fg = label_WrongAswer_color)
                            self.button_IC.configure(text= "Retour à l'accueil", command= lambda: self.screenChange(self.frame_PSWMod))
                            self.screenChange(self.frame_IC)

                            currentTryPsw = 0
                            self.entryUsr_PSWMod.delete(0, 'end')
                        else:
                            self.label_IC.configure(text = label_info_msg["wrongPassword"] + f"\nIl vous reste {maxTryPsw - currentTryPsw} tentative(s)", fg = label_WrongAswer_color)
                            self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_PSWMod))
                            self.screenChange(self.frame_IC)
                        self.entryPsw_PSWMod.delete(0, 'end')

                else: # L'user n'existe pas
                    self.label_IC.configure(text = label_info_msg["noUser"], fg = label_WrongAswer_color)
                    self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_PSWMod))
                    self.screenChange(self.frame_IC)
            else: # Illegal character
                self.label_IC.configure(text = label_info_msg["illegalCharacter"], fg = label_WrongAswer_color)
                self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_PSWMod))
                self.screenChange(self.frame_IC)
        else: # Username or password empty
            self.label_IC.configure(text = label_info_msg["emptyData"], fg = label_WrongAswer_color)
            self.button_IC.configure(text= "Retour", command= lambda: self.screenChange(self.frame_PSWMod))
            self.screenChange(self.frame_IC)


if __name__ == "__main__" :
    root = Interface()
    root.resizable(width=False,height=False)
    root.title("Gestion de compte")

    try:
        users = loadJson()
    except:
        logs("[WARN] Fichier d'utilisateur pas fait. Lancement du processus de création de fichier.")
        createJson(users)
        

    root.mainloop()