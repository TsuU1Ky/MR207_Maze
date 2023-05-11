from arcade.color import WHITE

# Titre de la fenêtre du jeu
SCREEN_TITLE = "MAZE BALL"

# Dimensions de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Taille du labyrinthe
MAZE_WIDTH = 10
MAZE_HEIGHT = 10

# Couleur par défaut
DEFAULT_COLOR = WHITE

# Taille d'une cellule
# CELL_SIZE = arrondie de la taille d'une cellule pour le plus petit Maze,
# multiplier par le ratio de la taille d'une cellule du plus grand Maze,
# divisé par la taille actuelle du Maze
CELL_SIZE = int(round(70 * 7.14 / MAZE_HEIGHT))

# Épaisseur d'un mur
WALL_THICKNESS = int(round(CELL_SIZE / 10))

# Rayon de la bille
MARBLE_RADIUS = int(CELL_SIZE / 2 * (1 - 0.25))

# Vitesse de rotation
ROTATION = 1


# Constantes liées au moteur physique

# Gravité
GRAVITY = 1500

# Amortissement - Vitesse perdue par seconde
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4

# Élasticité des murs
WALL_ELASTICITY = 0

# Friction entre les objets
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7

# Masse
PLAYER_MASS = 1.0

# Moment d'inertie
MOMENT_OF_INERTIA = (1 / 5) * PLAYER_MASS * MARBLE_RADIUS**2

# Limite de la vitesse
PLAYER_MAX_HORIZONTAL_SPEED = 1000
PLAYER_MAX_VERTICAL_SPEED = 1000
