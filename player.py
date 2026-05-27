# =============================================================================
# player.py  –  Séance 3
# Un joueur humain : possède un nom, une couleur, et saisit ses coups
# =============================================================================

class Player:
    """
    Représente un joueur humain.
    Attributs :
      - name  : chaîne de caractères (prénom / pseudo)
      - color : 0 = Blancs, 1 = Noirs
    """

    def __init__(self, name, color):
        self.__name  = name   # Nom du joueur
        self.__color = color  # 0 = blanc, 1 = noir

    # --- Getters ---

    def get_name(self):
        return self.__name

    def get_color(self):
        return self.__color

    def askMove(self):
        """
        Demande au joueur de saisir son coup au clavier.

        Format attendu : "Xrc1 rc2"
          X   = type de pièce (K, Q, B, N, R, P)
          rc1 = case de départ  (ex: b1)
          rc2 = case d'arrivée  (ex: c3)

        Exemples valides :
          'Nb1 c3'  → Cavalier de b1 vers c3
          'Pe2 e4'  → Pion de e2 vers e4
          'Re1 e5'  → Tour de e1 vers e5
        """
        color_label = "Blancs" if self.__color == 0 else "Noirs"
        move = input(f"[{color_label}] {self.__name} → entrez votre coup (ex: Nb1 c3) : ")
        return move.strip()

    def __str__(self):
        return self.__name

