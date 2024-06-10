""" 
NOTE: Background noise could be a problem, prevents threshold from triggering
    : Send item data to camera for pick up item
    : Include API calls
"""

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the TTS engine
try:
    engine = pyttsx3.init('nsss') # This is MACOS, use another argument for Windows "SAPI5"
except Exception as e:
    print("Error initializing pyttsx3:", e)
    exit(1)
    
def speak(audio):
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()
    print("🤖: ", audio)

def wishme():
    """Greet the user based on the current time."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("How can I help you today, Edward?")

def takecommand():
    """Listen for a command from the user and return it as a string."""
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Wait for a few moments")
        query = r.recognize_google(audio, language="en-in")
        print("User said:", query)
        return query
    except Exception as e:
        print(e)
        speak("Say that again, please.")
        return None

if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand()
        if query:
            query = query.lower()

            if "pick up" in query:
                """ 
                NOTE: Make this send the item to the camera for arm pick up
                """
                before, sep, after = query.partition("pick up")
                
                if after == "my":                   # This is just for tts to reply properly
                    query.replace("my", "your")     # Picking up "your" item instead of "my" item
                if sep:
                    item = after.strip()
                    speak(f"Picking up {item}")
                else:
                    print("Please say a valid item")

            elif "wikipedia" in query:
                speak("Searching in Wikipedia")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)

            elif "open youtube" in query:
                speak("Opening YouTube")
                webbrowser.open("https://youtube.com")

            elif "open google" in query:
                speak("Opening Google")
                webbrowser.open("https://google.com")
                
            elif "goodbye" in query:
                speak("Okay, goodbye!")
                quit()