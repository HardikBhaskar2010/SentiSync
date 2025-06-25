#!/usr/bin/env python3
"""
Voice utilities for Jarvis Assistant
Handles text-to-speech and speech-to-text with threading and fallbacks
"""

import threading
import queue
import speech_recognition as sr
import pyttsx3
import logging

logger = logging.getLogger(__name__)

class Voice:
    def __init__(self, config):
        """Initialize voice system with configuration."""
        self.config = config
        
        # Initialize TTS engine
        try:
            self.tts = pyttsx3.init()
            self._setup_tts()
        except Exception as e:
            logger.error(f"TTS initialization failed: {e}")
            self.tts = None
        
        # Initialize STT components
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Threading setup for non-blocking TTS
        self._speech_queue = queue.Queue()
        self._speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self._speech_thread.start()
        
        logger.info("Voice system initialized")

    def _setup_tts(self):
        """Configure TTS engine settings."""
        if not self.tts:
            return
        
        try:
            voices = self.tts.getProperty('voices')
            if voices and len(voices) > self.config.get('voice_id', 0):
                voice_id = self.config.get('voice_id', 0)
                self.tts.setProperty('voice', voices[voice_id].id)
            
            self.tts.setProperty('rate', self.config.get('voice_rate', 200))
            self.tts.setProperty('volume', self.config.get('voice_volume', 0.9))
        except Exception as e:
            logger.warning(f"TTS setup warning: {e}")

    def _speech_worker(self):
        """Background worker for TTS processing."""
        while True:
            try:
                text, emotion = self._speech_queue.get()
                if text is None:  # Shutdown signal
                    break
                
                if self.tts:
                    # Adjust rate based on emotion
                    base_rate = self.config.get('voice_rate', 200)
                    if emotion == 'excited':
                        rate = base_rate + 20
                    elif emotion == 'calm':
                        rate = base_rate - 20
                    else:
                        rate = base_rate
                    
                    self.tts.setProperty('rate', rate)
                    self.tts.say(text)
                    self.tts.runAndWait()
                
            except Exception as e:
                logger.error(f"TTS worker error: {e}")
            finally:
                self._speech_queue.task_done()

    def speak(self, text, emotion='neutral'):
        """Queue text for speech synthesis."""
        print(f"🗣️ Jarvis ({emotion}): {text}")
        
        if self.tts:
            self._speech_queue.put((text, emotion))
        else:
            logger.warning("TTS not available, text-only output")

    def listen(self, timeout=5, phrase_time_limit=10, offline_fallback=False):
        """Listen for voice input with proper timeout handling."""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Handle timeout at the listening level
                try:
                    audio = self.recognizer.listen(
                        source, 
                        timeout=timeout, 
                        phrase_time_limit=phrase_time_limit
                    )
                except sr.WaitTimeoutError:
                    # Normal timeout - no speech detected, not an error
                    return None
            
            print("🔄 Processing speech...")
            
            # Try Google Speech Recognition first (unless offline forced)
            if not offline_fallback:
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"👤 You said: {text}")
                    return text
                except sr.RequestError as e:
                    print(f"⚠️ Google STT failed: {e}. Trying offline fallback...")
                    # Fall through to offline recognition
                except sr.UnknownValueError:
                    print("⚠️ Google STT could not understand audio.")
                    return None
            
            # Offline fallback using PocketSphinx
            try:
                print("🔄 Processing with PocketSphinx (offline)...")
                text = self.recognizer.recognize_sphinx(audio).lower()
                print(f"👤 (offline) You said: {text}")
                return text
            except Exception as e:
                logger.warning(f"Offline STT failed: {e}")
                return None
            
        except Exception as e:
            # Only log unexpected errors, not timeouts
            logger.error(f"Unexpected listening error: {e}")
            return None

    def shutdown(self):
        """Gracefully shutdown voice system."""
        if hasattr(self, '_speech_queue'):
            self._speech_queue.put((None, None))  # Shutdown signal
        logger.info("Voice system shutdown")