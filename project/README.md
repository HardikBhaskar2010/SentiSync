# 🤖 Jarvis - Local AI Assistant

A powerful, voice-activated personal assistant that runs completely locally on your machine. Inspired by Tony Stark's Jarvis, this assistant combines voice recognition, text-to-speech, web searching, file management, and much more!

## ✨ Features

### 🎤 Voice & Text Interaction
- **Voice Commands**: Say "Jarvis" followed by your command
- **Text Interface**: Type commands directly for faster interaction
- **Natural Language**: Understands conversational commands
- **Text-to-Speech**: Responds with a friendly, customizable voice

### 🌐 Web & Information
- **Web Search**: Search Google and get instant summaries
- **Weather Info**: Get weather updates for any city
- **Time & Date**: Current time and date information
- **Smart Responses**: Context-aware, personality-driven replies

### 💻 System Control
- **App Launcher**: Open any application (Notepad, Chrome, Calculator, etc.)
- **File Management**: Create, read, and list files and directories
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **System Integration**: Deep OS integration for seamless control

### 📝 Personal Assistant
- **Note Taking**: Save and retrieve notes with timestamps
- **Reminders**: Voice-activated note creation
- **Entertainment**: Jokes, fun interactions, and personality
- **Customizable**: Adjust voice, speed, wake words, and behavior

### 🎨 Multiple Interfaces
- **Voice Mode**: Hands-free operation with wake word detection
- **Text Mode**: Fast keyboard-based interaction
- **GUI Mode**: Beautiful graphical interface with chat history

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Jarvis
```bash
# Voice Mode (Default)
python assistant.py

# Text Mode
python assistant.py --text

# GUI Mode
python gui_assistant.py
```

### 3. Start Commanding!
- **Voice**: "Jarvis, what time is it?"
- **Text**: `search for Python tutorials`

## 🎯 Example Commands

### Information & Search
- "Jarvis, search for machine learning tutorials"
- "Jarvis, what time is it?"
- "Jarvis, weather in New York"

### System Control
- "Jarvis, open Chrome"
- "Jarvis, open notepad"
- "Jarvis, list files"
- "Jarvis, create file shopping.txt"

### Personal Assistant
- "Jarvis, write a note: Meeting at 3 PM tomorrow"
- "Jarvis, read my notes"
- "Jarvis, tell me a joke"

### File Management
- "Jarvis, read file document.txt"
- "Jarvis, list files in Documents"
- "Jarvis, create file ideas.txt"

## 🛠️ Installation Guide

### Prerequisites
- Python 3.7+
- Microphone (for voice input)
- Speakers/headphones (for voice output)

### Step-by-Step Setup

1. **Clone or download** all files to a folder
2. **Install Python packages**:
   ```bash
   pip install speech_recognition pyttsx3 requests beautifulsoup4 pyaudio
   ```
3. **For Windows users** (if PyAudio fails):
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```
4. **Run the assistant**:
   ```bash
   python assistant.py
   ```

## ⚙️ Customization

### Voice Settings
Edit `config.json`:
```json
{
  "voice_rate": 200,        // Speech speed
  "voice_volume": 0.9,      // Volume level
  "voice_id": 0,            // Voice selection
  "wake_word": "jarvis",    // Custom wake word
  "auto_listen": true       // Continuous listening
}
```

### Adding Custom Commands
Extend functionality by modifying the `process_command` method in `assistant.py`:

```python
elif 'custom command' in command:
    # Your custom functionality
    self.speak("Custom response")
```

## 🎨 GUI Features

The GUI mode provides:
- **Chat Interface**: Visual conversation history
- **Voice Toggle**: Switch between voice and text modes
- **Notes Viewer**: Dedicated notes management
- **Status Indicators**: Real-time system status
- **Modern Design**: Dark theme with accent colors

## 🔒 Privacy & Security

- **100% Local**: No cloud dependencies for core functionality
- **No Data Collection**: Your conversations stay on your device
- **Open Source**: Full transparency in code and functionality
- **Secure**: No external API keys required for basic features

## 🌟 Advanced Features

### Multi-Modal Interaction
- Seamlessly switch between voice and text
- GUI provides visual feedback and history
- Batch command processing

### Intelligent Responses
- Context-aware conversations
- Personality-driven interactions
- Error handling with helpful suggestions

### System Integration
- Cross-platform application launching
- File system navigation and management
- Web browser integration

## 🤝 Contributing

Want to make Jarvis even better? Here are some ideas:
- Add new voice commands
- Improve natural language processing
- Create new GUI themes
- Add integration with more applications
- Enhance web scraping capabilities

## 📋 Requirements

### Python Packages
- `speech_recognition` - Voice input processing
- `pyttsx3` - Text-to-speech conversion
- `requests` - Web requests and API calls
- `beautifulsoup4` - Web scraping and parsing
- `pyaudio` - Audio input/output handling

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100MB for installation
- **Audio**: Microphone and speakers/headphones

## 🎯 Roadmap

- [ ] Integration with calendar applications
- [ ] Email management capabilities
- [ ] Smart home device control
- [ ] Machine learning for better command recognition
- [ ] Plugin system for easy extensibility
- [ ] Mobile app companion

## 🆘 Troubleshooting

### Common Issues
1. **Microphone not detected**: Check system permissions and device settings
2. **Voice recognition fails**: Ensure internet connection for Google Speech API
3. **PyAudio installation error**: Use platform-specific installation methods
4. **Application won't open**: Check if application exists and is in system PATH

### Getting Help
- Check the detailed setup instructions in `setup_instructions.md`
- Review error messages in the console
- Test with text mode if voice mode fails
- Verify all dependencies are installed correctly

---

**Made with ❤️ for productivity and fun!**

*Transform your computer into an intelligent assistant that actually understands you.*