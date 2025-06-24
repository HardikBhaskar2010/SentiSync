#!/usr/bin/env python3
"""
Jarvis GUI - Graphical User Interface for the AI Assistant
A beautiful, modern GUI for the Jarvis Assistant.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
from assistant import JarvisAssistant
import datetime

class JarvisGUI:
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("Jarvis - AI Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize assistant
        self.assistant = None
        self.message_queue = queue.Queue()
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.setup_assistant()
        
        # Start message processing
        self.process_messages()

    def setup_styles(self):
        """Setup custom styles for the GUI."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background='#1a1a1a', 
                       foreground='#00ff41', 
                       font=('Arial', 24, 'bold'))
        
        style.configure('Status.TLabel', 
                       background='#1a1a1a', 
                       foreground='#ffffff', 
                       font=('Arial', 10))
        
        style.configure('Custom.TButton',
                       background='#00ff41',
                       foreground='#000000',
                       font=('Arial', 12, 'bold'))

    def create_widgets(self):
        """Create and layout GUI widgets."""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="🤖 JARVIS", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Initializing...", style='Status.TLabel')
        self.status_label.pack(pady=(0, 10))
        
        # Chat display
        chat_frame = tk.Frame(main_frame, bg='#1a1a1a')
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            bg='#2a2a2a',
            fg='#ffffff',
            font=('Consolas', 11),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg='#1a1a1a')
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_entry = tk.Entry(
            input_frame,
            bg='#2a2a2a',
            fg='#ffffff',
            font=('Arial', 12),
            insertbackground='#00ff41'
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind('<Return>', self.send_message)
        
        self.send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            style='Custom.TButton'
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(fill=tk.X)
        
        self.voice_button = ttk.Button(
            button_frame,
            text="🎤 Voice Mode",
            command=self.toggle_voice_mode,
            style='Custom.TButton'
        )
        self.voice_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(
            button_frame,
            text="Clear Chat",
            command=self.clear_chat,
            style='Custom.TButton'
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.notes_button = ttk.Button(
            button_frame,
            text="📝 Notes",
            command=self.show_notes,
            style='Custom.TButton'
        )
        self.notes_button.pack(side=tk.LEFT)
        
        # Initialize chat
        self.add_message("System", "Welcome to Jarvis! Type your commands or click Voice Mode to speak.")

    def setup_assistant(self):
        """Initialize the assistant in a separate thread."""
        def init_assistant():
            try:
                self.assistant = JarvisAssistant()
                self.message_queue.put(("status", "Ready"))
                self.message_queue.put(("system", "Jarvis is online and ready!"))
            except Exception as e:
                self.message_queue.put(("status", "Error"))
                self.message_queue.put(("system", f"Error initializing assistant: {e}"))
        
        thread = threading.Thread(target=init_assistant, daemon=True)
        thread.start()

    def process_messages(self):
        """Process messages from the queue."""
        try:
            while True:
                msg_type, content = self.message_queue.get_nowait()
                
                if msg_type == "status":
                    self.status_label.config(text=f"Status: {content}")
                elif msg_type == "system":
                    self.add_message("Jarvis", content)
                elif msg_type == "user":
                    self.add_message("You", content)
                elif msg_type == "response":
                    self.add_message("Jarvis", content)
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_messages)

    def add_message(self, sender, message):
        """Add a message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Color coding
        if sender == "You":
            color = "#00ff41"
        elif sender == "Jarvis":
            color = "#41a6ff"
        else:
            color = "#ffff41"
        
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"{sender}: ", sender.lower())
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Configure tags
        self.chat_display.tag_config("timestamp", foreground="#888888")
        self.chat_display.tag_config("you", foreground="#00ff41", font=('Arial', 11, 'bold'))
        self.chat_display.tag_config("jarvis", foreground="#41a6ff", font=('Arial', 11, 'bold'))
        self.chat_display.tag_config("system", foreground="#ffff41", font=('Arial', 11, 'bold'))
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        """Send a text message to the assistant."""
        message = self.input_entry.get().strip()
        if not message or not self.assistant:
            return
        
        self.input_entry.delete(0, tk.END)
        self.add_message("You", message)
        
        # Process command in separate thread
        def process_command():
            try:
                # Capture assistant's response
                original_speak = self.assistant.speak
                
                def capture_speak(text):
                    self.message_queue.put(("response", text))
                    original_speak(text)
                
                self.assistant.speak = capture_speak
                self.assistant.process_command(message)
                self.assistant.speak = original_speak
                
            except Exception as e:
                self.message_queue.put(("response", f"Error: {e}"))
        
        thread = threading.Thread(target=process_command, daemon=True)
        thread.start()

    def toggle_voice_mode(self):
        """Toggle voice input mode."""
        if not self.assistant:
            messagebox.showerror("Error", "Assistant not initialized yet!")
            return
        
        def voice_loop():
            try:
                self.message_queue.put(("system", "Voice mode activated. Say 'Jarvis' to wake me up."))
                
                while True:
                    command = self.assistant.listen(timeout=1)
                    
                    if command is None:
                        continue
                    
                    if self.assistant.config['wake_word'] in command:
                        self.message_queue.put(("system", "Listening for command..."))
                        
                        command = self.assistant.listen(timeout=10)
                        if command:
                            self.message_queue.put(("user", command))
                            
                            # Process command
                            original_speak = self.assistant.speak
                            
                            def capture_speak(text):
                                self.message_queue.put(("response", text))
                                original_speak(text)
                            
                            self.assistant.speak = capture_speak
                            result = self.assistant.process_command(command)
                            self.assistant.speak = original_speak
                            
                            if not result:
                                break
                    
                    elif any(word in command for word in ['quit voice', 'stop voice', 'exit voice']):
                        break
                        
            except Exception as e:
                self.message_queue.put(("system", f"Voice mode error: {e}"))
            
            self.message_queue.put(("system", "Voice mode deactivated."))
        
        thread = threading.Thread(target=voice_loop, daemon=True)
        thread.start()

    def clear_chat(self):
        """Clear the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_message("System", "Chat cleared.")

    def show_notes(self):
        """Show notes in a popup window."""
        if not self.assistant:
            messagebox.showerror("Error", "Assistant not initialized yet!")
            return
        
        notes_window = tk.Toplevel(self.root)
        notes_window.title("Your Notes")
        notes_window.geometry("600x400")
        notes_window.configure(bg='#1a1a1a')
        
        notes_text = scrolledtext.ScrolledText(
            notes_window,
            bg='#2a2a2a',
            fg='#ffffff',
            font=('Arial', 11),
            wrap=tk.WORD
        )
        notes_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if self.assistant.notes:
            for i, note in enumerate(self.assistant.notes, 1):
                timestamp = datetime.datetime.fromisoformat(note['timestamp'])
                formatted_time = timestamp.strftime("%B %d, %Y at %I:%M %p")
                notes_text.insert(tk.END, f"{i}. {note['text']}\n")
                notes_text.insert(tk.END, f"   Saved: {formatted_time}\n\n")
        else:
            notes_text.insert(tk.END, "No notes saved yet.")
        
        notes_text.config(state=tk.DISABLED)

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    """Main function to start the GUI."""
    try:
        app = JarvisGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")


if __name__ == "__main__":
    main()