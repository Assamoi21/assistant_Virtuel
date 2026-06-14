# Assistant Virtuel 🎙️

Un assistant vocal en français tournant sous Windows, capable d'écouter vos commandes, de parler, de rechercher des informations et d'ouvrir des applications.

## Fonctionnalités

- Salutation adaptée à l'heure (matin / après-midi / soir)
- Recherche Wikipedia en français
- Recherche Google vocale
- Météo en temps réel (OpenWeatherMap)
- Heure et date en français
- Ouverture de sites web (YouTube, Google, Facebook, GitHub, Gmail, Stack Overflow)
- Lecture de musique locale
- Envoi d'emails via Gmail
- Commande d'aide listant toutes les fonctions

## Prérequis

- Windows 10 / 11
- [uv](https://docs.astral.sh/uv/) (gestionnaire Python)
- Microphone + haut-parleurs

## Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/Assamoi21/assistant_Virtuel.git
cd assistant_Virtuel

# 2. Créer l'environnement virtuel Python 3.11
uv venv .venv --python 3.11

# 3. Installer les dépendances
uv pip install pyttsx3 SpeechRecognition wikipedia requests python-dotenv pyaudio --python .venv\Scripts\python.exe
```

## Configuration

Copiez le fichier `.env` et remplissez vos informations :

```env
EMAIL_ADDRESS=votre_email@gmail.com
EMAIL_PASSWORD=votre_mot_de_passe_application
EMAIL_DESTINATAIRE=ami@gmail.com
MUSIC_DIR=C:\Users\VotreNom\Music
WEATHER_API_KEY=votre_cle_openweathermap
WEATHER_CITY=Abidjan
```

> **Note :** Pour `EMAIL_PASSWORD`, utilisez un [mot de passe d'application Gmail](https://myaccount.google.com/apppasswords), pas votre mot de passe principal.
> Pour `WEATHER_API_KEY`, créez un compte gratuit sur [openweathermap.org](https://openweathermap.org).

## Lancement

```bash
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location 'chemin\vers\assistant'; .venv\Scripts\python.exe assistant_virtuel.py"
```

## Commandes vocales

| Dites...                  | Action                              |
|---------------------------|-------------------------------------|
| `météo`                   | Météo de la ville configurée        |
| `météo à Lyon`            | Météo d'une ville précise           |
| `quelle heure`            | Annonce l'heure actuelle            |
| `quelle date`             | Annonce la date du jour             |
| `wikipedia [sujet]`       | Résumé Wikipedia en français        |
| `cherche [sujet]`         | Recherche Google                    |
| `ouvre youtube`           | Ouvre YouTube dans le navigateur    |
| `ouvre google`            | Ouvre Google                        |
| `ouvre facebook`          | Ouvre Facebook                      |
| `ouvre github`            | Ouvre GitHub                        |
| `ouvre gmail`             | Ouvre Gmail                         |
| `ouvre stack overflow`    | Ouvre Stack Overflow                |
| `musique`                 | Lance le premier fichier musical    |
| `email`                   | Envoie un email au destinataire     |
| `aide`                    | Liste toutes les commandes          |
| `au revoir` / `quitter`   | Ferme l'assistant                   |

## Dépendances

| Package          | Rôle                              |
|------------------|-----------------------------------|
| pyttsx3          | Synthèse vocale (text-to-speech)  |
| SpeechRecognition| Reconnaissance vocale             |
| PyAudio          | Accès au microphone               |
| wikipedia        | Recherche Wikipedia               |
| requests         | Appels API météo                  |
| python-dotenv    | Chargement du fichier .env        |
