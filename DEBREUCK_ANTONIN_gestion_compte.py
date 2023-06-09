# -*- coding: utf-8 -*-
"""
Account management

Created on Thuesday April 27 2023 at 15:51
"Finished" on Friday May 12 2023 at 12:20

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
import platform # For the python version
import json
import re # For Regex
from colorama import Fore # For Colors in terminal

#=========================================================================================================#

            #-------------------- Mofiable/Changeable variables | Options --------------------#

#=========================================================================================================#
            
#================================================== Parameters ==================================================#

frame_width = 1000
ratio = 16/9

version = '1.1.13'

# =============== Colors =============== #
bg_frame_color = 'black'
bg_button_color = 'gray11'

label_color = '#FFF'
label_button_color = '#FFF'

label_correct_answer_color = '#33FF33'
label_wrong_answer_color = '#F00'

label_error_color = '#CC0000'

# =============== Labels Displays =============== #

label_info_msg = {
    "login_successfully" : "Vous êtes bien connecté !",
    "successfully_new_account" : "Compte créé !",
    "psw_successfully_updated" : "Votre mot de pase est bien mis à jour !",
    "account_successfully_delete" : "Votre compte est bien supprimé !",
    "connnection_refused" : "Connexion refusée !",

    "no_users" : "Il y a aucun utilisateur dans notre base de données actuellement.",
    "no_user" : "Cet utilisateur n'existe pas !",
    "user_allready_exist" : "Cet utilisateur existe déjà !",
    "wrong_password" : "Le mot de passe entré, n'est pas bon !",
    "empty_data" : "Merci de remplir tous les champs !\nIl manque votre pseudo et/ou votre mot de passe.",
    "same_user_psw" : "Pour des raison de sécurité, nous n'autorisons pas un mot de passe identique à l'utilisateur.",
    "too_easy_psw" : "Mot de passe trop connu et pas assez robuste.",
    "too_poor_psw" : "Mot de passe pas assez robuste !\nIl doit contenir au moins 8 caractères dont 1 spécial, une minuscule et une majuscule.",
    "to_many_try" : "Vous avez essayer trop de fois des mots de passe incorrects !\nNous soupçonnons une tentative d'attaque brute force.",
    "illegal_character" : "Caractère non autorisée !\nNous soupçonnons une tentative d'injection de code.",

    "not_same_new_psw" : "Le nouveau mot de passe et la confirmation ne correspondent pas !"
}

# =============== Password =============== #

max_try_psw = 3
regex_psw_pattern = r'[^\w\s]'

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
current_try_psw = 0

#=========================================================================================================#

                        #-------------------- Homemade Function/Class --------------------#

#=========================================================================================================#

#================================================== Operations ==================================================#

def log(info):
    """
    Description : S'assure la création des log pour toutes les informations.
    Les log contiendront toutes les informations qui pourraient aider à débloquer le jeu
    
    Input :
        info : string -> Message à mettre dans les log
    Output : /
    """
    global date
    info = str(info)
    datenow = datetime.datetime.now()

    # To avoid 1 file per log
    if date == "":
        date = f"{datenow.day}-{datenow.month}-{datenow.year}_{datenow.hour}-{datenow.minute}-{datenow.second}"

    if not os.path.exists(cwd + logs_folder + logs_file + "_" + date + ".txt"):
        if not os.path.exists(cwd + files_folder):
            os.mkdir(cwd + files_folder)
        if not os.path.exists(cwd + logs_folder):
            os.mkdir(cwd + logs_folder)
            
    with open(cwd + logs_folder + logs_file + "_" + date + ".txt", 'a') as f:
        f.write('[' + str(datenow) + '] ' + info + '\n')

    if "[ERROR]" in info:
        color = Fore.RED
    elif "[WARN]" in info:
        color = Fore.YELLOW
    else:
        color = Fore.RESET
    print(color + '[' + str(datenow) + '] ' + info)

# ===== JSON ===== #
def load_json():
    """
    Description : Lit le fichier JSON pour récupérer tous les comptes des utilisateurs.
    
    Input : /
    Output :
        users_in_file : dict -> Dictionnaire du fichier JSON
    """
    try:
        with open(cwd + files_folder + data_file + ".json") as jf: # jf = Json file
            users_in_file = json.load(jf)
        log("[INFO] Recharge les utilisateur du fichier JSON")
        return users_in_file
    except FileNotFoundError :
        log("[WARN] Fichier d'utilisateur pas fait. Lancement du processus de création de fichier. (Avec les utilisateurs qu'il y avait au lancement)")
        global users
        create_json(users)
        users = load_json()
    except Exception as Err :
        log("[ERROR] Prévenez un admin (contact@antodb.be) !\nL'erreur :\n")
        log(Err)

def create_json(users : dict):
    """
    Description : Écrit dans le fichier JSON les comptes des utilisateurs.
    
    Input :
        users : dict -> Dictionnaire à mettre dans le fichier JSON
    Output : /
    """
    try:
        with open(cwd + files_folder + data_file + ".json", "w") as fp:
            json.dump(users, fp)
        log("[INFO] Crée ou écrit un fichier JSON avec les utilisateurs")
    except:
        log("[ERROR] Impossible de créer le fichier")

# ===== Users treatment ===== #
def user_exist(logins: dict, username: str):
    """
    Description : Renvoie un booléen en fonction de si l'utilsateur existe
    
    Input :
        logins : dict -> Dictionnaire contenant les utilisateurs et leurs mots de passe
        username : str -> Le nom d'utilisateur
    Output :
        bool -> True si l'utilisateur existe dans la base de données, False dans le cas contraire
    """
    try:
        if username in logins.keys() :
            return True
        else :
            return False
    except AttributeError:
        log("[WARN] Fichier vide or censé être créé avec utilisateurs !")
        global users
        create_json(users)
    except Exception as Err:
        log("[ERROR] Impossible de récupérer les données des utilisateurs\nL'erreur :\n")
        log(Err)
    
def psw_correct(logins: dict, username: str, password: str):
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
        
def update_user(logins: dict, username: str, password: str):
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
    create_json(logins)
    log("[INFO] Utilisateur bien mis à jour !")
    return logins

def remove_user(logins: dict, username: str):
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
        create_json(logins)
        log("[INFO] Utilisateur supprimé !")
    return logins

# ===== Input & Psw treatment ===== #
def check_no_injection(input: str):
    """
    Description : Renvoie un booléen en fonction de si le texte ne contient pas des caractères suspects
    
    Input :
        input : str -> La chaine de caractère à analyser
    Output :
        bool -> True si pas de caractères spéciaux sensible, False dans le cas contraire
    """
    if "#" in input or "\"" in input :
        log("[WARN] Soupçon de tentative d'injection de code.")
        return False
    return True

def check_no_easy_psw(input: str):
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

def check_no_poor_psw(input: str):
    """
    Description : Renvoie un booléen en fonction de si le texte n'est pas trop pauvre en robustesse
    
    Input :
        input : str -> La chaine de caractère à analyser
    Output :
        bool -> True si le mot de passe n'est pas trop simple, False dans le cas contraire
    """
    if len(input) >= 8 and input != input.lower() and input != input.upper() and bool(re.search(regex_psw_pattern, input)) : # Dernier : Renvoie true si le regex est juste (s'il y a un caractère spécial de trouvé dans le str)
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
        self.frame_mh = Frame(self)
        self.canvas_mh = Canvas(self.frame_mh, bg=bg_frame_color, width=frame_width, height=frame_width/ratio, highlightthickness = 0)
    
        self.label_mh_title = Label(self.frame_mh, bg=bg_frame_color, fg=label_color, text="Gestionnaire de comptes", font =("Helvetica", 25))

        self.button_mh1 = Button(self.frame_mh, bg=bg_button_color, fg=label_button_color, text="Se connecter", width = 25, height = 3, font =("Helvetica", 15), command=lambda: self.modify_screen_after_login("login"))
        self.button_mh2 = Button(self.frame_mh, bg=bg_button_color, fg=label_button_color, text="Créer un compte", width = 25, height = 3, font =("Helvetica", 15), command=lambda: self.screen_change(self.frame_create))  
        self.button_mh3 = Button(self.frame_mh, bg=bg_button_color, fg=label_button_color, text="Changer votre mot de passe", width = 25, height = 2, font =("Helvetica", 15), command=lambda: self.screen_change(self.frame_pswmod))
        self.button_mh4 = Button(self.frame_mh, bg=bg_button_color, fg=label_button_color, text="Supprimer votre compte", width = 25, height = 2, font =("Helvetica", 15), command=lambda: self.modify_screen_after_login("delPsw"))
        self.button_mh5 = Button(self.frame_mh, bg=bg_button_color, fg=label_button_color, text="Afficher les utilisateurs", width = 25, height = 2, font =("Helvetica", 15), command=lambda: self.display_account())

        Label(self.frame_mh, bg=bg_frame_color, fg=label_color, text="Python V : " + str(platform.python_version())).place(x = 10 , y = frame_width/ratio-65)
        Label(self.frame_mh, bg=bg_frame_color, fg=label_color, text="App V : " + version).place(x = 10 , y = frame_width/ratio-45)
        Button(self.frame_mh, bg=bg_button_color, fg=label_button_color, text="Quitter", width = 20, height = 2, font =("Helvetica", 15), command=self.destroy).grid(row = 5, column = 3)

        self.canvas_mh.grid(row = 1, column = 1, rowspan = 5, columnspan = 5)

        self.label_mh_title.grid(row = 1, column = 1, columnspan = 5)

        self.button_mh1.grid(row = 2, column = 2)
        self.button_mh2.grid(row = 2, column = 4)
        self.button_mh3.grid(row = 4, column = 2)
        self.button_mh4.grid(row = 4, column = 3)
        self.button_mh5.grid(row = 4, column = 4)

        log("[INFO] Menu de démarrage fait")

        # Affichage premier écran & Prend quel écran c'est & Met le titre
            
        self.mes_autres_frames = {}
        self.current_frame = self.frame_mh
        self.current_frame.grid()

        # =============== Création des autres fenêtres =============== #

        """
        Description : Création de l'écran de connexion
        
        Input : /
        Output : /
        """
        # Con = Connexion
        self.frame_con = Frame(self)
        self.canvas_con = Canvas(self.frame_con, bg=bg_frame_color, width=frame_width, height=frame_width/ratio, highlightthickness = 0)
    
        Label(self.frame_con, bg=bg_frame_color, fg=label_color, text="Se connecter", font =("Helvetica", 25)).grid(row = 1, column = 1)

        Label(self.frame_con, bg=bg_frame_color, fg=label_color, text="Pseudo", font =("Helvetica", 25)).place(x=frame_width/2-220, y=frame_width/ratio/5*1.2)
        Label(self.frame_con, bg=bg_frame_color, fg=label_color, text="Mot de passe", font =("Helvetica", 25)).place(x=frame_width/2-300, y=frame_width/ratio/5*2)

        self.entry_usr_con = Entry(self.frame_con, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))
        self.entry_psw_con = Entry(self.frame_con, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))

        self.button_con1 = Button(self.frame_con, bg=bg_button_color, fg=label_button_color, text="Se connecter", width = 20, height = 2, font =("Helvetica", 15), command=lambda: self.connection("login"))
        self.button_con2 = Button(self.frame_con, bg=bg_button_color, fg=label_button_color, text="Retour à l'accueil", width = 15, height = 2, font =("Helvetica", 15), command=lambda: self.screen_change(self.frame_mh))

        self.canvas_con.grid(row = 1, column = 1, rowspan = 5)

        self.entry_usr_con.grid(row = 2, column = 1)
        self.entry_psw_con.grid(row = 3, column = 1)

        self.button_con1.grid(row = 4, column = 1)
        self.button_con2.grid(row = 5, column = 1)

        log("[INFO] Menu de connexion fait")

        """
        Description : Création de l'écran de création de compte
        
        Input : /
        Output : /
        """
        # Create = Création (de compte)
        self.frame_create = Frame(self)
        self.canvas_create = Canvas(self.frame_create, bg=bg_frame_color, width=frame_width, height=frame_width/ratio, highlightthickness = 0)
    
        Label(self.frame_create, bg=bg_frame_color, fg=label_color, text="Créer votre compte", font =("Helvetica", 25)).grid(row = 1, column = 1)

        Label(self.frame_create, bg=bg_frame_color, fg=label_color, text="Pseudo", font =("Helvetica", 25)).place(x=frame_width/2-220, y=frame_width/ratio/6*1.2)
        Label(self.frame_create, bg=bg_frame_color, fg=label_color, text="Mot de passe", font =("Helvetica", 25)).place(x=frame_width/2-300, y=frame_width/ratio/6*2)
        Label(self.frame_create, bg=bg_frame_color, fg=label_color, text="Confirmation du nouveau\nmot de passe", font =("Helvetica", 18)).place(x=frame_width/2-380, y=frame_width/ratio/6*2.8)

        self.entry_usr_create = Entry(self.frame_create, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))
        self.entry_psw_Create = Entry(self.frame_create, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))
        self.entry_conf_psw_create = Entry(self.frame_create, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))

        self.button_create1 = Button(self.frame_create, bg=bg_button_color, fg=label_button_color, text="Créer le compte", width = 15, height = 2, font =("Helvetica", 15), command=self.create_account)
        self.button_create2 = Button(self.frame_create, bg=bg_button_color, fg=label_button_color, text="Retour à l'accueil", width = 15, height = 2, font =("Helvetica", 15), command=lambda: self.screen_change(self.frame_mh))

        self.canvas_create.grid(row = 1, column = 1, rowspan = 6)

        self.entry_usr_create.grid(row = 2, column = 1)
        self.entry_psw_Create.grid(row = 3, column = 1)
        self.entry_conf_psw_create.grid(row = 4, column = 1)

        self.button_create1.grid(row = 5, column = 1)
        self.button_create2.grid(row = 6, column = 1)

        log("[INFO] Menu de création de compte fait")

        """
        Description : Création de l'écran d'information de connexion/modification/suppression
        
        Input : /
        Output : /
        """
        # IC = Info Connexion
        self.frame_ic = Frame(self)
        Canvas(self.frame_ic, bg=bg_frame_color, width=frame_width, height=frame_width/ratio, highlightthickness = 0).grid(row = 1, column = 1, rowspan = 2)
    
        self.label_ic = Label(self.frame_ic, bg=bg_frame_color, fg=label_color, text="Si vous lisez ceci, c'est une erreur.\nPrévenez le créateur en expliquant votre manipulation.", font =("Helvetica", 18), height=2)
        self.button_ic = Button(self.frame_ic, bg=bg_button_color, fg=label_button_color, text="Retour à l'accueil", width = 20, height = 2, font =("Helvetica", 15), command=lambda: self.screen_change(self.frame_mh))

        self.label_ic.grid(row = 1, column = 1)
        self.button_ic.grid(row = 2, column = 1)

        log("[INFO] Écran d'affichage message de connexion/modification/suppression.")

        """
        Description : Création de l'écran de modification de mot de passe
        
        Input : /
        Output : /
        """
        # PSWMod = Password Modification = Modification de mot de passe
        self.frame_pswmod = Frame(self)
        self.canvas_pswmod = Canvas(self.frame_pswmod, bg=bg_frame_color, width=frame_width, height=frame_width/ratio, highlightthickness = 0)
    
        Label(self.frame_pswmod, bg=bg_frame_color, fg=label_color, text="Modifiez votre mot de passe", font =("Helvetica", 25)).grid(row = 1, column = 1)

        Label(self.frame_pswmod, bg=bg_frame_color, fg=label_color, text="Pseudo", font =("Helvetica", 18)).place(x=frame_width/2-220, y=frame_width/ratio/8*1.2)
        Label(self.frame_pswmod, bg=bg_frame_color, fg=label_color, text="Mot de passe\nactuel", font =("Helvetica", 18)).place(x=frame_width/2-280, y=frame_width/ratio/8*2)

        self.entry_usr_pswmod = Entry(self.frame_pswmod, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))
        self.entry_psw_pswmod = Entry(self.frame_pswmod, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))

        Label(self.frame_pswmod, bg=bg_frame_color, fg=label_color, text="Nouveau\nmot de passe", font =("Helvetica", 18)).place(x=frame_width/2-280, y=frame_width/ratio/8*3.2)
        Label(self.frame_pswmod, bg=bg_frame_color, fg=label_color, text="Confirmation du nouveau\nmot de passe", font =("Helvetica", 18)).place(x=frame_width/2-400, y=frame_width/ratio/8*4.2)

        self.entry_new_psw_pswmod = Entry(self.frame_pswmod, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))
        self.entry_conf_new_psw_PSWMod = Entry(self.frame_pswmod, bg=bg_button_color, fg=label_button_color, width = 15, font =("Helvetica", 15))

        self.button_pswmod1 = Button(self.frame_pswmod, bg=bg_button_color, fg=label_button_color, text="Modifier le mot de passe", width = 20, height = 2, font =("Helvetica", 15), command=self.modify_account_psw)
        self.button_pswmod2 = Button(self.frame_pswmod, bg=bg_button_color, fg=label_button_color, text="Retour à l'accueil", width = 15, height = 2, font =("Helvetica", 15), command=lambda: self.screen_change(self.frame_mh))

        self.canvas_pswmod.grid(row = 1, column = 1, rowspan = 8)

        self.entry_usr_pswmod.grid(row = 2, column = 1)
        self.entry_psw_pswmod.grid(row = 3, column = 1)
        self.entry_new_psw_pswmod.grid(row = 5, column = 1)
        self.entry_conf_new_psw_PSWMod.grid(row = 6, column = 1)

        self.button_pswmod1.grid(row = 7, column = 1)
        self.button_pswmod2.grid(row = 8, column = 1)

        log("[INFO] Menu de modification de mot de passe fait")

        """
        Description : Création du menu de statistique.
        Contient les catégories : Nom/Pseudo, Points, Nombres de parties (Dont réussie, Dont ratée), Nombres de pions placés, Temps joué
        
        Input : /
        Output : /
        """
        # DA = Display Account = Affiche compte
        self.frame_da = Frame(self, bg=bg_frame_color)
        self.canvas_da = Canvas(self.frame_da, bg=bg_frame_color, width=frame_width, height=frame_width/ratio, highlightthickness = 0)
    
        Label(self.frame_da, bg=bg_frame_color, fg=label_color, text="Comptes enregistrés", font = ("Helvetica", 25)).grid(row = 1, column = 1)
    
        Label(self.frame_da, bg=bg_frame_color, fg=label_color, text="Noms/Pseudos", font = ("Helvetica", 25)).grid(row = 2, column = 1, sticky=W)
        
        self.text_da = Text(self.frame_da, font = ("Helvetica", 15), height=10)
        self.text_da.grid(row = 3, column = 1, sticky=EW)

        # create a scrollbar widget and set its command to the text widget
        scrollbar = Scrollbar(self.frame_da, orient='vertical', command=self.text_da.yview)
        scrollbar.grid(row=3, column=2, sticky=NS)

        #  communicate back to the scrollbar
        self.text_da['yscrollcommand'] = scrollbar.set
        
        Button(self.frame_da, bg=bg_button_color, fg=label_button_color, text="Retour à l'accueil", width = 15, height = 2, font =("Helvetica", 15), command=lambda: self.screen_change(self.frame_mh)).grid(row = 5, column = 1, columnspan= 2)

        self.canvas_da.grid(row = 1, column = 1, rowspan=5)

        log("[INFO] Écran d'affichage de comptes fait")

    # ===== Interface treatment ===== #

    def display_account(self):
        """
        Description : Pour pouvoir afficher les comptes utilisateurs
        Actions : Change la textbox avec les datas et demande le changement d'écran
        
        Input :
            self
        Output : /
        """
        global users
        users = load_json() # Must update the variable in the code if account where created ou deleted

        #print(users)
        #print(users.items())
        #(list(enumerate(users.items())))
        self.text_da.configure(state=NORMAL)
        self.text_da.delete('1.0', END)
        try:
            for index, (key, values) in enumerate(users.items()):
                self.text_da.insert(f'{index+1}.0', f'{key}\n')
                print(f"index : {index+1}, key : {key}")
        except AttributeError:
            log("[WARN] Not found users. Retry after (probably) recreated file.")
            self.display_account()
        except Exception as Err:
            log("[ERROR] Please call the dev !\nThe error :\n")
            log(Err)
        self.text_da.configure(state=DISABLED)

        self.screen_change(self.frame_da)

    def screen_change(self, arg : object):
        """
        Description : Affiche le menu demandé.
        Actions : Enlève le précédent écran, affiche celui demandé, set une variable sur cette écran
        
        Input :
            self
            arg = object -> Fenêtre à placer
        Output : /
        """
        #print(dir(arg)) # Possibilité d'opération sur l'object
        log("[INFO] Changement fenêtre : " + str(self.current_frame) + " > " + str(arg))
        self.current_frame.grid_remove()
        self.current_frame = arg
        self.current_frame.grid()
    
    def modify_screen_after_login(self, operation : str):
        """
        Description : Change le bouton de connexion Affiche le menu demandé.
        Actions : Enlève le précédent écran, affiche celui demandé, set une variable sur cette écran
        
        Input :
            self
            frame : object -> Fenêtre à placer
            operation : str -> Quel opération à faire et quelle frame a afficher si la connexion est réussie
        Output : /
        """
        if operation == "display_users":
            self.button_con1.configure(text= "Afficher les comptes", command= lambda: self.connection(operation))
        elif operation == "delPsw":
            self.button_con1.configure(text= "Suprimmer le compte", command= lambda: self.connection(operation))
        else:
            self.button_con1.configure(text= "Se connecter", command= lambda: self.connection(operation))
        self.entry_usr_con.delete(0, 'end')
        self.entry_psw_con.delete(0, 'end')
        self.screen_change(self.frame_con)

    def connection(self, operation : str):
        """
        Description : Essaye de connecter l'utilsateur en fonction de s'il est dans la db et s'il a entré des bonne données
        
        Input :
            self
            operation : str -> Quel opération à faire et quelle frame a afficher si la connexion est réussie
        Output : /
        """
        users = load_json() # Must update the variable in the code if account where created ou deleted
        users = load_json() # Must update the variable in the code if account where created ou deleted (twice to get if the file is recreated at the previous step)
        username = self.entry_usr_con.get()
        password = self.entry_psw_con.get()
        if username != "" and password != "":
            if check_no_injection(username) and check_no_injection(password):
                if user_exist(users, username):
                    if psw_correct(users, username, password):
                        if operation == "display_users" :
                            self.label_ic.configure(text = label_info_msg["psw_successfully_updated"] + f"\nBonjour {username} !", fg = label_correct_answer_color)
                            self.button_ic.configure(text= "Retour à l'accueil", command= lambda: self.screen_change(self.frame_mh))
                            
                            self.display_account()
                        elif operation == "delPsw" :
                            self.label_ic.configure(text = label_info_msg["account_successfully_delete"], fg = label_correct_answer_color)
                            self.button_ic.configure(text= "Retour à l'accueil", command= lambda: self.screen_change(self.frame_mh))
                            remove_user(users, username)
                            users = load_json()

                            self.screen_change(self.frame_ic)
                        else :
                            self.label_ic.configure(text = label_info_msg["login_successfully"] + f"\nBonjour {username} !", fg = label_correct_answer_color)
                            self.button_ic.configure(text= "Retour à l'accueil", command= lambda: self.screen_change(self.frame_mh))
                            self.screen_change(self.frame_ic)

                    else: # Le mmot de passe est incorrect
                        global current_try_psw
                        current_try_psw += 1
                        if current_try_psw >= max_try_psw:
                            self.label_ic.configure(text = label_info_msg["to_many_try"], fg = label_wrong_answer_color)
                            self.button_ic.configure(text= "Retour à l'accueil", command= lambda: self.screen_change(self.frame_mh))
                            self.screen_change(self.frame_ic)

                            current_try_psw = 0
                            self.entry_usr_con.delete(0, 'end')
                        else:
                            self.label_ic.configure(text = label_info_msg["wrong_password"] + f"\nIl vous reste {max_try_psw - current_try_psw} tentative(s)", fg = label_wrong_answer_color)
                            self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_con))
                            self.screen_change(self.frame_ic)
                        self.entry_psw_con.delete(0, 'end')

                else: # L'user n'existe pas
                    self.label_ic.configure(text = label_info_msg["no_user"], fg = label_wrong_answer_color)
                    self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_con))
                    self.screen_change(self.frame_ic)
            else: # Illegal character
                self.label_ic.configure(text = label_info_msg["illegal_character"], fg = label_wrong_answer_color)
                self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_con))
                self.screen_change(self.frame_ic)
        else: # Username or password empty
            self.label_ic.configure(text = label_info_msg["empty_data"], fg = label_wrong_answer_color)
            self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_con))
            self.screen_change(self.frame_ic)
    
    def create_account(self):
        """
        Description : Essaye de connecter l'utilsateur en fonction de s'il est dans la db et s'il a entré des bonne données
        
        Input :
            self
        Output : /
        """
        users = load_json()

        username = self.entry_usr_create.get()
        password = self.entry_psw_Create.get()
        confPsw = self.entry_conf_psw_create.get()
        if username != "" and password != "" and confPsw != "" :
            if check_no_injection(username) and check_no_injection(password) and check_no_injection(confPsw):
                if username != password:
                    if user_exist(users, username): # L'user est déjà existant
                        self.label_ic.configure(text = label_info_msg["user_allready_exist"], fg = label_wrong_answer_color)
                        self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_create))
                        self.screen_change(self.frame_ic)
                    else: # L'user n'existe pas
                        if password == confPsw:
                            if check_no_easy_psw(password): # Le mot de passe n'est pas trop simple (1234, salut, ...)
                                if check_no_poor_psw(password): # Le mot de passe est assez robuste
                                    update_user(users, username, password)

                                    self.label_ic.configure(text = label_info_msg["successfully_new_account"], fg = label_correct_answer_color)
                                    self.button_ic.configure(text= "Retour à l'accueil", command= lambda: self.screen_change(self.frame_mh))
                                    self.screen_change(self.frame_ic)

                                    self.entry_usr_create.delete(0, 'end')
                                    self.entry_psw_Create.delete(0, 'end')
                                    self.entry_conf_psw_create.delete(0, 'end')

                                else: # Password too poor
                                    self.label_ic.configure(text = label_info_msg["too_poor_psw"], fg = label_wrong_answer_color)
                                    self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_create))
                                    self.screen_change(self.frame_ic)
                            else: # Password too easy
                                self.label_ic.configure(text = label_info_msg["too_easy_psw"], fg = label_wrong_answer_color)
                                self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_create))
                                self.screen_change(self.frame_ic)
                        else: # New psw and confirmation of new psw not the same
                            self.label_ic.configure(text = label_info_msg["not_same_new_psw"], fg = label_wrong_answer_color)
                            self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_create))
                            self.screen_change(self.frame_ic)
                else: # Username et password identique
                    self.label_ic.configure(text = label_info_msg["same_user_psw"], fg = label_wrong_answer_color)
                    self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_create))
                    self.screen_change(self.frame_ic)
            else: # Illegal character
                self.label_ic.configure(text = label_info_msg["illegal_character"], fg = label_wrong_answer_color)
                self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_create))
                self.screen_change(self.frame_ic)
        else: # Username or password empty
            self.label_ic.configure(text = label_info_msg["empty_data"], fg = label_wrong_answer_color)
            self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_create))
            self.screen_change(self.frame_ic)
    
    def modify_account_psw(self):
        """
        Description : Change le mot de passe en fonction de s'il est dans la db et s'il a entré des bonne données
        
        Input :
            self
        Output : /
        """
        username = self.entry_usr_pswmod.get()
        password = self.entry_psw_pswmod.get()
        if username != "" and password != "":
            if check_no_injection(username) and check_no_injection(password):
                if user_exist(users, username):
                    if psw_correct(users, username, password): # LOGIN, now check new password
                        newPsw = self.entry_new_psw_pswmod.get()
                        confNewPsw = self.entry_conf_new_psw_PSWMod.get()

                        if newPsw != "" and confNewPsw != "":
                            if check_no_injection(newPsw) and check_no_injection(confNewPsw):
                                if newPsw == confNewPsw:
                                    if username != newPsw:
                                        if check_no_easy_psw(newPsw): # Le mot de passe n'est pas trop simple
                                            if check_no_poor_psw(newPsw): # Le mot de passe est assez robuste
                                                update_user(users, username, newPsw)

                                                self.label_ic.configure(text = label_info_msg["psw_successfully_updated"], fg = label_correct_answer_color)
                                                self.button_ic.configure(text= "Retour à l'accueil", command= lambda: self.screen_change(self.frame_mh))
                                                self.screen_change(self.frame_ic)

                                                self.entry_usr_pswmod.delete(0, 'end')
                                                self.entry_psw_pswmod.delete(0, 'end')
                                                self.entry_conf_new_psw_PSWMod.delete(0, 'end')

                                            else: # Password too poor
                                                self.label_ic.configure(text = label_info_msg["too_poor_psw"], fg = label_wrong_answer_color)
                                                self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_pswmod))
                                                self.screen_change(self.frame_ic)
                                        else: # Password too easy
                                            self.label_ic.configure(text = label_info_msg["too_easy_psw"], fg = label_wrong_answer_color)
                                            self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_pswmod))
                                            self.screen_change(self.frame_ic)
                                    else: # Username et password identique
                                        self.label_ic.configure(text = label_info_msg["same_user_psw"], fg = label_wrong_answer_color)
                                        self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_pswmod))
                                        self.screen_change(self.frame_ic)
                                else: # New psw and confirmation of new psw not the same
                                    self.label_ic.configure(text = label_info_msg["not_same_new_psw"], fg = label_wrong_answer_color)
                                    self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_pswmod))
                                    self.screen_change(self.frame_ic)
                            else: # Illegal character
                                self.label_ic.configure(text = label_info_msg["illegal_character"], fg = label_wrong_answer_color)
                                self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_pswmod))
                                self.screen_change(self.frame_ic)
                        else: # Username or password empty
                            self.label_ic.configure(text = label_info_msg["empty_data"], fg = label_wrong_answer_color)
                            self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_pswmod))
                            self.screen_change(self.frame_ic)

                    else: # Le mmot de passe est incorrect
                        global current_try_psw
                        current_try_psw += 1
                        if current_try_psw >= max_try_psw:
                            self.label_ic.configure(text = label_info_msg["to_many_try"], fg = label_wrong_answer_color)
                            self.button_ic.configure(text= "Retour à l'accueil", command= lambda: self.screen_change(self.frame_pswmod))
                            self.screen_change(self.frame_ic)

                            current_try_psw = 0
                            self.entry_usr_pswmod.delete(0, 'end')
                        else:
                            self.label_ic.configure(text = label_info_msg["wrong_password"] + f"\nIl vous reste {max_try_psw - current_try_psw} tentative(s)", fg = label_wrong_answer_color)
                            self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_pswmod))
                            self.screen_change(self.frame_ic)
                        self.entry_psw_pswmod.delete(0, 'end')

                else: # L'user n'existe pas
                    self.label_ic.configure(text = label_info_msg["no_user"], fg = label_wrong_answer_color)
                    self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_pswmod))
                    self.screen_change(self.frame_ic)
            else: # Illegal character
                self.label_ic.configure(text = label_info_msg["illegal_character"], fg = label_wrong_answer_color)
                self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_pswmod))
                self.screen_change(self.frame_ic)
        else: # Username or password empty
            self.label_ic.configure(text = label_info_msg["empty_data"], fg = label_wrong_answer_color)
            self.button_ic.configure(text= "Retour", command= lambda: self.screen_change(self.frame_pswmod))
            self.screen_change(self.frame_ic)


if __name__ == "__main__" :
    root = Interface()
    root.resizable(width=False,height=False)
    root.title("Gestion de compte")

    try:
        users = load_json()
    except:
        log("[WARN] Fichier d'utilisateur pas fait. Lancement du processus de création de fichier.")
        create_json(users)
        

    root.mainloop()
