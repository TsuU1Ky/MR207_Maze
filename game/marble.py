import arcade


class Marble(arcade.Sprite):
    """
    Bille dans le labyrinthe.
    """

    def __init__(self, center_x: int, center_y: int, scale: float = 0.1) -> None:
        """Crée une nouvelle instance de la classe Marble.

        Args:
            center_x (int): La position x du centre de la bille.
            center_y (int): La position y du centre de la bille.
            scale (float): Taille du sprite.
        """

        # Appel du constructeur parent
        super().__init__(
            "./img/FrontBoll.png",
            scale=scale,
            center_x=center_x,
            center_y=center_y,
            hit_box_algorithm="Detailed",
        )
