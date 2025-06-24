#!/usr/bin/env python3
"""
Jarvis - Local AI Assistant
A powerful, voice-activated personal assistant that runs completely locally.
"""

import speech_recognition as sr
import pyttsx3
import os
import subprocess
import platform
import requests
from bs4 import BeautifulSoup
import json
import datetime
import time
import threading
import re
import webbrowser
import random
from pathlib import Path

class JarvisAssistant:
    def __init__(self):
        """Initialize the Jarvis Assistant with all necessary components."""
        self.system = platform.system()
        self.notes_file = "notes.json"
        self.config_file = "config.json"
        
        # Initialize speech components
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Load configuration
        self.config = self.load_config()
        self.setup_voice()
        
        # Load notes
        self.notes = self.load_notes()
        
        # Personality responses
        self.greetings = [
            "Hello! I'm Jarvis, your personal assistant. How can I help you today?",
            "Good to see you! What can I do for you?",
            "Hey there! Ready to get things done?",
            "At your service! What's on your mind?"
        ]
        
        self.confirmations = [
            "Done!",
            "Consider it handled!",
            "All set!",
            "Mission accomplished!",
            "Got it covered!"
        ]
        
        print("🤖 Jarvis Assistant initialized successfully!")
        self.speak("Jarvis online and ready for action!")

    def load_config(self):
        """Load configuration settings."""
        default_config = {
            "voice_rate": 200,
            "voice_volume": 0.9,
            "voice_id": 0,
            "wake_word": "jarvis",
            "auto_listen": True
        }
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except FileNotFoundError:
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config

    def setup_voice(self):
        """Configure text-to-speech settings."""
        voices = self.tts_engine.getProperty('voices')
        if voices and len(voices) > self.config['voice_id']:
            self.tts_engine.setProperty('voice', voices[self.config['voice_id']].id)
        
        self.tts_engine.setProperty('rate', self.config['voice_rate'])
        self.tts_engine.setProperty('volume', self.config['voice_volume'])

    def speak(self, text):
        """Convert text to speech."""
        print(f"🗣️ Jarvis: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self, timeout=5):
        """Listen for voice input and convert to text."""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            print("🔄 Processing...")
            text = self.recognizer.recognize_google(audio).lower()
            print(f"👤 You said: {text}")
            return text
        
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you repeat?")
            return None
        except sr.RequestError as e:
            self.speak("Sorry, there was an error with the speech recognition service.")
            print(f"Error: {e}")
            return None

    def load_notes(self):
        """Load notes from JSON file."""
        try:
            with open(self.notes_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_notes(self):
        """Save notes to JSON file."""
        with open(self.notes_file, 'w') as f:
            json.dump(self.notes, f, indent=2)

    def add_note(self, note_text):
        """Add a new note with timestamp."""
        note = {
            "text": note_text,
            "timestamp": datetime.datetime.now().isoformat(),
            "id": len(self.notes) + 1
        }
        self.notes.append(note)
        self.save_notes()
        self.speak(f"Note saved: {note_text}")

    def read_notes(self):
        """Read all saved notes."""
        if not self.notes:
            self.speak("You don't have any notes saved.")
            return
        
        self.speak(f"You have {len(self.notes)} notes:")
        for i, note in enumerate(self.notes[-5:], 1):  # Read last 5 notes
            timestamp = datetime.datetime.fromisoformat(note['timestamp'])
            formatted_time = timestamp.strftime("%B %d at %I:%M %p")
            self.speak(f"Note {i}: {note['text']} - saved on {formatted_time}")

    def search_web(self, query):
        """Search the web and provide summary."""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to get featured snippet or first result
            featured = soup.find('div', class_='BNeawe')
            if featured:
                result = featured.get_text()
                self.speak(f"Here's what I found: {result}")
            else:
                self.speak(f"I've opened a web search for {query} in your browser.")
                webbrowser.open(search_url)
                
        except Exception as e:
            self.speak(f"Sorry, I couldn't search for that right now. Opening browser instead.")
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")

    def open_application(self, app_name):
        """Open applications based on the operating system."""
        app_name = app_name.lower()
        
        apps = {
            'notepad': {
                'Windows': 'notepad.exe',
                'Darwin': 'open -a TextEdit',
                'Linux': 'gedit'
            },
            'calculator': {
                'Windows': 'calc.exe',
                'Darwin': 'open -a Calculator',
                'Linux': 'gnome-calculator'
            },
            'browser': {
                'Windows': 'start chrome',
                'Darwin': 'open -a "Google Chrome"',
                'Linux': 'google-chrome'
            },
            'chrome': {
                'Windows': 'start chrome',
                'Darwin': 'open -a "Google Chrome"',
                'Linux': 'google-chrome'
            },
            'firefox': {
                'Windows': 'start firefox',
                'Darwin': 'open -a Firefox',
                'Linux': 'firefox'
            },
            'file manager': {
                'Windows': 'explorer',
                'Darwin': 'open .',
                'Linux': 'nautilus'
            },
            'music': {
                'Windows': 'start wmplayer',
                'Darwin': 'open -a Music',
                'Linux': 'rhythmbox'
            }
        }
        
        try:
            if app_name in apps and self.system in apps[app_name]:
                command = apps[app_name][self.system]
                if self.system == 'Windows':
                    subprocess.Popen(command, shell=True)
                else:
                    subprocess.Popen(command.split())
                
                self.speak(f"Opening {app_name}")
            else:
                self.speak(f"Sorry, I don't know how to open {app_name} on {self.system}")
                
        except Exception as e:
            self.speak(f"Sorry, I couldn't open {app_name}")
            print(f"Error: {e}")

    def get_time(self):
        """Get current time."""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%A, %B %d, %Y")
        self.speak(f"It's {time_str} on {date_str}")

    def tell_joke(self):
        """Tell a random joke."""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't programmers like nature? It has too many bugs!",
            "I'm reading a book about anti-gravity. It's impossible to put down!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "I used to hate facial hair, but then it grew on me.",
            "Why do programmers prefer dark mode? Because light attracts bugs!"
        ]
        
        joke = random.choice(jokes)
        self.speak(joke)

    def get_weather(self, city=""):
        """Get weather information (requires API key for full functionality)."""
        if not city:
            self.speak("Which city would you like the weather for?")
            return
        
        # For demo purposes, we'll open a weather website
        # In production, you'd use a weather API like OpenWeatherMap
        weather_url = f"https://www.weather.com/weather/today/l/{city.replace(' ', '+')}"
        webbrowser.open(weather_url)
        self.speak(f"I've opened the weather forecast for {city} in your browser.")

    def list_files(self, directory="."):
        """List files in a directory."""
        try:
            files = os.listdir(directory)
            if not files:
                self.speak(f"The directory {directory} is empty.")
                return
            
            self.speak(f"Here are the files in {directory}:")
            for file in files[:10]:  # Limit to first 10 files
                self.speak(file)
            
            if len(files) > 10:
                self.speak(f"And {len(files) - 10} more files.")
                
        except Exception as e:
            self.speak(f"Sorry, I couldn't access that directory.")
            print(f"Error: {e}")

    def create_file(self, filename, content=""):
        """Create a new file."""
        try:
            with open(filename, 'w') as f:
                f.write(content)
            self.speak(f"File {filename} created successfully.")
        except Exception as e:
            self.speak(f"Sorry, I couldn't create the file {filename}")
            print(f"Error: {e}")

    def read_file(self, filename):
        """Read contents of a file."""
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            if len(content) > 500:
                self.speak(f"The file {filename} is quite long. Here's the beginning:")
                self.speak(content[:500] + "...")
            else:
                self.speak(f"Contents of {filename}: {content}")
                
        except FileNotFoundError:
            self.speak(f"Sorry, I couldn't find the file {filename}")
        except Exception as e:
            self.speak(f"Sorry, I couldn't read the file {filename}")
            print(f"Error: {e}")

    def process_command(self, command):
        """Process and execute user commands."""
        command = command.lower().strip()
        
        # Greeting responses
        if any(word in command for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            greeting = random.choice(self.greetings)
            self.speak(greeting)
        
        # Time and date
        elif any(word in command for word in ['time', 'date', 'what time']):
            self.get_time()
        
        # Notes
        elif 'write a note' in command or 'add note' in command or 'note:' in command:
            if ':' in command:
                note_text = command.split(':', 1)[1].strip()
            else:
                note_text = command.replace('write a note', '').replace('add note', '').strip()
            
            if note_text:
                self.add_note(note_text)
            else:
                self.speak("What would you like me to note down?")
        
        elif 'read notes' in command or 'my notes' in command:
            self.read_notes()
        
        # Web search
        elif 'search for' in command or 'search' in command:
            query = command.replace('search for', '').replace('search', '').strip()
            if query:
                self.search_web(query)
            else:
                self.speak("What would you like me to search for?")
        
        # Open applications
        elif 'open' in command:
            app_name = command.replace('open', '').strip()
            if app_name:
                self.open_application(app_name)
            else:
                self.speak("What would you like me to open?")
        
        # File operations
        elif 'list files' in command or 'show files' in command:
            if 'in' in command:
                directory = command.split('in', 1)[1].strip()
                self.list_files(directory)
            else:
                self.list_files()
        
        elif 'create file' in command:
            filename = command.replace('create file', '').strip()
            if filename:
                self.create_file(filename)
            else:
                self.speak("What should I name the file?")
        
        elif 'read file' in command:
            filename = command.replace('read file', '').strip()
            if filename:
                self.read_file(filename)
            else:
                self.speak("Which file would you like me to read?")
        
        # Weather
        elif 'weather' in command:
            city = command.replace('weather in', '').replace('weather', '').strip()
            self.get_weather(city)
        
        # Jokes
        elif 'joke' in command or 'funny' in command:
            self.tell_joke()
        
        # Music/Entertainment
        elif 'play music' in command or 'play song' in command:
            self.open_application('music')
        
        # Exit commands
        elif any(word in command for word in ['goodbye', 'bye', 'exit', 'quit', 'stop']):
            self.speak("Goodbye! It was great helping you today!")
            return False
        
        # Help
        elif 'help' in command or 'what can you do' in command:
            help_text = """I can help you with many things! Here are some examples:
            - Say 'search for Python tutorials' to search the web
            - Say 'open notepad' to open applications
            - Say 'write a note: buy groceries' to save notes
            - Say 'read my notes' to hear your notes
            - Say 'what time is it' for current time
            - Say 'tell me a joke' for entertainment
            - Say 'weather in New York' for weather info
            - Say 'list files' to see directory contents
            - Say 'create file test.txt' to create files
            - Say 'play music' to open music player"""
            self.speak(help_text)
        
        # Unknown command
        else:
            responses = [
                "I'm not sure how to help with that. Try saying 'help' to see what I can do.",
                "Could you rephrase that? I didn't quite understand.",
                "I'm still learning! Try asking me something else or say 'help' for options.",
                "Hmm, I'm not sure about that one. What else can I help you with?"
            ]
            self.speak(random.choice(responses))
        
        return True

    def run_text_mode(self):
        """Run the assistant in text-only mode."""
        print("\n🤖 Jarvis Assistant - Text Mode")
        print("Type 'help' to see what I can do, or 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                if not user_input:
                    continue
                
                if not self.process_command(user_input):
                    break
                    
            except KeyboardInterrupt:
                print("\n")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

    def run_voice_mode(self):
        """Run the assistant in voice mode."""
        print("\n🤖 Jarvis Assistant - Voice Mode")
        print("Say 'Jarvis' to wake me up, then give your command.")
        print("Say 'quit' or 'exit' to stop.\n")
        
        while True:
            try:
                # Listen for wake word
                command = self.listen(timeout=1)
                
                if command is None:
                    continue
                
                # Check for wake word
                if self.config['wake_word'] in command:
                    self.speak("Yes?")
                    
                    # Listen for actual command
                    command = self.listen(timeout=10)
                    if command:
                        if not self.process_command(command):
                            break
                
                elif any(word in command for word in ['quit', 'exit', 'goodbye']):
                    self.speak("Goodbye!")
                    break
                    
            except KeyboardInterrupt:
                print("\n")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

    def run(self, mode='voice'):
        """Run the assistant in specified mode."""
        if mode == 'text':
            self.run_text_mode()
        else:
            self.run_voice_mode()


def main():
    """Main function to start the assistant."""
    print("🚀 Starting Jarvis Assistant...")
    
    # Check if running in text mode
    import sys
    mode = 'text' if '--text' in sys.argv else 'voice'
    
    try:
        assistant = JarvisAssistant()
        assistant.run(mode)
    except KeyboardInterrupt:
        print("\nShutting down Jarvis Assistant. Goodbye!")
    except Exception as e:
        print(f"Error starting assistant: {e}")
        print("Try running with --text flag for text-only mode")


if __name__ == "__main__":
    main()