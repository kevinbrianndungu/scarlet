import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set the voice and rate for the text-to-speech engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 for male, 1 for female
engine.setProperty('rate', 150)  # Speed of speech


def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def listen():
    """Listen to user input and convert it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')  # Use Google Speech Recognition
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return ""


def greet():
    """Greet the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")


def get_time():
    """Tell the current time."""
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")  # Format: HH:MM AM/PM
    speak(f"The current time is {current_time}")


def get_date():
    """Tell the current date."""
    now = datetime.datetime.now()
    current_date = now.strftime("%B %d, %Y")  # Format: Month Day, Year
    speak(f"Today's date is {current_date}")


def open_website(url):
    """Open a website in the default browser."""
    webbrowser.open(url)
    speak(f"Opening {url}")


def search_web(query):
    """Perform a web search using Google."""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    speak(f"Here are the results for {query}")


def main():
    """Main function to run the voice assistant."""
    greet()
    speak("How can I assist you today?")

    while True:
        query = listen()

        if "hello" in query:
            speak("Hello! How can I help you?")
        elif "time" in query:
            get_time()
        elif "date" in query:
            get_date()
        elif "open youtube" in query:
            open_website("https://www.youtube.com")
        elif "open google" in query:
            open_website("https://www.google.com")
        elif "search" in query:
            query = query.replace("search", "").strip()
            search_web(query)
        elif "exit" in query or "quit" in query:
            speak("Goodbye!")
            break
        else:
            speak("I'm sorry, I can't perform that task yet.")


if __name__ == "__main__":
    main()
