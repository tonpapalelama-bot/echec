# =============================================================================
# ai_player.py  –  Séance 5
# Joueur artificiel : hérite de Player, génère des coups aléatoires valides
# =============================================================================

import random
from player import Player
from position import Position

class AIPlayer(Player):
    """
    Sous-classe de Player dont la méthode askMove() est automatique.
    L'IA cherche un coup valide parmi toutes ses pièces de manière aléatoire.

    Héritage : AIPlayer → Player
    On redéfinit (override) uniquement askMove().
    """

    def __init__(self, name, color):
        # On appelle le constructeur du parent (Player)
        super().__init__(name, color)

    def askMove(self, board=None):
        """
        Génère automatiquement un coup pour l'IA.
        - Si board est fourni → cherche un coup VALIDE parmi les pièces de l'IA
        - Sinon (fallback)   → génère deux positions totalement aléatoires
        """
        if board is not None:
            return self.__generate_valid_move(board)
        return self.__generate_random_move()

    def __generate_valid_move(self, board):
        """
        Stratégie de l'IA : parcourt toutes ses pièces dans un ordre aléatoire
        et retourne le premier coup valide trouvé.
        """
        columns = 'abcdefgh'

        # Collecter toutes les pièces appartenant à l'IA (même couleur)
        my_pieces = []
        for col in columns:
            for row in range(1, 9):
                pos = Position(col, row)
                piece = board.getPiece(pos)
                if piece is not None and piece.get_color() == self.get_color():
                    my_pieces.append(piece)

        # Mélanger pour que l'IA ne joue pas toujours la même pièce
        random.shuffle(my_pieces)

        # Pour chaque pièce, tester toutes les destinations possibles
        all_positions = [Position(c, r) for c in columns for r in range(1, 9)]

        for piece in my_pieces:
            random.shuffle(all_positions)
            for new_pos in all_positions:
                if piece.isValidMove(new_pos, board):
                    src = piece.get_position()
                    # Retourner le coup au format "Xrc1 rc2"
                    return f"{str(piece)}{src} {new_pos}"

        # Aucun coup valide trouvé → fallback aléatoire
        return self.__generate_random_move()

    def __generate_random_move(self):
        """
        Génère deux positions aléatoires sans vérifier la validité.
        C'est la version SIMPLIFIÉE demandée au début (séance 3).
        """
        piece_types = ['K', 'Q', 'B', 'N', 'R', 'P']
        piece_type = random.choice(piece_types)
        col1 = random.choice('abcdefgh')
        row1 = random.randint(1, 8)
        col2 = random.choice('abcdefgh')
        row2 = random.randint(1, 8)
        return f"{piece_type}{col1}{row1} {col2}{row2}"

    def __str__(self):
        return f"IA ({self.get_name()})"
