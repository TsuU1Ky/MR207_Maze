from __future__ import annotations
from random import choice, shuffle, randint


class Maze:
    """
    Représentation d'un labyrinthe sous forme de graphe non-orienté.

    Sa structure est représentée par un dictionnaire dont les clés sont les sommets
    et les valeurs sont les ensembles des sommets voisins accessibles.
    Chaque sommet est une cellule sous forme d'un couple (x, y).

    Attributes:
        height (int): La hauteur du labyrinthe.
        width (int): La largeur du labyrinthe.
        neighbors (dict): Un dictionnaire représentant les voisins accessibles de chaque cellule du labyrinthe.
    """

    def __init__(self, height: int, width: int, empty: bool = False) -> None:
        """
        Crée un nouveau labyrinthe avec les dimensions données.

        Args:
            height (int): La hauteur du labyrinthe, en nombre de cellules.
            width (int): La largeur du labyrinthe, en nombre de cellules.
            empty (bool, optional): Indique si le labyrinthe doit être créé sans murs.
                Par défaut le labyrinthe est créé avec uniquement des murs.

        Returns:
            None
        """

        self.height = height
        self.width = width
        if empty:
            self.neighbors = {}
            for i in range(height):
                for j in range(width):
                    self.neighbors[(i, j)] = set()

                    if (i + 1) < height:
                        self.neighbors[(i, j)] |= {(i + 1, j)}
                    if (j + 1) < width:
                        self.neighbors[(i, j)] |= {(i, j + 1)}
                    if (i - 1) > 0:
                        self.neighbors[(i, j)] |= {(i - 1, j)}
                    if (j - 1) > 0:
                        self.neighbors[(i, j)] |= {(i, j - 1)}
        else:
            self.neighbors = {
                (i, j): set() for i in range(height) for j in range(width)
            }

    def info(self) -> str:
        """
        Renvoie une chaîne de caractères décrivant le labyrinthe.

        **NE PAS MODIFIER CETTE MÉTHODE**

        Returns:
            str: Description textuelle des attributs de l'objet
        """

        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors) + "\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += (
            "- Structure cohérente\n"
            if valid
            else f"- Structure incohérente : {c1} X {c2}\n"
        )

        return txt

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle du labyrinthe en utilisant des caractères ascii.

        **NE PAS MODIFIER CETTE MÉTHODE**

        Returns:
            str: Représentation textuelle du labyrinthe.
        """

        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width - 1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width - 1):
            txt += "   ┃" if (0, j + 1) not in self.neighbors[(0, j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height - 1):
            txt += "┣"
            for j in range(self.width - 1):
                txt += "━━━╋" if (i + 1, j) not in self.neighbors[(i, j)] else "   ╋"
            txt += (
                "━━━┫\n"
                if (i + 1, self.width - 1) not in self.neighbors[(i, self.width - 1)]
                else "   ┫\n"
            )
            txt += "┃"
            for j in range(self.width):
                txt += (
                    "   ┃"
                    if (i + 1, j + 1) not in self.neighbors[(i + 1, j)]
                    else "    "
                )
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width - 1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt

    def add_wall(self, c1: tuple, c2: tuple) -> None:
        """
        Ajoute un mur entre les deux cellules spécifiées.

        Args:
            c1 (tuple): Cellule sous forme d'un couple (x, y).
            c2 (tuple): Cellule sous forme d'un couple (x, y).

        Returns:
            None
        """

        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert (
            0 <= c1[0] < self.height
            and 0 <= c1[1] < self.width
            and 0 <= c2[0] < self.height
            and 0 <= c2[1] < self.width
        ), f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées ne sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:  # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2)  # on le retire
        if c1 in self.neighbors[c2]:  # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1)  # on le retire

    def remove_wall(self, c1: tuple, c2: tuple) -> None:
        """
        Supprime le mur entre les deux cellules spécifiées.

        Args:
            c1 (tuple): Cellule sous forme d'un couple (x, y).
            c2 (tuple): Cellule sous forme d'un couple (x, y).

        Returns:
            None
        """

        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert (
            0 <= c1[0] < self.height
            and 0 <= c1[1] < self.width
            and 0 <= c2[0] < self.height
            and 0 <= c2[1] < self.width
        ), f"Erreur lors de la suppression d'un mur entre {c1} et {c2} : les coordonnées ne sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 not in self.neighbors[c1]:  # Si c2 est dans les voisines de c1
            self.neighbors[c1].add(c2)  # on le retire
        if c1 not in self.neighbors[c2]:  # Si c3 est dans les voisines de c2
            self.neighbors[c2].add(c1)  # on le retire

    def get_walls(self) -> list:
        """
        Retourne la liste de tous les murs sous la forme d'une liste de couple de cellules.

        Returns:
            list: Liste de tuple de cellules représentant les murs du labyrinthe.
        """

        walls = []

        for cell in self.neighbors:
            # Création d'allias pour les cellules voisines
            voisin_bas: tuple = (cell[0] + 1, cell[1])
            voisin_droite: tuple = (cell[0], cell[1] + 1)

            # Si le voisin de droite existe dans le labyrinthe ET qu'il n'est pas dans les voisins de 'cell', faire
            if (
                voisin_droite[0] < self.width
                and voisin_droite[1] < self.height
                and voisin_droite not in self.neighbors[cell]
            ):
                # On ajoute le couple 'cell' et la cellule voisine droite
                walls.append((cell, voisin_droite))

            # Si le voisin du bas existe dans le labyrinthe ET qu'il n'est pas dans les voisins de 'cell', faire
            if (
                voisin_bas[0] < self.width
                and voisin_bas[1] < self.height
                and voisin_bas not in self.neighbors[cell]
            ):
                # On ajoute le couple 'cell' et la cellule voisine bas
                walls.append((cell, voisin_bas))

        return walls

    def fill(self) -> None:
        """
        Ajoute tous les murs possibles dans le labyrinthe.

        C'est-à-dire enlève tous les couples.

        Returns:
            None
        """

        for cell in self.neighbors:
            self.neighbors[cell] = set()

    def empty(self) -> None:
        """
        Vide le labyrinthe de tous les murs.

        C'est-à-dire ajoute tous les couples possibles.

        Returns:
            None
        """

        self.neighbors = {}

        for i in range(self.height):
            for j in range(self.width):
                self.neighbors[(i, j)] = set()

                if (i + 1) < self.height:
                    self.neighbors[(i, j)] |= {(i + 1, j)}
                if (j + 1) < self.width:
                    self.neighbors[(i, j)] |= {(i, j + 1)}
                if (i - 1) > 0:
                    self.neighbors[(i, j)] |= {(i - 1, j)}
                if (j - 1) > 0:
                    self.neighbors[(i, j)] |= {(i, j - 1)}

    def get_contiguous_cells(self, cell: tuple) -> list:
        """
        Retourne la liste des cellules adjacentes à la cellule donnée.

        C'est-à-dire sans s'occuper des murs éventuels.

        Args:
            cell (tuple): Cellule sous forme d'un couple (x, y).

        Returns:
            list: Une liste de tuples représentant les cellules adjacentes à la cellule donnée.
        """

        cells = []

        if cell[0] - 1 >= 0:
            cells.append((cell[0] - 1, cell[1]))
        if cell[0] + 1 < self.height:
            cells.append((cell[0] + 1, cell[1]))
        if cell[1] - 1 >= 0:
            cells.append((cell[0], cell[1] - 1))
        if cell[1] + 1 < self.width:
            cells.append((cell[0], cell[1] + 1))

        return cells

    def get_reachable_cells(self, cell: tuple) -> list:
        """
        Retourne la liste des cellules adjacentes et accessibles depuis la cellule donnée.

        Args:
            cell (tuple): Cellule sous forme d'un couple (x, y).

        Returns:
            list: Une liste de tuples représentant les cellules accessibles depuis la cellule donnée.
        """
        reachable = []

        # Pour chaque cellule contigües, on regarde s'il fait parti de ses voisins
        for c in self.get_contiguous_cells(cell):
            if c in self.neighbors[cell]:
                reachable.append(c)

        return reachable

    @classmethod
    def gen_btree(cls, h: int, w: int) -> Maze:
        """
        Construit un labyrinthe vide en utilisant la génération par arbre binaire.

        Args:
            h (int): Hauteur du labyrinthe.
            w (int): Largeur du labyrinthe.

        Returns:
            Maze: Une instance de la classe Maze représentant le labyrinthe.
        """

        lab = cls(h, w, False)

        # Parcours de toutes les cellules du layrinthe
        for i in range(h):
            for j in range(w):
                contiguous_cells = lab.get_contiguous_cells((i, j))
                voisin_est = (i, j + 1)
                voisin_sud = (i + 1, j)

                # Si la cellule 'EST' ET la cellule 'SUD' existe dans les voisins contigues de (i,j)
                if voisin_est in contiguous_cells and voisin_sud in contiguous_cells:
                    # On supprime au hasard le mur 'EST' ou 'SUD' entre la cellule (i,j) et sa voisine
                    lab.remove_wall((i, j), choice((voisin_est, voisin_sud)))

                # Si la cellule 'EST' existe dans les voisins contigues de (i,j) ET la cellule 'SUD' n'j existe pas
                elif (
                    voisin_est in contiguous_cells
                    and voisin_sud not in contiguous_cells
                ):
                    # On supprime le mur 'EST' entre la cellule (i,j) et sa voisine
                    lab.remove_wall((i, j), voisin_est)

                # Si la cellule 'EST' n'existe dans les voisins contigues de (i,j) ET la cellule 'SUD' j existe
                elif (
                    voisin_est not in contiguous_cells
                    and voisin_sud in contiguous_cells
                ):
                    # On supprime le mur 'SUD' entre la cellule (i,j) et sa voisine
                    lab.remove_wall((i, j), voisin_sud)

        return lab

    @classmethod
    def gen_sidewinder(cls, h: int, w: int) -> Maze:
        """
        Construit un labyrinthe vide en utilisant la génération par sidewinder.

        Args:
            h (int): Hauteur du labyrinthe.
            w (int): Largeur du labyrinthe.

        Returns:
            Maze: Une instance de la classe Maze représentant le labyrinthe.
        """

        # Initialisation d’un labyrinthe plein
        lab = cls(h, w, False)

        # Parcours de toutes les cellules du layrinthe
        for i in range(h - 1):
            sequence = []
            for j in range(w - 1):
                # Ajouter la cellule (i, j) à la séquence
                sequence.append((i, j))
                # Tirer à pile ou face
                pile_face = choice(["pile", "face"])

                # Si c’est pile
                if pile_face == "pile":
                    # Casser le mur EST de la cellule (i, j)
                    lab.remove_wall((i, j), (i, j + 1))

                # Si c’est face :
                if pile_face == "face":
                    # Casser le mur SUD d’une des cellules, au hasard, présente dans la liste 'sequence'.
                    rand_cell = choice(sequence)
                    lab.remove_wall(rand_cell, (rand_cell[0] + 1, rand_cell[1]))
                    # Réinitialiser 'sequence' à une liste vide
                    sequence = []

            # Ajouter la dernière cellule à la séquence
            sequence.append((i, j))

            # Tirer une cellule au sort dans la séquence et casser son mur SUD
            rand_cell = choice(sequence)
            lab.remove_wall(rand_cell, (rand_cell[0] + 1, rand_cell[1]))

        # Casser tous les murs EST de la dernière ligne
        for y in range(w - 1):
            lab.remove_wall((h - 1, y), (h - 1, y + 1))

        return lab

    @classmethod
    def gen_fusion(cls, h: int, w: int) -> Maze:
        """
        Construit un labyrinthe vide en utilisant la génération par fusion de chemins.

        Args:
            h (int): Hauteur du labyrinthe.
            w (int): Largeur du labyrinthe.

        Returns:
            Maze: Une instance de la classe Maze représentant le labyrinthe.
        """

        # Initialisation d’un labyrinthe plein
        lab = cls(h, w, False)

        # On labélise les cellules de 0 à 'h*w'-1
        # Pour représenter chaque cellule dans une liste,
        # on peut simplement la numéroter de gauche à droite et de haut en bas.
        # Cela signifie que la cellule (i, j) sera représentée dans la liste par i * w + j.
        labels = list(range(h * w))

        # On extrait la liste de tous les murs mélangés
        lst_mur = lab.get_walls()
        shuffle(lst_mur)

        # Pour chaque mur de la liste
        for mur in lst_mur:
            # Si les deux cellules séparées par le mur n’ont pas le même label
            x1, y1 = mur[0]
            x2, y2 = mur[1]
            # w = largeur du labyrinthe (nombre de cellules par ligne)
            # x * w = index de la première cellule dans la ligne x de la liste
            # x * w + y = index de la cellule (x, y) dans la liste
            if labels[x1 * w + y1] != labels[x2 * w + y2]:
                # Casse le mur
                lab.remove_wall(mur[0], mur[1])

                # Affecte le label de la première cellule à toutes les cellules ayant le même label que la seconde cellule
                old_label = labels[x2 * w + y2]
                new_label = labels[x1 * w + y1]
                for i in range(h):
                    for j in range(w):
                        if labels[i * w + j] == old_label:
                            labels[i * w + j] = new_label

        return lab

    @classmethod
    def gen_exploration(cls, h: int, w: int) -> Maze:
        """
        Construit un labyrinthe vide en utilisant la génération par exploration.

        Args:
            h (int): Hauteur du labyrinthe.
            w (int): Largeur du labyrinthe.

        Returns:
            Maze: Une instance de la classe Maze représentant le labyrinthe.
        """

        # Initialisation d’un labyrinthe plein
        lab = cls(h, w, False)

        # Choisir une cellule au hasard
        x = randint(0, w - 1)
        y = randint(0, h - 1)

        # Marquer cette cellule comme étant visitée
        cell_visited = set((y, x))

        # Mettre cette cellule sur une pile
        pile = [(y, x)]

        # Tant que la pile n’est pas vide
        while pile:
            # Prendre la cellule en haut de la pile et l’en retirer
            cellule = pile.pop()

            # Initialisation d'une liste représentant toutes les cellules voisines non-visitées
            cell_not_visited = []
            # On récupère tout les voisins non-visités parmis tout les voisins de la cellule
            for voisin in lab.get_contiguous_cells(cellule):
                if voisin not in cell_visited:
                    cell_not_visited.append(voisin)

            # Si cette cellule a des voisins qui n’ont pas encore été visités
            if cell_not_visited:
                # La remettre sur la pile
                pile.append(cellule)
                # Choisir au hasard l’une de ses cellules contigües qui n’a pas été visitée
                rand_cell = choice(cell_not_visited)
                # Casser le mur entre la cellule et celle qui vient d’être choisie
                lab.remove_wall(cellule, rand_cell)
                # Marquer la cellule qui vient d’être choisie comme visitée
                cell_visited.add(rand_cell)
                # La mettre sur la pile
                pile.append(rand_cell)

        return lab

    @classmethod
    def gen_wilson(cls, h: int, w: int) -> Maze:
        """
        Construit un labyrinthe vide en utilisant la génération par algorithme de Wilson.

        Args:
            h (int): Hauteur du labyrinthe.
            w (int): Largeur du labyrinthe.

        Returns:
            Maze: Une instance de la classe Maze représentant le labyrinthe.
        """

        # Initialisation d’un labyrinthe plein
        lab = cls(h, w, False)

        # Création d'une liste de toutes les cellules
        cell_unvisited = [(i, j) for i in range(h) for j in range(w)]

        # Choisir une cellule au hasard sur la grille
        rand_cell = choice(cell_unvisited)
        # Retirer la cellule choisie de la liste des cellules non-visitées
        cell_unvisited.remove(rand_cell)
        # Marquer cette cellule
        cell_visited = [rand_cell]

        # Tant qu’il reste des cellules non marquées
        while cell_unvisited:
            # Choisir une cellule de départ au hasard, parmi les cellules non marquées
            head = choice(cell_unvisited)

            # Effectuer une marche aléatoire jusqu'à ce qu'une cellule marquée soit atteinte
            # Initialisation d'une marche aux positions de la cellule de départ
            marche = [head]

            # Tant que la cellule actuelle n'est pas marquée
            while head not in cell_visited:
                # Choisir un voisin aléatoirement dans les voisins de la cellule,
                # l'ajouter dans la marche, puis le définir comme cellule actuelle
                voisin = choice(lab.get_contiguous_cells(head))
                marche.append(voisin)
                head = voisin

                # Si la tête du serpent se trouve dans le corps,
                # supprimer toutes les cellules visitées depuis le dernier passage sur la cellule courante
                if head in marche[:-1]:
                    marche = marche[: marche.index(head) + 1]

            # Pour chaque cellule dans la 'marche', on la retire des cellules non-visitées et
            # l'ajoute aux cellules visitées, enfin supprimer le mur entre la cellule[i] et la cellule[i+1] de la marche
            for i in range(len(marche) - 1):
                cell_unvisited.remove(marche[i])
                cell_visited.append(marche[i])
                lab.remove_wall(marche[i], marche[i + 1])

        return lab

    def overlay(self, content: dict = {}) -> str:
        """
        Renvoie une représentation textuelle du labyrinthe avec du contenu dans les cellules en utilisant des caractères ascii.

        Args:
            content (dict, optional): Un dictionnaire où chaque clé est une cellule et chaque valeur est le contenu de la cellule.
                Le contenu est représenté par un caractère.
                Par défaut le dictionnaire est vide.

        Returns:
            str: Le labyrinthe représenté sous forme de chaîne de caractères.
        """

        if not content:
            content = {
                (i, j): " " for i in range(self.height) for j in range(self.width)
            }
        else:
            c = {
                (i, j): " "
                for i in range(self.height)
                for j in range(self.width)
                if (i, j) not in content
            }
            content = {**content, **c}
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width - 1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width - 1):
            txt += (
                " " + content[(0, j)] + " ┃"
                if (0, j + 1) not in self.neighbors[(0, j)]
                else " " + content[(0, j)] + "  "
            )
        txt += " " + content[(0, self.width - 1)] + " ┃\n"
        # Lignes normales
        for i in range(self.height - 1):
            txt += "┣"
            for j in range(self.width - 1):
                txt += "━━━╋" if (i + 1, j) not in self.neighbors[(i, j)] else "   ╋"
            txt += (
                "━━━┫\n"
                if (i + 1, self.width - 1) not in self.neighbors[(i, self.width - 1)]
                else "   ┫\n"
            )
            txt += "┃"
            for j in range(self.width):
                txt += (
                    " " + content[(i + 1, j)] + " ┃"
                    if (i + 1, j + 1) not in self.neighbors[(i + 1, j)]
                    else " " + content[(i + 1, j)] + "  "
                )
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width - 1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt

    def solve_dfs(self, start: tuple, stop: tuple) -> list:
        """
        Retourne le chemin afin de résoudre le labyrinthe selon un parcours en profondeur.

        Args:
            start (tuple): Cellule de départ sous forme d'un couple (x, y).
            stop (tuple): Cellule d'arrivée sous forme d'un couple (x, y).

        Returns:
            list: Une liste de tuples représentant les cellules parcourues pour atteindre la sortie du labyrinthe.
        """

        # Initialisation
        # Placer 'start' dans la struture d’attente, et marquer D
        pile = [start]
        visited = {start: None}

        # Tant qu’il reste des cellules non-marquées
        while pile:
            # Prendre la première cellule et la retirer de la structure
            cell = pile.pop()

            # Si 'cell' correspond à 'stop'
            if cell == stop:
                # Reconstruction du chemin à partir des prédécesseurs
                path = []
                cell = stop
                while cell != start:
                    path.append(cell)
                    cell = visited[cell]

                # Chemin trouvé
                return list(reversed(path))

            # Sinon, pour chaque voisine de 'cell'
            for neighbor in self.get_reachable_cells(cell):
                # Si elle n’est pas marquée
                if neighbor not in visited:
                    # La marquer
                    visited[neighbor] = cell
                    # La mettre dans la structure d’attente
                    pile.append(neighbor)

        # Chemin non-trouvé
        return None

    def solve_bfs(self, start: tuple, stop: tuple) -> list:
        """
        Retourne le chemin afin de résoudre le labyrinthe selon un parcours en largeur.

        Args:
            start (tuple): Cellule de départ sous forme d'un couple (x, y).
            stop (tuple): Cellule d'arrivée sous forme d'un couple (x, y).

        Returns:
            list: Une liste de tuples représentant les cellules parcourues pour atteindre la sortie du labyrinthe.
        """

        # Initialisation
        # Placer 'start' dans la struture d’attente, et marquer D
        file = [start]
        visited = {start: None}

        # Tant qu’il reste des cellules non-marquées
        while file:
            # Prendre la première cellule et la retirer de la structure
            cell = file.pop(0)

            # Si 'cell' correspond à 'stop'
            if cell == stop:
                # Reconstruction du chemin à partir des prédécesseurs
                path = []
                cell = stop
                while cell != start:
                    path.append(cell)
                    cell = visited[cell]

                # Chemin trouvé
                return list(reversed(path))

            # Sinon, pour chaque voisine de 'cell'
            for neighbor in self.get_reachable_cells(cell):
                # Si elle n’est pas marquée
                if neighbor not in visited:
                    # La marquer
                    visited[neighbor] = cell
                    # La mettre dans la structure d’attente
                    file = [neighbor] + file

        # Chemin non-trouvé
        return None

    def solve_rhr(self, start: tuple, stop: tuple) -> list:
        """
        Retourne le chemin afin de résoudre le labyrinthe selon la méthode de résolution en aveugle par main droite.

        Args:
            start (tuple): Cellule de départ sous forme d'un couple (x, y).
            stop (tuple): Cellule d'arrivée sous forme d'un couple (x, y).

        Returns:
            list: Une liste de tuples représentant les cellules parcourues pour atteindre la sortie du labyrinthe.
        """

        # Initialisation
        # Placer 'start' dans la struture d’attente, et marquer D
        pile = [start]
        path = []
        visited = {start: None}

        i = 0

        # Tant qu’il reste des cellules non-marquées
        while pile:
            # Prendre la première cellule et la retirer de la structure
            cell = pile.pop()

            # Si 'cell' correspond à 'stop'
            if cell == stop:
                # Chemin trouvé
                return list(reversed(path))

            # Sinon, on cherche la prochaine cellule à suivre
            neighbors = self.get_reachable_cells(cell)
            x, y = cell

            # Potentielles prochaine cellule
            nord = (x - 1, y)
            est = (x, y + 1)
            sud = (x + 1, y)
            ouest = (x, y - 1)

            directions = [ouest, sud, est, nord]

            next = None

            # Ici on cherche la cellule suivante dans le sens des aiguilles d'une montre
            # en commençant par l'ouest selon l'ordre logique de la main droite
            # 1. 'droite' : ici ouest car on commence vers le 'bas'
            # 2. 'tout droit' : ici sud
            # 3. 'gauche' : est
            # 4. 'demi-tour' : nord
            # On boucle 4 fois (longueur de directions),
            # 1 fois sur chaque direction
            for j in range(0, 4):
                # check_cell correspond à la prochaine cellule dans la direction actuelle,
                # en prenant en compte l'orientation actuelle sur la grille (i)
                # (sens des aiguilles d'une montre).
                # Modulo 4 pour ne pas sortir des limites de 'directions'.
                check_cell = directions[(i + j) % 4]

                # On vérifie ensuite si la cellule check_cell est accessible
                # et si elle n'a pas été visitée.
                if check_cell in neighbors and check_cell not in visited:
                    # Si c'est le cas,
                    # on peut la considérer comme la prochaine cellule à suivre
                    # et on l'assigne à la variable next.
                    next = check_cell

                    # On incrémente également la variable i de j
                    # pour changer l'orientation.
                    i += j

            # Si on a une cellule suivante, on s'y 'déplace' lors de la prochaine itération
            if next:
                # La marquer
                visited[next] = cell
                # La mettre dans la structure d’attente
                pile.append(next)
            # Sinon, on fait 'demi-tour'
            else:
                pile.append(visited[cell])

            path.append(pile[-1])

        # Chemin non-trouvé
        return None

    def distance_geo(self, c1: tuple, c2: tuple) -> int:
        """
        Calcule et retourne la distance géodésique entre deux cellules dans le labyrinthe.

        Args:
            start (tuple): Cellule de départ sous forme d'un couple (x, y).
            stop (tuple): Cellule d'arrivée sous forme d'un couple (x, y).

        Returns:
            int: La distance minimale de déplacements nécessaires pour aller de c1 à c2.
        """

        return len(self.solve_dfs(c1, c2))

    def distance_man(self, c1: tuple, c2: tuple) -> int:
        """
        Calcule et retourne la distance de Manhattan entre 2 cellules.

        C'est à dire le nombre minimal de déplacements nécessaires pour aller de c1 à c2 si le labyrinthe était vide de tout mur.

        Args:
            start (tuple): Cellule de départ sous forme d'un couple (x, y).
            stop (tuple): Cellule d'arrivée sous forme d'un couple (x, y).

        Returns:
            int: La distance de Manhattan entre les deux cellules.
        """

        # On calcule la différence absolue entre les coordonnées verticales (x) des deux cellules
        # On y ajoute la différence absolue entre les coordonnées horizontales (y) des deux cellules
        return abs(c2[0] - c1[0]) + abs(c2[1] - c1[1])
