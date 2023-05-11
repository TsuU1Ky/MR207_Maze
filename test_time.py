from maze import Maze
import time

# Test de la génération par arbre binaire
tmps = 0
for _ in range(100):
    deb = time.time()
    laby = Maze.gen_btree(25, 25)
    tmps += time.time() - deb

print("Temps moyen de génération par arbre binaire : ", round(tmps / 100, 3), " s")

# Test de la génération 'sidewinder'
tmps = 0
for _ in range(100):
    deb = time.time()
    laby = Maze.gen_sidewinder(25, 25)
    tmps += time.time() - deb

print("Temps moyen de génération par sidewinder : ", round(tmps / 100, 3), " s")

# Test de fusion
tmps = 0
for _ in range(100):
    deb = time.time()
    laby = Maze.gen_fusion(25, 25)
    tmps += time.time() - deb

print("Temps moyen de génération par fusion : ", round(tmps / 100, 3), " s")

# Test de l'exploration exhaustive
tmps = 0
for _ in range(100):
    deb = time.time()
    laby = Maze.gen_exploration(25, 25)
    tmps += time.time() - deb

print(
    "Temps moyen de génération par exploration exhaustive : ",
    round(tmps / 100, 3),
    " s",
)

# Test l'exploration par wilson
tmps = 0
for _ in range(100):
    deb = time.time()
    laby = Maze.gen_wilson(25, 25)
    tmps += time.time() - deb

print("Temps moyen de génération par wilson : ", round(tmps / 100, 3), " s")
