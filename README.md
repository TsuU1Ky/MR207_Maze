# SAE MR207 Graphes

Auteurs :

-   Valente Gabriel
-   Terrier Antoine

Veuillez trouver la classe `Maze` dans [`maze.py`](./maze.py). Les tests sont disponibles dans [`test_maze.py`](./test_maze.py)

# Maze Ball

Bonus SAE MR207 Graphes.

## Jouer au jeu

-   Le jeu se trouve dans [`game`](./game/).
-   Déplacez dans vous dans ce dossier (`cd game`).
-   Installez les [`requirements`](./game/requirements.txt) avec:
    `pip3 install -r requirements.txt`.
-   Lancez le jeu avec `python3 main.py`.

## Comment jouer

-   Tourner le labyrinthe dans le sens anti-horaire avec <kbd>LEFT</kbd>.
-   Tourner le labyrinthe dans le sens horaire avec <kbd>RIGHT</kbd>.
-   Le but est d'atteindre la case verte en bas à droite du labyrinthe.

## Bugs connus

-   La bille peut passer à travers certains murs lors de la rotation.
-   La bille peut atteindre la case d'arrivée à travers un mur.
