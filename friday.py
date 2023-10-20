# F.R.I.D.A.Y.: Your Personal AI Companion
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import subprocess
from imdb import IMDb #for movies list
import random
#to control device volume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):   
    engine.say(audio) 
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning sir!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon sir!")

    else:
        speak("Good Evining sir!")

    print("I am FRIDAY your digital companion,How can I help you ?")
    speak("I am FRIDAY your digital companion,How can I help you ?")
 
def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")
        speak("Say that again please...")  
        return "None" #None string will be returned
    return query    

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('jarvisforpython@gmail.com','jarvisforpython@25')
    server.sendmail('anujchimanpure25@gmail.com', to, content)
    server.close()

ia = IMDb()
# Search for random movies
def suggest_random_movie():
    random_keyword = "random_keyword"  # Replace with an actual random keyword
    search_results = ia.search_movie(random_keyword)
    if search_results:
        random_movie = random.choice(search_results)
        return random_movie
    else:
        return None
    
# Display suggested random movie
def display_movie_info(movie):
    if movie:
        print("Suggested Random Movie:")
        speak("Suggested Random Movie:")
        print("Title:", movie.get("title"))
        speak(movie.get("title"))
        print("Year:", movie.get("year"))
        speak(movie.get("year")) 
    else:
        print("No random movie suggestions found.")
        speak("No random movie suggestions found.")

def increase_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current_volume + 0.1)  # Increase volume by 0.1
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def decrease_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current_volume - 0.1)  # deccrease volume by 0.1
    volume.SetMasterVolumeLevelScalar(new_volume, None)    

#NEWS API 
def get_latest_news(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "articles" in data:
        articles = data["articles"]
        return articles
    else:
        return []
    
 
news_api_key = "6c714b9a2c414fdba0aaf1cf445b55af" #api for news
num_articles_to_print = 5

program_path = 'tic tac toe.py' #path of the game code.



if __name__ =="__main__":
    wishMe()
    while True:
    #if 1:
        query = takeCommand().lower()

        # logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak("Here we go")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'open my college website' in query:
            speak("Opening your college's official webiste")
            webbrowser.open("https://www.scoea.org")

        elif 'open stack overflow' in query:
            speak("Opening Stack overflow.com")
            webbrowser.open("https://www.stackoverflow.com") 

        elif 'eat pizza' in query:
            speak("Opening dominos")
            webbrowser.open("https://www.dominos.co.in")

        elif 'play music' in query:
            music_dir = 'G:\\Anuj\\music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Sir the time is {strTime}")
            speak(f"Sir the time is {strTime}")

        elif 'open code' in query:
            speak("Okay opening visual studio app")
            codePath = "C:\\Program Files (x86)\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'email to anuj' in query:
            try:
                speak("What should I say ?")
                content = takeCommand()
                to = "anujchimanpure@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry sir there is being some issue while sending the mail at this moment.")

        elif 'open calculator' in query:
            try:
                subprocess.Popen('calc.exe')
                print("Calculator opened successfully.")
            except Exception as e:
                print("Error:", str(e))
                speak("Sorry sir there is some issue while opening the calculator.")

        elif 'open tic-tac-toe' in query:
            try:
                subprocess.run(['python', program_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"An error occurred: {e}")
                speak("Sorry sir an error occurred.")

        elif 'suggest me a movie' in query:
            try:
                suggested_movie = suggest_random_movie()
                display_movie_info(suggested_movie)
            except Exception as e:
                print(f"An error occurred: {e}")

        elif 'increase volume' in query:
            try:
                increase_volume()
                print("Volume increased by 10%.")
                speak("Volume increased by 10%.")
            except Exception as e:
                print(f"An error occurred: {e}")
                speak("Sorry sir an error occurred:")

        elif 'decrease volume' in query:
            try:
                decrease_volume()
                print("Volume decreased by 10%.")
                speak("Volume decreased by 10%.")
            except Exception as e:
                print(f"An error occurred: {e}")
                speak("Sorry sir an error occurred:") 

        elif 'news today' in query:
            try:
                news_articles = get_latest_news(news_api_key)
                if news_articles:
                    print(f"Latest {num_articles_to_print} News Headlines:")
                    for idx, article in enumerate(news_articles[:num_articles_to_print], start=1):
                        print(f"{idx}. {article['title']}")
                        speak(f"{idx}. {article['title']}")
                        print(article['description'])
                        print("Source:", article['source']['name'])
                        print("-" * 50)
                else:
                    print("No news articles available.")
                    speak("No news articles available.")
            except Exception as e:
                print(f"An error occurred: {e}")
                speak("ERROR!")

        elif 'introduce yourself' in query:
            print("Greetings! I am FRIDAY, an advanced artificial intelligence designed to assist you in various tasks and operations. The acronym FRIDAY stands for Female Replacement Intelligent Digital Assistant Youth. My capabilities include analyzing data, providing real-time information, and coordinating tasks. Your goals are my priority, and I am here to help you achieve them efficiently and effectively. Just let me know what you need, and I will do my best to assist you. It's important to note that that I am currently under development, which means that I'm continuously learning and improving. As a result, I might encounter some limitations or occasional hiccups, so let's embark on this journey of exploration together. Remember, even superheroes had their origin stories. ")
            speak("Greetings! I am FRIDAY, an advanced artificial intelligence designed to assist you in various tasks and operations. The acronym FRIDAY stands for Female Replacement Intelligent Digital Assistant Youth. My capabilities include analyzing data, providing real-time information, and coordinating tasks. Your goals are my priority, and I am here to help you achieve them efficiently and effectively. Just let me know what you need, and I will do my best to assist you. It's important to note that that I am currently under development, which means that I'm continuously learning and improving. As a result, I might encounter some limitations or occasional hiccups, so let's embark on this journey of exploration together. Remember, even superheroes had their origin stories. ")
        
        elif 'search google for' in query:
            print('Searching ....')
            query = query.replace("search Google for", "") 
            search_url = f"https://www.google.com/search?q={query}"
            speak(f"Opening Google search results for: '{query}'")
            webbrowser.open(search_url)

        
        elif 'exit' in query:
            print("Okay sir, then it's time for me to take a digital nap. It was nice assisting you. If you need anything, don't hesitate to ask. Goodbye Until next time!")
            speak("Okay sir, then it's time for me to take a digital nap. It was nice assisting you. If you need anything, don't hesitate to ask. Goodbye Until next time!")
            break

#End of the code....