#!/usr/bin/env python3
"""
Main entry point for the Multilingual Healthcare Chatbot
This script handles initialization and startup of all services
"""

import os
import sys
import logging
import time
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from config import Config
from translation_service import TranslationService
from healthcare_faq import HealthcareFAQ
from query_logger import QueryLogger

def setup_logging():
    """Setup comprehensive logging"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=log_format,
        handlers=[
            logging.FileHandler(f'logs/{Config.LOG_FILE}'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific logger levels
    logging.getLogger('transformers').setLevel(logging.WARNING)
    logging.getLogger('torch').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

def check_dependencies():
    """Check if all required dependencies are available"""
    required_packages = [
        'flask', 'transformers', 'torch', 'sklearn', 
        'pandas', 'numpy', 'sentencepiece', 'sacremoses'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True

def initialize_services():
    """Initialize all chatbot services"""
    print("🚀 Initializing Healthcare Chatbot Services...")
    
    services = {}
    
    try:
        # Initialize Translation Service
        print("📡 Loading translation models...")
        translation_service = TranslationService()
        start_time = time.time()
        translation_service.initialize()
        load_time = time.time() - start_time
        
        if translation_service.is_ready():
            print(f"✅ Translation service ready ({load_time:.1f}s)")
            services['translation'] = translation_service
        else:
            print("⚠️  Translation service failed to initialize")
            return None
        
        # Initialize Healthcare FAQ
        print("📚 Loading healthcare FAQ system...")
        healthcare_faq = HealthcareFAQ()
        start_time = time.time()
        healthcare_faq.initialize()
        load_time = time.time() - start_time
        
        if healthcare_faq.is_ready():
            print(f"✅ Healthcare FAQ ready ({load_time:.1f}s)")
            services['faq'] = healthcare_faq
        else:
            print("⚠️  Healthcare FAQ failed to initialize")
            return None
        
        # Initialize Query Logger
        print("📊 Setting up query logging...")
        query_logger = QueryLogger()
        query_logger.initialize()
        
        if query_logger.is_ready():
            print("✅ Query logger ready")
            services['logger'] = query_logger
        else:
            print("⚠️  Query logger failed to initialize")
            return None
        
        return services
        
    except Exception as e:
        logging.error(f"Service initialization failed: {str(e)}")
        print(f"❌ Service initialization failed: {str(e)}")
        return None

def print_startup_info():
    """Print startup information and instructions"""
    print("\n" + "=" * 70)
    print("🏥 MULTILINGUAL HEALTHCARE CHATBOT")
    print("=" * 70)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Web Interface: http://localhost:5000")
    print(f"🔧 API Endpoint: http://localhost:5000/api/chat")
    print(f"📊 Statistics: http://localhost:5000/api/stats")
    print(f"❤️  Health Check: http://localhost:5000/api/health")
    print("\n🌍 Supported Languages:")
    for code, name in Config.SUPPORTED_LANGUAGES.items():
        print(f"   {code}: {name}")
    
    print("\n📋 Features:")
    print("   ✅ Multilingual translation (MarianMT)")
    print("   ✅ Healthcare FAQ responses")
    print("   ✅ Query logging and analytics")
    print("   ✅ Modern web interface")
    print("   ✅ REST API endpoints")
    print("   ✅ Accuracy tracking")
    
    print("\n⚠️  Important Notes:")
    print("   • This chatbot provides general information only")
    print("   • For medical emergencies, contact emergency services")
    print("   • Always consult healthcare professionals for medical advice")
    print("=" * 70)

def main():
    """Main application entry point"""
    try:
        # Setup logging
        setup_logging()
        
        # Check dependencies
        if not check_dependencies():
            return False
        
        # Initialize Flask app configuration
        Config.init_app(app)
        
        # Initialize services
        services = initialize_services()
        if not services:
            print("❌ Failed to initialize services")
            return False
        
        # Print startup information
        print_startup_info()
        
        # Start the Flask application
        print("\n🚀 Starting web server...")
        print("Press Ctrl+C to stop the server\n")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=Config.DEBUG,
            threaded=True
        )
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Healthcare Chatbot...")
        print("Thank you for using our service!")
        return True
        
    except Exception as e:
        logging.error(f"Application startup failed: {str(e)}")
        print(f"\n❌ Application startup failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
