from transformers import MarianMTModel, MarianTokenizer
import torch
import logging
from typing import Dict, Optional

class TranslationService:
    """Handles multilingual translation using MarianMT models"""
    
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.ready = False
        
        # Language mappings for MarianMT model names
        self.language_pairs = {
            'fr': 'Helsinki-NLP/opus-mt-fr-en',  # French to English
            'de': 'Helsinki-NLP/opus-mt-de-en',  # German to English
            'es': 'Helsinki-NLP/opus-mt-es-en',  # Spanish to English
            'hi': 'Helsinki-NLP/opus-mt-hi-en',  # Hindi to English
        }
        
        self.reverse_pairs = {
            'fr': 'Helsinki-NLP/opus-mt-en-fr',  # English to French
            'de': 'Helsinki-NLP/opus-mt-en-de',  # English to German
            'es': 'Helsinki-NLP/opus-mt-en-es',  # English to Spanish
            'hi': 'Helsinki-NLP/opus-mt-en-hi',  # English to Hindi
        }
    
    def initialize(self):
        """Initialize translation models"""
        try:
            logging.info("Loading translation models...")
            
            # Load models for translating TO English
            for lang, model_name in self.language_pairs.items():
                logging.info(f"Loading {lang} -> en model: {model_name}")
                self.tokenizers[f"{lang}_to_en"] = MarianTokenizer.from_pretrained(model_name)
                self.models[f"{lang}_to_en"] = MarianMTModel.from_pretrained(model_name).to(self.device)
            
            # Load models for translating FROM English
            for lang, model_name in self.reverse_pairs.items():
                logging.info(f"Loading en -> {lang} model: {model_name}")
                self.tokenizers[f"en_to_{lang}"] = MarianTokenizer.from_pretrained(model_name)
                self.models[f"en_to_{lang}"] = MarianMTModel.from_pretrained(model_name).to(self.device)
            
            self.ready = True
            logging.info("All translation models loaded successfully!")
            
        except Exception as e:
            logging.error(f"Error loading translation models: {str(e)}")
            self.ready = False
    
    def translate_to_english(self, text: str, source_language: str) -> str:
        """Translate text from source language to English"""
        if source_language == 'en':
            return text
        
        if not self.ready:
            logging.warning("Translation service not ready, returning original text")
            return text
        
        try:
            model_key = f"{source_language}_to_en"
            if model_key not in self.models:
                logging.warning(f"No model found for {source_language} -> en")
                return text
            
            tokenizer = self.tokenizers[model_key]
            model = self.models[model_key]
            
            # Tokenize and translate
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model.generate(**inputs, max_length=512, num_beams=4, early_stopping=True)
            
            translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            logging.info(f"Translated '{text[:50]}...' from {source_language} to en")
            
            return translated_text
            
        except Exception as e:
            logging.error(f"Error translating to English: {str(e)}")
            return text
    
    def translate_from_english(self, text: str, target_language: str) -> str:
        """Translate text from English to target language"""
        if target_language == 'en':
            return text
        
        if not self.ready:
            logging.warning("Translation service not ready, returning original text")
            return text
        
        try:
            model_key = f"en_to_{target_language}"
            if model_key not in self.models:
                logging.warning(f"No model found for en -> {target_language}")
                return text
            
            tokenizer = self.tokenizers[model_key]
            model = self.models[model_key]
            
            # Tokenize and translate
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model.generate(**inputs, max_length=512, num_beams=4, early_stopping=True)
            
            translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            logging.info(f"Translated '{text[:50]}...' from en to {target_language}")
            
            return translated_text
            
        except Exception as e:
            logging.error(f"Error translating from English: {str(e)}")
            return text
    
    def is_ready(self) -> bool:
        """Check if translation service is ready"""
        return self.ready
    
    def get_supported_languages(self) -> list:
        """Get list of supported language codes"""
        return ['en', 'fr', 'de', 'es', 'hi']
