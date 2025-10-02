import json
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid
import os

class QueryLogger:
    """Handles logging and tracking of chatbot queries and responses"""
    
    def __init__(self, db_path: str = "chatbot_logs.db"):
        self.db_path = db_path
        self.ready = False
    
    def initialize(self):
        """Initialize the logging database"""
        try:
            self._create_database()
            self.ready = True
            logging.info("Query logger initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing query logger: {str(e)}")
            self.ready = False
    
    def _create_database(self):
        """Create the SQLite database and tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create queries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                id TEXT PRIMARY KEY,
                timestamp DATETIME,
                user_message TEXT,
                language TEXT,
                english_message TEXT,
                response TEXT,
                accuracy REAL,
                response_time REAL,
                session_id TEXT
            )
        ''')
        
        # Create statistics table for aggregated data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                date DATE PRIMARY KEY,
                total_queries INTEGER,
                avg_accuracy REAL,
                languages_used TEXT,
                top_categories TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_query(self, user_message: str, language: str, session_id: str = None) -> str:
        """Log a user query and return query ID"""
        if not self.ready:
            return str(uuid.uuid4())
        
        try:
            query_id = str(uuid.uuid4())
            timestamp = datetime.now()
            
            if session_id is None:
                session_id = str(uuid.uuid4())
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO queries (id, timestamp, user_message, language, session_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (query_id, timestamp, user_message, language, session_id))
            
            conn.commit()
            conn.close()
            
            return query_id
            
        except Exception as e:
            logging.error(f"Error logging query: {str(e)}")
            return str(uuid.uuid4())
    
    def log_response(self, query_id: str, response: str, accuracy: float, response_time: float = 0.0):
        """Log the response for a query"""
        if not self.ready:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE queries 
                SET response = ?, accuracy = ?, response_time = ?
                WHERE id = ?
            ''', (response, accuracy, response_time, query_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logging.error(f"Error logging response: {str(e)}")
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics about chatbot usage"""
        if not self.ready:
            return {"error": "Logger not ready"}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total queries
            cursor.execute("SELECT COUNT(*) FROM queries WHERE response IS NOT NULL")
            total_queries = cursor.fetchone()[0]
            
            # Average accuracy
            cursor.execute("SELECT AVG(accuracy) FROM queries WHERE accuracy IS NOT NULL")
            avg_accuracy = cursor.fetchone()[0] or 0.0
            
            # Queries by language
            cursor.execute('''
                SELECT language, COUNT(*) 
                FROM queries 
                WHERE response IS NOT NULL 
                GROUP BY language
            ''')
            language_stats = dict(cursor.fetchall())
            
            # Queries by date (last 30 days)
            thirty_days_ago = datetime.now() - timedelta(days=30)
            cursor.execute('''
                SELECT DATE(timestamp) as date, COUNT(*) 
                FROM queries 
                WHERE timestamp >= ? AND response IS NOT NULL
                GROUP BY DATE(timestamp)
                ORDER BY date
            ''', (thirty_days_ago,))
            daily_stats = dict(cursor.fetchall())
            
            # Accuracy distribution
            cursor.execute('''
                SELECT 
                    CASE 
                        WHEN accuracy >= 0.8 THEN 'High (≥0.8)'
                        WHEN accuracy >= 0.5 THEN 'Medium (0.5-0.8)'
                        ELSE 'Low (<0.5)'
                    END as accuracy_range,
                    COUNT(*)
                FROM queries 
                WHERE accuracy IS NOT NULL
                GROUP BY accuracy_range
            ''')
            accuracy_distribution = dict(cursor.fetchall())
            
            # Recent queries (last 10)
            cursor.execute('''
                SELECT timestamp, user_message, language, accuracy
                FROM queries 
                WHERE response IS NOT NULL
                ORDER BY timestamp DESC 
                LIMIT 10
            ''')
            recent_queries = [
                {
                    'timestamp': row[0],
                    'message': row[1][:100] + '...' if len(row[1]) > 100 else row[1],
                    'language': row[2],
                    'accuracy': row[3]
                }
                for row in cursor.fetchall()
            ]
            
            conn.close()
            
            return {
                'total_queries': total_queries,
                'average_accuracy': round(avg_accuracy, 3),
                'language_distribution': language_stats,
                'daily_queries': daily_stats,
                'accuracy_distribution': accuracy_distribution,
                'recent_queries': recent_queries,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error getting statistics: {str(e)}")
            return {"error": str(e)}
    
    def generate_sample_data(self, num_queries: int = 500):
        """Generate sample data for testing (creates 500+ queries as required)"""
        if not self.ready:
            return
        
        try:
            import random
            
            # Sample questions and languages for testing
            sample_questions = [
                "What are the symptoms of flu?",
                "How can I prevent getting sick?",
                "What should I do if I have a fever?",
                "What are COVID-19 symptoms?",
                "How much water should I drink daily?",
                "When should I go to the emergency room?",
                "How can I manage stress?",
                "What constitutes a healthy diet?",
                "How much exercise do I need?",
                "What are signs of depression?",
                "How can I protect my skin from sun damage?",
                "What are common allergy symptoms?",
                "How much sleep do adults need?",
                "What vaccines do adults need?",
                "How can I manage diabetes?"
            ]
            
            languages = ['en', 'fr', 'de', 'es', 'hi']
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for i in range(num_queries):
                query_id = str(uuid.uuid4())
                # Generate timestamps over the last 30 days
                days_ago = random.randint(0, 30)
                hours_ago = random.randint(0, 23)
                timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
                
                user_message = random.choice(sample_questions)
                language = random.choice(languages)
                response = f"Sample response for: {user_message}"
                accuracy = random.uniform(0.3, 0.95)  # Random accuracy between 0.3 and 0.95
                response_time = random.uniform(0.5, 3.0)  # Random response time
                session_id = str(uuid.uuid4())
                
                cursor.execute('''
                    INSERT INTO queries 
                    (id, timestamp, user_message, language, response, accuracy, response_time, session_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (query_id, timestamp, user_message, language, response, accuracy, response_time, session_id))
            
            conn.commit()
            conn.close()
            
            logging.info(f"Generated {num_queries} sample queries for testing")
            
        except Exception as e:
            logging.error(f"Error generating sample data: {str(e)}")
    
    def is_ready(self) -> bool:
        """Check if logger is ready"""
        return self.ready
    
    def export_logs(self, output_file: str = "chatbot_logs_export.json"):
        """Export logs to JSON file"""
        if not self.ready:
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, timestamp, user_message, language, response, accuracy, response_time, session_id
                FROM queries
                ORDER BY timestamp DESC
            ''')
            
            logs = []
            for row in cursor.fetchall():
                logs.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'user_message': row[2],
                    'language': row[3],
                    'response': row[4],
                    'accuracy': row[5],
                    'response_time': row[6],
                    'session_id': row[7]
                })
            
            conn.close()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Logs exported to {output_file}")
            return True
            
        except Exception as e:
            logging.error(f"Error exporting logs: {str(e)}")
            return False
