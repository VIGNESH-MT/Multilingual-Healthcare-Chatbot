import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'healthcare-chatbot-secret-key-2024')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Database settings
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'chatbot_logs.db')
    
    # Translation settings
    TRANSLATION_CACHE_SIZE = int(os.getenv('TRANSLATION_CACHE_SIZE', '1000'))
    MAX_TRANSLATION_LENGTH = int(os.getenv('MAX_TRANSLATION_LENGTH', '512'))
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'chatbot.log')
    
    # API settings
    MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '500'))
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
    
    # Healthcare FAQ settings
    FAQ_CONFIDENCE_THRESHOLD = float(os.getenv('FAQ_CONFIDENCE_THRESHOLD', '0.1'))
    MAX_FAQ_RESULTS = int(os.getenv('MAX_FAQ_RESULTS', '5'))
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'fr': 'Français', 
        'de': 'Deutsch',
        'es': 'Español',
        'hi': 'हिन्दी'
    }
    
    # Model settings
    DEVICE = os.getenv('DEVICE', 'auto')  # 'auto', 'cpu', or 'cuda'
    MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR', './models')
    
    @staticmethod
    def init_app(app):
        """Initialize Flask app with configuration"""
        app.config.from_object(Config)
        
        # Create necessary directories
        os.makedirs('logs', exist_ok=True)
        os.makedirs(Config.MODEL_CACHE_DIR, exist_ok=True)
        
        return app
