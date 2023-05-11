import arcade
from constants import WINDOW_WIDTH, WINDOW_HEIGHT


class Wall(arcade.SpriteSolidColor):
    """
    Mur d'un labyrinthe.
    """

    def __init__(
        self,
        center_x: int,
        center_y: int,
        width: int,
        height: int,
        color: arcade.Color = arcade.color.WHITE,
    ) -> None:
        """Crée une nouvelle instance de la classe Wall.

        Args:
            center_x (int): La position x du centre du mur.
            center_y (int): La position y du centre du mur.
            width (int): La largeur du mur.
            height (int): La hauteur du mur.
            color (arcade.Color, optional): La couleur du mur. Par défaut, la couleur est arcade.color.WHITE.
        """

        # Appel du constructeur parent
        super().__init__(width, height, color)

        self.center_x = center_x
        self.center_y = center_y
