import webbrowser
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
from googlesearch import search
import AppOpener

# Initialize speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Set default voice
engine.setProperty('voice', voices[0].id)  # You can change to 0/2 for other voices

activation_phrase = "Tars"  # Users can change this phrase to activate commands


# Function to make the assistant talk
def talk(text):
    engine.say(text)
    engine.runAndWait()


# Provide options for selecting voice
def customize_voice():
    print("Available voices:")
    for index, voice in enumerate(voices):
        print(f"{index + 1}. {voice.name}")
    choice = int(input("Enter the number of your preferred voice: ")) - 1
    if 0 <= choice < len(voices):
        engine.setProperty('voice', voices[choice].id)
        talk(f"Voice updated to {voices[choice].name}")
    else:
        talk("Invalid choice. Using default voice.")


# Take user commands via microphone or fallback via text
def takecommand():
    try:
        with sr.Microphone() as source:
            print("Listening... Press 'Ctrl+C' to stop listening")
            talk("I am listening. Please say something.")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if activation_phrase in command:
                command = command.replace(activation_phrase, "")
                return command
    except Exception as e:
        print(f"Error: {e} (Fallback to text input)")
        command = input("Couldn't hear you. Type your command here: ").lower()
    return command


# Function to show available commands
def available_features():
    features = """
    I can do the following:
    1. Play music videos from YouTube (e.g., "play [song]").
    2. Tell you the current time (say "time").
    3. Provide summaries from Wikipedia (e.g., "tell me about [topic]").
    4. Tell jokes (say "joke").
    5. Open websites (e.g., "visit [website]").
    6. Open applications (e.g., "open [app name]").
    7. Search Google (e.g., "search [query]").
    """
    print(features)
    talk(features)


# Main function to process commands
def runTars():
    talk("Welcome! How can I help you today?")
    while True:
        command = takecommand()
        print(f"Command received: {command}")

        if 'play' in command:
            song = command.replace('play', '').strip()
            talk(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"The current time is {time}")
            print(f"The current time is {time}")

        elif 'tell me about' in command:
            topic = command.replace('tell me about', '').strip()
            talk("Searching for information...")
            try:
                info = wikipedia.summary(topic, sentences=2)
                print(info)
                talk(info)
            except wikipedia.exceptions.DisambiguationError:
                talk("There are many articles about this topic. Please be more specific.")
            except Exception as e:
                talk("Sorry, I couldn't find any information on this topic.")

        elif 'joke' in command:
            joke = pyjokes.get_joke(language='en')
            talk(joke)
            print(joke)

        elif 'visit' in command:
            site = command.replace('visit', '').strip().replace(' ', '')
            if '.com' not in site and '.org' not in site:
                site += '.com'
            try:
                webbrowser.open(f"https://{site}")
                talk(f"Opening {site}")
            except Exception as e:
                talk(f"Sorry, I couldn't open {site}. Error: {e}")

        elif 'open' in command:
            app = command.replace('open', '').strip()
            try:
                AppOpener.open(app)
                talk(f"Opening {app}")
            except Exception as e:
                talk(f"Sorry, I couldn't open {app}. Error: {e}")

        elif 'search' in command:
            query = command.replace('search', '').strip()
            talk(f"Searching for {query} on Google")
            try:
                results = [url for url in search(query, num=5, stop=5, pause=2)]
                print("Search Results:")
                for idx, result in enumerate(results, start=1):
                    print(f"{idx}. {result}")
                # Optionally, open the first result
                webbrowser.open(results[0])
            except Exception as e:
                talk(f"Sorry, I couldn't complete the search. Error: {e}")

        elif 'what can you do' in command:
            available_features()

        elif 'customize voice' in command:
            customize_voice()

        elif 'exit' in command or 'quit' in command:
            talk("Goodbye! Have a great day.")
            break
        elif 'how are you' in command:
            talk("I'm just a bunch of code, but I'm feeling great! How about you?")
        elif 'what is your name' in command:
            talk("My name is Tars, your virtual assistant.")
        elif 'who created you' in command:
            talk("I was created by a student of Uttarakhand Technical University to assist you.")
        elif 'thank you' in command:
            talk("You're welcome! Let me know if I can help with anything else.")
        elif 'goodbye' in command or 'bye' in command:
            talk("Goodbye! Have a great day.")
            break
        else:
            talk("I'm sorry, I didn't understand that. Please try again!")


# Give users instructions for first-time usage
talk("Hello! You can give me commands by saying my name followed by what you want.")
talk("My name is Tars, your virtual assistant.")
talk("If you don't know what to do, just say 'what can you do'.")
runTars()
