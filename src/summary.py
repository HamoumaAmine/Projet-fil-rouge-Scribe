"""Génération d'un compte rendu structuré via l'API chat completions de Groq.

Le LLM répond en JSON (JSON mode). resumer() retourne un dictionnaire structuré ;
json_vers_markdown() reconstruit un compte rendu Markdown lisible à partir de ce dict.
"""

import os
import json
from groq import Groq
from src.config import GROQ_API_KEY, LLM_MODEL

CHEMIN_PROMPT = "prompts/systeme_compte_rendu.txt"


def _charger_prompt_systeme():
    if not os.path.isfile(CHEMIN_PROMPT):
        raise FileNotFoundError(f"Prompt système introuvable : {CHEMIN_PROMPT}")
    with open(CHEMIN_PROMPT, "r", encoding="utf-8") as f:
        return f.read()


def resumer(transcription):
    """Reçoit une transcription brute et retourne un compte rendu structuré (dict).

    Le LLM est appelé en JSON mode. Lève RuntimeError si l'appel ou le parsing échoue.
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
            response_format={"type": "json_object"},
        )
        contenu = reponse.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'appel à l'API de compte rendu : {e}")

    try:
        return json.loads(contenu)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Réponse du LLM non conforme au JSON attendu : {e}")


def json_vers_markdown(data):
    """Reconstruit un compte rendu Markdown lisible à partir du dict structuré."""
    lignes = []
    lignes.append(f"# {data.get('titre', 'Compte rendu')}")
    lignes.append("")
    lignes.append("## Résumé")
    lignes.append(data.get("resume", ""))
    lignes.append("")
    lignes.append("## Points clés")
    for point in data.get("points_cles", []):
        lignes.append(f"- {point}")
    lignes.append("")
    lignes.append("## Décisions et actions")
    for action in data.get("decisions_actions", []):
        lignes.append(f"- {action}")
    return "\n".join(lignes)


if __name__ == "__main__":
    from src.transcription import transcrire
    print("Transcription en cours...")
    texte = transcrire("audio_examples/reunion_test.mp3")
    print("Rédaction du compte rendu en cours...")
    data = resumer(texte)
    print("\n--- JSON ---\n")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print("\n--- Markdown ---\n")
    print(json_vers_markdown(data))