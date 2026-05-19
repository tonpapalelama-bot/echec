# =============================================================================
# rook.py  –  Séance 3 (squelette) → Séance 5 (isValidMove complet)
# La Tour : se déplace en ligne droite (horizontal ou vertical)
# =============================================================================

from piece import Piece
from position import Position

class Rook(Piece):
    """
    La Tour (R) se déplace en ligne droite sur n'importe quelle distance,
    horizontalement ou verticalement. Elle ne peut pas sauter par-dessus les pièces.
    """

    def __init__(self, position, color):
        super().__init__(position, color)

    def isValidMove(self, newPosition, board):
        """
        Règle de la Tour :
          - Se déplace uniquement sur la même ligne (row) ou la même colonne (column)
          - Ne peut pas traverser une pièce sur son chemin
          - Ne peut pas aller sur une case occupée par une pièce alliée
        """
        current = self.get_position()

        col_diff = ord(newPosition.get_column()) - ord(current.get_column())
        row_diff = newPosition.get_row() - current.get_row()

        # Pas de mouvement
        if col_diff == 0 and row_diff == 0:
            return False

        # La Tour doit rester sur la même ligne OU la même colonne
        # Si les deux diffèrent → mouvement diagonal ou oblique → invalide
        if col_diff != 0 and row_diff != 0:
            return False

        # Vérifier qu'il n'y a pas de pièce alliée à la destination
        target_piece = board.getPiece(newPosition)
        if target_piece is not None and target_piece.get_color() == self.get_color():
            return False

        # --- Vérifier qu'il n'y a pas d'obstacle sur le chemin ---
        # step_col / step_row : direction du déplacement (-1, 0 ou +1)
        step_col = 0 if col_diff == 0 else (1 if col_diff > 0 else -1)
        step_row = 0 if row_diff == 0 else (1 if row_diff > 0 else -1)

        # On part de la case suivante et on avance jusqu'à la case juste avant la destination
        cur_col = ord(current.get_column()) + step_col
        cur_row = current.get_row() + step_row

        dest_col = ord(newPosition.get_column())
        dest_row = newPosition.get_row()

        while (cur_col, cur_row) != (dest_col, dest_row):
            intermediate = Position(chr(cur_col), cur_row)
            if board.getPiece(intermediate) is not None:
                return False  # Une pièce bloque le chemin
            cur_col += step_col
            cur_row += step_row

        return True

    def __str__(self):
        return 'R'
