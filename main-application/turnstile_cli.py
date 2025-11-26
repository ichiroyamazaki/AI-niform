#!/usr/bin/env python3
"""
Turnstile Control Command Line Interface
Simple command-line interface for controlling the Arduino turnstile system.
"""

import serial
import time
import sys
import glob

class TurnstileCLI:
    def __init__(self):
        self.serial_connection = None
        self.is_connected = False
        
    def find_arduino_port(self):
        """Find the Arduino serial port"""
        # Common serial ports for different operating systems
        possible_ports = [
            '/dev/cu.usbserial*',  # macOS (FTDI/CH340 chips)
            '/dev/tty.usbmodem*',  # macOS (Arduino Uno R3)
            '/dev/ttyUSB*',        # Linux
            'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10'  # Windows
        ]
        
        for port_pattern in possible_ports:
            if '*' in port_pattern:
                ports = glob.glob(port_pattern)
                for port in ports:
                    if self.try_connect(port):
                        return port
            else:
                if self.try_connect(port_pattern):
                    return port
        
        # Try specific known ports as fallback
        specific_ports = ['/dev/cu.usbserial-11210', '/dev/cu.usbserial-0000', '/dev/cu.usbserial-0001']
        for port in specific_ports:
            if self.try_connect(port):
                return port
                
        return None
        
    def try_connect(self, port):
        """Try to connect to a specific serial port"""
        try:
            self.serial_connection = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            
            # Test connection
            self.serial_connection.write(b"status\n")
            time.sleep(0.5)
            
            if self.serial_connection.in_waiting > 0:
                response = self.serial_connection.readline().decode().strip()
                print(f"Connected to Arduino on {port}")
                print(f"Arduino response: {response}")
                self.is_connected = True
                return True
                
        except Exception as e:
            if self.serial_connection:
                self.serial_connection.close()
                self.serial_connection = None
            print(f"Failed to connect to {port}: {str(e)}")
            
        return False
        
    def send_command(self, command):
        """Send a command to Arduino"""
        if not self.is_connected or not self.serial_connection:
            print("Error: Not connected to Arduino")
            return False
            
        try:
            self.serial_connection.write(f"{command}\n".encode())
            print(f"Sent: {command}")
            
            # Wait for response
            time.sleep(0.5)
            if self.serial_connection.in_waiting > 0:
                response = self.serial_connection.readline().decode().strip()
                print(f"Arduino: {response}")
                return True
            return False
            
        except Exception as e:
            print(f"Error sending command: {str(e)}")
            return False
            
    def open_turnstile(self):
        """Open turnstile for 5 seconds"""
        if self.send_command("OPEN"):
            print("Turnstile opened! Will auto-close in 5 seconds...")
            time.sleep(5)
            self.close_turnstile()
            
    def close_turnstile(self):
        """Close turnstile"""
        self.send_command("CLOSE")
        print("Turnstile closed!")
        
    def interactive_mode(self):
        """Run in interactive mode"""
        print("\n=== Turnstile Control CLI ===")
        print("Commands:")
        print("  open  - Open turnstile for 5 seconds")
        print("  close - Close turnstile")
        print("  quit  - Exit program")
        print("=============================\n")
        
        while True:
            try:
                command = input("Enter command: ").strip().lower()
                
                if command == "quit" or command == "exit":
                    break
                elif command == "open":
                    self.open_turnstile()
                elif command == "close":
                    self.close_turnstile()
                elif command == "help":
                    print("Commands: open, close, quit")
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break
                
    def run(self):
        """Main run method"""
        print("Looking for Arduino...")
        port = self.find_arduino_port()
        
        if not port:
            print("Error: Could not find Arduino. Please check connection and try again.")
            return
            
        print(f"Connected to Arduino on {port}")
        
        # If command line arguments provided, execute them
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()
            if command == "open":
                self.open_turnstile()
            elif command == "close":
                self.close_turnstile()
            else:
                print(f"Unknown command: {command}")
                print("Usage: python turnstile_cli.py [open|close]")
        else:
            # Run in interactive mode
            self.interactive_mode()
            
        # Cleanup
        if self.serial_connection:
            self.serial_connection.close()

def main():
    """Main function"""
    try:
        cli = TurnstileCLI()
        cli.run()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
