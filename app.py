from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import logging
from datetime import datetime
import os
from translation_service import TranslationService
from healthcare_faq import HealthcareFAQ
from query_logger import QueryLogger

app = Flask(__name__)
CORS(app)

# Initialize services
translation_service = TranslationService()
healthcare_faq = HealthcareFAQ()
query_logger = QueryLogger()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)

@app.route('/')
def index():
    """Serve the main chatbot interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        target_language = data.get('language', 'en')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Log the incoming query
        query_id = query_logger.log_query(user_message, target_language)
        
        # Translate user message to English if needed
        english_message = user_message
        if target_language != 'en':
            english_message = translation_service.translate_to_english(user_message, target_language)
        
        # Get response from healthcare FAQ
        english_response = healthcare_faq.get_response(english_message)
        
        # Translate response back to target language if needed
        final_response = english_response
        if target_language != 'en':
            final_response = translation_service.translate_from_english(english_response, target_language)
        
        # Calculate accuracy (simplified - based on FAQ match confidence)
        accuracy = healthcare_faq.get_last_confidence()
        
        # Log the response
        query_logger.log_response(query_id, final_response, accuracy)
        
        response_data = {
            'response': final_response,
            'language': target_language,
            'accuracy': accuracy,
            'query_id': query_id
        }
        
        logging.info(f"Query processed: {user_message[:50]}... -> Response: {final_response[:50]}...")
        
        return jsonify(response_data)
        
    except Exception as e:
        logging.error(f"Error processing chat request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    languages = {
        'en': 'English',
        'fr': 'French',
        'de': 'German',
        'es': 'Spanish',
        'hi': 'Hindi'
    }
    return jsonify(languages)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get chatbot usage statistics"""
    try:
        stats = query_logger.get_statistics()
        return jsonify(stats)
    except Exception as e:
        logging.error(f"Error getting statistics: {str(e)}")
        return jsonify({'error': 'Failed to retrieve statistics'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'translation': translation_service.is_ready(),
            'faq': healthcare_faq.is_ready(),
            'logging': query_logger.is_ready()
        }
    })

if __name__ == '__main__':
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Initialize services
    logging.info("Initializing chatbot services...")
    translation_service.initialize()
    healthcare_faq.initialize()
    query_logger.initialize()
    
    logging.info("Multilingual Healthcare Chatbot started successfully!")
    app.run(debug=True, host='0.0.0.0', port=5000)
