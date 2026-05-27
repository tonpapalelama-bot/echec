# =============================================================================
# test_chess.py  –  Séance 3 (tests unitaires avec le framework unittest)
# Lance avec : python -m pytest test_chess.py  ou  python test_chess.py
# =============================================================================

import unittest
from position import Position
from board    import Board
from king     import King
from queen    import Queen
from bishop   import Bishop
from knight   import Knight
from rook     import Rook
from pawn     import Pawn


# =============================================================================
# Tests de la classe Position
# =============================================================================
class TestPosition(unittest.TestCase):

    def test_str_retourne_position(self):
        """__str__ doit retourner 'e4' pour colonne='e' et ligne=4"""
        pos = Position('e', 4)
        self.assertEqual(str(pos), 'e4')

    def test_egalite_deux_positions(self):
        """Deux positions avec mêmes colonne et ligne doivent être égales"""
        self.assertEqual(Position('a', 1), Position('a', 1))

    def test_inegalite(self):
        """Deux positions différentes ne sont pas égales"""
        self.assertNotEqual(Position('a', 1), Position('b', 1))

    def test_getters(self):
        """Les getters doivent retourner les bonnes valeurs"""
        pos = Position('h', 8)
        self.assertEqual(pos.get_column(), 'h')
        self.assertEqual(pos.get_row(), 8)


# =============================================================================
# Tests du Cavalier (Knight)
# =============================================================================
class TestKnight(unittest.TestCase):

    def setUp(self):
        """setUp est appelé avant chaque test : prépare un plateau initial"""
        self.board = Board()

    def test_deplacement_valide_L(self):
        """Le cavalier en b1 peut aller en c3 (L = 1 colonne + 2 lignes)"""
        knight = self.board.getPiece(Position('b', 1))
        self.assertTrue(knight.isValidMove(Position('c', 3), self.board))

    def test_deplacement_valide_L2(self):
        """Le cavalier en b1 peut aller en a3 (L = 1 colonne + 2 lignes, autre direction)"""
        knight = self.board.getPiece(Position('b', 1))
        self.assertTrue(knight.isValidMove(Position('a', 3), self.board))

    def test_deplacement_invalide_ligne_droite(self):
        """Le cavalier ne peut pas se déplacer en ligne droite"""
        knight = self.board.getPiece(Position('b', 1))
        self.assertFalse(knight.isValidMove(Position('b', 3), self.board))

    def test_ne_capture_pas_allie(self):
        """Le cavalier ne peut pas aller sur une case occupée par une pièce alliée"""
        knight = self.board.getPiece(Position('b', 1))
        # d2 est un pion blanc → même couleur que le cavalier b1
        self.assertFalse(knight.isValidMove(Position('d', 2), self.board))

    def test_peut_sauter_par_dessus(self):
        """Le cavalier PEUT sauter par-dessus d'autres pièces"""
        # Au départ, g1 est un cavalier blanc et f1/h1 sont ocupées
        # Le cavalier g1 peut aller en f3 malgré les pions f2
        knight = self.board.getPiece(Position('g', 1))
        self.assertTrue(knight.isValidMove(Position('f', 3), self.board))


# =============================================================================
# Tests de la Tour (Rook)
# =============================================================================
class TestRook(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_bloquee_au_depart(self):
        """La tour a1 est bloquée par le pion a2 → ne peut pas avancer"""
        rook = self.board.getPiece(Position('a', 1))
        self.assertFalse(rook.isValidMove(Position('a', 5), self.board))

    def test_ne_se_deplace_pas_en_diagonal(self):
        """La tour ne peut pas se déplacer en diagonale"""
        rook = self.board.getPiece(Position('a', 1))
        self.assertFalse(rook.isValidMove(Position('b', 2), self.board))


# =============================================================================
# Tests du Fou (Bishop)
# =============================================================================
class TestBishop(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_bloque_au_depart(self):
        """Le fou c1 est bloqué par les pions b2 et d2"""
        bishop = self.board.getPiece(Position('c', 1))
        self.assertFalse(bishop.isValidMove(Position('e', 3), self.board))

    def test_mouvement_non_diagonal_invalide(self):
        """Le fou ne peut pas se déplacer en ligne droite"""
        bishop = self.board.getPiece(Position('c', 1))
        self.assertFalse(bishop.isValidMove(Position('c', 4), self.board))


# =============================================================================
# Tests du Pion (Pawn)
# =============================================================================
class TestPawn(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_avance_une_case(self):
        """Le pion blanc e2 peut avancer d'une case en e3"""
        pawn = self.board.getPiece(Position('e', 2))
        self.assertTrue(pawn.isValidMove(Position('e', 3), self.board))

    def test_avance_deux_cases_depart(self):
        """Le pion blanc e2 peut avancer de deux cases en e4 depuis sa position initiale"""
        pawn = self.board.getPiece(Position('e', 2))
        self.assertTrue(pawn.isValidMove(Position('e', 4), self.board))

    def test_ne_recule_pas(self):
        """Le pion blanc ne peut pas reculer"""
        pawn = self.board.getPiece(Position('e', 2))
        self.assertFalse(pawn.isValidMove(Position('e', 1), self.board))

    def test_ne_capture_pas_case_vide(self):
        """Le pion ne peut pas capturer en diagonale si la case est vide"""
        pawn = self.board.getPiece(Position('e', 2))
        self.assertFalse(pawn.isValidMove(Position('f', 3), self.board))

    def test_ne_passe_pas_par_dessus(self):
        """Le pion ne peut pas avancer de 2 cases si la case intermédiaire est occupée"""
        # Place un pion en e3 pour bloquer e2→e4
        from pawn import Pawn
        blocking_pawn = Pawn(Position('e', 3), 1)
        self.board._Board__pieces['e3'] = blocking_pawn
        pawn = self.board.getPiece(Position('e', 2))
        self.assertFalse(pawn.isValidMove(Position('e', 4), self.board))


# =============================================================================
# Tests du plateau (Board)
# =============================================================================
class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_roi_blanc_en_e1(self):
        """Le Roi blanc doit être en e1 au départ"""
        king = self.board.getPiece(Position('e', 1))
        self.assertIsNotNone(king)
        self.assertEqual(str(king), 'K')
        self.assertEqual(king.get_color(), 0)

    def test_roi_noir_en_e8(self):
        """Le Roi noir doit être en e8 au départ"""
        king = self.board.getPiece(Position('e', 8))
        self.assertIsNotNone(king)
        self.assertEqual(king.get_color(), 1)

    def test_case_vide_au_milieu(self):
        """e4 doit être vide au début de la partie"""
        self.assertIsNone(self.board.getPiece(Position('e', 4)))

    def test_deplacement_pion(self):
        """Déplacer le pion de e2 à e4 → e2 vide, e4 occupée"""
        self.board.movePiece(Position('e', 2), Position('e', 4))
        self.assertIsNone(self.board.getPiece(Position('e', 2)))
        self.assertIsNotNone(self.board.getPiece(Position('e', 4)))

    def test_capture(self):
        """Placer une pièce adverse sur une case et la capturer"""
        # On déplace un pion blanc en e4 puis un pion noir en d5, puis on capture
        self.board.movePiece(Position('e', 2), Position('e', 4))
        self.board.movePiece(Position('d', 7), Position('d', 5))
        # Le pion blanc e4 capture en d5
        self.board.movePiece(Position('e', 4), Position('d', 5))
        piece = self.board.getPiece(Position('d', 5))
        self.assertIsNotNone(piece)
        self.assertEqual(piece.get_color(), 0)  # C'est maintenant le pion blanc


# =============================================================================
# Point d'entrée
# =============================================================================
if __name__ == '__main__':
    # verbose=2 affiche le détail de chaque test
    unittest.main(verbosity=2)

