import pyttsx3
import random
import speech_recognition as sr
import webbrowser
import os
import datetime
import pyautogui
from plyer import notification
import wikipedia
import pywhatkit as pwt
import mtranslate



engine = pyttsx3.init()
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)




def speak(Audio):
    engine.say(Audio)
    engine.runAndWait()

def command():
    content = ""
    while content == "":
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        try:
            content = r.recognize_google(audio, language='en-in')
            print("You Said............" + content)
            content = mtranslate.translate(content, to_language="en-in")
            print("You Said............" + content)
        except Exception as e:
            print("Please try again...")
    return content

def main_process():
    while True:
        request = command()

        if 'Hello' in request:
            speak("Hello, I am your AI assistant. How can I help you?")
            break
        elif 'play song ' in request:
            speak("Which platform would you like to play the song on? You can choose from YouTube, Spotify, or SoundCloud.")
            platform = command()  
            song_name = request.replace("play song", "").strip()

            if 'YouTube' in platform:
                speak(f"Opening YouTube for the song {song_name}.")
                webbrowser.open(f"https://www.youtube.com/results?search_query={song_name}")
            elif 'Spotify' in platform:
                speak(f"Opening Spotify for the song {song_name}.")
                webbrowser.open(f"https://open.spotify.com/search/{song_name}")
            elif 'SoundCloud' in platform:
                speak(f"Opening SoundCloud for the song {song_name}.")
                webbrowser.open(f"https://soundcloud.com/search?q={song_name}")
            else:
                speak("Sorry, I don't recognize that platform. Please choose between YouTube, Spotify, or SoundCloud.")

        elif 'say time' in request:
            nowtime=datetime.datetime.now()
            speak(f"Time is {nowtime.strftime('%I:%M %p')}")
        elif 'open website' in request:
            speak("Which website would you like to open?")
            website = command()
            webbrowser.open(f"https://{website}")
            speak(f"Opening {website}.")

        elif 'task view' in request:
            speak("Opening Task View.")
            pyautogui.hotkey('win', 'tab')




        elif 'open' in request:
            app_name = request.replace("open", "").strip()

            # Open Google Chrome
            if 'chrome' in app_name:
                speak("Opening Google Chrome.")
                os.system("start chrome")

            # Open Notepad
            elif 'notepad' in app_name:
                speak("Opening Notepad.")
                os.system("notepad")

            # Open Calculator
            elif 'calculator' in app_name:
                speak("Opening Calculator.")
                os.system("calc")

            # Open WhatsApp (Desktop Version if installed)
            elif 'whatsapp' in app_name:
                speak("Opening WhatsApp.")
                try:
                    os.system("start whatsapp")  # For WhatsApp Desktop App
                except Exception:
                    webbrowser.open("https://web.whatsapp.com")  # Fallback to web version

            # Open Facebook (Desktop Version if installed)
            elif 'facebook' in app_name:
                speak("Opening Facebook.")
                try:
                    os.system("start chrome https://www.facebook.com")  # Open Facebook in Chrome
                except Exception:
                    webbrowser.open("https://www.facebook.com")  # Fallback to web version

            # Open Instagram (Desktop Version if installed)
            elif 'instagram' in app_name:
                speak("Opening Instagram.")
                try:
                    os.system("start chrome https://www.instagram.com")  # Open Instagram in Chrome
                except Exception:
                    webbrowser.open("https://www.instagram.com")  # Fallback to web version

            # Open Twitter (Web Version)
            elif 'twitter' in app_name:
                speak("Opening Twitter.")
                webbrowser.open("https://www.twitter.com")

            # Open LinkedIn (Web Version)
            elif 'linkedin' in app_name:
                speak("Opening LinkedIn.")
                webbrowser.open("https://www.linkedin.com")

            # Open Telegram (Desktop Version if installed)
            elif 'telegram' in app_name:
                speak("Opening Telegram.")
                try:
                    os.system("start telegram")  # For Telegram Desktop App
                except Exception:
                    webbrowser.open("https://web.telegram.org")  # Fallback to web version

            # Handle apps that are not recognized
            else:
                speak(f"Sorry, I can't open {app_name}. Please check the name and try again.")
        # Tell time
        elif 'time' in request:
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak(f"The current time is {current_time}")

        # Tell date
        elif 'date' in request:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            speak(f"Today's date is {current_date}")

        # Shut down or exit
        elif 'exit' in request or 'shutdown' in request:
            speak("Goodbye! Shutting down now.")
            break

        elif "new task" in request:
            task = request.replace("new task", "")
            task = task.strip()
            if task != "":
                speak(f"Creating new task: {task}")
                with open("tasks.txt", "a") as file:
                    file.write(f"{task}\n")
        
        # Clear all tasks
        elif "what task include" in request:
            speak("Here are the tasks on your list:")
            if os.path.exists("tasks.txt"):
                with open("tasks.txt", "r") as file:
                    tasks = file.readlines()
                    for i, task in enumerate(tasks):
                        speak(f"Task {i + 1}: {task.strip()}")
            else:
                speak("No tasks found.")

        # Read content of specific files
        elif 'read' in request and 'file' in request:
            file_name = request.replace("read file", "").strip()

            # Check if it's a .txt or .py file and handle accordingly
            if file_name.endswith(".txt") or file_name.endswith(".py"):
                if os.path.exists(file_name):
                    speak(f"Reading content of the file {file_name}...")
                    with open(file_name, "r") as file:
                        content = file.read()
                        speak(f"Content of the file {file_name}:")
                        speak(content)
                else:
                    speak(f"Sorry, the file {file_name} does not exist.")
            else:
                speak("Please specify a valid file type such as .txt or .py.")
def create_file(file_name, content=""):
    try:
        with open(file_name, "w") as file:
            file.write(content)
        speak(f"File {file_name} created successfully.")
    except Exception as e:
        speak(f"Failed to create the file: {e}")

def delete_file(file_name):
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
            speak(f"File {file_name} deleted successfully.")
        else:
            speak(f"File {file_name} does not exist.")
    except Exception as e:
        speak(f"Failed to delete the file: {e}")

def search_file(file_name, directory="."):
    try:
        files = os.listdir(directory)
        if file_name in files:
            speak(f"File {file_name} found in {directory}.")
        else:
            speak(f"File {file_name} not found in {directory}.")
    except Exception as e:
        speak(f"Error while searching for the file: {e}")

def enter_data_into_file(file_name, data):
    try:
        with open(file_name, "a") as file:
            file.write(data + "\n")
        speak(f"Data entered into file {file_name}.")
    except Exception as e:
        speak(f"Failed to enter data into the file: {e}")

def main_process():
    while True:
        request = command()

        if 'hello' in request:
            speak("Hello, I am your AI assistant. How can I help you?")

        # Create file and add content
        elif 'create file' in request:
            file_name = request.replace("create file", "").strip()
            if file_name:
                speak(f"Please provide content to write in {file_name}:")
                content = input("Enter content: ")
                create_file(file_name, content)
            else:
                speak("Please specify the file name.")

        # Delete a file
        elif 'delete file' in request:
            file_name = request.replace("delete file", "").strip()
            if file_name:
                delete_file(file_name)
            else:
                speak("Please specify the file name to delete.")

        # Search for a file
        elif 'search file' in request:
            file_name = request.replace("search file", "").strip()
            if file_name:
                speak(f"Searching for {file_name}...")
                search_file(file_name)
            else:
                speak("Please specify the file name to search for.")

        # Enter data into an existing file
        elif 'enter data' in request:
            file_name = request.replace("enter data", "").strip()
            if file_name:
                speak(f"Please provide the data to enter into {file_name}:")
                data = input("Enter data: ")
                enter_data_into_file(file_name, data)
            else:
                speak("Please specify the file name to enter data into.")

        elif "show work"    in request:
            with open("", "r") as file:
                tasks = file.readlines()
            notification.notify(
                title = "Work",
                message = tasks,
            )

        elif "open" in request:
            query = request.replace("open", "")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
            
        elif "search " in request:
            result = request.replace("KITI", "")
            result = request.replace("search ", "")
            print(request)
            result = wikipedia.summary("request", sentences=2)
            print(result)
            speak(result)

        elif "search " in request:
            result = request.replace("KITI", "")
            result = request.replace("search ", "")
            webbrowser.open(f"https://www.google.com/search?q"+request)
            print(request)

        elif "send whatapp" in request:
            pwt.sendwhatmsg("+94", "Hi", 2, 3, 10)
        else:
            speak("Please say the command again.") 

if __name__ =="__main__":
    main_process()