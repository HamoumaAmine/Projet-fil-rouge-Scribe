"""Scribe — point d'entrée en ligne de commande.

Usage : python -m src.main <chemin_audio>
Enchaîne transcription puis compte rendu (JSON mode), affiche le résultat et
sauvegarde deux fichiers datés : un .json structuré et un .md lisible.
"""

import sys
import os
import json
from datetime import datetime

from src.config import check_config
from src.transcription import transcrire
from src.summary import resumer, json_vers_markdown


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
        data = resumer(transcription)
    except FileNotFoundError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)

    markdown = json_vers_markdown(data)

    # Affichage à l'écran
    print("\n--- Compte rendu ---\n")
    print(markdown)

    # Sauvegarde des deux fichiers datés
    os.makedirs("comptes_rendus", exist_ok=True)
    horodatage = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base = os.path.join("comptes_rendus", f"compte_rendu_{horodatage}")

    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"\nCompte rendu sauvegardé dans :\n- {base}.json\n- {base}.md")


if __name__ == "__main__":
    main()