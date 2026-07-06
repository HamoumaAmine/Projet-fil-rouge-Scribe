"""Configuration centralisée de Scribe.

Charge les secrets depuis .env et expose les reglages du projet.
Les noms de modeles ne sont definis qu'ici, a un seul endroit.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

STT_MODEL = "whisper-large-v3-turbo"
LLM_MODEL = "llama-3.3-70b-versatile"


def check_config():
    """Verifie que la configuration est valide, sinon arrete le programme
    avec un message clair plutot qu'un plantage cryptique plus tard."""
    if not GROQ_API_KEY:
        print(
            "Erreur : la variable GROQ_API_KEY est absente.\n"
            "Cree un fichier .env a la racine du projet a partir de .env.example, "
            "et renseigne ta cle API Groq.",
            file=sys.stderr,
        )
        sys.exit(1)
