# =============================================================================
# chess_game.py  –  Séance 4 (intégration) + Séance 5 (isCheckMate complet)
# Classe Chess : chef d'orchestre du jeu, gère la boucle de jeu
# =============================================================================

from board      import Board
from player     import Player
from ai_player  import AIPlayer
from position   import Position

class Chess:
    """
    Classe principale qui gère la partie d'échecs.
    Elle coordonne : le plateau (Board), les joueurs (Player/AIPlayer),
    la validation des coups et la détection de fin de partie.

    Attributs :
      __board         : l'échiquier (Board)
      __players       : liste de 2 joueurs [Player, Player]
      __currentPlayer : le joueur dont c'est le tour
    """

    def __init__(self):
        self.__board         = Board()
        self.__players       = []
        self.__currentPlayer = None

    # =========================================================================
    # Séance 3 – Initialisation
    # =========================================================================

    def initPlayers(self):
        """
        Demande les noms des deux joueurs.
        Si le nom saisi est 'AI' → instancie un AIPlayer au lieu d'un Player.
        Les Blancs jouent toujours en premier.
        """
        print("=== Initialisation des joueurs ===")
        labels = ["Blancs (couleur 0 – jouent en premier)",
                  "Noirs  (couleur 1)"]

        for i, label in enumerate(labels):
            name = input(f"Nom du joueur {label} [tapez 'AI' pour l'ordinateur] : ").strip()
            if name.upper() == "AI":
                self.__players.append(AIPlayer(name, i))
                print(f"  → Joueur IA créé pour les {'Blancs' if i == 0 else 'Noirs'}.")
            else:
                self.__players.append(Player(name, i))

        # Les blancs (index 0) commencent
        self.__currentPlayer = self.__players[0]

    # =========================================================================
    # Séance 4 – Affichage et boucle de jeu
    # =========================================================================

    def displayBoard(self):
        """Affiche l'état actuel du plateau"""
        self.__board.display()

    def switchPlayer(self):
        """Passe la main à l'autre joueur"""
        if self.__currentPlayer is self.__players[0]:
            self.__currentPlayer = self.__players[1]
        else:
            self.__currentPlayer = self.__players[0]

    def parseMove(self, move):
        """
        Analyse la chaîne de mouvement au format "Xrc1 rc2".
        Exemple : "Nb1 c3"
          → piece_type = 'N'
          → from_pos   = Position('b', 1)
          → to_pos     = Position('c', 3)

        Retourne le tuple (piece_type, from_pos, to_pos) ou None si format invalide.
        """
        try:
            parts = move.strip().split()
            if len(parts) != 2:
                return None

            from_str = parts[0]  # ex: "Nb1"
            to_str   = parts[1]  # ex: "c3"

            if len(from_str) < 3 or len(to_str) < 2:
                return None

            piece_type = from_str[0]              # 'N'
            from_col   = from_str[1]              # 'b'
            from_row   = int(from_str[2])         # 1
            to_col     = to_str[0]                # 'c'
            to_row     = int(to_str[1])           # 3

            from_pos = Position(from_col, from_row)
            to_pos   = Position(to_col, to_row)

            return (piece_type, from_pos, to_pos)

        except (IndexError, ValueError):
            return None

    def isValidMove(self, move):
        """
        Vérifie qu'un coup est légal :
          1) Le format de la chaîne est correct
          2) Il existe une pièce du joueur courant à la position source
          3) La pièce peut se déplacer vers la destination selon ses règles
        """
        parsed = self.parseMove(move)
        if parsed is None:
            print("  ✗ Format invalide. Exemple correct : Nb1 c3")
            return False

        piece_type, from_pos, to_pos = parsed

        # Récupérer la pièce sur la case source
        piece = self.__board.getPiece(from_pos)

        if piece is None:
            print(f"  ✗ Aucune pièce en {from_pos}.")
            return False

        if piece.get_color() != self.__currentPlayer.get_color():
            print(f"  ✗ La pièce en {from_pos} n'est pas à vous.")
            return False

        if str(piece) != piece_type:
            print(f"  ✗ La pièce en {from_pos} est '{str(piece)}', pas '{piece_type}'.")
            return False

        if not piece.isValidMove(to_pos, self.__board):
            print(f"  ✗ Déplacement interdit pour {str(piece)} de {from_pos} vers {to_pos}.")
            return False

        return True

    def updateBoard(self, move):
        """
        Applique le mouvement sur le plateau (après validation).
        """
        parsed = self.parseMove(move)
        if parsed:
            _, from_pos, to_pos = parsed
            self.__board.movePiece(from_pos, to_pos)

    # =========================================================================
    # Séance 5 – Détection de l'échec et mat
    # =========================================================================

    def isCheckMate(self):
        """
        Détermine si le joueur COURANT est en échec et mat.
        Algorithme :
          1) Trouver le Roi du joueur courant
          2) Vérifier si une pièce adverse peut capturer ce Roi → est-il en échec ?
          3) Si oui, tester si le Roi peut fuir vers une case non menacée
          4) Si le Roi ne peut fuir nulle part → ÉCHEC ET MAT → True
        """
        columns = 'abcdefgh'
        current_color   = self.__currentPlayer.get_color()
        opponent_color  = 1 - current_color

        # --- Étape 1 : trouver le Roi du joueur courant ---
        king     = None
        king_pos = None
        for col in columns:
            for row in range(1, 9):
                pos = Position(col, row)
                p   = self.__board.getPiece(pos)
                if p is not None and str(p) == 'K' and p.get_color() == current_color:
                    king     = p
                    king_pos = pos

        if king is None:
            return True  # Le Roi a été capturé → fin de partie

        # --- Étape 2 : le Roi est-il en échec ? ---
        def is_attacked(pos):
            """Retourne True si la position pos est menacée par une pièce adverse."""
            for col in columns:
                for row in range(1, 9):
                    p = self.__board.getPiece(Position(col, row))
                    if p is not None and p.get_color() == opponent_color:
                        if p.isValidMove(pos, self.__board):
                            return True
            return False

        if not is_attacked(king_pos):
            return False  # Pas en échec → pas mat

        # --- Étape 3 : le Roi peut-il fuir vers une case sûre ? ---
        for dc in [-1, 0, 1]:
            for dr in [-1, 0, 1]:
                if dc == 0 and dr == 0:
                    continue  # Ignorer la case actuelle
                new_col_ord = ord(king_pos.get_column()) + dc
                new_row     = king_pos.get_row() + dr

                # Vérifier que la nouvelle position est sur l'échiquier
                if not (ord('a') <= new_col_ord <= ord('h') and 1 <= new_row <= 8):
                    continue

                new_pos = Position(chr(new_col_ord), new_row)

                # Vérifier que le Roi peut légalement aller sur cette case
                if not king.isValidMove(new_pos, self.__board):
                    continue

                # Simuler le déplacement du Roi sur new_pos
                captured = self.__board.getPiece(new_pos)
                self.__board.movePiece(king_pos, new_pos)

                # La case new_pos est-elle toujours menacée après le déplacement ?
                still_attacked = is_attacked(new_pos)

                # Annuler la simulation
                self.__board.movePiece(new_pos, king_pos)
                if captured is not None:
                    # Remettre la pièce capturée à sa place
                    self.__board._Board__pieces[str(new_pos)] = captured
                    captured.set_position(new_pos)

                if not still_attacked:
                    return False  # Le Roi peut fuir → pas mat

        return True  # Aucune fuite possible → ÉCHEC ET MAT

    # =========================================================================
    # Sauvegarde / Restauration (contrainte du cahier des charges)
    # =========================================================================

    def save_game(self, filename="sauvegarde.txt"):
        """
        Sauvegarde la partie dans un fichier texte.
        Format de chaque ligne : type_piece,couleur,position
        Exemple : R,0,a1  (Tour blanche en a1)
        """
        with open(filename, 'w', encoding='utf-8') as f:
            # Sauvegarder qui doit jouer
            f.write(f"currentPlayer:{self.__currentPlayer.get_color()}\n")
            # Sauvegarder chaque pièce
            for col in 'abcdefgh':
                for row in range(1, 9):
                    pos   = Position(col, row)
                    piece = self.__board.getPiece(pos)
                    if piece is not None:
                        f.write(f"{str(piece)},{piece.get_color()},{col}{row}\n")
        print(f"  ✓ Partie sauvegardée dans '{filename}'.")

    # =========================================================================
    # Boucle principale du jeu
    # =========================================================================

    def play(self):
        """
        Méthode principale – suit le pseudo-code du cahier des charges :

          Initialisation des joueurs
          Tant qu'il n'y a pas d'échec et mat :
              Afficher le plateau
              Tant que le mouvement n'est pas valide :
                  Demander au joueur courant de bouger une pièce
              Mettre à jour l'échiquier
              Basculer vers l'autre joueur
        """
        self.initPlayers()

        print("\n╔══════════════════════════════════════╗")
        print("║       JEU D'ÉCHECS – Début !         ║")
        print("║  Format : Xrc1 rc2  (ex: Nb1 c3)    ║")
        print("║  'save' pour sauvegarder             ║")
        print("║  'quit' pour abandonner              ║")
        print("╚══════════════════════════════════════╝\n")

        while not self.isCheckMate():
            self.displayBoard()
            color_label = "Blancs" if self.__currentPlayer.get_color() == 0 else "Noirs"
            print(f"Tour de {self.__currentPlayer.get_name()} ({color_label})")

            move_valid = False
            while not move_valid:
                # L'IA génère son coup automatiquement
                if isinstance(self.__currentPlayer, AIPlayer):
                    move = self.__currentPlayer.askMove(self.__board)
                    print(f"  L'IA joue : {move}")
                else:
                    move = self.__currentPlayer.askMove()

                if move.lower() == 'quit':
                    print("Partie abandonnée.")
                    return
                if move.lower() == 'save':
                    self.save_game()
                    continue

                move_valid = self.isValidMove(move)

            self.updateBoard(move)
            self.switchPlayer()

        # Fin de partie
        print("\n╔══════════════════════════════╗")
        print("║       ÉCHEC ET MAT !         ║")
        print("╚══════════════════════════════╝")
        # Le gagnant est celui qui vient de jouer (l'autre a le roi en échec)
        winner = self.__players[1 - self.__currentPlayer.get_color()]
        print(f"Félicitations à {winner.get_name()} – vous avez gagné !\n")
