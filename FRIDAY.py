# F.R.I.D.A.Y.: Your Personal AI Companion
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
#Open web browsers
import webbrowser
#Provides a way to interact with the operating system(system-related tasks,file and directory paths,)
import os
#Email
import smtplib
import subprocess
#For movies list
from imdb import IMDb 
import random
#To control device volume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import requests
#For device configuration
import platform
import socket
#capture photo
import cv2
from googletrans import Translator, LANGUAGES
#check internet speed
import speedtest



#text-to-speech (TTS) engine and retrieving the available voices.
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id) for Female voice
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

#to control device volume
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

#news 
def get_latest_news(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "articles" in data:
        articles = data["articles"]
        return articles
    else:
        return []
    
 #weather info 
weatherstack_access_key = "83b5432664fe7f9cc513653b9a1e7173"  #api for weather info 

def get_weather(city):
    base_url = "http://api.weatherstack.com/current"
    params = {
        "access_key": weatherstack_access_key,
        "query": city,
        "units": "m"
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        current = data['current']
        weather_desc = current['weather_descriptions'][0]
        temperature = current['temperature']
        humidity = current['humidity']

        return f"Current weather in {city}: {weather_desc}. Temperature: {temperature}°C. Humidity: {humidity}%."
    else:
        return "Sorry, couldn't fetch weather information at the moment."
    
random_thoughts = [
    "The only way to do great work is to love what you do.",
    "Believe you can and you're halfway there.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "The only person you should try to be better than is the person you were yesterday.",
    "Don't watch the clock; do what it does. Keep going.",
    "Your time is limited, don't waste it living someone else's life.",
    "The future belongs to those who believe in the beauty of their dreams.", 
    "Happiness is not by chance, but by choice.",
    "The journey of a thousand miles begins with one step.",
    "In the middle of every difficulty lies opportunity.",
    "Embrace the challenges that come your way, for they are the stepping stones to your success.",
    "Your potential is limitless, remember to always believe in yourself.",
    "Kindness is like a boomerang, it comes back to you when you least expect it.",
    "Every day is a new opportunity to create a better version of yourself.",
    "Don't be afraid of failure; it's a part of the journey towards achieving greatness.",
    "Smile often, your positivity can brighten not only your day but also the days of those around you.",
    "Small acts of courage can lead to extraordinary achievements.",
    "Success is the sum of small efforts repeated day in and day out.",
    "Challenge yourself to step out of your comfort zone and embrace growth.",
    "The present moment is a gift, make the most of it and create beautiful memories."
    ]

def get_random_thought():
    return random.choice(random_thoughts)

#notes
# Dictionary to store notes
notes = {}
def take_note(note_title, note_content):
    notes[note_title] = note_content
    print("Note saved:", note_title)
    speak("Note saved!")
    save_notes_to_file()  # Save notes to file after adding a new note

# Function to save notes to a file
def save_notes_to_file():
    with open("notes.txt", "w") as file:
        for title, content in notes.items():
            file.write(f"{title}:{content}\n")

# Function to load notes from a file
def load_notes_from_file():
    try:
        with open("notes.txt", "r") as file:
            for line in file:
                # Check if the line contains the expected delimiter ":"
                if ":" in line:
                    title, content = line.strip().split(":", 1)
                    notes[title] = content
    except FileNotFoundError:
        print("File not found. Creating a new file.")

# Function to read and display the latest saved note
def read_latest_note():
    if notes:
        latest_title = max(notes.keys())
        latest_content = notes[latest_title]
        print("Latest Note:")
        print("Title:", latest_title)
        print("Content:", latest_content)
        speak("Here is your latest note:")
        speak(f"Title: {latest_title}")
        speak(f"Content: {latest_content}")
    else:
        print("No notes available.")
        speak("You don't have any saved notes.")

# Function to delete a note
def delete_note(note_title):
    if note_title in notes:
        del notes[note_title]
        save_notes_to_file()
        print("Note deleted:", note_title)
        speak("Note deleted!")
    else:
        print("Note not found.")
        speak("Note not found.")

# Function to display all saved notes
def display_all_notes():
    if notes:
        print("All Saved Notes:")
        for title, content in notes.items():
            print("Title:", title)
            print("Content:", content)
            print("-" * 30)
    else:
        print("No notes available.")
        speak("You don't have any saved notes.")

    # Get system information
def get_device_configuration():
    system_info = platform.uname()
    system_name = system_info.system
    node_name = system_info.node
    release = system_info.release
    version = system_info.version
    machine = system_info.machine
    processor = system_info.processor

    # Get network information
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    device_configuration = f"""
    Device Configuration:
    System: {system_name}
    Node Name: {node_name}
    Release: {release}
    Version: {version}
    Machine: {machine}
    Processor: {processor}

    Hostname: {hostname}
    IP Address: {ip_address}
    """

    return device_configuration

# Password to access main code
correct_password = "3000"
max_attempts = 3
current_attempts = 0
# Path to the VS Code executable
vs_code_path = "C:\\Program Files (x86)\\Microsoft VS Code\\Code.exe"

def check_password():
    global current_attempts
    while current_attempts < max_attempts:
        speak("Sir, please enter your password!")
        user_input = input("Please enter the password: ")

        if user_input == correct_password:
            return True
        else:
            current_attempts += 1
            remaining_attempts = max_attempts - current_attempts
            print(f"Access denied. {remaining_attempts} attempts remaining. Please try again.")
            speak(f"Access denied.")

    print("Maximum login attempts reached. Closing the program.")
    speak("Maximum login attempts reached. Closing the program.")
    capture_photo()
    close_vs_code()
    return False

def close_vs_code():
    try:
        subprocess.run(['taskkill', '/f', '/im', 'Code.exe'], check=True)
        print("VS Code closed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while closing VS Code: {e}")
        speak("Sorry sir, an error occurred while closing VS Code.")

def capture_photo():
    # Open the camera
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    # Save the captured frame as a photo
    photo_path = "captured_photo.jpg"
    cv2.imwrite(photo_path, frame)

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

    print(f"Photo captured and saved as {photo_path}.")
        
news_api_key = "6c714b9a2c414fdba0aaf1cf445b55af" #api for news
num_articles_to_print = 5

program_path = 'tic tac toe.py' #path of the game code.

to_do_list = []

#To get news specified in india
def get_latest_news_in_india(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "articles" in data:
        articles = data["articles"]
        return articles
    else:
        return []

def handle_to_do_list(query):
    global to_do_list

    # Command to make a new to-do list
    if 'make to do list' in query:
        to_do_list.clear()  # Clear existing to-do list
        print("Sure, I've created a new to-do list for you.")
        speak("Sure, I've created a new to-do list for you.")

    # Command to add to-do list items
    elif 'add to do' in query:
        print("Sure, please tell me the task you want to add to the to-do list.")
        speak("Sure, please tell me the task you want to add to the to-do list.")
        task = takeCommand()
        if task != "None":
            to_do_list.append(task)
            print(f"Task '{task}' added to the to-do list.")
            speak(f"Task '{task}' added to the to-do list.")
    
    elif 'delete to do' in query:
        if to_do_list:
            print("Sure, please tell me the task number you want to delete from the to-do list.")
            speak("Sure, please tell me the task number you want to delete from the to-do list.")
            task_number = takeCommand()
            try:
                task_number = int(task_number)
                if 1 <= task_number <= len(to_do_list):
                    deleted_task = to_do_list.pop(task_number - 1)
                    print(f"Task '{deleted_task}' deleted from the to-do list.")
                    speak(f"Task '{deleted_task}' deleted from the to-do list.")
                else:
                    print("Invalid task number. Please provide a valid task number.")
                    speak("Invalid task number. Please provide a valid task number.")
            except ValueError:
                print("Invalid input. Please provide a valid task number.")
                speak("Invalid input. Please provide a valid task number.")
        else:
            print("Your to-do list is empty. There's nothing to delete.")
            speak("Your to-do list is empty. There's nothing to delete.")

    # Command to show the to-do list
    elif 'show to do list' in query:
        if to_do_list:
            print("To-Do List:")
            speak("To-Do List:")
            for idx, task in enumerate(to_do_list, start=1):
                print(f"{idx}. {task}")
                speak(f"{idx}. {task}")
        else:
            print("Your to-do list is empty.")
            speak("Your to-do list is empty.")

#Game
def guess_the_number_game():
    print("Welcome to the Guess the Number game!")
    speak("Welcome to the Guess the Number game!")
    
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    
    print("I have selected a number between 1 and 100. Try to guess it!")
    speak("I have selected a number between 1 and 100. Try to guess it!")

    while True:
        user_guess = input("Enter your guess: ")

        try:
            user_guess = int(user_guess)
        except ValueError:
            print("Invalid input. Please enter a number.")
            speak("Invalid input. Please enter a number.")
            continue

        attempts += 1

        if user_guess == secret_number:
            print(f"Congratulations! You guessed the number in {attempts} attempts.")
            speak(f"Congratulations! You guessed the number in {attempts} attempts.")
            break
        elif user_guess < secret_number:
            print("Too low. Try again.")
            speak("Too low. Try again.")
        else:
            print("Too high. Try again.")
            speak("Too high. Try again.")

#Fitness
def provide_fitness_tip():
    fitness_tips = [
        "Remember to stay hydrated throughout the day. Water is essential for your overall health.",
        "Incorporate a variety of fruits and vegetables into your diet for a balanced nutrition.",
        "Regular physical activity is crucial. Aim for at least 30 minutes of exercise every day.",
        "Get enough sleep each night to support your body's recovery and overall well-being.",
        "Practice mindfulness and stress-reducing activities like meditation or deep breathing exercises.",
        "Avoid sitting for extended periods. Take short breaks and stretch to improve flexibility.",
        "Choose whole grains over refined carbohydrates for sustained energy levels.",
        "Don't forget to warm up before exercising to prevent injuries.",
        "Maintain a positive mindset. Your mental health is just as important as your physical health.",
        "Consider consulting with a fitness professional for personalized workout and nutrition advice."
    ]

    selected_tip = random.choice(fitness_tips)
    print("Fitness Tip of the Day:")
    print(selected_tip)
    speak("Fitness Tip of the Day:")
    speak(selected_tip)

def speak_translated_bhagavad_gita_shloka(chapter, sloka):
    api_url = f"https://bhagavadgitaapi.in/slok/{chapter}/{sloka}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if 'transliteration' in data:
            transliteration_text = data['transliteration']
            print(f"Bhagavad Gita Chapter {chapter}, Shloka {sloka} (Translated):")
            print(transliteration_text)
            speak(transliteration_text)
        else:
            print("No translated shloka found for the specified chapter and shloka number.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

#To translate text
def translate_text():
    translator = Translator()

    print("Enter the text you want to translate:")
    text_to_translate = input()

    print("Enter the target language (e.g., 'French', 'Spanish'):")
    target_language_name = input().capitalize()

    # Convert the language name to the language code
    target_language_code = None
    for code, name in LANGUAGES.items():
        if name.lower() == target_language_name.lower():
            target_language_code = code
            break

    if target_language_code:
        try:
            translated_text = translator.translate(text_to_translate, dest=target_language_code).text
            print(f"Translated text ({target_language_name}):")
            print(translated_text)
            speak("Here's the translated text:")
            speak(translated_text)
        except Exception as e:
            print(f"Error translating text: {e}")
            speak("Sorry, there was an error translating the text.")
    else:
        print("Invalid target language. Please enter a valid language name.")
        speak("Invalid target language. Please enter a valid language name.")


       
if __name__ =="__main__":
    if check_password():
        print("Access granted. Starting the main program.")
        speak("Access granted!")
    else:
        exit()
    load_notes_from_file()
    wishMe()
    while True:
    #if 1:
        query = takeCommand().lower()
        if query == "none":
            print("Sorry, I couldn't understand that. Please try again.")
            continue  # Skip the rest of the loop and start over

        # logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            print("Sure, what would you like to search for on YouTube?")
            speak("Sure, what would you like to search for on YouTube?")
            search_query = takeCommand().lower()
            if search_query != 'none':
                search_url = f"https://www.youtube.com/results?search_query={search_query}"
                speak(f"Searching for '{search_query}' on YouTube.")
                webbrowser.open(search_url)

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'open my college website' in query:
            speak("Opening your college's official website")
            webbrowser.open("https://www.scoea.org")

        elif 'open stackoverflow' in query:
            speak("Opening Stackoverflow.com")
            webbrowser.open("https://www.stackoverflow.com") 

        elif 'eat pizza' in query:
            speak("Opening dominos")
            webbrowser.open("https://www.dominos.co.in")

        elif 'watch movies' in query or 'open netflix' in query:
            speak("Opening netflix")
            webbrowser.open("https://www.netflix.com/in/")

        elif 'play music' in query:
            music_dir = 'G:\\Anuj\\music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir the time is {strTime}")

        elif 'open visual code' in query or 'let\s code'in query:
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
        

        elif 'open tic tac toe' in query or 'let\s play tic tac toe' in query:
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

        elif 'today\'s news' in query or 'what\s happining in the world' in query:
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

        elif 'introduce yourself' in query or 'who are you' in query:
            print("Greetings! I am FRIDAY, an advanced artificial intelligence designed to assist you in various tasks and operations. The acronym FRIDAY stands for Female Replacement Intelligent Digital Assistant Youth. My capabilities include analyzing data,providing real-time information, and coordinating tasks. Your goals are my priority, and I am here to help you achieve them efficiently and effectively. Just let me know what you need, and I will do my best to assist you. It's important to note that that I am currently under development, which means that I'm continuously learning and improving. As a result, I might encounter some limitations or occasional hiccups, so let's embark on this journey of exploration together. Remember, even superheroes had their origin stories.")
            speak("Greetings! I am FRIDAY, an advanced artificial intelligence designed to assist you in various tasks and operations. The acronym FRIDAY stands for Female Replacement Intelligent Digital Assistant Youth. My capabilities include analyzing data,providing real-time information, and coordinating tasks. Your goals are my priority, and I am here to help you achieve them efficiently and effectively. Just let me know what you need, and I will do my best to assist you. It's important to note that that I am currently under development, which means that I'm continuously learning and improving. As a result, I might encounter some limitations or occasional hiccups, so let's embark on this journey of exploration together. Remember, even superheroes had their origin stories.")
        
        elif 'search google for' in query:
            print('Searching ....')
            query = query.replace("search Google for", "") 
            search_url = f"https://www.google.com/search?q={query}"
            speak(f"Opening Google search results for: '{query}'")
            webbrowser.open(search_url)

        elif 'weather' in query:
            try:
                print("Sure, please tell me the city name.")
                speak("Sure, please tell me the city name.")
                city_name = takeCommand().capitalize()
                if city_name != "None":  # Validate the city name
                    weather_info = get_weather(city_name)
                    print(weather_info)
                    speak(weather_info)
                    weather_info = get_weather(city_name)
            except Exception as e:
                print(f"An error occurred: {e}")
                speak("Sorry, couldn't fetch weather information at the moment.")

        elif 'tell me about' in query:
            speak('Searching.....')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            print(results)
            speak(results)

        elif 'exit' in query or 'bye friday' in query:
            print("Okay sir, then it's time for me to take a digital nap. It was nice assisting you. If you need anything, don't hesitate to ask. Goodbye Until next time!")
            speak("Okay sir, then it's time for me to take a digital nap. It was nice assisting you. If you need anything, don't hesitate to ask. Goodbye Until next time!")
            break

        elif 'i am feeling sad' in query:
            print("Hey there, I sense you might be feeling down. Just a reminder that I'm here for you, offering a virtual shoulder to lean on. It's okay to feel this way, and I'm here to listen or chat about anything. You've got the strength to get through this,and I'm cheering you on. Take care, Friday")
            speak("Hey there, I sense you might be feeling down. Just a reminder that I'm here for you, offering a virtual shoulder to lean on. It's okay to feel this way, and I'm here to listen or chat about anything. You've got the strength to get through this,and I'm cheering you on. Take care, Friday")

        elif 'thought of the day' in query:
            random_thought = get_random_thought()
            print("Random Thought of the Day:")
            print(random_thought)
            speak("Random Thought of the Day:")
            speak(random_thought)

        elif 'take a note' in query:
            print("Sure, please provide the note title.")
            speak("Sure, please provide the note title.")
            note_title = takeCommand()
            print("Please provide the note content.")
            speak("Please provide the note content.")
            note_content = takeCommand()
            take_note(note_title, note_content)

        elif 'read latest note' in query:
            read_latest_note()

        elif 'display all notes' in query:
            display_all_notes()

        elif 'delete note' in query:
            print("Sure, please provide the note title to delete from bellow.")
            speak("Sure, please provide the note title to delete from bellow.")
            display_all_notes()
            note_title = takeCommand()
            delete_note(note_title)
      
        elif 'get device configuration' in query:
            device_config = get_device_configuration()
            print(device_config)
            speak("Here is your device configuration:")
            speak(device_config)

        if 'to do' in query:
            handle_to_do_list(query)

        elif 'news in india' in query or 'latest news in india' in query:
            try:
                news_articles = get_latest_news_in_india(news_api_key)
                if news_articles:
                    print(f"Latest {num_articles_to_print} News Headlines in India:")
                    for idx, article in enumerate(news_articles[:num_articles_to_print], start=1):
                        print(f"{idx}. {article['title']}")
                        speak(f"{idx}. {article['title']}")
                        print(article['description'])
                        print("Source:", article['source']['name'])
                        print("-" * 50)
                else:
                    print("Sorry No news articles available for India.")
                    speak("Sorry No news articles available for India.")
            except Exception as e:
                print(f"An error occurred: {e}")
                speak("ERROR!")

        if 'play guess the number' in query:
            guess_the_number_game()

        if 'fitness tip' in query or 'health tip' in query:
            provide_fitness_tip()

        if 'bhagavad gita' in query or 'bhagavad geeta' in query:
            chapter_number = input("Enter the chapter number: ")
            sloka_number = input("Enter the sloka number: ")
            speak_translated_bhagavad_gita_shloka(chapter_number, sloka_number)

        if 'translate' in query:
             translate_text()

        elif 'open website' in query:
            print("Sure, please provide the website URL.")
            speak("Sure, please provide the website URL.")
            website_url = takeCommand().lower()
            if website_url != "None":
                webbrowser.open(website_url)
            else:
                print("Enter Proper website url")
                speak("kindly enter proper URL")

        
        #End of the code....