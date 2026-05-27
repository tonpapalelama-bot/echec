# =============================================================================
# main.py  –  Séance 4
# Point d'entrée du programme – crée un Chess et lance play()
# =============================================================================

from chess_game import Chess

def main():
    """
    Programme principal.
    On importe Chess (pas de copier-coller du code → respecte le cahier des charges).
    On crée une instance et on lance la partie.
    """
    print("╔════════════════════════════════╗")
    print("║    JEU D'ÉCHECS – I1 LISEP     ║")
    print("╚════════════════════════════════╝\n")

    game = Chess()
    game.play()


# Ce bloc s'exécute uniquement si on lance main.py directement
# (pas si on l'importe depuis un autre fichier)
if __name__ == "__main__":
    main()

