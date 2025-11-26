#!/usr/bin/env python3
"""
Turnstile Control Python Interface
Communicates with Arduino turnstile control system via serial port.
Features:
- Simple GUI with OK button to open turnstile
- Serial communication with Arduino
- Status display
- Auto-close after 5 seconds
"""

import serial
import time
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime

class TurnstileController:
    def __init__(self):
        self.serial_connection = None
        self.is_connected = False
        self.turnstile_open = False
        self.auto_close_timer = None
        
        # Create GUI
        self.root = tk.Tk()
        self.root.title("Turnstile Control System")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        self.setup_gui()
        self.connect_to_arduino()
        
    def setup_gui(self):
        """Setup the GUI components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Turnstile Control System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Connection status
        self.connection_label = ttk.Label(status_frame, text="Disconnected", 
                                         foreground="red", font=("Arial", 10, "bold"))
        self.connection_label.grid(row=0, column=0, sticky=tk.W)
        
        # Turnstile status
        self.turnstile_label = ttk.Label(status_frame, text="Turnstile: Unknown", 
                                        font=("Arial", 10))
        self.turnstile_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Control", padding="10")
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # OK Button (Open Turnstile)
        self.open_button = ttk.Button(control_frame, text="OK - Open Turnstile", 
                                     command=self.open_turnstile, state="disabled")
        self.open_button.grid(row=0, column=0, padx=(0, 10))
        
        # Close Button
        self.close_button = ttk.Button(control_frame, text="Close Turnstile", 
                                      command=self.close_turnstile, state="disabled")
        self.close_button.grid(row=0, column=1)
        
        # Info frame
        info_frame = ttk.LabelFrame(main_frame, text="Information", padding="10")
        info_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Info text
        info_text = """Instructions:
1. Make sure Arduino is connected via USB
2. Upload the turnstile_car.ino sketch
3. Click 'OK - Open Turnstile' to open for 5 seconds
4. Use 'Close Turnstile' to manually close
5. Turnstile will auto-close after 5 seconds"""
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.grid(row=0, column=0, sticky=tk.W)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Log text area
        self.log_text = tk.Text(log_frame, height=6, width=50, state="disabled")
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def log_message(self, message):
        """Add a message to the log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        
    def connect_to_arduino(self):
        """Attempt to connect to Arduino via serial port"""
        # Common serial ports for different operating systems
        possible_ports = [
            '/dev/cu.usbserial*',  # macOS (FTDI/CH340 chips)
            '/dev/tty.usbmodem*',  # macOS (Arduino Uno R3)
            '/dev/ttyUSB*',        # Linux
            'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10'  # Windows
        ]
        
        # Try to find Arduino port
        import glob
        for port_pattern in possible_ports:
            if '*' in port_pattern:
                ports = glob.glob(port_pattern)
                for port in ports:
                    if self.try_connect(port):
                        return
            else:
                if self.try_connect(port_pattern):
                    return
        
        # Try specific known ports as fallback
        specific_ports = ['/dev/cu.usbserial-11210', '/dev/cu.usbserial-0000', '/dev/cu.usbserial-0001']
        for port in specific_ports:
            if self.try_connect(port):
                return
        
        # If no port found, show error
        self.log_message("ERROR: Could not find Arduino. Please check connection.")
        self.connection_label.config(text="Disconnected", foreground="red")
        
    def try_connect(self, port):
        """Try to connect to a specific serial port"""
        try:
            self.serial_connection = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            
            # Test connection by sending a status request
            self.serial_connection.write(b"status\n")
            time.sleep(0.5)
            
            if self.serial_connection.in_waiting > 0:
                response = self.serial_connection.readline().decode().strip()
                self.log_message(f"Connected to Arduino on {port}")
                self.log_message(f"Arduino response: {response}")
                
                self.is_connected = True
                self.connection_label.config(text=f"Connected ({port})", foreground="green")
                self.open_button.config(state="normal")
                self.close_button.config(state="normal")
                
                # Start listening for Arduino messages
                self.start_serial_listener()
                return True
                
        except Exception as e:
            if self.serial_connection:
                self.serial_connection.close()
                self.serial_connection = None
            self.log_message(f"Failed to connect to {port}: {str(e)}")
            
        return False
        
    def start_serial_listener(self):
        """Start a thread to listen for Arduino messages"""
        def listen():
            while self.is_connected and self.serial_connection:
                try:
                    if self.serial_connection.in_waiting > 0:
                        message = self.serial_connection.readline().decode().strip()
                        if message:
                            self.log_message(f"Arduino: {message}")
                            
                            # Update turnstile status based on Arduino response
                            if "OK OPEN" in message:
                                self.turnstile_open = True
                                self.update_turnstile_status()
                            elif "OK CLOSE" in message:
                                self.turnstile_open = False
                                self.update_turnstile_status()
                                
                except Exception as e:
                    self.log_message(f"Serial read error: {str(e)}")
                    break
                    
                time.sleep(0.1)
                
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
        
    def update_turnstile_status(self):
        """Update the turnstile status display"""
        status = "OPEN" if self.turnstile_open else "CLOSED"
        color = "green" if self.turnstile_open else "red"
        self.turnstile_label.config(text=f"Turnstile: {status}", foreground=color)
        
    def open_turnstile(self):
        """Send open command to Arduino"""
        if not self.is_connected or not self.serial_connection:
            messagebox.showerror("Error", "Not connected to Arduino")
            return
            
        try:
            self.serial_connection.write(b"OPEN\n")
            self.log_message("Sent: OPEN command")
            
            # Cancel any existing auto-close timer
            if self.auto_close_timer:
                self.root.after_cancel(self.auto_close_timer)
                
            # Set auto-close timer for 5 seconds
            self.auto_close_timer = self.root.after(5000, self.auto_close_turnstile)
            self.log_message("Auto-close scheduled in 5 seconds")
            
        except Exception as e:
            self.log_message(f"Error sending OPEN command: {str(e)}")
            messagebox.showerror("Error", f"Failed to send command: {str(e)}")
            
    def close_turnstile(self):
        """Send close command to Arduino"""
        if not self.is_connected or not self.serial_connection:
            messagebox.showerror("Error", "Not connected to Arduino")
            return
            
        try:
            self.serial_connection.write(b"CLOSE\n")
            self.log_message("Sent: CLOSE command")
            
            # Cancel auto-close timer
            if self.auto_close_timer:
                self.root.after_cancel(self.auto_close_timer)
                self.auto_close_timer = None
                
        except Exception as e:
            self.log_message(f"Error sending CLOSE command: {str(e)}")
            messagebox.showerror("Error", f"Failed to send command: {str(e)}")
            
    def auto_close_turnstile(self):
        """Automatically close turnstile after 5 seconds"""
        self.log_message("Auto-closing turnstile...")
        self.close_turnstile()
        self.auto_close_timer = None
        
    def on_closing(self):
        """Handle application closing"""
        if self.serial_connection:
            self.serial_connection.close()
        self.root.destroy()
        
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main():
    """Main function"""
    print("Starting Turnstile Control System...")
    print("Make sure your Arduino is connected and the turnstile_car.ino sketch is uploaded.")
    
    try:
        app = TurnstileController()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
