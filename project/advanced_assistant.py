#!/usr/bin/env python3
"""
Advanced Jarvis - AI-Powered Local Assistant
Enhanced with OpenAI GPT, weather APIs, news APIs, and more advanced capabilities.
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
import openai
from typing import Dict, List, Optional
import asyncio
import aiohttp
import wikipedia
import wolframalpha
import yfinance as yf
import pyautogui
import psutil
import schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

class AdvancedJarvisAssistant:
    def __init__(self):
        """Initialize the Advanced Jarvis Assistant with AI capabilities."""
        self.system = platform.system()
        self.notes_file = "notes.json"
        self.config_file = "advanced_config.json"
        self.conversation_history = []
        
        # Initialize speech components
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Load configuration and API keys
        self.config = self.load_config()
        self.setup_apis()
        self.setup_voice()
        
        # Load data
        self.notes = self.load_notes()
        self.reminders = self.load_reminders()
        
        # Advanced personality system
        self.personality_traits = {
            "humor_level": 0.7,
            "formality": 0.3,
            "enthusiasm": 0.8,
            "helpfulness": 0.9,
            "curiosity": 0.6
        }
        
        # Context awareness
        self.current_context = {
            "last_command": None,
            "user_mood": "neutral",
            "conversation_topic": None,
            "time_of_day": self.get_time_period()
        }
        
        print("🚀 Advanced Jarvis Assistant initialized successfully!")
        self.speak("Advanced Jarvis online! I'm powered by AI and ready for anything!")

    def load_config(self):
        """Load advanced configuration settings."""
        default_config = {
            "voice_rate": 200,
            "voice_volume": 0.9,
            "voice_id": 0,
            "wake_word": "jarvis",
            "auto_listen": True,
            "openai_api_key": "",
            "weather_api_key": "",
            "news_api_key": "",
            "wolfram_api_key": "",
            "email_settings": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "email": "",
                "password": ""
            },
            "ai_model": "gpt-3.5-turbo",
            "max_conversation_history": 10,
            "enable_learning": True,
            "personality_mode": "friendly"
        }
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except FileNotFoundError:
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config

    def setup_apis(self):
        """Initialize API connections."""
        # OpenAI setup
        if self.config.get('openai_api_key'):
            openai.api_key = self.config['openai_api_key']
            self.ai_enabled = True
        else:
            self.ai_enabled = False
            print("⚠️ OpenAI API key not configured. AI features disabled.")
        
        # Wolfram Alpha setup
        if self.config.get('wolfram_api_key'):
            self.wolfram_client = wolframalpha.Client(self.config['wolfram_api_key'])
            self.wolfram_enabled = True
        else:
            self.wolfram_enabled = False

    def setup_voice(self):
        """Configure advanced text-to-speech settings."""
        voices = self.tts_engine.getProperty('voices')
        if voices and len(voices) > self.config['voice_id']:
            self.tts_engine.setProperty('voice', voices[self.config['voice_id']].id)
        
        self.tts_engine.setProperty('rate', self.config['voice_rate'])
        self.tts_engine.setProperty('volume', self.config['voice_volume'])

    def speak(self, text, emotion="neutral"):
        """Enhanced text-to-speech with emotion and context."""
        # Adjust speech based on emotion
        if emotion == "excited":
            self.tts_engine.setProperty('rate', self.config['voice_rate'] + 20)
        elif emotion == "calm":
            self.tts_engine.setProperty('rate', self.config['voice_rate'] - 20)
        else:
            self.tts_engine.setProperty('rate', self.config['voice_rate'])
        
        print(f"🗣️ Jarvis ({emotion}): {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self, timeout=5):
        """Enhanced voice input with noise reduction."""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Enhanced listening with longer timeout for complex queries
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
            
            print("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio).lower()
            print(f"👤 You said: {text}")
            return text
        
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            self.speak("I didn't catch that clearly. Could you repeat?", "calm")
            return None
        except sr.RequestError as e:
            self.speak("There's an issue with the speech recognition service.", "calm")
            print(f"Error: {e}")
            return None

    def get_ai_response(self, user_input: str, context: str = "") -> str:
        """Get intelligent response from OpenAI GPT."""
        if not self.ai_enabled:
            return self.get_fallback_response(user_input)
        
        try:
            # Build conversation context
            messages = [
                {
                    "role": "system",
                    "content": f"""You are Jarvis, an advanced AI assistant inspired by Tony Stark's AI. 
                    You are helpful, witty, intelligent, and have a personality. You can:
                    - Answer questions intelligently
                    - Help with tasks and planning
                    - Engage in casual conversation
                    - Provide technical assistance
                    - Be creative and entertaining
                    
                    Current context: {context}
                    Time of day: {self.current_context['time_of_day']}
                    User's apparent mood: {self.current_context['user_mood']}
                    
                    Respond in a conversational, helpful manner. Keep responses concise but informative.
                    """
                }
            ]
            
            # Add conversation history
            for msg in self.conversation_history[-5:]:  # Last 5 exchanges
                messages.append(msg)
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            response = openai.ChatCompletion.create(
                model=self.config['ai_model'],
                messages=messages,
                max_tokens=200,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Keep history manageable
            if len(self.conversation_history) > self.config['max_conversation_history'] * 2:
                self.conversation_history = self.conversation_history[-self.config['max_conversation_history']:]
            
            return ai_response
            
        except Exception as e:
            print(f"AI Error: {e}")
            return self.get_fallback_response(user_input)

    def get_fallback_response(self, user_input: str) -> str:
        """Fallback responses when AI is unavailable."""
        responses = [
            "I understand you're asking about that. Let me help you in a different way.",
            "That's an interesting question. While I process that, is there something specific I can help with?",
            "I'm thinking about that. In the meantime, I can help with files, apps, searches, or notes.",
            "Good question! I can assist with various tasks while I work on that."
        ]
        return random.choice(responses)

    def get_weather(self, city: str = "") -> str:
        """Get detailed weather information using API."""
        if not self.config.get('weather_api_key'):
            return "Weather API not configured. Opening weather website instead."
        
        try:
            if not city:
                city = "current location"
            
            api_key = self.config['weather_api_key']
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']
                city_name = data['name']
                
                weather_report = f"Weather in {city_name}: {description.title()}, {temp}°C (feels like {feels_like}°C), humidity {humidity}%"
                return weather_report
            else:
                return f"Couldn't get weather for {city}. {data.get('message', 'Unknown error')}"
                
        except Exception as e:
            return f"Weather service unavailable: {e}"

    def get_news(self, topic: str = "technology") -> List[str]:
        """Get latest news using News API."""
        if not self.config.get('news_api_key'):
            return ["News API not configured."]
        
        try:
            api_key = self.config['news_api_key']
            url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&pageSize=3&apiKey={api_key}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                articles = data['articles']
                news_items = []
                
                for article in articles[:3]:
                    title = article['title']
                    source = article['source']['name']
                    news_items.append(f"{title} - {source}")
                
                return news_items
            else:
                return ["Couldn't fetch news right now."]
                
        except Exception as e:
            return [f"News service error: {e}"]

    def get_stock_price(self, symbol: str) -> str:
        """Get stock price information."""
        try:
            stock = yf.Ticker(symbol.upper())
            info = stock.info
            current_price = info.get('currentPrice', 'N/A')
            company_name = info.get('longName', symbol.upper())
            
            return f"{company_name} ({symbol.upper()}) is currently at ${current_price}"
        except Exception as e:
            return f"Couldn't get stock info for {symbol}: {e}"

    def wolfram_query(self, query: str) -> str:
        """Query Wolfram Alpha for computational answers."""
        if not self.wolfram_enabled:
            return "Wolfram Alpha not configured."
        
        try:
            res = self.wolfram_client.query(query)
            answer = next(res.results).text
            return f"According to Wolfram Alpha: {answer}"
        except Exception as e:
            return f"Couldn't compute that: {e}"

    def get_system_info(self) -> str:
        """Get detailed system information."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info = f"""System Status:
            CPU Usage: {cpu_percent}%
            Memory: {memory.percent}% used ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
            Disk: {disk.percent}% used ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)
            """
            return info
        except Exception as e:
            return f"Couldn't get system info: {e}"

    def take_screenshot(self, filename: str = None) -> str:
        """Take a screenshot."""
        try:
            if not filename:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return f"Screenshot saved as {filename}"
        except Exception as e:
            return f"Couldn't take screenshot: {e}"

    def send_email(self, to_email: str, subject: str, body: str) -> str:
        """Send email using configured SMTP."""
        email_config = self.config.get('email_settings', {})
        
        if not all([email_config.get('email'), email_config.get('password')]):
            return "Email not configured. Please set up email settings."
        
        try:
            msg = MIMEMultipart()
            msg['From'] = email_config['email']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['email'], email_config['password'])
            
            text = msg.as_string()
            server.sendmail(email_config['email'], to_email, text)
            server.quit()
            
            return f"Email sent to {to_email}"
        except Exception as e:
            return f"Couldn't send email: {e}"

    def set_reminder(self, reminder_text: str, when: str) -> str:
        """Set a reminder for later."""
        try:
            reminder = {
                "text": reminder_text,
                "when": when,
                "created": datetime.datetime.now().isoformat(),
                "id": len(self.reminders) + 1
            }
            
            self.reminders.append(reminder)
            self.save_reminders()
            
            return f"Reminder set: {reminder_text} for {when}"
        except Exception as e:
            return f"Couldn't set reminder: {e}"

    def load_reminders(self):
        """Load reminders from file."""
        try:
            with open("reminders.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_reminders(self):
        """Save reminders to file."""
        with open("reminders.json", 'w') as f:
            json.dump(self.reminders, f, indent=2)

    def get_time_period(self) -> str:
        """Get current time period for context."""
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"

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
        return f"Note saved: {note_text}"

    def search_web_advanced(self, query: str) -> str:
        """Advanced web search with AI summarization."""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract search results
            results = []
            for result in soup.find_all('div', class_='BNeawe')[:3]:
                results.append(result.get_text())
            
            if results and self.ai_enabled:
                # Use AI to summarize results
                summary_prompt = f"Summarize these search results for '{query}': {' '.join(results)}"
                summary = self.get_ai_response(summary_prompt, "web_search")
                return summary
            elif results:
                return f"Found: {results[0]}"
            else:
                webbrowser.open(search_url)
                return f"Opened web search for {query}"
                
        except Exception as e:
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            return f"Opened browser search for {query}"

    def process_advanced_command(self, command: str) -> bool:
        """Process advanced AI-powered commands."""
        command = command.lower().strip()
        
        # Update context
        self.current_context['last_command'] = command
        
        # AI-powered general conversation
        if any(word in command for word in ['how are you', 'what do you think', 'tell me about', 'explain', 'why', 'what if']):
            response = self.get_ai_response(command, "general_conversation")
            self.speak(response, "friendly")
        
        # Weather queries
        elif 'weather' in command:
            if 'in' in command:
                city = command.split('in', 1)[1].strip()
            else:
                city = ""
            weather_info = self.get_weather(city)
            self.speak(weather_info, "informative")
        
        # News queries
        elif 'news' in command:
            topic = "general"
            if 'about' in command:
                topic = command.split('about', 1)[1].strip()
            elif 'on' in command:
                topic = command.split('on', 1)[1].strip()
            
            news_items = self.get_news(topic)
            self.speak(f"Here are the latest {topic} news:", "informative")
            for item in news_items:
                self.speak(item, "neutral")
        
        # Stock prices
        elif 'stock price' in command or 'stock' in command:
            if 'of' in command:
                symbol = command.split('of', 1)[1].strip()
            else:
                symbol = command.replace('stock price', '').replace('stock', '').strip()
            
            if symbol:
                stock_info = self.get_stock_price(symbol)
                self.speak(stock_info, "informative")
            else:
                self.speak("Which stock would you like to check?", "questioning")
        
        # Mathematical/computational queries
        elif any(word in command for word in ['calculate', 'compute', 'what is', 'solve']):
            if self.wolfram_enabled:
                result = self.wolfram_query(command)
                self.speak(result, "informative")
            else:
                response = self.get_ai_response(f"Help me with this calculation or question: {command}", "math")
                self.speak(response, "helpful")
        
        # System information
        elif 'system info' in command or 'system status' in command:
            sys_info = self.get_system_info()
            self.speak(sys_info, "technical")
        
        # Screenshot
        elif 'screenshot' in command or 'take a picture' in command:
            result = self.take_screenshot()
            self.speak(result, "accomplished")
        
        # Email
        elif 'send email' in command:
            self.speak("Email feature requires setup. Please configure your email settings.", "informative")
        
        # Reminders
        elif 'remind me' in command or 'set reminder' in command:
            reminder_text = command.replace('remind me to', '').replace('remind me', '').replace('set reminder', '').strip()
            if reminder_text:
                result = self.set_reminder(reminder_text, "later")
                self.speak(result, "accomplished")
            else:
                self.speak("What would you like me to remind you about?", "questioning")
        
        # Enhanced web search
        elif 'search for' in command or 'search' in command:
            query = command.replace('search for', '').replace('search', '').strip()
            if query:
                result = self.search_web_advanced(query)
                self.speak(result, "informative")
            else:
                self.speak("What would you like me to search for?", "questioning")
        
        # Wikipedia search
        elif 'wikipedia' in command or 'wiki' in command:
            topic = command.replace('wikipedia', '').replace('wiki', '').replace('search', '').strip()
            if topic:
                try:
                    summary = wikipedia.summary(topic, sentences=2)
                    self.speak(f"According to Wikipedia: {summary}", "informative")
                except Exception as e:
                    self.speak(f"Couldn't find Wikipedia information about {topic}", "apologetic")
            else:
                self.speak("What topic would you like me to look up on Wikipedia?", "questioning")
        
        # Notes with AI enhancement
        elif 'note' in command:
            if 'write' in command or 'add' in command or ':' in command:
                if ':' in command:
                    note_text = command.split(':', 1)[1].strip()
                else:
                    note_text = command.replace('write a note', '').replace('add note', '').strip()
                
                if note_text:
                    result = self.add_note(note_text)
                    self.speak(result, "accomplished")
                else:
                    self.speak("What would you like me to note down?", "questioning")
            
            elif 'read' in command:
                if not self.notes:
                    self.speak("You don't have any notes saved.", "informative")
                else:
                    self.speak(f"You have {len(self.notes)} notes. Here are the recent ones:", "informative")
                    for note in self.notes[-3:]:  # Last 3 notes
                        timestamp = datetime.datetime.fromisoformat(note['timestamp'])
                        formatted_time = timestamp.strftime("%B %d at %I:%M %p")
                        self.speak(f"{note['text']} - saved on {formatted_time}", "neutral")
        
        # Time and date
        elif any(word in command for word in ['time', 'date', 'what time']):
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M %p")
            date_str = now.strftime("%A, %B %d, %Y")
            self.speak(f"It's {time_str} on {date_str}", "informative")
        
        # Jokes with AI
        elif 'joke' in command:
            if self.ai_enabled:
                joke_response = self.get_ai_response("Tell me a clever, witty joke", "entertainment")
                self.speak(joke_response, "humorous")
            else:
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "I told my computer a joke about UDP... but I'm not sure if it got it.",
                    "Why do programmers prefer dark mode? Because light attracts bugs!"
                ]
                self.speak(random.choice(jokes), "humorous")
        
        # Exit commands
        elif any(word in command for word in ['goodbye', 'bye', 'exit', 'quit', 'stop']):
            farewell_response = self.get_ai_response("Generate a friendly goodbye message", "farewell")
            self.speak(farewell_response if self.ai_enabled else "Goodbye! It was great helping you today!", "warm")
            return False
        
        # Help
        elif 'help' in command:
            help_text = """I'm your advanced AI assistant! I can help with:
            - Intelligent conversations and questions
            - Weather, news, and stock information
            - Web searches with AI summaries
            - Mathematical calculations
            - System monitoring and screenshots
            - Notes and reminders
            - Wikipedia lookups
            - And much more! Just ask me naturally."""
            self.speak(help_text, "helpful")
        
        # Default AI response for unmatched commands
        else:
            if self.ai_enabled:
                response = self.get_ai_response(command, "general_assistance")
                self.speak(response, "helpful")
            else:
                responses = [
                    "I'm not sure about that specific request, but I'm here to help with various tasks.",
                    "Could you rephrase that? I want to make sure I understand correctly.",
                    "That's interesting! Let me know how I can assist you with that."
                ]
                self.speak(random.choice(responses), "questioning")
        
        return True

    def run_advanced_mode(self):
        """Run the advanced assistant with AI capabilities."""
        print("\n🚀 Advanced Jarvis Assistant - AI Mode")
        print("Say 'Jarvis' to wake me up, then give your command.")
        print("I'm powered by AI and can handle complex conversations!")
        print("Say 'quit' or 'exit' to stop.\n")
        
        while True:
            try:
                # Listen for wake word or direct command
                command = self.listen(timeout=2)
                
                if command is None:
                    continue
                
                # Check for wake word
                if self.config['wake_word'] in command:
                    self.speak("Yes? I'm listening.", "attentive")
                    
                    # Listen for actual command with longer timeout
                    command = self.listen(timeout=15)
                    if command:
                        if not self.process_advanced_command(command):
                            break
                
                elif any(word in command for word in ['quit', 'exit', 'goodbye']):
                    self.speak("Goodbye! Take care!", "warm")
                    break
                    
            except KeyboardInterrupt:
                print("\n")
                self.speak("Goodbye!", "warm")
                break
            except Exception as e:
                print(f"Error: {e}")

    def run_text_mode(self):
        """Run in advanced text mode."""
        print("\n🤖 Advanced Jarvis Assistant - Text Mode")
        print("Type your questions or commands. I'm powered by AI!")
        print("Type 'help' to see what I can do, or 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                if not user_input:
                    continue
                
                if not self.process_advanced_command(user_input):
                    break
                    
            except KeyboardInterrupt:
                print("\n")
                self.speak("Goodbye!", "warm")
                break
            except Exception as e:
                print(f"Error: {e}")

    def run(self, mode='voice'):
        """Run the advanced assistant."""
        if mode == 'text':
            self.run_text_mode()
        else:
            self.run_advanced_mode()


def main():
    """Main function to start the advanced assistant."""
    print("🚀 Starting Advanced Jarvis Assistant...")
    
    import sys
    mode = 'text' if '--text' in sys.argv else 'voice'
    
    try:
        assistant = AdvancedJarvisAssistant()
        assistant.run(mode)
    except KeyboardInterrupt:
        print("\nShutting down Advanced Jarvis Assistant. Goodbye!")
    except Exception as e:
        print(f"Error starting assistant: {e}")
        print("Make sure you have all required packages installed and API keys configured.")


if __name__ == "__main__":
    main()