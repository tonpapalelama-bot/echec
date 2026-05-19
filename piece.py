# =============================================================================
# piece.py  –  Séance 3
# Classe abstraite : tous les types de pièces héritent d'elle
# =============================================================================

from abc import ABC, abstractmethod

class Piece(ABC):
    """
    Classe ABSTRAITE représentant une pièce d'échecs.
    On ne peut pas instancier Piece directement → on doit passer par King, Pawn, etc.

    Attributs communs à TOUTES les pièces :
      - position : objet Position
      - color    : 0 = blanc, 1 = noir
    """

    def __init__(self, position, color):
        self.__position = position  # de type Position
        self.__color = color        # 0 = blanc, 1 = noir

    # --- Getters ---

    def get_position(self):
        """Retourne la position actuelle de la pièce"""
        return self.__position

    def get_color(self):
        """Retourne la couleur (0=blanc, 1=noir)"""
        return self.__color

    # --- Setter ---

    def set_position(self, position):
        """Met à jour la position de la pièce (utilisé après un déplacement)"""
        self.__position = position

    # --- Méthodes abstraites (OBLIGATOIRES dans chaque sous-classe) ---

    @abstractmethod
    def isValidMove(self, newPosition, board):
        """
        Vérifie si le déplacement vers newPosition est légal.
        Chaque type de pièce a ses propres règles → à redéfinir dans chaque sous-classe.
        newPosition : Position de destination
        board       : le plateau (Board) pour vérifier les obstacles
        Retourne True si le coup est valide, False sinon.
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Retourne l'identifiant en une lettre :
        K=Roi  Q=Reine  B=Fou  N=Cavalier  R=Tour  P=Pion
        """
        pass
