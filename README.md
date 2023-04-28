# Exercice/Travail du cours de Laboratoire d'Informatique Passerelle
Exercice obligatoire du cours de laboratoire informatique passerelle (mi-quadri).
Consigne d'exercice de la séance :

# Séance 5

## Concepts de design

### *DRY : Don't Repeat Yourself*

La définition de ce principe est : *"Every piece of knowledge or logic must have a single, unambiguous, representation within a system."*.

Défini autrement, ce principe consiste à faire en sorte de toujours subdiviser son code afin de ne pas avoir plusieurs fois dans son programme des portions de code qui font la même chose. Concrètement, cela passe par l'écriture de fonctions (et de classes/sous classes lorsqu'on fait de l'orientée objet).

### *KISS : Keep It Simple, Stupid*

Ce principe est là pour se rappeler que notre code ne doit pas être inutilement complexe. Lorsqu'on programme, on peut d'abord trouver une première solution à notre problème, puis se rendre compte qu'il est possible de faire beaucoup plus simplement.

Il faut ainsi toujours garder en tête que notre code doit être le plus simple possible. Cela rend sa lecture et sa compréhension plus aisée.

Ce principe conseille également de n'implémenter que l'essentiel. On peut parfois avoir envie de coder une fonctionnalité qui n'est pas explicitement nécessaire à l'instant t, mais dont on peut penser qu'elle sera nécessaire plus tard dans le projet. Si l'on garde en tête que notre programme doit toujours être simple et "stupide", alors tout ce qui n'est pas nécessaire n'a pas de raison d'être dans notre programme.

## Exercices

### Gestionnaire de comptes

L'objectif de cet exercice est d'écrire un programme de gestion de comptes, C'est-à-dire des paires `username`; `password`. Ces comptes devront être stockés dans un dictionnaire.

Le programme doit intégrer les fonctionnalités suivantes :

- Création d'un nouveau compte
- Changement du mot de passe d'un compte
- Suppression d'un compte
- Affichage des pseudos existants

Comme pour un vrai site :

- il ne peut pas y avoir plusieurs comptes avec le même *username*
- Avant d'autoriser la modification ou la suppression d'un compte, le programme doit demander le mot de passe du compte en question et vérifier qu'il est le bon

Le programme principal doit être dans un bloc `if __name__ == "__main__"` et devra tourner dans une boucle `while`. Code de départ :

Le programme devra être compartimenté judicieusement : c'est-à-dire contenir des fonctions. Par exemple :

```python
def is_username(logins: dict, username: str):
    pass
```

La fonction `is_username()` servirait ici à vérifier si un pseudo est déjà pris.

Ici, la fonction n'a pas encore de corps (c'est-à-dire de code à l'intérieur). Pour quand même laisser cette fonction dans le script et pouvoir l'exécuter sans que cela produise d'erreur de syntaxe, on utilise l'instruction `pass`, qui ne fait rien.

Le programme devra également importer et exporter les comptes utilisateurs dans un fichier JSON. Pour cela, il devra :

- Au démarrage, ouvrir le fichier texte contenant les infos des comptes déjà existants. Si le fichier n'existe pas encore (ce qui devrait être le cas au moins à la première exécution du programme), traitez ce cas de figure comme une exception (pour plus d'information, se renseigner sur `FileNotFoundError`).
- À la fermeture, sauvegarder tous les nouveaux comptes créés dans ce même fichier JSON.
