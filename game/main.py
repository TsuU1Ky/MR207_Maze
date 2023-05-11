import arcade, math
from constants import *
from marble import Marble
from wall import Wall
from wincell import WinCell
from maze import Maze


class Game(arcade.Window):
    """
    Fenêtre principale.
    """

    def __init__(self) -> None:
        """
        Crée une nouvelle instance de la classe Game.
        """

        # Appel du constructeur parent
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, SCREEN_TITLE)

        self.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

        # Liste contenant les sprites
        self.marble_list = None
        self.wall_list = None
        self.special_cells_list = None

        # Bille
        self.marble = None

        # État des 2 touches de rotation
        self.left_pressed = False
        self.right_pressed = False

        # Représentation interne du labyrinthe
        self.maze = None

        # Case d'arrivée
        self.win_cell = None

        self.physics_engine = None

        arcade.set_background_color(arcade.color.BLACK)

    def make_borders(self, x: int, y: int) -> None:
        """
        Crée les murs qui entourent la zone de jeu.

        Args:
            x (int): La position en x où les murs doivent commencer.
            y (int): La position en y où les murs doivent commencer.
        """

        # Mur ouest
        wall = Wall(
            x,
            y + (MAZE_HEIGHT * CELL_SIZE) / 2,
            WALL_THICKNESS,
            CELL_SIZE * MAZE_HEIGHT,
        )
        self.wall_list.append(wall)

        # Mur est
        wall = Wall(
            WINDOW_WIDTH - x,
            y + (MAZE_HEIGHT * CELL_SIZE) / 2,
            WALL_THICKNESS,
            CELL_SIZE * MAZE_HEIGHT,
        )
        self.wall_list.append(wall)

        # Mur nord
        wall = Wall(
            x + (MAZE_WIDTH * CELL_SIZE) / 2,
            WINDOW_HEIGHT - y,
            CELL_SIZE * MAZE_WIDTH,
            WALL_THICKNESS,
        )
        self.wall_list.append(wall)

        # Mur sud
        wall = Wall(
            x + (MAZE_WIDTH * CELL_SIZE) / 2,
            y,
            CELL_SIZE * MAZE_WIDTH,
            WALL_THICKNESS,
        )
        self.wall_list.append(wall)

    def make_walls(self, x: int, y: int, walls: list) -> None:
        """
        Crée les murs intérieurs du labyrinthe.

        Args:
            x (int): La position en x où les murs doivent commencer.
            y (int): La position en y où les murs doivent commencer.
            walls (list): La liste des coordonnées des murs dans le labyrinthe.
        """

        for wall in walls:
            # On remet le x/y dans l'ordre logique du plan cartésien par rapport à ce qui est fait dans maze.py
            y1, x1 = wall[0]
            y2, x2 = wall[1]

            wall = None

            # Si x a un écart non nul supérieur à celui de y,
            # le mur est vertical
            if abs(x2 - x1) > abs(y2 - y1):
                wall = Wall(
                    x + CELL_SIZE + (CELL_SIZE * min(x1, x2)),
                    y - (CELL_SIZE / 2) - (CELL_SIZE * min(y1, y2)),
                    WALL_THICKNESS,
                    CELL_SIZE,
                )

            # Sinon y a un écart non nul supérieur à celui de x,
            # le mur est horizontal
            else:
                wall = Wall(
                    x + (CELL_SIZE / 2) + (CELL_SIZE * min(x1, x2)),
                    y - CELL_SIZE - (CELL_SIZE * min(y1, y2)),
                    CELL_SIZE,
                    WALL_THICKNESS,
                )

            self.wall_list.append(wall)

    def get_rotated(self) -> None:
        """
        Fait tourner le labyrinthe.

        Rotation dans le sens horaire (FLÈCHE DROITE).
        Rotation dans le sens anti-horaire (FLÈCHE GAUCHE).
        """

        # Si aucune rotation n'est appliquée, on a une différence de 0 soit aucun changement
        delta_angle = 0

        # Si FLÈCHE GAUCHE est pressée et pas FLÈCHE DROITE
        if self.left_pressed and not self.right_pressed:
            # On ajoute la rotation à l'angle de différence
            delta_angle += ROTATION
        # Sinon si FLÈCHE DROITE est pressée et pas FLÈCHE GAUCHE
        elif self.right_pressed and not self.left_pressed:
            # On soustrait la rotation à l'angle de différence
            delta_angle -= ROTATION

        # Pour chaque mur des murs du labyrinthe
        for wall in self.wall_list:
            wall_physics = self.physics_engine.get_physics_object(wall)

            # Fait tourner le sprite pendant que sa position est déplacée
            wall_physics.body.angle += math.radians(delta_angle)

            # Déplace le sprite le long d'un cercle centré autour du centre de la fenêtre
            wall_physics.body.position = tuple(
                arcade.rotate_point(
                    wall_physics.body.position[0],
                    wall_physics.body.position[1],
                    self.center[0],
                    self.center[1],
                    delta_angle,
                )
            )

            if wall.collides_with_sprite(self.marble):
                self.physics_engine.step(resync_sprites=True)

        for special_cell in self.special_cells_list:
            special_cell_physics = self.physics_engine.get_physics_object(special_cell)

            # Fait tourner le sprite pendant que sa position est déplacée
            special_cell_physics.body.angle += math.radians(delta_angle)

            # Déplace le sprite le long d'un cercle centré autour du centre de la fenêtre
            special_cell_physics.body.position = tuple(
                arcade.rotate_point(
                    special_cell_physics.body.position[0],
                    special_cell_physics.body.position[1],
                    self.center[0],
                    self.center[1],
                    delta_angle,
                )
            )

    def setup(self) -> None:
        """
        Effectue la configuration initiale du jeu.

        Appeler cette fonction pour redémarrer le jeu.
        """

        # Création des SpriteLists
        self.marble_list = arcade.SpriteList()
        self.special_cells_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # On prévoit un espace entre la bordure de la fenêtre et celle du labyrinthe
        start_x = int((WINDOW_WIDTH - (CELL_SIZE * MAZE_WIDTH)) / 2)
        start_y = int((WINDOW_HEIGHT - (CELL_SIZE * MAZE_HEIGHT)) / 2)

        # Création du labyrinthe
        self.maze = Maze.gen_wilson(MAZE_WIDTH, MAZE_HEIGHT)

        # Création de l'enceinte du labyrinthe
        self.make_borders(start_x, start_y)

        # Obtention des murs du labyrinthe
        maze_walls = self.maze.get_walls()

        # On 'remonte' le curseur au coin supérieur gauche du labyrinthe
        start_y += CELL_SIZE * MAZE_HEIGHT

        # Création de la bille
        self.marble = Marble(start_x + CELL_SIZE / 2, start_y - CELL_SIZE / 2, 0.1)

        self.marble_list.append(self.marble)

        # Création des murs internes du labyrinthe
        self.make_walls(start_x, start_y, maze_walls)

        self.win_cell = WinCell(
            start_x + CELL_SIZE * MAZE_WIDTH - CELL_SIZE / 2,
            WINDOW_HEIGHT - start_y + CELL_SIZE / 2,
            int(CELL_SIZE - WALL_THICKNESS),
            int(CELL_SIZE - WALL_THICKNESS),
        )

        self.special_cells_list.append(self.win_cell)

        # --- Pymunk Physics Engine Setup ---

        # La valeur par défaut du damping (amortissement) pour chaque objet contrôle le pourcentage de vélocité que l'objet conservera chaque seconde. Une valeur de 1,0 correspond à aucune perte de vitesse, 0,9 correspond à 10% par seconde, 0,1 correspond à 90% par seconde.
        # Pour les jeux en vue de dessus, il s'agit essentiellement du frottement pour les objets en mouvement. Pour les jeux de plateforme avec gravité, cette valeur devrait probablement être définie à 1,0.
        # La valeur par défaut est 1,0 si elle n'est pas spécifiée.
        damping = DEFAULT_DAMPING

        # Définir la gravité. (0, 0) est bon pour l'espace et la vue de dessus.
        gravity = (0, -GRAVITY)

        # Créer le moteur physique
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=damping, gravity=gravity
        )

        # Ajouter le joueur.
        # Pour le joueur, nous définissons un damping plus faible, ce qui augmente le taux d'amortissement. Cela empêche le personnage de se déplacer trop loin après que le joueur a relâché les touches de mouvement.
        # En définissant le moment sur PymunkPhysicsEngine.MOMENT_INF, nous empêchons la rotation.
        # La friction se situe normalement entre 0 (pas de friction) et 1,0 (friction élevée).
        # La friction est entre deux objets en contact. Il est important de se rappeler
        # dans les jeux en vue de dessus que la friction se déplaçant le long du 'sol' est contrôlée par l'amortissement.
        self.physics_engine.add_sprite(
            self.marble,
            friction=PLAYER_FRICTION,
            mass=PLAYER_MASS,
            moment_of_inertia=MOMENT_OF_INERTIA,
            collision_type="player",
            max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
            max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED,
        )

        # Créer les murs.
        # En définissant le type de corps sur PymunkPhysicsEngine.STATIC, les murs ne peuvent pas se déplacer.
        # Les objets mobiles qui répondent aux forces sont PymunkPhysicsEngine.DYNAMIC.
        # Les objets PymunkPhysicsEngine.KINEMATIC se déplaceront, mais on suppose qu'ils seront repositionnés par le code et ne répondent pas aux forces physiques.
        # Dynamique est la valeur par défaut.
        self.physics_engine.add_sprite_list(
            self.wall_list,
            friction=WALL_FRICTION,
            collision_type="wall",
            body_type=arcade.PymunkPhysicsEngine.KINEMATIC,
        )

        # Créer les cellules spéciales.
        # En définissant le type de corps sur PymunkPhysicsEngine.STATIC, les murs ne peuvent pas se déplacer.
        # Les objets mobiles qui répondent aux forces sont PymunkPhysicsEngine.DYNAMIC.
        # Les objets PymunkPhysicsEngine.KINEMATIC se déplaceront, mais on suppose qu'ils seront repositionnés par le code et ne répondent pas aux forces physiques.
        # Dynamique est la valeur par défaut.
        self.physics_engine.add_sprite_list(
            self.special_cells_list,
            friction=0.0,
            collision_type="special_cell",
            body_type=arcade.PymunkPhysicsEngine.KINEMATIC,
        )

    def on_draw(self) -> None:
        """
        Rendu de l'écran.

        Efface l'écran et le background, puis dessine les sprites à l'écran.
        """

        # Clear l'écran et le background
        self.clear()

        # Dessine les sprites à l'écran
        self.wall_list.draw()
        self.special_cells_list.draw()
        self.marble_list.draw()

    def on_update(self, delta_time: float):
        """
        Met à jour le mouvement et la logique du jeu.

        Exécuté à chaque image du jeu.

        Args:
            delta_time (float): Temps écoulé depuis la dernière mise à jour.
        """

        # On met à jour les rotations des murs
        self.get_rotated()

        self.physics_engine.step(delta_time)

        # Condition de victoire
        if self.marble.collides_with_sprite(self.win_cell):
            self.setup()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Appelée à chaque fois qu'une touche est pressée.

        Args:
            key (int): Touche pressée.
            modifiers (int): Bitwise AND des modifiers (shift, ctrl, num lock) pressés.
        """
        # Si le joueur presse une touche, effectuer une rotation.
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key: int, modifiers: int) -> None:
        """
        Appelée à chaque fois qu'une touche est relachée.

        Args:
            key (int): Touche pressée.
            modifiers (int): Bitwise AND des modifiers (shift, ctrl, num lock) pressés.
        """

        # Si le joueur relache une touche, arrêter la rotation.
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


def main():
    """
    Fonction principale.

    Initialise une nouvelle instance de la classe Game et lance le jeu.
    """

    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
