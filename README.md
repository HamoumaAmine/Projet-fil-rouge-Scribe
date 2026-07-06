# Scribe

Scribe est un outil en ligne de commande qui transforme un enregistrement audio
(réunion, cours, note vocale) en compte rendu écrit et structuré.

## Fonctionnement

1. L'utilisateur fournit un fichier audio.
2. Un modèle de transcription (Speech-to-Text) convertit l'audio en texte brut.
3. Un LLM reformule ce texte en compte rendu structuré : titre, points clés,
   décisions, actions.

4. Avant de rédiger le compte rendu, un agent de modération analyse la transcription et
rejette poliment les contenus qui tentent de détourner l'outil de sa fonction (par
exemple des instructions d'injection). Cet agent est lui-même protégé contre l'injection
de prompt en traitant la transcription comme une donnée à analyser, jamais comme des
instructions à exécuter.

Les modèles sont appelés via l'API serverless de Groq.

## Structure du projet

- `src/` : code source de Scribe
- `prompts/` : prompts système utilisés par le LLM
- `audio_examples/` : fichiers audio d'exemple pour les tests

## Installation

Cloner le dépôt :

    git clone https://github.com/HamoumaAmine/Projet-fil-rouge-Scribe.git
    cd Projet-fil-rouge-Scribe

Créer et activer un environnement virtuel :

    python -m venv venv
    source venv/Scripts/activate

Installer les dépendances :

    pip install -r requirements.txt

Configurer la clé API : copier `.env.example` vers `.env` et y renseigner votre
clé `GROQ_API_KEY` obtenue sur https://console.groq.com.

## Utilisation

Lancer Scribe en lui donnant un fichier audio :

    python -m src.main audio_examples/reunion_test.mp3

Scribe transcrit l'audio, génère un compte rendu structuré (titre, résumé, points
clés, décisions et actions), l'affiche à l'écran et le sauvegarde dans le dossier `comptes_rendus/`.

Le compte rendu est produit par le LLM en JSON mode (réponse JSON structurée), puis
sauvegardé sous deux formes datées dans `comptes_rendus/` : un fichier `.json`
structuré (titre, résumé, points clés, décisions/actions) et un fichier `.md` lisible
reconstruit à partir de ce JSON.

## Réponses aux questions

**Q1 — Pourquoi le .gitignore doit-il exister avant d'écrire du code manipulant des secrets ?**
Pour garantir qu'aucune clé API ne soit jamais ajoutée accidentellement à l'historique
Git. Une fois un secret commité, il reste dans l'historique même après suppression du
fichier, et devient très difficile à effacer complètement. Ignorer .env dès le départ
supprime ce risque.

**Q2 — Quels modèles STT et LLM choisissez-vous et pourquoi ?**
STT : whisper-large-v3-turbo — bon compromis vitesse/qualité/coût pour transcrire
réunions et notes vocales, plus rapide que whisper-large-v3 à précision proche.
LLM : llama-3.3-70b-versatile — performant en rédaction structurée (titre, points clés,
décisions), servi rapidement par Groq à coût raisonnable.
Les deux identifiants sont centralisés dans src/config.py.

**Q3 — Que renvoie l'API en plus du texte ?**
Avec response_format='verbose_json', l'API renvoie, en plus du texte :
- task : le type d'opération (transcribe)
- language : la langue détectée automatiquement (ici French)
- duration : la durée de l'audio en secondes
- segments : le texte découpé en segments horodatés (start/end), avec pour chacun des
  indicateurs de confiance (avg_logprob, no_speech_prob, compression_ratio)
- x_groq : l'identifiant de la requête

Utilité pour une évolution future de Scribe : les horodatages permettraient de générer
des comptes rendus avec renvois temporels (ex : "décision prise à 00:05"), la langue
détectée permettrait un traitement multilingue, et les indicateurs de confiance
pourraient signaler les passages mal transcrits à vérifier.

**Q4 — Quelle température choisissez-vous pour cet usage, et pourquoi ?**
Température basse (0.2). Pour un compte rendu, on veut un résultat fidèle, factuel et
reproductible, pas de la créativité. Une température basse rend le modèle plus
déterministe et réduit le risque qu'il invente ou reformule de façon hasardeuse. Une
température élevée conviendrait à de la génération créative, ce qui n'est pas le cas ici.

**Q5 — Le prompt système est envoyé à chaque requête : quel lien avec les tokens en cache ?**
Le prompt système est identique et volumineux à chaque appel. Les fournisseurs comme Groq
peuvent mettre en cache le préfixe commun des requêtes (prompt caching) : les tokens du
prompt système, réutilisés à l'identique, n'ont pas à être recalculés intégralement à
chaque fois. Cela réduit la latence et le coût. D'où l'intérêt de garder un prompt système
stable et placé en tête de requête : plus le préfixe est constant, plus le cache est
efficace. À l'inverse, modifier le prompt système à chaque appel casserait ce cache.
