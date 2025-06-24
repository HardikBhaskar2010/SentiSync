#!/usr/bin/env python3
"""
Enhanced Jarvis - AI Assistant with Free APIs
Uses free AI services like Hugging Face, Ollama, and other open-source models.
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
import asyncio
import aiohttp
import wikipedia
import yfinance as yf
import pyautogui
import psutil
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FreeAIAssistant:
    def __init__(self):
        """Initialize the Enhanced AI Assistant with free APIs."""
        self.system = platform.system()
        self.notes_file = "notes.json"
        self.config_file = "free_ai_config.json"
        self.conversation_history = []
        
        # Initialize speech components
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Load configuration
        self.config = self.load_config()
        self.setup_voice()
        
        # Load data
        self.notes = self.load_notes()
        
        # AI service endpoints (free alternatives)
        self.ai_services = {
            'huggingface': 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium',
            'ollama': 'http://localhost:11434/api/generate',
            'groq': 'https://api.groq.com/openai/v1/chat/completions',
            'together': 'https://api.together.xyz/inference'
        }
        
        # Context awareness
        self.current_context = {
            "last_command": None,
            "user_mood": "neutral",
            "conversation_topic": None,
            "time_of_day": self.get_time_period()
        }
        
        print("🚀 Enhanced Free AI Assistant initialized successfully!")
        self.speak("Enhanced Jarvis online! I'm powered by free AI services and ready for anything!")

    def load_config(self):
        """Load configuration settings with free API options."""
        default_config = {
            "voice_rate": 200,
            "voice_volume": 0.9,
            "voice_id": 0,
            "wake_word": "jarvis",
            "auto_listen": True,
            "ai_service": "huggingface",  # Default to Hugging Face
            "huggingface_token": "",  # Free tier available
            "groq_api_key": "",  # Free tier: 100 requests/day
            "together_api_key": "",  # Free tier available
            "weather_api_key": "",  # OpenWeatherMap free tier
            "news_api_key": "",  # NewsAPI free tier
            "max_conversation_history": 10,
            "enable_learning": True,
            "personality_mode": "friendly",
            "fallback_responses": True
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

    def setup_voice(self):
        """Configure text-to-speech settings."""
        try:
            voices = self.tts_engine.getProperty('voices')
            if voices and len(voices) > self.config['voice_id']:
                self.tts_engine.setProperty('voice', voices[self.config['voice_id']].id)
            
            self.tts_engine.setProperty('rate', self.config['voice_rate'])
            self.tts_engine.setProperty('volume', self.config['voice_volume'])
        except Exception as e:
            logger.warning(f"Voice setup warning: {e}")

    def speak(self, text, emotion="neutral"):
        """Enhanced text-to-speech with emotion."""
        try:
            if emotion == "excited":
                self.tts_engine.setProperty('rate', self.config['voice_rate'] + 20)
            elif emotion == "calm":
                self.tts_engine.setProperty('rate', self.config['voice_rate'] - 20)
            else:
                self.tts_engine.setProperty('rate', self.config['voice_rate'])
            
            print(f"🗣️ Jarvis ({emotion}): {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"Speech error: {e}")
            print(f"🗣️ Jarvis ({emotion}): {text}")

    def listen(self, timeout=5):
        """Enhanced voice input with better error handling."""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
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
            logger.error(f"Speech recognition error: {e}")
            return None

    async def get_huggingface_response(self, user_input: str) -> str:
        """Get response from Hugging Face Inference API (Free)."""
        try:
            headers = {}
            if self.config.get('huggingface_token'):
                headers['Authorization'] = f"Bearer {self.config['huggingface_token']}"
            
            payload = {
                "inputs": user_input,
                "parameters": {
                    "max_length": 100,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.ai_services['huggingface'],
                    headers=headers,
                    json=payload,
                    timeout=10
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if isinstance(result, list) and len(result) > 0:
                            return result[0].get('generated_text', '').replace(user_input, '').strip()
                    else:
                        logger.warning(f"Hugging Face API error: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Hugging Face API error: {e}")
            return None

    async def get_groq_response(self, user_input: str) -> str:
        """Get response from Groq API (Free tier: 100 requests/day)."""
        if not self.config.get('groq_api_key'):
            return None
        
        try:
            headers = {
                'Authorization': f"Bearer {self.config['groq_api_key']}",
                'Content-Type': 'application/json'
            }
            
            payload = {
                "model": "llama2-70b-4096",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Jarvis, a helpful AI assistant. Be concise and friendly."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.ai_services['groq'],
                    headers=headers,
                    json=payload,
                    timeout=10
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['choices'][0]['message']['content'].strip()
                    else:
                        logger.warning(f"Groq API error: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return None

    def get_ollama_response(self, user_input: str) -> str:
        """Get response from local Ollama instance (Free, runs locally)."""
        try:
            payload = {
                "model": "llama2",  # or any model you have installed
                "prompt": f"You are Jarvis, a helpful AI assistant. User: {user_input}\nJarvis:",
                "stream": False
            }
            
            response = requests.post(
                self.ai_services['ollama'],
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                logger.warning(f"Ollama not available: {response.status_code}")
                return None
        except requests.exceptions.ConnectionError:
            logger.info("Ollama not running locally")
            return None
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return None

    async def get_ai_response(self, user_input: str, context: str = "") -> str:
        """Get intelligent response using available free AI services."""
        # Try different AI services in order of preference
        ai_service = self.config.get('ai_service', 'huggingface')
        
        response = None
        
        # Try primary service
        if ai_service == 'groq':
            response = await self.get_groq_response(user_input)
        elif ai_service == 'ollama':
            response = self.get_ollama_response(user_input)
        else:  # Default to Hugging Face
            response = await self.get_huggingface_response(user_input)
        
        # Fallback to other services if primary fails
        if not response:
            if ai_service != 'huggingface':
                response = await self.get_huggingface_response(user_input)
            
            if not response and ai_service != 'ollama':
                response = self.get_ollama_response(user_input)
            
            if not response and ai_service != 'groq':
                response = await self.get_groq_response(user_input)
        
        # Final fallback to rule-based responses
        if not response:
            response = self.get_fallback_response(user_input)
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Keep history manageable
        if len(self.conversation_history) > self.config['max_conversation_history'] * 2:
            self.conversation_history = self.conversation_history[-self.config['max_conversation_history']:]
        
        return response

    def get_fallback_response(self, user_input: str) -> str:
        """Enhanced fallback responses with pattern matching."""
        user_input = user_input.lower()
        
        # Greeting patterns
        if any(word in user_input for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            responses = [
                "Hello! How can I assist you today?",
                "Hi there! What can I help you with?",
                "Hey! Ready to get things done?",
                f"Good {self.get_time_period()}! How may I help you?"
            ]
            return random.choice(responses)
        
        # Question patterns
        if any(word in user_input for word in ['what', 'how', 'why', 'when', 'where']):
            responses = [
                "That's an interesting question! Let me help you find information about that.",
                "I'd be happy to help you understand that better. Let me search for relevant information.",
                "Great question! While I process that, I can help with searches, notes, or system tasks."
            ]
            return random.choice(responses)
        
        # Emotional patterns
        if any(word in user_input for word in ['tired', 'stressed', 'frustrated', 'sad']):
            responses = [
                "I understand that can be challenging. Is there something specific I can help you with?",
                "I'm here to help make things easier for you. What would be most helpful right now?",
                "Let me assist you with whatever you need. Sometimes organizing tasks can help reduce stress."
            ]
            return random.choice(responses)
        
        # Default responses
        responses = [
            "I understand you're asking about that. How can I assist you further?",
            "That's interesting! I can help with searches, notes, system tasks, or information lookup.",
            "I'm here to help! Try asking me to search for something, take notes, or open applications.",
            "I'd be happy to help! I can search the web, manage files, take notes, or control applications."
        ]
        return random.choice(responses)

    def get_weather(self, city: str = "") -> str:
        """Get weather information using free OpenWeatherMap API."""
        if not self.config.get('weather_api_key'):
            return "Weather API not configured. You can get a free API key from OpenWeatherMap."
        
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
                
                return f"Weather in {city_name}: {description.title()}, {temp}°C (feels like {feels_like}°C), humidity {humidity}%"
            else:
                return f"Couldn't get weather for {city}. {data.get('message', 'Unknown error')}"
                
        except Exception as e:
            return f"Weather service unavailable: {e}"

    def get_news(self, topic: str = "technology") -> List[str]:
        """Get latest news using free NewsAPI."""
        if not self.config.get('news_api_key'):
            return ["News API not configured. You can get a free API key from NewsAPI.org"]
        
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
        """Get stock price using free yfinance library."""
        try:
            stock = yf.Ticker(symbol.upper())
            info = stock.info
            current_price = info.get('currentPrice', 'N/A')
            company_name = info.get('longName', symbol.upper())
            
            return f"{company_name} ({symbol.upper()}) is currently at ${current_price}"
        except Exception as e:
            return f"Couldn't get stock info for {symbol}: {e}"

    def search_web_enhanced(self, query: str) -> str:
        """Enhanced web search with AI summarization."""
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
                text = result.get_text().strip()
                if text and len(text) > 10:
                    results.append(text)
            
            if results:
                # Try to get AI summary of results
                summary_prompt = f"Summarize this information about '{query}': {' '.join(results[:2])}"
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    summary = loop.run_until_complete(self.get_ai_response(summary_prompt, "web_search"))
                    loop.close()
                    return summary
                except:
                    return f"Found: {results[0]}"
            else:
                webbrowser.open(search_url)
                return f"Opened web search for {query}"
                
        except Exception as e:
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            return f"Opened browser search for {query}"

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

    def process_enhanced_command(self, command: str) -> bool:
        """Process commands with AI enhancement."""
        command = command.lower().strip()
        
        # Update context
        self.current_context['last_command'] = command
        
        # AI-powered general conversation
        if any(word in command for word in ['how are you', 'what do you think', 'tell me about', 'explain', 'why', 'what if', 'chat']):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(self.get_ai_response(command, "general_conversation"))
                loop.close()
                self.speak(response, "friendly")
            except Exception as e:
                logger.error(f"AI response error: {e}")
                self.speak("I'm having trouble with my AI services right now, but I'm still here to help with other tasks!", "apologetic")
        
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
        
        # Enhanced web search
        elif 'search for' in command or 'search' in command:
            query = command.replace('search for', '').replace('search', '').strip()
            if query:
                result = self.search_web_enhanced(query)
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
        
        # Notes
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
                    for note in self.notes[-3:]:
                        timestamp = datetime.datetime.fromisoformat(note['timestamp'])
                        formatted_time = timestamp.strftime("%B %d at %I:%M %p")
                        self.speak(f"{note['text']} - saved on {formatted_time}", "neutral")
        
        # Time and date
        elif any(word in command for word in ['time', 'date', 'what time']):
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M %p")
            date_str = now.strftime("%A, %B %d, %Y")
            self.speak(f"It's {time_str} on {date_str}", "informative")
        
        # Jokes
        elif 'joke' in command:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                joke_response = loop.run_until_complete(self.get_ai_response("Tell me a clever, witty joke", "entertainment"))
                loop.close()
                self.speak(joke_response, "humorous")
            except:
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "I told my computer a joke about UDP... but I'm not sure if it got it.",
                    "Why do programmers prefer dark mode? Because light attracts bugs!"
                ]
                self.speak(random.choice(jokes), "humorous")
        
        # Exit commands
        elif any(word in command for word in ['goodbye', 'bye', 'exit', 'quit', 'stop']):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                farewell_response = loop.run_until_complete(self.get_ai_response("Generate a friendly goodbye message", "farewell"))
                loop.close()
                self.speak(farewell_response, "warm")
            except:
                self.speak("Goodbye! It was great helping you today!", "warm")
            return False
        
        # Help
        elif 'help' in command:
            help_text = """I'm your enhanced AI assistant powered by free AI services! I can help with:
            - Intelligent conversations and questions
            - Weather, news, and stock information
            - Web searches with AI summaries
            - Wikipedia lookups
            - Notes and reminders
            - And much more! Just ask me naturally."""
            self.speak(help_text, "helpful")
        
        # Default AI response
        else:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(self.get_ai_response(command, "general_assistance"))
                loop.close()
                self.speak(response, "helpful")
            except Exception as e:
                logger.error(f"AI response error: {e}")
                response = self.get_fallback_response(command)
                self.speak(response, "helpful")
        
        return True

    def run_enhanced_mode(self):
        """Run the enhanced assistant with free AI capabilities."""
        print("\n🚀 Enhanced Free AI Assistant")
        print("Say 'Jarvis' to wake me up, then give your command.")
        print("I'm powered by free AI services and can handle complex conversations!")
        print("Say 'quit' or 'exit' to stop.\n")
        
        while True:
            try:
                command = self.listen(timeout=2)
                
                if command is None:
                    continue
                
                if self.config['wake_word'] in command:
                    self.speak("Yes? I'm listening.", "attentive")
                    
                    command = self.listen(timeout=15)
                    if command:
                        if not self.process_enhanced_command(command):
                            break
                
                elif any(word in command for word in ['quit', 'exit', 'goodbye']):
                    self.speak("Goodbye! Take care!", "warm")
                    break
                    
            except KeyboardInterrupt:
                print("\n")
                self.speak("Goodbye!", "warm")
                break
            except Exception as e:
                logger.error(f"Error: {e}")

    def run_text_mode(self):
        """Run in enhanced text mode."""
        print("\n🤖 Enhanced Free AI Assistant - Text Mode")
        print("Type your questions or commands. I'm powered by free AI services!")
        print("Type 'help' to see what I can do, or 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                if not user_input:
                    continue
                
                if not self.process_enhanced_command(user_input):
                    break
                    
            except KeyboardInterrupt:
                print("\n")
                self.speak("Goodbye!", "warm")
                break
            except Exception as e:
                logger.error(f"Error: {e}")

    def run(self, mode='voice'):
        """Run the enhanced assistant."""
        if mode == 'text':
            self.run_text_mode()
        else:
            self.run_enhanced_mode()


def main():
    """Main function to start the enhanced assistant."""
    print("🚀 Starting Enhanced Free AI Assistant...")
    
    import sys
    mode = 'text' if '--text' in sys.argv else 'voice'
    
    try:
        assistant = FreeAIAssistant()
        assistant.run(mode)
    except KeyboardInterrupt:
        print("\nShutting down Enhanced Free AI Assistant. Goodbye!")
    except Exception as e:
        print(f"Error starting assistant: {e}")
        logger.error(f"Startup error: {e}")


if __name__ == "__main__":
    main()