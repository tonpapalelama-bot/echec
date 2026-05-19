# ============================================================================= 
# bishop.py  –  Séance 3 (squelette) → Séance 5 (isValidMove complet)
# Le Fou : se déplace en diagonale sur n'importe quelle distance
# =============================================================================

from piece import Piece
from position import Position

class Bishop(Piece):
    """
    Le Fou (B) se déplace uniquement en diagonale, sur n'importe quelle distance.
    Il ne peut pas sauter par-dessus les pièces.
    Un Fou reste toujours sur les cases de la même couleur.
    """

    def __init__(self, position, color):
        super().__init__(position, color)

    def isValidMove(self, newPosition, board):
        """
        Règle du Fou :
          - La différence de colonne doit être ÉGALE à la différence de ligne
            (ex: de c1 à f4 → 3 colonnes et 3 lignes = diagonal)
          - Ne peut pas traverser une pièce sur son chemin
          - Ne peut pas aller sur une case occupée par une pièce alliée
        """
        current = self.get_position()

        col_diff = ord(newPosition.get_column()) - ord(current.get_column())
        row_diff = newPosition.get_row() - current.get_row()

        # Pas de mouvement
        if col_diff == 0 and row_diff == 0:
            return False

        # Mouvement diagonal uniquement : |col_diff| doit être égal à |row_diff|
        if abs(col_diff) != abs(row_diff):
            return False

        # Vérifier qu'il n'y a pas de pièce alliée à la destination
        target_piece = board.getPiece(newPosition)
        if target_piece is not None and target_piece.get_color() == self.get_color():
            return False

        # --- Vérifier les obstacles sur le chemin diagonal ---
        step_col = 1 if col_diff > 0 else -1
        step_row = 1 if row_diff > 0 else -1

        cur_col = ord(current.get_column()) + step_col
        cur_row = current.get_row() + step_row

        dest_col = ord(newPosition.get_column())
        dest_row = newPosition.get_row()

        while (cur_col, cur_row) != (dest_col, dest_row):
            intermediate = Position(chr(cur_col), cur_row)
            if board.getPiece(intermediate) is not None:
                return False  # Une pièce bloque le chemin diagonal
            cur_col += step_col
            cur_row += step_row

        return True

    def __str__(self):
        return 'B'
