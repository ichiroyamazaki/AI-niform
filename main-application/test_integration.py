#!/usr/bin/env python3
"""
Test script to demonstrate the integration between ai_niform_login.py and testmainscreen.py

This script simulates the flow:
1. Guard login (ai_niform_login.py)
2. After successful login, launches main screen (testmainscreen.py)
3. Press ESC in main screen to return to login
"""

import subprocess
import sys
import os
import time

def test_integration():
    print("=== AI-niform Integration Test ===")
    print("1. Starting login application...")
    print("2. Simulate guard login (you'll need to scan a guard card)")
    print("3. After successful login, main screen will launch automatically")
    print("4. Press ESC in main screen to return to login")
    print("5. Press Ctrl+C to exit this test")
    print("\nStarting login application...")
    
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        login_path = os.path.join(current_dir, "ai_niform_login.py")
        
        # Launch the login application
        process = subprocess.Popen([sys.executable, login_path])
        
        print(f"Login application started with PID: {process.pid}")
        print("Follow the on-screen instructions to test the integration.")
        
        # Wait for the process to complete
        process.wait()
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
        if 'process' in locals():
            process.terminate()
            print("Login application terminated.")
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_integration()
