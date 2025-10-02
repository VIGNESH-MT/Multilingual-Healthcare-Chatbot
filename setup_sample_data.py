#!/usr/bin/env python3
"""
Setup script to generate sample data for the Healthcare Chatbot
This creates 500+ sample queries as required for testing and demonstration
"""

import sys
import os
import logging
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from query_logger import QueryLogger

def setup_logging():
    """Setup logging for the setup script"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('setup.log')
        ]
    )

def main():
    """Main setup function"""
    setup_logging()
    
    print("=" * 60)
    print("Healthcare Chatbot - Sample Data Setup")
    print("=" * 60)
    
    try:
        # Initialize query logger
        print("Initializing query logger...")
        query_logger = QueryLogger()
        query_logger.initialize()
        
        if not query_logger.is_ready():
            print("❌ Error: Query logger failed to initialize")
            return False
        
        print("✅ Query logger initialized successfully")
        
        # Generate sample data
        print("\nGenerating sample data...")
        print("This will create 500+ sample queries for testing and demonstration...")
        
        # Generate the required 500+ queries
        num_queries = 550  # Generate a bit more than required
        query_logger.generate_sample_data(num_queries)
        
        print(f"✅ Generated {num_queries} sample queries")
        
        # Get and display statistics
        print("\nRetrieving statistics...")
        stats = query_logger.get_statistics()
        
        if 'error' not in stats:
            print("\n📊 Sample Data Statistics:")
            print(f"   Total Queries: {stats['total_queries']}")
            print(f"   Average Accuracy: {stats['average_accuracy']:.1%}")
            print(f"   Languages Used: {', '.join(stats['language_distribution'].keys())}")
            
            print("\n📈 Language Distribution:")
            for lang, count in stats['language_distribution'].items():
                print(f"   {lang}: {count} queries")
            
            print("\n🎯 Accuracy Distribution:")
            for range_name, count in stats['accuracy_distribution'].items():
                print(f"   {range_name}: {count} queries")
        
        # Export sample data
        print("\nExporting sample data...")
        if query_logger.export_logs('sample_data_export.json'):
            print("✅ Sample data exported to 'sample_data_export.json'")
        else:
            print("⚠️  Warning: Failed to export sample data")
        
        print("\n" + "=" * 60)
        print("✅ Sample data setup completed successfully!")
        print("You can now run the chatbot with: python app.py")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        logging.error(f"Setup failed: {str(e)}")
        print(f"\n❌ Setup failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
