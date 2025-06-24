#!/usr/bin/env python3
"""
Enhanced Jarvis GUI - Free AI-Powered Graphical Interface
Beautiful, modern GUI with free AI conversation capabilities.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import queue
from free_ai_assistant import FreeAIAssistant
import datetime
import json
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedJarvisGUI:
    def __init__(self):
        """Initialize the enhanced GUI application."""
        self.root = tk.Tk()
        self.root.title("Enhanced Jarvis - Free AI Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')
        
        # Initialize assistant
        self.assistant = None
        self.message_queue = queue.Queue()
        self.conversation_active = False
        
        # Setup GUI
        self.setup_styles()
        self.create_enhanced_widgets()
        self.setup_assistant()
        
        # Start message processing
        self.process_messages()

    def setup_styles(self):
        """Setup enhanced custom styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Enhanced color scheme
        colors = {
            'bg_primary': '#0a0a0a',
            'bg_secondary': '#1a1a1a',
            'bg_tertiary': '#2a2a2a',
            'accent_blue': '#00d4ff',
            'accent_green': '#00ff88',
            'accent_orange': '#ff8800',
            'accent_purple': '#8800ff',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc'
        }
        
        # Configure enhanced styles
        style.configure('Title.TLabel', 
                       background=colors['bg_primary'], 
                       foreground=colors['accent_blue'], 
                       font=('Arial', 28, 'bold'))
        
        style.configure('Subtitle.TLabel', 
                       background=colors['bg_primary'], 
                       foreground=colors['accent_green'], 
                       font=('Arial', 14, 'bold'))
        
        style.configure('Status.TLabel', 
                       background=colors['bg_primary'], 
                       foreground=colors['text_secondary'], 
                       font=('Arial', 10))
        
        style.configure('Enhanced.TButton',
                       background=colors['accent_blue'],
                       foreground=colors['bg_primary'],
                       font=('Arial', 11, 'bold'),
                       borderwidth=0)

    def create_enhanced_widgets(self):
        """Create enhanced GUI layout with multiple panels."""
        # Main container
        main_container = tk.Frame(self.root, bg='#0a0a0a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header section
        header_frame = tk.Frame(main_container, bg='#0a0a0a', height=100)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title and status
        title_label = ttk.Label(header_frame, text="🤖 ENHANCED JARVIS", style='Title.TLabel')
        title_label.pack(side=tk.LEFT, padx=(20, 0), pady=10)
        
        self.status_label = ttk.Label(header_frame, text="Initializing free AI systems...", style='Status.TLabel')
        self.status_label.pack(side=tk.RIGHT, padx=(0, 20), pady=10)
        
        # AI service indicator
        self.ai_indicator = tk.Label(header_frame, text="🧠 FREE AI", bg='#0a0a0a', fg='#ff8800', font=('Arial', 12, 'bold'))
        self.ai_indicator.pack(side=tk.RIGHT, padx=(0, 10), pady=10)
        
        # Service status indicators
        self.service_frame = tk.Frame(header_frame, bg='#0a0a0a')
        self.service_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10)
        
        self.hf_indicator = tk.Label(self.service_frame, text="HF", bg='#0a0a0a', fg='#888888', font=('Arial', 8))
        self.hf_indicator.pack(side=tk.TOP)
        
        self.groq_indicator = tk.Label(self.service_frame, text="GROQ", bg='#0a0a0a', fg='#888888', font=('Arial', 8))
        self.groq_indicator.pack(side=tk.TOP)
        
        # Main content area
        content_frame = tk.Frame(main_container, bg='#0a0a0a')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Chat
        left_panel = tk.Frame(content_frame, bg='#1a1a1a', width=700)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Chat header
        chat_header = tk.Frame(left_panel, bg='#1a1a1a', height=40)
        chat_header.pack(fill=tk.X, padx=10, pady=(10, 0))
        chat_header.pack_propagate(False)
        
        chat_title = ttk.Label(chat_header, text="💬 Free AI Conversation", style='Subtitle.TLabel')
        chat_title.pack(side=tk.LEFT, pady=5)
        
        # AI service selector
        self.service_var = tk.StringVar(value="huggingface")
        service_menu = ttk.Combobox(chat_header, textvariable=self.service_var, 
                                   values=["huggingface", "groq", "ollama"], 
                                   state="readonly", width=12)
        service_menu.pack(side=tk.RIGHT, pady=5)
        service_menu.bind('<<ComboboxSelected>>', self.change_ai_service)
        
        # Chat display with enhanced styling
        self.chat_display = scrolledtext.ScrolledText(
            left_panel,
            bg='#2a2a2a',
            fg='#ffffff',
            font=('Consolas', 11),
            wrap=tk.WORD,
            state=tk.DISABLED,
            insertbackground='#00d4ff',
            selectbackground='#00d4ff',
            selectforeground='#000000'
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Input section
        input_frame = tk.Frame(left_panel, bg='#1a1a1a', height=60)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        input_frame.pack_propagate(False)
        
        self.input_entry = tk.Entry(
            input_frame,
            bg='#2a2a2a',
            fg='#ffffff',
            font=('Arial', 12),
            insertbackground='#00d4ff',
            relief=tk.FLAT,
            bd=5
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=15)
        self.input_entry.bind('<Return>', self.send_message)
        
        self.send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            style='Enhanced.TButton'
        )
        self.send_button.pack(side=tk.RIGHT, pady=15)
        
        # Right panel - Controls and Info
        right_panel = tk.Frame(content_frame, bg='#1a1a1a', width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # Control section
        control_header = tk.Frame(right_panel, bg='#1a1a1a', height=40)
        control_header.pack(fill=tk.X, padx=10, pady=(10, 0))
        control_header.pack_propagate(False)
        
        control_title = ttk.Label(control_header, text="🎛️ Controls", style='Subtitle.TLabel')
        control_title.pack(side=tk.LEFT, pady=5)
        
        # Control buttons
        button_frame = tk.Frame(right_panel, bg='#1a1a1a')
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.voice_button = ttk.Button(
            button_frame,
            text="🎤 Voice Mode",
            command=self.toggle_voice_mode,
            style='Enhanced.TButton'
        )
        self.voice_button.pack(fill=tk.X, pady=2)
        
        self.clear_button = ttk.Button(
            button_frame,
            text="🗑️ Clear Chat",
            command=self.clear_chat,
            style='Enhanced.TButton'
        )
        self.clear_button.pack(fill=tk.X, pady=2)
        
        self.notes_button = ttk.Button(
            button_frame,
            text="📝 Notes Manager",
            command=self.show_notes_manager,
            style='Enhanced.TButton'
        )
        self.notes_button.pack(fill=tk.X, pady=2)
        
        self.settings_button = ttk.Button(
            button_frame,
            text="⚙️ Settings",
            command=self.show_settings,
            style='Enhanced.TButton'
        )
        self.settings_button.pack(fill=tk.X, pady=2)
        
        # API Setup button
        self.api_button = ttk.Button(
            button_frame,
            text="🔑 Setup APIs",
            command=self.show_api_setup,
            style='Enhanced.TButton'
        )
        self.api_button.pack(fill=tk.X, pady=2)
        
        # Info section
        info_header = tk.Frame(right_panel, bg='#1a1a1a', height=40)
        info_header.pack(fill=tk.X, padx=10, pady=(20, 0))
        info_header.pack_propagate(False)
        
        info_title = ttk.Label(info_header, text="📊 System Info", style='Subtitle.TLabel')
        info_title.pack(side=tk.LEFT, pady=5)
        
        # System info display
        self.info_display = scrolledtext.ScrolledText(
            right_panel,
            bg='#2a2a2a',
            fg='#ffffff',
            font=('Consolas', 9),
            wrap=tk.WORD,
            state=tk.DISABLED,
            height=8
        )
        self.info_display.pack(fill=tk.X, padx=10, pady=10)
        
        # Quick actions
        quick_frame = tk.Frame(right_panel, bg='#1a1a1a')
        quick_frame.pack(fill=tk.X, padx=10, pady=10)
        
        quick_title = ttk.Label(quick_frame, text="⚡ Quick Actions", style='Subtitle.TLabel')
        quick_title.pack(anchor=tk.W, pady=(0, 5))
        
        quick_buttons = [
            ("🌤️ Weather", lambda: self.quick_command("weather")),
            ("📰 News", lambda: self.quick_command("news")),
            ("🕒 Time", lambda: self.quick_command("what time is it")),
            ("😄 Joke", lambda: self.quick_command("tell me a joke")),
            ("🤖 Chat", lambda: self.quick_command("how are you today?"))
        ]
        
        for text, command in quick_buttons:
            btn = ttk.Button(quick_frame, text=text, command=command, style='Enhanced.TButton')
            btn.pack(fill=tk.X, pady=1)
        
        # Initialize chat
        self.add_message("System", "🚀 Enhanced Free AI Assistant initialized!")
        self.add_message("System", "I'm powered by free AI services like Hugging Face, Groq, and Ollama!")
        self.add_message("System", "Click 'Setup APIs' to configure free API keys for enhanced features.")
        
        # Start system info updates
        self.update_system_info()

    def setup_assistant(self):
        """Initialize the enhanced assistant."""
        def init_assistant():
            try:
                self.assistant = FreeAIAssistant()
                self.message_queue.put(("status", "🟢 Free AI Systems Online"))
                self.message_queue.put(("ai_status", "active"))
                self.message_queue.put(("system", "All systems operational! Ready for free AI assistance."))
                self.update_service_indicators()
            except Exception as e:
                self.message_queue.put(("status", "🔴 Error"))
                self.message_queue.put(("ai_status", "error"))
                self.message_queue.put(("system", f"Error initializing AI: {e}"))
                logger.error(f"Assistant initialization error: {e}")
        
        thread = threading.Thread(target=init_assistant, daemon=True)
        thread.start()

    def update_service_indicators(self):
        """Update AI service status indicators."""
        if not self.assistant:
            return
        
        # Check Hugging Face
        if self.assistant.config.get('huggingface_token'):
            self.hf_indicator.config(fg='#00ff88')
        else:
            self.hf_indicator.config(fg='#ffff00')  # Yellow for free tier
        
        # Check Groq
        if self.assistant.config.get('groq_api_key'):
            self.groq_indicator.config(fg='#00ff88')
        else:
            self.groq_indicator.config(fg='#888888')

    def change_ai_service(self, event=None):
        """Change the active AI service."""
        if self.assistant:
            new_service = self.service_var.get()
            self.assistant.config['ai_service'] = new_service
            self.add_message("System", f"Switched to {new_service.title()} AI service", "system")

    def process_messages(self):
        """Process messages from the queue."""
        try:
            while True:
                msg_type, content = self.message_queue.get_nowait()
                
                if msg_type == "status":
                    self.status_label.config(text=content)
                elif msg_type == "ai_status":
                    if content == "active":
                        self.ai_indicator.config(fg='#00ff88')
                    elif content == "error":
                        self.ai_indicator.config(fg='#ff4444')
                elif msg_type == "system":
                    self.add_message("Jarvis", content, "system")
                elif msg_type == "user":
                    self.add_message("You", content, "user")
                elif msg_type == "response":
                    self.add_message("Jarvis", content, "ai")
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_messages)

    def add_message(self, sender, message, msg_type="normal"):
        """Add a message with enhanced styling."""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Insert timestamp
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Insert sender with appropriate styling
        if sender == "You":
            self.chat_display.insert(tk.END, f"{sender}: ", "user_name")
        elif sender == "Jarvis":
            if msg_type == "ai":
                self.chat_display.insert(tk.END, f"🧠 {sender}: ", "ai_name")
            else:
                self.chat_display.insert(tk.END, f"🤖 {sender}: ", "jarvis_name")
        else:
            self.chat_display.insert(tk.END, f"⚙️ {sender}: ", "system_name")
        
        # Insert message
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Configure tags with enhanced styling
        self.chat_display.tag_config("timestamp", foreground="#888888", font=('Arial', 9))
        self.chat_display.tag_config("user_name", foreground="#00ff88", font=('Arial', 11, 'bold'))
        self.chat_display.tag_config("ai_name", foreground="#00d4ff", font=('Arial', 11, 'bold'))
        self.chat_display.tag_config("jarvis_name", foreground="#ff8800", font=('Arial', 11, 'bold'))
        self.chat_display.tag_config("system_name", foreground="#ffff00", font=('Arial', 11, 'bold'))
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        """Send message to AI assistant."""
        message = self.input_entry.get().strip()
        if not message or not self.assistant:
            return
        
        self.input_entry.delete(0, tk.END)
        self.add_message("You", message, "user")
        
        # Process with AI
        def process_ai_command():
            try:
                original_speak = self.assistant.speak
                
                def capture_speak(text, emotion="neutral"):
                    self.message_queue.put(("response", text))
                    # Still use original speak for audio
                    try:
                        original_speak(text, emotion)
                    except:
                        pass  # Don't fail if TTS fails
                
                self.assistant.speak = capture_speak
                self.assistant.process_enhanced_command(message)
                self.assistant.speak = original_speak
                
            except Exception as e:
                self.message_queue.put(("response", f"Error: {e}"))
                logger.error(f"Command processing error: {e}")
        
        thread = threading.Thread(target=process_ai_command, daemon=True)
        thread.start()

    def quick_command(self, command):
        """Execute quick command."""
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, command)
        self.send_message()

    def toggle_voice_mode(self):
        """Toggle voice input mode."""
        if not self.assistant:
            messagebox.showerror("Error", "AI Assistant not initialized!")
            return
        
        if self.conversation_active:
            self.conversation_active = False
            self.voice_button.config(text="🎤 Voice Mode")
            self.add_message("System", "Voice mode deactivated.", "system")
            return
        
        self.conversation_active = True
        self.voice_button.config(text="🛑 Stop Voice")
        
        def voice_loop():
            try:
                self.message_queue.put(("system", "🎤 Voice mode activated. Say 'Jarvis' to start conversation."))
                
                while self.conversation_active:
                    command = self.assistant.listen(timeout=1)
                    
                    if command is None:
                        continue
                    
                    if not self.conversation_active:
                        break
                    
                    if self.assistant.config['wake_word'] in command:
                        self.message_queue.put(("system", "👂 Listening for your command..."))
                        
                        command = self.assistant.listen(timeout=15)
                        if command and self.conversation_active:
                            self.message_queue.put(("user", command))
                            
                            # Process with AI
                            original_speak = self.assistant.speak
                            
                            def capture_speak(text, emotion="neutral"):
                                self.message_queue.put(("response", text))
                                try:
                                    original_speak(text, emotion)
                                except:
                                    pass
                            
                            self.assistant.speak = capture_speak
                            result = self.assistant.process_enhanced_command(command)
                            self.assistant.speak = original_speak
                            
                            if not result:
                                break
                    
                    elif any(word in command for word in ['stop voice', 'exit voice']):
                        break
                        
            except Exception as e:
                self.message_queue.put(("system", f"Voice error: {e}"))
                logger.error(f"Voice mode error: {e}")
            
            self.conversation_active = False
            self.voice_button.config(text="🎤 Voice Mode")
            self.message_queue.put(("system", "Voice mode deactivated."))
        
        thread = threading.Thread(target=voice_loop, daemon=True)
        thread.start()

    def clear_chat(self):
        """Clear chat display."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_message("System", "Chat cleared.", "system")

    def show_notes_manager(self):
        """Show enhanced notes manager."""
        if not self.assistant:
            messagebox.showerror("Error", "Assistant not initialized!")
            return
        
        notes_window = tk.Toplevel(self.root)
        notes_window.title("📝 Enhanced Notes Manager")
        notes_window.geometry("800x600")
        notes_window.configure(bg='#1a1a1a')
        
        # Notes display
        notes_frame = tk.Frame(notes_window, bg='#1a1a1a')
        notes_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        notes_text = scrolledtext.ScrolledText(
            notes_frame,
            bg='#2a2a2a',
            fg='#ffffff',
            font=('Arial', 11),
            wrap=tk.WORD
        )
        notes_text.pack(fill=tk.BOTH, expand=True)
        
        # Load and display notes
        if self.assistant.notes:
            for i, note in enumerate(self.assistant.notes, 1):
                timestamp = datetime.datetime.fromisoformat(note['timestamp'])
                formatted_time = timestamp.strftime("%B %d, %Y at %I:%M %p")
                notes_text.insert(tk.END, f"📌 Note {i}:\n{note['text']}\n")
                notes_text.insert(tk.END, f"🕒 Saved: {formatted_time}\n")
                notes_text.insert(tk.END, "-" * 50 + "\n\n")
        else:
            notes_text.insert(tk.END, "No notes saved yet.\n\nTry saying: 'Jarvis, write a note: Your note here'")
        
        notes_text.config(state=tk.DISABLED)

    def show_settings(self):
        """Show enhanced settings window."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Enhanced Settings")
        settings_window.geometry("600x500")
        settings_window.configure(bg='#1a1a1a')
        
        # Settings content
        settings_frame = tk.Frame(settings_window, bg='#1a1a1a')
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        settings_text = scrolledtext.ScrolledText(
            settings_frame,
            bg='#2a2a2a',
            fg='#ffffff',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        settings_text.pack(fill=tk.BOTH, expand=True)
        
        # Display current configuration
        if self.assistant:
            config_text = json.dumps(self.assistant.config, indent=2)
            settings_text.insert(tk.END, "Current Configuration:\n\n")
            settings_text.insert(tk.END, config_text)
            settings_text.insert(tk.END, "\n\n" + "="*50 + "\n\n")
            settings_text.insert(tk.END, "To modify settings:\n")
            settings_text.insert(tk.END, "1. Edit 'free_ai_config.json' file\n")
            settings_text.insert(tk.END, "2. Add your free API keys\n")
            settings_text.insert(tk.END, "3. Restart the application\n")

    def show_api_setup(self):
        """Show API setup guide window."""
        api_window = tk.Toplevel(self.root)
        api_window.title("🔑 Free API Setup Guide")
        api_window.geometry("800x600")
        api_window.configure(bg='#1a1a1a')
        
        # API setup content
        api_frame = tk.Frame(api_window, bg='#1a1a1a')
        api_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        api_text = scrolledtext.ScrolledText(
            api_frame,
            bg='#2a2a2a',
            fg='#ffffff',
            font=('Arial', 11),
            wrap=tk.WORD
        )
        api_text.pack(fill=tk.BOTH, expand=True)
        
        setup_guide = """🚀 FREE AI API SETUP GUIDE

🧠 HUGGING FACE (FREE)
• Go to: https://huggingface.co/
• Sign up for free account
• Go to Settings > Access Tokens
• Create new token (read access)
• Add to config: "huggingface_token": "your_token_here"
• Free tier: Rate limited but generous

⚡ GROQ (FREE TIER)
• Go to: https://console.groq.com/
• Sign up for free account
• Get API key from dashboard
• Add to config: "groq_api_key": "your_key_here"
• Free tier: 100 requests/day

🦙 OLLAMA (COMPLETELY FREE)
• Download from: https://ollama.ai/
• Install locally on your computer
• Run: ollama pull llama2
• No API key needed - runs offline!
• Unlimited usage, completely private

🌤️ WEATHER API (FREE)
• Go to: https://openweathermap.org/api
• Sign up for free account
• Get API key from dashboard
• Add to config: "weather_api_key": "your_key_here"
• Free tier: 1,000 calls/day

📰 NEWS API (FREE)
• Go to: https://newsapi.org/
• Sign up for free account
• Get API key from dashboard
• Add to config: "news_api_key": "your_key_here"
• Free tier: 1,000 requests/day

💡 TIPS:
• Start with Hugging Face - no API key needed for basic usage
• Ollama is best for privacy and unlimited usage
• Groq is fastest for quick responses
• All services have generous free tiers
• You can use multiple services as fallbacks

🔧 CONFIGURATION:
Edit 'free_ai_config.json' file with your API keys and restart the application.
"""
        
        api_text.insert(tk.END, setup_guide)
        api_text.config(state=tk.DISABLED)

    def update_system_info(self):
        """Update system information display."""
        if self.assistant:
            try:
                import psutil
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                
                # Check AI service status
                ai_service = self.assistant.config.get('ai_service', 'huggingface')
                hf_status = "🟢 Ready" if self.assistant.config.get('huggingface_token') else "🟡 Free Tier"
                groq_status = "🟢 Configured" if self.assistant.config.get('groq_api_key') else "🔴 Not Set"
                
                info_text = f"""System Status:
CPU: {cpu_percent:.1f}%
Memory: {memory.percent:.1f}%
Available: {memory.available // (1024**3):.1f}GB

AI Services:
Active: {ai_service.title()}
Hugging Face: {hf_status}
Groq: {groq_status}
Ollama: {'🟢 Available' if self.assistant.get_ollama_response('test') else '🔴 Not Running'}

Features:
Weather: {'🟢 Ready' if self.assistant.config.get('weather_api_key') else '🔴 Not Set'}
News: {'🟢 Ready' if self.assistant.config.get('news_api_key') else '🔴 Not Set'}

Conversation History: {len(self.assistant.conversation_history)} messages
Notes: {len(self.assistant.notes)} saved
"""
                
                self.info_display.config(state=tk.NORMAL)
                self.info_display.delete(1.0, tk.END)
                self.info_display.insert(tk.END, info_text)
                self.info_display.config(state=tk.DISABLED)
                
            except Exception as e:
                logger.error(f"System info update error: {e}")
        
        # Schedule next update
        self.root.after(5000, self.update_system_info)

    def run(self):
        """Start the enhanced GUI."""
        self.root.mainloop()


def main():
    """Main function to start the enhanced GUI."""
    try:
        app = EnhancedJarvisGUI()
        app.run()
    except Exception as e:
        print(f"Error starting Enhanced GUI: {e}")
        logger.error(f"GUI startup error: {e}")


if __name__ == "__main__":
    main()