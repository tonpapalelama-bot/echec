# =============================================================================
# knight.py  –  Séance 3 (squelette) → Séance 5 (isValidMove complet)
# Le Cavalier : se déplace en L, seule pièce qui saute par-dessus les autres
# =============================================================================

from piece import Piece

class Knight(Piece):
    """
    Le Cavalier (N) se déplace en forme de L :
      - 2 cases dans une direction puis 1 case perpendiculaire
      - OU 1 case dans une direction puis 2 cases perpendiculaires
    C'est la SEULE pièce qui peut sauter par-dessus les autres → pas besoin
    de vérifier les obstacles sur le chemin.
    """

    def __init__(self, position, color):
        super().__init__(position, color)

    def isValidMove(self, newPosition, board):
        """
        Règle du Cavalier :
          - (col_diff, row_diff) doit être (±2, ±1) ou (±1, ±2)
          - Peut sauter par-dessus d'autres pièces (aucune vérification du chemin)
          - Ne peut pas aller sur une case occupée par une pièce alliée
        """
        current = self.get_position()

        col_diff = abs(ord(newPosition.get_column()) - ord(current.get_column()))
        row_diff = abs(newPosition.get_row() - current.get_row())

        # Mouvement en L : (2,1) ou (1,2) uniquement
        valid_l_move = (col_diff == 2 and row_diff == 1) or (col_diff == 1 and row_diff == 2)
        if not valid_l_move:
            return False

        # Vérifier qu'il n'y a pas de pièce alliée à la destination
        target_piece = board.getPiece(newPosition)
        if target_piece is not None and target_piece.get_color() == self.get_color():
            return False

        # Pas de vérification du chemin → le Cavalier saute !
        return True

    def __str__(self):
        return 'N'

