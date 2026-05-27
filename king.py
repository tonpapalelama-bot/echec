# =============================================================================
# king.py  –  Séance 3 (squelette) → Séance 5 (isValidMove complet)
# Le Roi : se déplace d'une seule case dans toutes les directions
# =============================================================================

from piece import Piece

class King(Piece):
    """
    Le Roi (K) peut se déplacer d'exactement 1 case dans n'importe quelle direction
    (horizontal, vertical ou diagonal), à condition que la case d'arrivée ne soit
    pas occupée par une pièce de même couleur.
    """

    def __init__(self, position, color):
        # On appelle le constructeur de la classe parente (Piece)
        super().__init__(position, color)

    def isValidMove(self, newPosition, board):
        """
        Règle du Roi :
          - Au maximum 1 case d'écart en colonne ET en ligne
          - Ne peut pas rester sur place
          - Ne peut pas aller sur une case occupée par une pièce alliée
        """
        current = self.get_position()

        # Calculer la différence de colonne (les lettres se convertissent en entiers avec ord())
        # ord('a')=97, ord('b')=98, ... donc ord('c')-ord('a') = 2
        col_diff = abs(ord(newPosition.get_column()) - ord(current.get_column()))
        row_diff = abs(newPosition.get_row() - current.get_row())

        # Le roi doit bouger d'au plus 1 case dans chaque direction
        if col_diff > 1 or row_diff > 1:  #horizontale et verticale 
            return False

        # Interdit de rester sur place
        if col_diff == 0 and row_diff == 0:
            return False

        # Vérifier qu'il n'y a pas une pièce alliée sur la case d'arrivée
        target_piece = board.getPiece(newPosition)
        if target_piece is not None and target_piece.get_color() == self.get_color():
            return False

        return True

    def __str__(self):
        return 'K'

