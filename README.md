# Chess manager
### Chess manager vous permet de gerer une liste de joureurs, de creer des joueurs et des tournois. Il permet egalement de jouer les tournois avec le SYSTÈME SUISSE DES TOURNOIS.


# Installation du chess tournament manager
## Cloner le repo github en local

Lancer dans le terminal:

***git clone https://github.com/gsysaath/python_chess_manager.git chess_manager***

Rentrons dans le dossier tout juste cloné:

***cd chess_manager***
## Tout d'abord creer l'environnement virtuel

Lancez dans le terminal la commande qui va vous creer l'envrironnement virtuel appelé env:

- Pour Unix:

    ***python3 -m venv env***

- Pour windows:

    ***python -m venv env***
    
Activons le:
- Pour Unix:

    ***source ./env/bin/activate***
- Pour Windows:

    ***.env/Scripts/activate.bat***

## Installer les requirements

    pip install -r requirements.txt

## Et lancer le programme:

- Pour Unix:

    ***python3 main.py***

- Pour windows:

    ***python main.py*** 
    
## Lancer un reporting flake8 pour le pep8

***flake8 --format=html --htmldir=flake-report***
