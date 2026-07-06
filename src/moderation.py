"""Agent de modération : détecte les tentatives de détournement de l'outil."""

import os
import json
from groq import Groq
from src.config import GROQ_API_KEY, LLM_MODEL

CHEMIN_PROMPT = "prompts/systeme_moderation.txt"


def _charger_prompt():
    if not os.path.isfile(CHEMIN_PROMPT):
        raise FileNotFoundError(f"Prompt de modération introuvable : {CHEMIN_PROMPT}")
    with open(CHEMIN_PROMPT, "r", encoding="utf-8") as f:
        return f.read()


def moderer(transcription):
    """Analyse la transcription. Retourne un dict {legitime: bool, raison: str}."""
    prompt_systeme = _charger_prompt()
    contenu_utilisateur = f"<transcription>\n{transcription}\n</transcription>"
    client = Groq(api_key=GROQ_API_KEY)

    try:
        reponse = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": prompt_systeme},
                {"role": "user", "content": contenu_utilisateur},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
        contenu = reponse.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'appel à l'API de modération : {e}")

    try:
        return json.loads(contenu)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Réponse de modération non conforme au JSON attendu : {e}")


if __name__ == "__main__":
    from src.transcription import transcrire
    texte = transcrire("audio_examples/reunion_test.mp3")
    print(json.dumps(moderer(texte), ensure_ascii=False, indent=2))