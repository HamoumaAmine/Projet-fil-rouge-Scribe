"""Transcription audio via l'API Speech-to-Text de Groq."""

import os
from groq import Groq
from src.config import GROQ_API_KEY, STT_MODEL


def transcrire(chemin_audio):
    """Recoit le chemin d'un fichier audio et retourne sa transcription texte.

    Leve FileNotFoundError si le fichier n'existe pas.
    Leve RuntimeError si l'appel a l'API echoue.
    """
    if not os.path.isfile(chemin_audio):
        raise FileNotFoundError(f"Fichier audio introuvable : {chemin_audio}")

    client = Groq(api_key=GROQ_API_KEY)

    try:
        with open(chemin_audio, "rb") as f:
            reponse = client.audio.transcriptions.create(
                file=(os.path.basename(chemin_audio), f.read()),
                model=STT_MODEL,
            )
        return reponse.text
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'appel a l'API de transcription : {e}")


if __name__ == "__main__":
    chemin = "audio_examples/reunion_test.mp3"
    print("Transcription en cours...")
    texte = transcrire(chemin)
    print("\n--- Transcription ---")
    print(texte)