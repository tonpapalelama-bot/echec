# =============================================================================
# queen.py  –  Séance 3 (squelette) → Séance 5 (isValidMove complet)
# La Reine : combine Tour + Fou (la pièce la plus puissante)
# =============================================================================

from piece import Piece
from position import Position

class Queen(Piece):
    """
    La Reine (Q) combine les mouvements de la Tour et du Fou :
    elle peut se déplacer en ligne droite ou en diagonale sur n'importe quelle distance.
    Elle ne peut pas sauter par-dessus les pièces.
    """

    def __init__(self, position, color):
        super().__init__(position, color)

    def isValidMove(self, newPosition, board):
        """
        Règle de la Reine :
          - Mouvement en ligne droite (comme la Tour) OU en diagonale (comme le Fou)
          - Ne peut pas traverser une pièce
          - Ne peut pas aller sur une case occupée par une pièce alliée
        """
        current = self.get_position()

        col_diff = ord(newPosition.get_column()) - ord(current.get_column())
        row_diff = newPosition.get_row() - current.get_row()

        # Pas de mouvement
        if col_diff == 0 and row_diff == 0:
            return False

        # Vérifier que le mouvement est soit droit, soit diagonal
        # Droit : col_diff=0 ou row_diff=0
        # Diagonal : |col_diff| == |row_diff|
        is_straight  = (col_diff == 0 or row_diff == 0)
        is_diagonal  = (abs(col_diff) == abs(row_diff))

        if not is_straight and not is_diagonal:
            return False  # Mouvement en L ou autre → invalide pour la Reine

        # Vérifier qu'il n'y a pas de pièce alliée à la destination
        target_piece = board.getPiece(newPosition)
        if target_piece is not None and target_piece.get_color() == self.get_color():
            return False

        # --- Vérifier les obstacles sur le chemin ---
        step_col = 0 if col_diff == 0 else (1 if col_diff > 0 else -1)
        step_row = 0 if row_diff == 0 else (1 if row_diff > 0 else -1)

        cur_col = ord(current.get_column()) + step_col
        cur_row = current.get_row() + step_row

        dest_col = ord(newPosition.get_column())
        dest_row = newPosition.get_row()

        while (cur_col, cur_row) != (dest_col, dest_row):
            intermediate = Position(chr(cur_col), cur_row)
            if board.getPiece(intermediate) is not None:
                return False
            cur_col += step_col
            cur_row += step_row

        return True

    def __str__(self):
        return 'Q'
