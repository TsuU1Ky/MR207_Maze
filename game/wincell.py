import arcade


class WinCell(arcade.SpriteSolidColor):
    """
    Case d'arrivée
    """

    def __init__(
        self,
        center_x: int,
        center_y: int,
        width: int,
        height: int,
        color: arcade.Color = arcade.color.GREEN,
    ) -> None:
        """Crée une nouvelle instance de la classe WinCell.

        Args:
            center_x (int): La position x du centre de la case.
            center_y (int): La position y du centre de la case.
            width (int): La largeur de la case.
            height (int): La hauteur de la case.
            color (arcade.Color, optional): La couleur de la case. Par défaut, la couleur est arcade.color.GREEN.
        """

        # Appel du constructeur parent
        super().__init__(width, height, color)

        self.center_x = center_x
        self.center_y = center_y
