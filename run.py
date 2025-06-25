#!/usr/bin/env python3
"""
Enhanced Jarvis Assistant - Main Launcher
Single entry point for text, voice, or GUI mode
"""

import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.assistant import Assistant

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('jarvis.log')
    ]
)

logger = logging.getLogger(__name__)

def print_banner():
    """Print startup banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🤖 ENHANCED JARVIS                        ║
    ║                  Free AI-Powered Assistant                   ║
    ║                                                              ║
    ║  Powered by: Hugging Face • Groq • Ollama • Free APIs       ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def show_help():
    """Show usage help."""
    help_text = """
Usage: python run.py [OPTIONS]

Options:
  --text        Run in text-only mode (faster, no voice)
  --voice       Run in voice mode (default)
  --gui         Run with graphical interface (coming soon)
  --help        Show this help message

Examples:
  python run.py              # Voice mode
  python run.py --text       # Text mode
  python run.py --voice      # Explicit voice mode

Features:
  • AI-powered conversations using free services
  • Voice recognition and text-to-speech
  • Weather, news, and web search
  • Note-taking and reminders
  • Cross-platform compatibility
  • Completely free to use!

For setup instructions, see: free_ai_setup_guide.md
    """
    print(help_text)

def main():
    """Main entry point for the enhanced assistant."""
    try:
        # Parse command line arguments
        args = sys.argv[1:]
        
        if '--help' in args or '-h' in args:
            show_help()
            return
        
        # Determine mode
        if '--text' in args:
            mode = 'text'
        elif '--gui' in args:
            mode = 'gui'
        else:
            mode = 'voice'  # Default
        
        print_banner()
        
        if mode == 'gui':
            print("🚧 GUI mode coming soon! Using voice mode instead.")
            mode = 'voice'
        
        # Initialize and run assistant
        logger.info(f"Starting Enhanced Jarvis in {mode} mode")
        assistant = Assistant()
        
        try:
            if mode == 'text':
                assistant.run_text_mode()
            else:
                assistant.run_voice_mode()
        finally:
            assistant.shutdown()
            
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Enhanced Jarvis Assistant. Goodbye!")
        logger.info("Assistant shutdown via keyboard interrupt")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required packages: pip install -r free_ai_requirements.txt")
        logger.error(f"Import error: {e}")
    except Exception as e:
        print(f"❌ Error starting assistant: {e}")
        logger.error(f"Startup error: {e}")
        print("\nTroubleshooting:")
        print("1. Check that all dependencies are installed")
        print("2. Verify your microphone is working (for voice mode)")
        print("3. Try text mode: python run.py --text")
        print("4. Check the log file: jarvis.log")

if __name__ == "__main__":
    main()