import json
import re
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging

class HealthcareFAQ:
    """Healthcare FAQ system with intelligent response matching"""
    
    def __init__(self):
        self.faq_data = []
        self.vectorizer = None
        self.faq_vectors = None
        self.last_confidence = 0.0
        self.ready = False
        
    def initialize(self):
        """Initialize the FAQ system with healthcare data"""
        try:
            # Create comprehensive healthcare FAQ dataset
            self.faq_data = self._create_healthcare_faq_dataset()
            
            # Prepare questions for vectorization
            questions = [item['question'] for item in self.faq_data]
            
            # Create TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                max_features=5000,
                lowercase=True
            )
            
            # Fit and transform questions
            self.faq_vectors = self.vectorizer.fit_transform(questions)
            
            self.ready = True
            logging.info(f"Healthcare FAQ initialized with {len(self.faq_data)} entries")
            
        except Exception as e:
            logging.error(f"Error initializing healthcare FAQ: {str(e)}")
            self.ready = False
    
    def _create_healthcare_faq_dataset(self) -> List[Dict]:
        """Create a comprehensive healthcare FAQ dataset"""
        return [
            # General Health
            {
                "question": "What are the symptoms of flu?",
                "answer": "Common flu symptoms include fever, chills, muscle aches, cough, congestion, runny nose, headaches, and fatigue. Symptoms typically last 3-7 days.",
                "category": "general_health"
            },
            {
                "question": "How can I prevent getting sick?",
                "answer": "To prevent illness: wash hands frequently, get vaccinated, eat a balanced diet, exercise regularly, get adequate sleep, manage stress, and avoid close contact with sick people.",
                "category": "prevention"
            },
            {
                "question": "What should I do if I have a fever?",
                "answer": "For fever: rest, drink plenty of fluids, take fever-reducing medication like acetaminophen or ibuprofen, and seek medical attention if fever exceeds 103°F (39.4°C) or persists for more than 3 days.",
                "category": "symptoms"
            },
            
            # COVID-19
            {
                "question": "What are COVID-19 symptoms?",
                "answer": "COVID-19 symptoms include fever, cough, shortness of breath, fatigue, muscle aches, headache, loss of taste or smell, sore throat, congestion, nausea, and diarrhea.",
                "category": "covid19"
            },
            {
                "question": "How long should I quarantine if I have COVID-19?",
                "answer": "If you test positive for COVID-19, isolate for at least 5 days from symptom onset or positive test. You can end isolation after day 5 if fever-free for 24 hours and symptoms are improving.",
                "category": "covid19"
            },
            
            # Medications
            {
                "question": "How much acetaminophen can I take?",
                "answer": "Adults can take 325-650mg of acetaminophen every 4-6 hours, not exceeding 3000mg per day. Always follow package instructions and consult a healthcare provider for personalized advice.",
                "category": "medications"
            },
            {
                "question": "Can I take ibuprofen with acetaminophen?",
                "answer": "Yes, ibuprofen and acetaminophen can generally be taken together as they work differently. However, consult your healthcare provider or pharmacist for proper dosing and timing.",
                "category": "medications"
            },
            
            # Emergency Situations
            {
                "question": "When should I go to the emergency room?",
                "answer": "Seek emergency care for: chest pain, difficulty breathing, severe bleeding, signs of stroke, severe allergic reactions, high fever with stiff neck, or any life-threatening condition.",
                "category": "emergency"
            },
            {
                "question": "What are signs of a heart attack?",
                "answer": "Heart attack symptoms include chest pain or discomfort, shortness of breath, nausea, lightheadedness, cold sweats, and pain in arms, back, neck, jaw, or stomach. Call 911 immediately.",
                "category": "emergency"
            },
            
            # Chronic Conditions
            {
                "question": "How can I manage diabetes?",
                "answer": "Diabetes management includes monitoring blood sugar, taking medications as prescribed, eating a balanced diet, exercising regularly, maintaining a healthy weight, and regular medical checkups.",
                "category": "chronic_conditions"
            },
            {
                "question": "What foods should diabetics avoid?",
                "answer": "Diabetics should limit sugary drinks, refined carbohydrates, processed foods, high-sodium foods, and trans fats. Focus on whole grains, lean proteins, vegetables, and fruits in moderation.",
                "category": "chronic_conditions"
            },
            
            # Mental Health
            {
                "question": "How can I manage stress?",
                "answer": "Stress management techniques include regular exercise, meditation, deep breathing, adequate sleep, healthy eating, social support, time management, and professional counseling when needed.",
                "category": "mental_health"
            },
            {
                "question": "What are signs of depression?",
                "answer": "Depression symptoms include persistent sadness, loss of interest, fatigue, sleep changes, appetite changes, difficulty concentrating, feelings of worthlessness, and thoughts of self-harm.",
                "category": "mental_health"
            },
            
            # Nutrition and Diet
            {
                "question": "What constitutes a healthy diet?",
                "answer": "A healthy diet includes fruits, vegetables, whole grains, lean proteins, healthy fats, and adequate water. Limit processed foods, added sugars, and excessive sodium.",
                "category": "nutrition"
            },
            {
                "question": "How much water should I drink daily?",
                "answer": "Adults should aim for about 8 glasses (64 ounces) of water daily, though needs vary based on activity level, climate, and individual factors. Listen to your body's thirst cues.",
                "category": "nutrition"
            },
            
            # Exercise and Fitness
            {
                "question": "How much exercise do I need?",
                "answer": "Adults should get at least 150 minutes of moderate-intensity aerobic activity or 75 minutes of vigorous activity weekly, plus muscle-strengthening activities twice a week.",
                "category": "fitness"
            },
            {
                "question": "Is it safe to exercise when sick?",
                "answer": "Light exercise may be okay with mild cold symptoms above the neck. Avoid exercise with fever, body aches, or symptoms below the neck. Listen to your body and rest when needed.",
                "category": "fitness"
            },
            
            # Sleep
            {
                "question": "How much sleep do adults need?",
                "answer": "Most adults need 7-9 hours of sleep per night. Good sleep hygiene includes consistent bedtime, comfortable environment, avoiding screens before bed, and limiting caffeine.",
                "category": "sleep"
            },
            {
                "question": "What can I do for insomnia?",
                "answer": "For insomnia: maintain regular sleep schedule, create relaxing bedtime routine, avoid caffeine late in day, exercise regularly, manage stress, and consult a healthcare provider if persistent.",
                "category": "sleep"
            },
            
            # Vaccinations
            {
                "question": "What vaccines do adults need?",
                "answer": "Adults typically need annual flu vaccine, COVID-19 boosters, Tdap every 10 years, and others based on age, health conditions, and travel. Consult your healthcare provider.",
                "category": "vaccinations"
            },
            {
                "question": "Are vaccines safe?",
                "answer": "Yes, vaccines are rigorously tested for safety and effectiveness. Serious side effects are rare. The benefits of vaccination far outweigh the risks for most people.",
                "category": "vaccinations"
            },
            
            # Women's Health
            {
                "question": "How often should women get mammograms?",
                "answer": "Women should discuss mammogram screening with their healthcare provider. Generally recommended annually or biannually starting at age 40-50, depending on risk factors.",
                "category": "womens_health"
            },
            {
                "question": "What are normal menstrual cycle symptoms?",
                "answer": "Normal menstrual symptoms may include mild cramping, bloating, mood changes, and breast tenderness. Severe pain, heavy bleeding, or irregular cycles should be evaluated.",
                "category": "womens_health"
            },
            
            # Men's Health
            {
                "question": "When should men get prostate screening?",
                "answer": "Men should discuss prostate screening with their healthcare provider starting at age 50, or earlier (age 45) if at higher risk due to family history or ethnicity.",
                "category": "mens_health"
            },
            
            # Skin Health
            {
                "question": "How can I protect my skin from sun damage?",
                "answer": "Protect skin by using broad-spectrum SPF 30+ sunscreen, wearing protective clothing, seeking shade during peak hours (10am-4pm), and avoiding tanning beds.",
                "category": "skin_health"
            },
            {
                "question": "When should I see a dermatologist about a mole?",
                "answer": "See a dermatologist if a mole changes in size, shape, color, or texture, becomes asymmetrical, has irregular borders, or if you notice new moles after age 30.",
                "category": "skin_health"
            },
            
            # Allergies
            {
                "question": "What are common allergy symptoms?",
                "answer": "Common allergy symptoms include sneezing, runny nose, itchy eyes, skin rash, hives, and in severe cases, difficulty breathing or swallowing (anaphylaxis).",
                "category": "allergies"
            },
            {
                "question": "How can I manage seasonal allergies?",
                "answer": "Manage seasonal allergies by avoiding triggers, using air purifiers, keeping windows closed during high pollen days, taking antihistamines, and consulting an allergist if needed.",
                "category": "allergies"
            }
        ]
    
    def get_response(self, user_question: str) -> str:
        """Get the best matching response for a user question"""
        if not self.ready:
            return "I'm sorry, the healthcare FAQ system is not ready. Please try again later."
        
        try:
            # Preprocess the question
            processed_question = self._preprocess_question(user_question)
            
            # Vectorize the user question
            question_vector = self.vectorizer.transform([processed_question])
            
            # Calculate similarities
            similarities = cosine_similarity(question_vector, self.faq_vectors).flatten()
            
            # Get the best match
            best_match_idx = np.argmax(similarities)
            self.last_confidence = similarities[best_match_idx]
            
            # Return response if confidence is above threshold
            if self.last_confidence > 0.1:  # Adjust threshold as needed
                return self.faq_data[best_match_idx]['answer']
            else:
                return self._get_default_response()
                
        except Exception as e:
            logging.error(f"Error getting FAQ response: {str(e)}")
            return "I'm sorry, I encountered an error while processing your question. Please try rephrasing or contact a healthcare professional."
    
    def _preprocess_question(self, question: str) -> str:
        """Preprocess user question for better matching"""
        # Convert to lowercase
        question = question.lower()
        
        # Remove extra whitespace
        question = re.sub(r'\s+', ' ', question).strip()
        
        # Remove punctuation except for medical terms
        question = re.sub(r'[^\w\s\-]', '', question)
        
        return question
    
    def _get_default_response(self) -> str:
        """Return default response when no good match is found"""
        return ("I'm not sure about that specific question. For accurate medical advice, please consult with a healthcare professional. "
                "You can also try rephrasing your question or asking about common health topics like symptoms, medications, or prevention.")
    
    def get_last_confidence(self) -> float:
        """Get confidence score of the last response"""
        return self.last_confidence
    
    def is_ready(self) -> bool:
        """Check if FAQ system is ready"""
        return self.ready
    
    def get_categories(self) -> List[str]:
        """Get list of available FAQ categories"""
        categories = set(item['category'] for item in self.faq_data)
        return sorted(list(categories))
    
    def search_by_category(self, category: str) -> List[Dict]:
        """Get all FAQ items in a specific category"""
        return [item for item in self.faq_data if item['category'] == category]
