import pyttsx3           # pip install pyttsx3
import speech_recognition as sr  # pip install SpeechRecognition
import datetime
import wikipedia           # pip install wikipedia
import webbrowser
import os
import smtplib
import requests            # pip install requests
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()

# --- Configuration depuis .env ---
EMAIL_ADDRESS      = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD     = os.getenv("EMAIL_PASSWORD")
EMAIL_DESTINATAIRE = os.getenv("EMAIL_DESTINATAIRE")
MUSIC_DIR          = os.getenv("MUSIC_DIR", "C:\\Users\\Public\\Music")
WEATHER_API_KEY    = os.getenv("WEATHER_API_KEY")
WEATHER_CITY       = os.getenv("WEATHER_CITY", "Paris")

# --- Sites web ouverts par commande vocale ---
SITES = {
    'youtube':        'https://youtube.com',
    'google':         'https://google.com',
    'facebook':       'https://facebook.com',
    'stack overflow': 'https://stackoverflow.com',
    'github':         'https://github.com',
    'gmail':          'https://mail.google.com',
}

# --- Initialisation de la voix ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # voices[0]=homme, voices[1]=femme
engine.setProperty('rate', 170)


def speak(audio):
    print(f"Assistant : {audio}")
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Bonjour !")
    elif hour < 18:
        speak("Bon après-midi !")
    else:
        speak("Bonsoir !")
    speak("Je suis votre assistant virtuel. Comment puis-je vous aider ?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Écoute en cours...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        print("Reconnaissance en cours...")
        query = r.recognize_google(audio, language='fr-FR')
        print(f"Vous avez dit : {query}\n")
    except sr.UnknownValueError:
        print("Je n'ai pas compris, répétez s'il vous plaît...")
        return "none"
    except sr.RequestError:
        speak("Erreur de connexion au service de reconnaissance vocale.")
        return "none"
    return query


def get_weather(city):
    if not WEATHER_API_KEY:
        return "Clé API météo non configurée dans le fichier .env"
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=fr"
        )
        data = requests.get(url, timeout=5).json()
        if data.get("cod") != 200:
            return f"Ville introuvable : {city}"
        desc  = data['weather'][0]['description']
        temp  = data['main']['temp']
        feels = data['main']['feels_like']
        return f"{city} : {desc}, {temp}°C, ressenti {feels}°C"
    except Exception as e:
        return f"Impossible d'obtenir la météo : {e}"


def sendEmail(to, content):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("Identifiants email manquants dans le fichier .env")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, to, content)
    server.close()


def open_site(query):
    for site, url in SITES.items():
        if f'ouvre {site}' in query or f'open {site}' in query:
            webbrowser.open(url)
            speak(f"J'ouvre {site}")
            return True
    return False


if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand().lower()

        if query == "none":
            continue

        # --- Quitter ---
        if any(w in query for w in ['quitter', 'au revoir', 'stop', 'exit', 'quit']):
            speak("Au revoir ! À bientôt.")
            break

        # --- Wikipedia ---
        elif 'wikipedia' in query:
            try:
                speak("Je recherche sur Wikipedia...")
                terme = query.replace("wikipedia", "").strip()
                if not terme:
                    speak("Précisez ce que vous voulez rechercher sur Wikipedia.")
                else:
                    wikipedia.set_lang("fr")
                    results = wikipedia.summary(terme, sentences=2)
                    speak("Selon Wikipedia :")
                    print(results)
                    speak(results)
            except wikipedia.exceptions.DisambiguationError:
                speak("Votre recherche est trop vague. Soyez plus précis.")
            except wikipedia.exceptions.PageError:
                speak("Aucun résultat trouvé pour votre recherche.")
            except Exception as e:
                print(e)
                speak("Une erreur s'est produite lors de la recherche.")

        # --- Recherche Google ---
        elif 'recherche' in query or 'cherche' in query:
            terme = query.replace('recherche', '').replace('cherche', '').strip()
            if terme:
                webbrowser.open(f"https://google.com/search?q={terme}")
                speak(f"Je recherche {terme} sur Google.")
            else:
                speak("Que voulez-vous rechercher ?")

        # --- Ouvrir un site ---
        elif 'ouvre' in query or 'open' in query:
            if not open_site(query):
                speak("Je ne connais pas ce site.")

        # --- Musique ---
        elif 'musique' in query or 'music' in query:
            if os.path.isdir(MUSIC_DIR):
                songs = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav'))]
                if songs:
                    os.startfile(os.path.join(MUSIC_DIR, songs[0]))
                    speak(f"Je lance {songs[0]}")
                else:
                    speak("Aucun fichier musical trouvé dans le dossier.")
            else:
                speak("Le dossier musique est introuvable. Vérifiez le fichier .env")

        # --- Heure ---
        elif 'heure' in query or 'time' in query:
            heure = datetime.datetime.now().strftime("%H heures %M")
            speak(f"Il est {heure}.")

        # --- Date ---
        elif 'date' in query or 'jour' in query:
            jours = ['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']
            mois  = ['janvier','février','mars','avril','mai','juin',
                     'juillet','août','septembre','octobre','novembre','décembre']
            now   = datetime.datetime.now()
            date_str = f"{jours[now.weekday()]} {now.day} {mois[now.month - 1]} {now.year}"
            speak(f"Nous sommes le {date_str}.")

        # --- Météo ---
        elif 'météo' in query or 'meteo' in query or 'temps' in query:
            ville = WEATHER_CITY
            # Permet de demander la météo d'une ville précise : "météo à Lyon"
            for mot in ['à', 'a', 'de', 'pour']:
                if f' {mot} ' in query:
                    ville = query.split(f' {mot} ')[-1].strip()
                    break
            resultat = get_weather(ville)
            speak(resultat)

        # --- Email ---
        elif 'email' in query or 'mail' in query:
            try:
                speak("Que dois-je dire dans cet email ?")
                content = takeCommand()
                sendEmail(EMAIL_DESTINATAIRE, content)
                speak("L'email a été envoyé avec succès !")
            except Exception as e:
                print(e)
                speak("Désolé, je n'ai pas pu envoyer cet email.")

        # --- Aide ---
        elif 'aide' in query or 'help' in query or 'commandes' in query:
            aide = (
                "Voici ce que je sais faire : "
                "rechercher sur Wikipedia, "
                "ouvrir YouTube, Google, Facebook, GitHub, Stack Overflow, Gmail, "
                "lancer de la musique, "
                "donner l'heure et la date, "
                "afficher la météo, "
                "envoyer un email, "
                "et faire une recherche Google."
            )
            speak(aide)

        else:
            speak("Je n'ai pas compris. Dites 'aide' pour connaître les commandes disponibles.")
