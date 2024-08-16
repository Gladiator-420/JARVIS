import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import os
import subprocess
import requests
from groq import Groq

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
API_KEY = "88ae47b116db71d7f21ec4690703ada6"
CITY = "ranchi"
def get_weather():
    weather_report = "Unable to fetch weather data."  # Default message in case of failure
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        # Debugging: Print the entire response

        if weather_data.get("cod") == 200:
            main = weather_data.get("main", {})
            weather = weather_data.get("weather", [{}])[0]

            temperature = main.get("temp", "N/A")
            humidity = main.get("humidity", "N/A")
            weather_description = weather.get("description", "No description available")

            weather_report = (f"Temperature: {temperature}°C, "
                              f"Humidity: {humidity}%, "
                              f"Condition: {weather_description.capitalize()}.")
        else:
            weather_report = "Failed to get weather updates. Please try again later."

    except Exception as e:
        weather_report = f"An error occurred while fetching the weather: {str(e)}"
    
    return weather_report
def aiprocess(command):
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": command,
            }
        ]
    )
    response = completion.choices[0].message.content
    print(f"Jarvis: {response}")
    return response 

def processCommand(c):
    c = c.lower().strip()
    print(command)
    if "open google" in c:
        speak("opening google")
        webbrowser.open("https://google.com")
    elif c == "open youtube":
        speak("opening youtube")
        webbrowser.open("https://www.youtube.com")
    elif c.startswith("open youtube and search for"):
        search_query = c.replace("open youtube and search for", "").strip()
        if search_query:
            speak("opening youtube and searching for " + search_query)
            search_url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open(search_url)
        else:
            speak("I couldn't catch what to search for.")
    elif c.startswith("play"):
        song = c.split(" ")[1]
        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            webbrowser.open(link)
        else:
            speak("Song not found in the library.")
    elif "open instagram" in c:
        speak("opening instagram")
        subprocess.Popen(["start", "instagram://app"], shell=True)
        
    elif "open twitter" in c:
        speak("opening twitter")
        subprocess.Popen(["C:\Program Files\WindowsApps\Twitter.exe"])
        
    elif "open notepad" in c:
        speak("opening notepad")
        subprocess.Popen(["notepad.exe"])
        
    elif "open calculator" in c:
        speak("opening calculator")
        subprocess.Popen(["calc.exe"])
        
    elif "open paint" in c:
        speak("opening paint")
        subprocess.Popen(["mspaint.exe"])
    elif "weather update" in c:
        speak("Fetching weather updates.")
        weather_report = get_weather()
        print(weather_report,CITY)
        speak(weather_report)
    else:
        output = aiprocess(c)
        speak(output)

if __name__ == "__main__":
    user_name = "Swastik"  # Replace with your name
    print("Initializing jarvis please wait......")
    speak(f"Initializing Jarvis... Hello {user_name}!")
    while True:
        # Listen for wake word
        print("Recognizing>>>")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source,timeout=2,phrase_time_limit=5)  # Timeout can be added as an argument if needed
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis active")
                    audio = recognizer.listen(source,timeout=2,phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print("Error: {0}".format(e))