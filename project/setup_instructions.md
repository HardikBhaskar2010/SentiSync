# Jarvis AI Assistant - Setup Instructions

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.7 or higher
- Windows 10/11, macOS, or Linux
- Microphone (for voice input)
- Speakers/headphones (for voice output)

### Installation Steps

1. **Download the files**
   - Save all the Python files to a folder (e.g., `jarvis_assistant`)

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install PyAudio (Windows users)**
   If you encounter issues with PyAudio on Windows:
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

4. **Run the assistant**
   
   **Voice Mode (Default):**
   ```bash
   python assistant.py
   ```
   
   **Text Mode:**
   ```bash
   python assistant.py --text
   ```
   
   **GUI Mode:**
   ```bash
   python gui_assistant.py
   ```

## 🎯 How to Use

### Voice Commands
Say "Jarvis" followed by your command:

- **"Jarvis, what time is it?"** - Get current time and date
- **"Jarvis, search for Python tutorials"** - Search the web
- **"Jarvis, open notepad"** - Open applications
- **"Jarvis, write a note: Buy groceries"** - Save notes
- **"Jarvis, read my notes"** - Hear your saved notes
- **"Jarvis, tell me a joke"** - Get entertainment
- **"Jarvis, weather in New York"** - Get weather info
- **"Jarvis, list files"** - See directory contents
- **"Jarvis, create file test.txt"** - Create new files
- **"Jarvis, play music"** - Open music player

### Text Commands
Type commands directly (without "Jarvis"):

- `search for machine learning`
- `open chrome`
- `add note: Meeting at 3 PM`
- `what time is it`
- `help` - See all available commands

## 🛠️ Troubleshooting

### Common Issues

1. **"No module named 'speech_recognition'"**
   ```bash
   pip install speech_recognition
   ```

2. **PyAudio installation fails**
   - Windows: Use `pipwin install pyaudio`
   - macOS: `brew install portaudio` then `pip install pyaudio`
   - Linux: `sudo apt-get install python3-pyaudio`

3. **Microphone not working**
   - Check microphone permissions
   - Test with other applications
   - Try different microphone devices

4. **Voice recognition not working**
   - Ensure internet connection (Google Speech API)
   - Speak clearly and close to microphone
   - Check microphone volume levels

### Performance Tips

- **Faster startup**: Use text mode for quicker responses
- **Better recognition**: Speak clearly with minimal background noise
- **Custom wake word**: Edit `config.json` to change "jarvis" to something else
- **Voice settings**: Adjust speech rate and volume in `config.json`

## 🔧 Customization

### Voice Settings
Edit `config.json`:
```json
{
  "voice_rate": 200,        // Speech speed (150-300)
  "voice_volume": 0.9,      // Volume (0.0-1.0)
  "voice_id": 0,            // Voice selection (0, 1, 2...)
  "wake_word": "jarvis",    // Your custom wake word
  "auto_listen": true       // Continuous listening
}
```

### Adding New Commands
Edit `assistant.py` in the `process_command` method:

```python
elif 'your command' in command:
    # Your custom functionality here
    self.speak("Custom response")
```

### File Locations
- **Notes**: `notes.json`
- **Config**: `config.json`
- **Logs**: Console output

## 🌟 Features Overview

### Core Capabilities
- ✅ Voice recognition and text-to-speech
- ✅ Web searching with summaries
- ✅ Application launching
- ✅ File management (create, read, list)
- ✅ Note-taking system
- ✅ Time and date information
- ✅ Weather information
- ✅ Entertainment (jokes)
- ✅ Customizable personality

### Advanced Features
- 🎨 Beautiful GUI interface
- 🔧 Configurable settings
- 💾 Persistent note storage
- 🎤 Wake word detection
- 🌐 Cross-platform compatibility
- 🔒 Completely local (privacy-focused)

## 🚀 Next Steps

1. **Try different commands** - Experiment with various voice and text inputs
2. **Customize settings** - Adjust voice and behavior in `config.json`
3. **Add features** - Extend functionality by modifying the code
4. **Create shortcuts** - Set up desktop shortcuts for quick access

## 💡 Pro Tips

- Use the GUI for a more visual experience
- Keep commands simple and clear
- Save important information as notes
- Use text mode for faster interaction
- Customize the wake word to something unique

Enjoy your personal AI assistant! 🤖✨