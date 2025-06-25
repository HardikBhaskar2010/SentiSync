#!/usr/bin/env python3
"""
Enhanced Jarvis Assistant - Core Logic
Modular AI assistant with multiple service support and clean architecture
"""

import os
import json
import datetime
import asyncio
import requests
import webbrowser
import logging
import random
from pathlib import Path
from typing import Dict, List, Optional

import aiohttp
import wikipedia
import yfinance as yf
from bs4 import BeautifulSoup

from src.utils.voice import Voice

logger = logging.getLogger(__name__)

class Assistant:
    def __init__(self, config_path='free_ai_config.json'):
        """Initialize the enhanced assistant."""
        self.config = self._load_config(config_path)
        self.voice = Voice(self.config)
        self.notes = self._load_notes()
        self.conversation_history = []
        
        # AI service endpoints
        self.ai_services = {
            'huggingface': 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium',
            'groq': 'https://api.groq.com/openai/v1/chat/completions',
            'ollama': 'http://localhost:11434/api/generate'
        }
        
        # Personality responses
        self.greetings = [
            "Hello! I'm Jarvis, your enhanced AI assistant. How can I help?",
            "Good to see you! What can I do for you today?",
            "Hey there! Ready to get things done with AI power?",
            "At your service! What's on your mind?"
        ]
        
        self.confirmations = [
            "Done!", "Consider it handled!", "All set!", 
            "Mission accomplished!", "Got it covered!"
        ]
        
        logger.info("Assistant initialized successfully")
        self.voice.speak("Enhanced Jarvis online! Powered by free AI services and ready for action!", 'excited')

    def _load_config(self, path: str) -> Dict:
        """Load configuration with sensible defaults."""
        default_config = {
            "voice_rate": 200,
            "voice_volume": 0.9,
            "voice_id": 0,
            "wake_word": "jarvis",
            "ai_service": "huggingface",
            "huggingface_token": "",
            "groq_api_key": "",
            "weather_api_key": "",
            "news_api_key": "",
            "max_conversation_history": 10,
            "enable_learning": True,
            "personality_mode": "friendly",
            "fallback_responses": True
        }
        
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    user_config = json.load(f)
                # Merge with defaults
                config = {**default_config, **user_config}
            else:
                config = default_config
                # Save default config
                with open(path, 'w') as f:
                    json.dump(config, f, indent=2)
            
            return config
        except Exception as e:
            logger.error(f"Config loading error: {e}")
            return default_config

    def _load_notes(self) -> List[Dict]:
        """Load notes from JSON file."""
        notes_file = "notes.json"
        try:
            if os.path.exists(notes_file):
                with open(notes_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Notes loading error: {e}")
        return []

    def _save_notes(self):
        """Save notes to JSON file."""
        try:
            with open("notes.json", 'w') as f:
                json.dump(self.notes, f, indent=2)
        except Exception as e:
            logger.error(f"Notes saving error: {e}")

    def add_note(self, text: str):
        """Add a new note with timestamp."""
        note = {
            "text": text,
            "timestamp": datetime.datetime.now().isoformat(),
            "id": len(self.notes) + 1
        }
        self.notes.append(note)
        self._save_notes()
        self.voice.speak(f"Note saved: {text}", 'accomplished')

    def read_notes(self):
        """Read recent notes aloud."""
        if not self.notes:
            self.voice.speak("You don't have any notes saved.", 'informative')
            return
        
        self.voice.speak(f"You have {len(self.notes)} notes. Here are the recent ones:", 'informative')
        for note in self.notes[-3:]:  # Last 3 notes
            timestamp = datetime.datetime.fromisoformat(note['timestamp'])
            formatted_time = timestamp.strftime("%B %d at %I:%M %p")
            self.voice.speak(f"{note['text']} - saved on {formatted_time}", 'neutral')

    async def _get_huggingface_response(self, prompt: str) -> Optional[str]:
        """Get response from Hugging Face API."""
        try:
            headers = {}
            if self.config.get('huggingface_token'):
                headers['Authorization'] = f"Bearer {self.config['huggingface_token']}"
            
            payload = {
                "inputs": prompt,
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
                            return result[0].get('generated_text', '').replace(prompt, '').strip()
                    else:
                        logger.warning(f"Hugging Face API error: {response.status}")
        except Exception as e:
            logger.error(f"Hugging Face API error: {e}")
        return None

    async def _get_groq_response(self, prompt: str) -> Optional[str]:
        """Get response from Groq API."""
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
                    {"role": "system", "content": "You are Jarvis, a helpful AI assistant. Be concise and friendly."},
                    {"role": "user", "content": prompt}
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
        except Exception as e:
            logger.error(f"Groq API error: {e}")
        return None

    def _get_ollama_response(self, prompt: str) -> Optional[str]:
        """Get response from local Ollama instance."""
        try:
            payload = {
                "model": "llama2",
                "prompt": f"You are Jarvis, a helpful AI assistant. User: {prompt}\nJarvis:",
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
        except requests.exceptions.ConnectionError:
            logger.info("Ollama not running locally")
        except Exception as e:
            logger.error(f"Ollama error: {e}")
        return None

    def get_ai_response(self, prompt: str) -> str:
        """Get AI response with fallback chain."""
        ai_service = self.config.get('ai_service', 'huggingface')
        
        # Try primary service
        response = None
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            if ai_service == 'groq':
                response = loop.run_until_complete(self._get_groq_response(prompt))
            elif ai_service == 'ollama':
                response = self._get_ollama_response(prompt)
            else:  # Default to Hugging Face
                response = loop.run_until_complete(self._get_huggingface_response(prompt))
            
            loop.close()
        except Exception as e:
            logger.error(f"AI service error: {e}")
        
        # Fallback chain
        if not response:
            if ai_service != 'huggingface':
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response = loop.run_until_complete(self._get_huggingface_response(prompt))
                    loop.close()
                except:
                    pass
            
            if not response and ai_service != 'ollama':
                response = self._get_ollama_response(prompt)
        
        # Final fallback to rule-based responses
        if not response:
            response = self._get_fallback_response(prompt)
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": prompt})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Keep history manageable
        max_history = self.config.get('max_conversation_history', 10) * 2
        if len(self.conversation_history) > max_history:
            self.conversation_history = self.conversation_history[-max_history:]
        
        return response

    def _get_fallback_response(self, prompt: str) -> str:
        """Generate fallback responses for when AI services fail."""
        prompt_lower = prompt.lower()
        
        # Greeting patterns
        if any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'good morning']):
            return random.choice(self.greetings)
        
        # Question patterns
        if any(word in prompt_lower for word in ['what', 'how', 'why', 'when', 'where']):
            return "That's an interesting question! I can help with searches, notes, weather, news, and more."
        
        # Default responses
        responses = [
            "I understand you're asking about that. How can I assist you further?",
            "I can help with web searches, notes, weather, news, and system tasks. What would you like to do?",
            "I'm here to help! Try asking me to search for something, take notes, or get information.",
            "Let me know what you need - I can search the web, manage notes, or provide information."
        ]
        return random.choice(responses)

    def _get_weather(self, city: str = "") -> str:
        """Get weather information."""
        if not self.config.get('weather_api_key'):
            return "Weather API not configured. Get a free key from OpenWeatherMap."
        
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

    def _get_news(self, topic: str = "technology") -> List[str]:
        """Get latest news."""
        if not self.config.get('news_api_key'):
            return ["News API not configured. Get a free key from NewsAPI.org"]
        
        try:
            api_key = self.config['news_api_key']
            url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&pageSize=3&apiKey={api_key}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                articles = data['articles']
                return [f"{article['title']} - {article['source']['name']}" for article in articles[:3]]
            else:
                return ["Couldn't fetch news right now."]
                
        except Exception as e:
            return [f"News service error: {e}"]

    def handle_command(self, command: str) -> bool:
        """Process and handle user commands."""
        command = command.lower().strip()
        
        # AI-powered conversation
        if any(word in command for word in ['how are you', 'what do you think', 'tell me about', 'explain']):
            response = self.get_ai_response(command)
            self.voice.speak(response, 'friendly')
        
        # Notes
        elif 'note' in command:
            if 'read' in command:
                self.read_notes()
            elif any(word in command for word in ['write', 'add', ':']):
                if ':' in command:
                    note_text = command.split(':', 1)[1].strip()
                else:
                    note_text = command.replace('write a note', '').replace('add note', '').strip()
                
                if note_text:
                    self.add_note(note_text)
                else:
                    self.voice.speak("What would you like me to note down?", 'questioning')
        
        # Weather
        elif 'weather' in command:
            city = ""
            if 'in' in command:
                city = command.split('in', 1)[1].strip()
            weather_info = self._get_weather(city)
            self.voice.speak(weather_info, 'informative')
        
        # News
        elif 'news' in command:
            topic = "general"
            if 'about' in command:
                topic = command.split('about', 1)[1].strip()
            
            news_items = self._get_news(topic)
            self.voice.speak(f"Here are the latest {topic} news:", 'informative')
            for item in news_items:
                self.voice.speak(item, 'neutral')
        
        # Time
        elif any(word in command for word in ['time', 'date']):
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M %p")
            date_str = now.strftime("%A, %B %d, %Y")
            self.voice.speak(f"It's {time_str} on {date_str}", 'informative')
        
        # Web search
        elif 'search' in command:
            query = command.replace('search for', '').replace('search', '').strip()
            if query:
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                self.voice.speak(f"Opened web search for {query}", 'informative')
            else:
                self.voice.speak("What would you like me to search for?", 'questioning')
        
        # Jokes
        elif 'joke' in command:
            response = self.get_ai_response("Tell me a clever, witty joke")
            self.voice.speak(response, 'humorous')
        
        # Exit commands
        elif any(word in command for word in ['goodbye', 'bye', 'exit', 'quit', 'stop']):
            farewell = random.choice([
                "Goodbye! It was great helping you today!",
                "See you later! Take care!",
                "Until next time! Stay awesome!",
                "Farewell! I'll be here when you need me!"
            ])
            self.voice.speak(farewell, 'warm')
            return False
        
        # Help
        elif 'help' in command:
            help_text = """I'm your enhanced AI assistant! I can help with:
            - Intelligent conversations and questions
            - Weather, news, and information
            - Web searches and Wikipedia lookups
            - Notes and reminders
            - Time and date
            - Entertainment like jokes
            Just ask me naturally!"""
            self.voice.speak(help_text, 'helpful')
        
        # Default AI response
        else:
            response = self.get_ai_response(command)
            self.voice.speak(response, 'helpful')
        
        return True

    def run_text_mode(self):
        """Run assistant in text-only mode."""
        print("\n🤖 Enhanced Jarvis Assistant - Text Mode")
        print("Type your questions or commands. I'm powered by free AI services!")
        print("Type 'help' to see what I can do, or 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                if not user_input:
                    continue
                
                if not self.handle_command(user_input):
                    break
                    
            except KeyboardInterrupt:
                print("\n")
                self.voice.speak("Goodbye!", 'warm')
                break
            except Exception as e:
                logger.error(f"Text mode error: {e}")

    def run_voice_mode(self):
        """Run assistant in voice mode."""
        print("\n🤖 Enhanced Jarvis Assistant - Voice Mode")
        print("Say 'Jarvis' to wake me up, then give your command.")
        print("Say 'quit' or 'exit' to stop.\n")
        
        while True:
            try:
                # Listen for wake word
                command = self.voice.listen(timeout=2)
                
                if command is None:
                    continue
                
                # Check for wake word
                if self.config['wake_word'] in command:
                    self.voice.speak("Yes? I'm listening.", 'attentive')
                    
                    # Listen for actual command
                    command = self.voice.listen(timeout=15)
                    if command:
                        if not self.handle_command(command):
                            break
                
                elif any(word in command for word in ['quit', 'exit', 'goodbye']):
                    self.voice.speak("Goodbye!", 'warm')
                    break
                    
            except KeyboardInterrupt:
                print("\n")
                self.voice.speak("Goodbye!", 'warm')
                break
            except Exception as e:
                logger.error(f"Voice mode error: {e}")

    def shutdown(self):
        """Gracefully shutdown the assistant."""
        self.voice.shutdown()
        logger.info("Assistant shutdown complete")