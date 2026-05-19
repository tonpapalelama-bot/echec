# =============================================================================
# pawn.py  –  Séance 3 (squelette) → Séance 5 (isValidMove complet)
# Le Pion : avance d'1 ou 2 cases, capture en diagonale
# =============================================================================

from piece import Piece
from position import Position

class Pawn(Piece):
    """
    Le Pion (P) est la pièce la plus simple mais avec des règles particulières :
      - Avance d'1 case vers l'avant (si la case est libre)
      - Peut avancer de 2 cases depuis sa position de départ (si les 2 cases sont libres)
      - Capture uniquement en diagonale d'1 case vers l'avant
      - Les Blancs avancent vers les rangs croissants (row 1 → 8)
      - Les Noirs avancent vers les rangs décroissants (row 8 → 1)
    Note : la promotion des pions n'est PAS demandée dans ce projet.
    """

    def __init__(self, position, color):
        super().__init__(position, color)

    def isValidMove(self, newPosition, board):
        """
        Règles du Pion :
          1) Avancer d'1 case en ligne droite → case d'arrivée VIDE
          2) Avancer de 2 cases depuis la ligne de départ → les 2 cases VIDES
          3) Capturer en diagonale d'1 case → pièce ADVERSE sur la case d'arrivée
        """
        current = self.get_position()

        col_diff = ord(newPosition.get_column()) - ord(current.get_column())
        row_diff = newPosition.get_row() - current.get_row()

        # La direction dépend de la couleur :
        #   Blanc (0) → avance vers les lignes croissantes (+1)
        #   Noir  (1) → avance vers les lignes décroissantes (-1)
        direction = 1 if self.get_color() == 0 else -1

        # Ligne de départ : 2 pour les blancs, 7 pour les noirs
        start_row = 2 if self.get_color() == 0 else 7

        # --- Cas 1 : avance d'1 case en ligne droite ---
        if col_diff == 0 and row_diff == direction:
            # La case doit être vide (le pion ne capture pas devant lui !)
            if board.getPiece(newPosition) is None:
                return True

        # --- Cas 2 : avance de 2 cases depuis la position initiale ---
        if col_diff == 0 and row_diff == 2 * direction and current.get_row() == start_row:
            # La case intermédiaire ET la case d'arrivée doivent être vides
            intermediate = Position(current.get_column(), current.get_row() + direction)
            if board.getPiece(intermediate) is None and board.getPiece(newPosition) is None:
                return True

        # --- Cas 3 : capture en diagonale ---
        if abs(col_diff) == 1 and row_diff == direction:
            target = board.getPiece(newPosition)
            # Il doit y avoir une pièce ADVERSE sur la case diagonale
            if target is not None and target.get_color() != self.get_color():
                return True

        return False

    def __str__(self):
        return 'P'
