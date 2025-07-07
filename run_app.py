#!/usr/bin/env python3
"""
Simple script to run the Student Performance Prediction Application
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from main import main
    main()
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please ensure all required modules are installed.")
    print("Run: pip install -r requirements.txt")
except Exception as e:
    print(f"Error starting application: {e}")
    input("Press Enter to exit...")
