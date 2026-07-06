"""Scribe — point d'entrée en ligne de commande.

Usage : python -m src.main <chemin_audio>
Enchaîne transcription puis compte rendu, affiche et sauvegarde le résultat.
"""

import sys
import os
from datetime import datetime

from src.config import check_config
from src.transcription import transcrire
from src.summary import resumer


def main():
    check_config()

    if len(sys.argv) < 2:
        print("Usage : python -m src.main <chemin_audio>", file=sys.stderr)
        sys.exit(1)

    chemin_audio = sys.argv[1]

    try:
        print(f"[1/2] Transcription de {chemin_audio} en cours...")
        transcription = transcrire(chemin_audio)

        print("[2/2] Rédaction du compte rendu en cours...")
        compte_rendu = resumer(transcription)
    except FileNotFoundError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)

    print("\n--- Compte rendu ---\n")
    print(compte_rendu)

    os.makedirs("comptes_rendus", exist_ok=True)
    horodatage = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    chemin_sortie = os.path.join("comptes_rendus", f"compte_rendu_{horodatage}.md")
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        f.write(compte_rendu)

    print(f"\nCompte rendu sauvegardé dans : {chemin_sortie}")


if __name__ == "__main__":
    main()