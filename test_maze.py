from maze import Maze

laby = Maze(4, 4)
print(laby.info())
print(laby)

laby.neighbors = {
    (0, 0): {(1, 0)},
    (0, 1): {(0, 2), (1, 1)},
    (0, 2): {(0, 1), (0, 3)},
    (0, 3): {(0, 2), (1, 3)},
    (1, 0): {(2, 0), (0, 0)},
    (1, 1): {(0, 1), (1, 2)},
    (1, 2): {(1, 1), (2, 2)},
    (1, 3): {(2, 3), (0, 3)},
    (2, 0): {(1, 0), (2, 1), (3, 0)},
    (2, 1): {(2, 0), (2, 2)},
    (2, 2): {(1, 2), (2, 1)},
    (2, 3): {(3, 3), (1, 3)},
    (3, 0): {(3, 1), (2, 0)},
    (3, 1): {(3, 2), (3, 0)},
    (3, 2): {(3, 1)},
    (3, 3): {(2, 3)},
}

print(laby)

laby.neighbors[(1, 3)].remove((2, 3))
print(laby)
print(laby.info())

# Corrigeons ça :
laby.neighbors[(2, 3)].remove((1, 3))

# Testons maintenant s’il y a un mur entre deux cellules :
c1 = (1, 3)
c2 = (2, 3)
if c1 in laby.neighbors[c2] and c2 in laby.neighbors[c1]:
    print(
        f"Il n'y a pas de mur entre {c1} et {c2} car elles sont mutuellement voisines,\n"
    )
elif c1 not in laby.neighbors[c2] and c2 not in laby.neighbors[c1]:
    print(
        f"Il y a un mur entre {c1} et {c2} car {c1} n'est pas dans le voisinage de {c2} et {c2} n'est pas dans le voisinage de {c1},\n"
    )
else:
    print(f"Il y a une incohérence de réciprocité des voisinages de {c1} et {c2},\n")

# Le même code permet de tester si on peut accéder à une cellule depuis l’autre et vice-versa :
c1 = (1, 3)
c2 = (2, 3)
if c1 in laby.neighbors[c2] and c2 in laby.neighbors[c1]:
    print(f"{c1} est accessible depuis {c2} et vice-versa,\n")
elif c1 not in laby.neighbors[c2] and c2 not in laby.neighbors[c1]:
    print(f"{c1} n'est pas accessible depuis {c2} et vice-versa,\n")
else:
    print(f"Il y a une incohérence de réciprocité des voisinages de {c1} et {c2},\n")

# Parcourons maintenant la grille du labyrinthe pour lister l’ensemble des cellules :
L = []
for i in range(laby.height):
    for j in range(laby.width):
        L.append((i, j))
print(f"Liste des cellules : \n{L}\n")

# Différent test du constructeur, avec la variable 'Empty'
laby = Maze(4, 4, empty=True)
print(laby.info())
print(laby)

laby = Maze(4, 4, empty=False)
print(laby.info())
print(laby)

# Test de la méthode 'add_wall'
laby = Maze(5, 5, empty=True)
laby.add_wall((0, 0), (0, 1))
print("add_wall :\n" + str(laby))

# Test de la méthode 'fill'
laby = Maze(5, 5, empty=True)
laby.fill()
print("fill :\n" + str(laby))

# Test de la méthode 'remove_wall'
laby.remove_wall((0, 0), (0, 1))
print("remove_wall :\n" + str(laby))

# Test de la méthode 'empty'
laby.empty()
print("empty :\n" + str(laby))
laby.add_wall((0, 0), (0, 1))
laby.add_wall((0, 1), (1, 1))
print("empty, suite à l'ajout de 2 nouveaux murs :\n" + str(laby))

# Test de la méthode 'get_walls'
print("Liste des murs voisins (get_walls) :", laby.get_walls())

# Test de la méthode 'get_contiguous_cells'
print("Liste des cellules contigües à c :", laby.get_contiguous_cells((0, 1)))

# Test de la méthode 'get_reachable_cells'
print("Liste des cellule contigües accessibles :", laby.get_reachable_cells((0, 1)))

# Test de la génération par arbre binaire
laby = Maze.gen_btree(4, 4)
print("Génération par arbre binaire :\n" + str(laby))

# Test de la génération 'sidewinder'
laby = Maze.gen_sidewinder(4, 4)
print("Génération sidewinder :\n" + str(laby))

# Test de fusion
laby = Maze.gen_fusion(15, 15)
print("Génération par la fusion : \n" + str(laby))

# Test de l'exploration exhaustive
laby = Maze.gen_exploration(15, 15)
print("Génération par l'exploration exhaustive :\n" + str(laby))

# Test de l'exploration par wilson
laby = Maze.gen_wilson(12, 12)
print("Génération par wilson :\n" + str(laby))

# Test overlay #1
laby = Maze(4, 4, empty=True)
print(
    "Overlay #1 :\n"
    + laby.overlay(
        {
            (0, 0): "c",
            (0, 1): "o",
            (1, 1): "u",
            (2, 1): "c",
            (2, 2): "o",
            (3, 2): "u",
            (3, 3): "!",
        }
    ),
)

# Test overlay #2
laby = Maze(4, 4, empty=True)
path = {
    (0, 0): "@",
    (1, 0): "*",
    (1, 1): "*",
    (2, 1): "*",
    (2, 2): "*",
    (3, 2): "*",
    (3, 3): "§",
}
print("Overlay #2 :\n" + laby.overlay(path))


laby = Maze.gen_fusion(15, 15)

# Test de la résolution en profondeur
solution_dfs = laby.solve_dfs((0, 0), (14, 14))
str_solution = {c: "*" for c in solution_dfs}
str_solution[(0, 0)] = "D"
str_solution[(14, 14)] = "A"
print("Résolution en profondeur :\n" + str(laby.overlay(str_solution)))

# Test de la résolution en largeur
solution_bfs = laby.solve_bfs((0, 0), (14, 14))
str_solution = {c: "*" for c in solution_bfs}
str_solution[(0, 0)] = "D"
str_solution[(14, 14)] = "A"
print("Résolution en largeur :\n" + str(laby.overlay(str_solution)))

print(
    "Les 2 procédés donnent bien le même résultat :",
    solution_dfs == solution_bfs,
    "\n",
)

# Test de la résolution par 'la main droite'
solution_rhr = laby.solve_rhr((0, 0), (14, 14))
str_solution = {c: "*" for c in solution_rhr}
str_solution[(0, 0)] = "D"
str_solution[(14, 14)] = "A"
print("Résolution par 'la main droite' :\n" + str(laby.overlay(str_solution)))

print("Distance géodésique départ-arrivé :", laby.distance_geo((0, 0), (14, 14)))
print("Distance de Manhattan départ-arrivé :", laby.distance_man((0, 0), (14, 14)))
