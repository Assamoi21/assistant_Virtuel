import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib
# pip install PyAudio




engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)#voice[0]-male voice[1]-female


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am VA Sir. Please tell me how may I help you")


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("from_mail_id", "password")
    server.sendmail("from_mail_id", to, content)
    server.close()    

if __name__ == "__main__":
    wishMe()
    while True:
        # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            try:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "").strip() 
                if not query:
                    speak("Please specify what you want to search on Wikipedia.")
                else:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("Your query is too broad. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("I could not find any results for your query.")
            except Exception as e:
                print(e)
                speak("An error occurred while searching Wikipedia.")


        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'open facebook' in query:
            webbrowser.open("facebook.com")


        elif 'play music' in query:
            music_dir = 'E:\music' # your music playlist location path
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "E:\\code_opencv" #your code loaction
            os.startfile(codePath)
            
        elif 'open photo' in query:
            photoPath = "E:\\DISK_E\\photo_name" # your photo loaction
            os.startfile(photoPath)

            

        elif 'email to friend' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "To_mail_id" #for example :email@gmail.com
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry. I am not able to send this email")
                
        
