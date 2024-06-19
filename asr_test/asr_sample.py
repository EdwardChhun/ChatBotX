""" 
NOTE: Background noise could be a problem, prevents threshold from triggering
    : Send item data to camera for pick up item
    : Include API calls
    
INFO: Visit "https://lucid.app/lucidspark/d21eedee-cb57-42f3-819f-b939ea709794/edit?viewport_loc=-2253%2C1260%2C3344%2C1888%2C0_0&invitationId=inv_1be0147a-1ed2-4539-bdfc-eb924f6497f5"
      for flow chart
"""

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import requests

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the TTS engine
try:
    engine = pyttsx3.init() # This is MACOS, use another argument for Windows "SAPI5"
except Exception as e:
    print("Error initializing pyttsx3:", e)
    exit(1)
    
def speak(audio: str) -> None:
    """Convert text to speech."""
    print("🤖: ", audio)
    engine.say(audio)
    engine.runAndWait()

def wishme() -> None:
    """Greet the user based on the current time."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("How can I help you today, Edward?")

def takecommand() -> str:
    """Listen for a command from the user and return it as a string."""
    with sr.Microphone() as source:
        print("Listening.....")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Wait for a few moments")
        query = r.recognize_google(audio, language="en-in")
        print("🗣️:", query)
        return query
    except sr.UnknownValueError:6
        print("Could not understand the audio")
        speak("Say that again, please.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak("There was an error connecting to the speech service.")
        return None

def sendItemToCamera(item: str) -> None:
    """ 
    Parameters:
    item?: string | None
    Info: Sends item to camera for picking up using robotic arm
    """
    return item

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
                
                if "my" in query:                   # This is just for tts to reply properly
                    query.replace("my", "your")     # Picking up "your" item instead of "my" item
                if sep:
                    item = after.strip()
                    speak(f"Picking up {item}")
                else:
                    print("Please say a valid item")
            
            elif "weather" and "sacramento" in query:
                """ 
                HACK: Include WeatherAPI call
                """
                speak("The weather in Sacramento is looking forward to a fucking hot day")
                

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
