# 🏥 Multilingual Healthcare Chatbot

A sophisticated multilingual healthcare chatbot built with Python, featuring real-time translation, comprehensive healthcare FAQ responses, and advanced analytics. The chatbot supports 5 languages and provides accurate healthcare information with confidence scoring.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![Transformers](https://img.shields.io/badge/Transformers-4.35+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### Core Functionality
- **🌍 Multilingual Support**: English, French, German, Spanish, and Hindi
- **🤖 AI-Powered Translation**: MarianMT models from Hugging Face Transformers
- **🏥 Healthcare FAQ**: Comprehensive medical knowledge base with 25+ categories
- **📊 Analytics & Logging**: Query tracking with accuracy metrics (500+ sample queries included)
- **🎯 Confidence Scoring**: Response accuracy tracking and display
- **🌐 Modern Web Interface**: Responsive design with mobile support

### Technical Features
- **REST API**: Complete API endpoints for integration
- **Real-time Chat**: Interactive web interface with typing indicators
- **Query Logging**: SQLite database with comprehensive analytics
- **Health Monitoring**: Service health checks and status monitoring
- **Responsive Design**: Mobile-first UI with accessibility features

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 4GB+ RAM (for translation models)
- Internet connection (for initial model download)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/VIGNESH-MT/Multilingual-Healthcare-Chatbot.git
   cd Multilingual-Healthcare-Chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up sample data** (Creates 500+ queries for testing)
   ```bash
   python setup_sample_data.py
   ```

4. **Run the chatbot**
   ```bash
   python run_chatbot.py
   ```

5. **Access the application**
   - Web Interface: http://localhost:5000
   - API Documentation: http://localhost:5000/api/health

## 📖 Usage

### Web Interface
1. Open your browser to `http://localhost:5000`
2. Select your preferred language from the dropdown
3. Type your healthcare question in the input field
4. View the response with confidence scoring
5. Use quick question buttons for common queries

### API Usage

#### Send a Chat Message
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the symptoms of flu?",
    "language": "en"
  }'
```

#### Get Statistics
```bash
curl http://localhost:5000/api/stats
```

#### Health Check
```bash
curl http://localhost:5000/api/health
```

## 🏗️ Architecture

### Project Structure
```
Multilingual-Healthcare-Chatbot/
├── app.py                 # Flask application and API endpoints
├── translation_service.py # MarianMT translation service
├── healthcare_faq.py      # Healthcare FAQ system
├── query_logger.py        # Query logging and analytics
├── config.py             # Application configuration
├── run_chatbot.py        # Main application runner
├── setup_sample_data.py  # Sample data generator
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Web interface template
├── static/
│   ├── css/
│   │   └── style.css     # Responsive CSS styles
│   └── js/
│       └── app.js        # Frontend JavaScript
└── logs/                 # Application logs
```

### Core Components

#### 1. Translation Service (`translation_service.py`)
- **MarianMT Models**: Helsinki-NLP translation models
- **Bidirectional Translation**: To/from English for all supported languages
- **Caching**: Efficient model loading and memory management
- **Error Handling**: Graceful fallbacks for translation failures

#### 2. Healthcare FAQ (`healthcare_faq.py`)
- **TF-IDF Vectorization**: Semantic question matching
- **25+ Categories**: Comprehensive healthcare topics
- **Confidence Scoring**: Cosine similarity-based accuracy
- **Fallback Responses**: Default responses for unmatched queries

#### 3. Query Logger (`query_logger.py`)
- **SQLite Database**: Persistent query storage
- **Analytics**: Comprehensive usage statistics
- **Sample Data**: 500+ pre-generated queries for testing
- **Export Functionality**: JSON export for data analysis

#### 4. Web Interface
- **Responsive Design**: Mobile-first approach
- **Real-time Chat**: WebSocket-like experience with AJAX
- **Accessibility**: WCAG compliant design
- **Progressive Enhancement**: Works without JavaScript

## 🌍 Supported Languages

| Language | Code | Translation Model |
|----------|------|-------------------|
| English  | `en` | Native (base language) |
| French   | `fr` | Helsinki-NLP/opus-mt-fr-en ↔ Helsinki-NLP/opus-mt-en-fr |
| German   | `de` | Helsinki-NLP/opus-mt-de-en ↔ Helsinki-NLP/opus-mt-en-de |
| Spanish  | `es` | Helsinki-NLP/opus-mt-es-en ↔ Helsinki-NLP/opus-mt-en-es |
| Hindi    | `hi` | Helsinki-NLP/opus-mt-hi-en ↔ Helsinki-NLP/opus-mt-en-hi |

## 📊 Healthcare FAQ Categories

The chatbot covers 25+ healthcare categories including:

- **General Health**: Symptoms, prevention, wellness
- **COVID-19**: Symptoms, quarantine, safety measures
- **Medications**: Dosages, interactions, safety
- **Emergency Care**: When to seek help, warning signs
- **Chronic Conditions**: Diabetes, hypertension management
- **Mental Health**: Stress, depression, anxiety
- **Nutrition**: Diet, hydration, supplements
- **Exercise & Fitness**: Activity recommendations, safety
- **Sleep Health**: Sleep hygiene, insomnia
- **Vaccinations**: Schedules, safety, effectiveness
- **Women's Health**: Reproductive health, screenings
- **Men's Health**: Prostate health, screenings
- **Skin Health**: Sun protection, dermatology
- **Allergies**: Symptoms, management, prevention

## 📈 Analytics & Logging

### Query Tracking
- **Unique Query IDs**: Each interaction tracked
- **Timestamp Logging**: Precise timing information
- **Language Detection**: Usage patterns by language
- **Accuracy Metrics**: Confidence scoring for responses
- **Session Management**: User session tracking

### Statistics Available
- Total queries processed
- Average response accuracy
- Language usage distribution
- Daily query patterns
- Accuracy distribution ranges
- Recent query history

### Sample Data
The system includes 500+ pre-generated sample queries for:
- **Testing**: Validate system functionality
- **Demonstration**: Show capabilities to users
- **Analytics**: Provide baseline statistics
- **Development**: Test new features

## 🔧 Configuration

### Environment Variables
Create a `.env` file for custom configuration:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=False

# Database
DATABASE_PATH=chatbot_logs.db

# Translation Settings
TRANSLATION_CACHE_SIZE=1000
MAX_TRANSLATION_LENGTH=512

# Logging
LOG_LEVEL=INFO
LOG_FILE=chatbot.log

# API Settings
MAX_MESSAGE_LENGTH=500
RATE_LIMIT_PER_MINUTE=60

# FAQ Settings
FAQ_CONFIDENCE_THRESHOLD=0.1
MAX_FAQ_RESULTS=5

# Model Settings
DEVICE=auto
MODEL_CACHE_DIR=./models
```

### Hardware Requirements

#### Minimum Requirements
- **CPU**: 2+ cores
- **RAM**: 4GB
- **Storage**: 2GB free space
- **Network**: Internet for model download

#### Recommended Requirements
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **GPU**: CUDA-compatible (optional, for faster inference)
- **Storage**: 5GB+ free space

## 🚀 Deployment

### Local Development
```bash
python run_chatbot.py
```

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "run_chatbot.py"]
```

#### Environment Setup
```bash
# Build and run
docker build -t healthcare-chatbot .
docker run -p 5000:5000 healthcare-chatbot
```

## 🧪 Testing

### Run Sample Data Setup
```bash
python setup_sample_data.py
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/api/health

# Test chat in different languages
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuáles son los síntomas de la gripe?", "language": "es"}'

# Get statistics
curl http://localhost:5000/api/stats
```

### Manual Testing
1. Open web interface at `http://localhost:5000`
2. Test each supported language
3. Try various healthcare questions
4. Check accuracy scores and statistics
5. Test mobile responsiveness

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include error handling
- Write tests for new features
- Update documentation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**Important Medical Disclaimer:**

This chatbot is designed for informational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

**In case of medical emergencies:**
- **Call emergency services immediately (911 in the US)**
- **Do not rely on this chatbot for emergency medical guidance**
- **Contact your healthcare provider for urgent medical concerns**

## 🙏 Acknowledgments

- **Hugging Face**: For the Transformers library and MarianMT models
- **Helsinki-NLP**: For the high-quality translation models
- **Flask Community**: For the excellent web framework
- **scikit-learn**: For machine learning utilities
- **Font Awesome**: For beautiful icons
- **Healthcare Community**: For medical knowledge validation

## 📞 Support

For support, questions, or suggestions:

- **GitHub Issues**: [Create an issue](https://github.com/VIGNESH-MT/Multilingual-Healthcare-Chatbot/issues)
- **Email**: [Contact the maintainer](mailto:vignesh@example.com)
- **Documentation**: Check this README and code comments

## 🔮 Future Enhancements

- **Voice Input/Output**: Speech recognition and synthesis
- **More Languages**: Expand to 10+ languages
- **Medical Image Analysis**: Basic image interpretation
- **Appointment Scheduling**: Integration with healthcare systems
- **Symptom Checker**: Advanced diagnostic assistance
- **Medication Reminders**: Personal health management
- **Telemedicine Integration**: Connect with healthcare providers

---

**Made with ❤️ for better healthcare accessibility worldwide**
