# =============================================================================
# position.py  –  Séance 3
# Représente une case de l'échiquier (ex: e4, a1, h8)
# =============================================================================

class Position:
    on('e', 4) représente la case e4
    """

    def __init__(self, column, row):
        # Les attributs sont privés (__ = encapsulation)
        self.__column = column  # ex: 'e'
        self.__row = row        # ex: 4

    # --- Getters (lire les attributs privés depuis l'extérieur) ---

    def get_column(self):
        """Retourne la colonne (lettre)"""
        return self.__column

    def get_row(self):
        """Retourne la ligne (entier)"""
        return self.__row

    # --- Setters (modifier les attributs avec validation) ---

    def set_column(self, column):
        """Modifie la colonne uniquement si elle est valide (a-h)"""
        if column in 'abcdefgh':
            self.__column = column

    def set_row(self, row):
        """Modifie la ligne uniquement si elle est valide (1-8)"""
        if 1 <= row <= 8:
            self.__row = row

    def __str__(self):
        """
        Redéfinition de __str__ : retourne la position sous forme lisible.
        Exemple : str(Position('e', 4)) → 'e4'
        """
        return f"{self.__column}{self.__row}"

    def __eq__(self, other):
        """
        Permet de comparer deux positions avec == .
        Exemple : Position('e',4) == Position('e',4) → True
        """
        if isinstance(other, Position):
            return self.__column == other.__column and self.__row == other.__row
        return False

    def __hash__(self):
        """Nécessaire pour utiliser des Position comme clés de dictionnaire"""
        return hash((self.__column, self.__row))

