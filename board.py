# =============================================================================
# board.py  –  Séance 3
# L'échiquier : contient toutes les pièces et gère leurs positions
# =============================================================================

from position import Position
from king    import King
from queen   import Queen
from bishop  import Bishop
from knight  import Knight
from rook    import Rook
from pawn    import Pawn

class Board:
    """
    Représente l'état complet de l'échiquier.

    Structure de données principale :
      __pieces : DICTIONNAIRE  { str(position) → Piece }
      Exemple  : { 'e1': <King blanc>, 'e8': <King noir>, 'e4': None (case vide) }

      → On utilise un dictionnaire car la recherche par clé est O(1) (très rapide).
        La clé est la représentation textuelle de la position (ex: 'e4').
    """

    def __init__(self):
        # Le dictionnaire des pièces (clé = "colonne+ligne", valeur = instance de Piece)
        self.__pieces = {}
        self.__setup_initial_position()

    def __setup_initial_position(self):
        """
        Place toutes les 32 pièces à leur position initiale.
        Blancs  → rangées 1 (pièces) et 2 (pions)
        Noirs   → rangées 8 (pièces) et 7 (pions)
        """

        # ── Pièces BLANCHES (color = 0) ────────────────────────────────────
        self.__pieces['a1'] = Rook(Position('a', 1), 0)
        self.__pieces['b1'] = Knight(Position('b', 1), 0)
        self.__pieces['c1'] = Bishop(Position('c', 1), 0)
        self.__pieces['d1'] = Queen(Position('d', 1), 0)
        self.__pieces['e1'] = King(Position('e', 1), 0)
        self.__pieces['f1'] = Bishop(Position('f', 1), 0)
        self.__pieces['g1'] = Knight(Position('g', 1), 0)
        self.__pieces['h1'] = Rook(Position('h', 1), 0)

        for col in 'abcdefgh':
            self.__pieces[f'{col}2'] = Pawn(Position(col, 2), 0)

        # ── Pièces NOIRES (color = 1) ───────────────────────────────────────
        self.__pieces['a8'] = Rook(Position('a', 8), 1)
        self.__pieces['b8'] = Knight(Position('b', 8), 1)
        self.__pieces['c8'] = Bishop(Position('c', 8), 1)
        self.__pieces['d8'] = Queen(Position('d', 8), 1)
        self.__pieces['e8'] = King(Position('e', 8), 1)
        self.__pieces['f8'] = Bishop(Position('f', 8), 1)
        self.__pieces['g8'] = Knight(Position('g', 8), 1)
        self.__pieces['h8'] = Rook(Position('h', 8), 1)

        for col in 'abcdefgh':
            self.__pieces[f'{col}7'] = Pawn(Position(col, 7), 1)

    # --- Méthodes du cahier des charges ---

    def getPiece(self, position):
        """
        Retourne la pièce à la position donnée.
        Retourne None si la case est vide.
        Exemple : board.getPiece(Position('e', 1)) → King blanc
        """
        key = str(position)          # Convertit Position('e',1) en 'e1'
        return self.__pieces.get(key, None)

    def getPosition(self, piece):
        """
        Retourne la position d'une pièce.
        Retourne None si la pièce a été capturée (elle n'est plus dans le dictionnaire).
        On parcourt le dictionnaire pour trouver la pièce.
        """
        for key, p in self.__pieces.items():
            if p is piece:  # 'is' compare les références (même objet en mémoire)
                return p.get_position()
        return None

    def movePiece(self, oldPosition, newPosition):
        """
        Déplace une pièce de oldPosition vers newPosition.
        Si une pièce adverse occupe newPosition, elle est capturée (supprimée du dict).
        Met aussi à jour la position interne de la pièce.
        """
        key_old = str(oldPosition)
        key_new = str(newPosition)

        if key_old in self.__pieces:
            piece = self.__pieces.pop(key_old)  # Retire la pièce de l'ancienne case
            piece.set_position(newPosition)      # Met à jour sa position interne
            self.__pieces[key_new] = piece       # La place sur la nouvelle case
            # Si une pièce adverse était sur key_new, elle est écrasée → capturée

    def display(self):
        """
        Affiche l'échiquier en mode texte dans le terminal.
        Convention : MAJUSCULE = pièce blanche, minuscule = pièce noire, '.' = case vide.
        """
        print("\n    a   b   c   d   e   f   g   h")
        print("  +---+---+---+---+---+---+---+---+")
        for row in range(8, 0, -1):  # De la ligne 8 (haut) à la ligne 1 (bas)
            print(f"{row} |", end="")
            for col in 'abcdefgh':
                piece = self.getPiece(Position(col, row))
                if piece is None:
                    symbol = '.'
                elif piece.get_color() == 0:
                    symbol = str(piece)          # Blanc → majuscule (K, Q, R...)
                else:
                    symbol = str(piece).lower()  # Noir  → minuscule (k, q, r...)
                print(f" {symbol} |", end="")
            print(f" {row}")
        print("  +---+---+---+---+---+---+---+---+")
        print("    a   b   c   d   e   f   g   h\n")
