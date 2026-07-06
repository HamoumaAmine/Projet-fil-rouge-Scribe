"""Génération d'un compte rendu structuré via l'API chat completions de Groq."""

import os
from groq import Groq
from src.config import GROQ_API_KEY, LLM_MODEL

CHEMIN_PROMPT = "prompts/systeme_compte_rendu.txt"


def _charger_prompt_systeme():
    """Charge le prompt système depuis son fichier texte."""
    if not os.path.isfile(CHEMIN_PROMPT):
        raise FileNotFoundError(f"Prompt système introuvable : {CHEMIN_PROMPT}")
    with open(CHEMIN_PROMPT, "r", encoding="utf-8") as f:
        return f.read()


def resumer(transcription):
    """Reçoit une transcription brute et retourne un compte rendu structuré.

    Lève RuntimeError si l'appel à l'API échoue.
    """
    prompt_systeme = _charger_prompt_systeme()
    client = Groq(api_key=GROQ_API_KEY)

    try:
        reponse = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": prompt_systeme},
                {"role": "user", "content": transcription},
            ],
            temperature=0.2,
        )
        return reponse.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'appel à l'API de compte rendu : {e}")


if __name__ == "__main__":
    from src.transcription import transcrire
    print("Transcription en cours...")
    texte = transcrire("audio_examples/reunion_test.mp3")
    print("Rédaction du compte rendu en cours...")
    compte_rendu = resumer(texte)
    print("\n--- Compte rendu ---\n")
    print(compte_rendu)