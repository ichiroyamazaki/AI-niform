# Turnstile Control Python Interface

This directory contains Python scripts to control the Arduino turnstile system via serial communication.

## Files

- `turnstile_control.py` - GUI application with buttons to control the turnstile
- `turnstile_cli.py` - Command-line interface for terminal control
- `turnstile_requirements.txt` - Python dependencies
- `arduino/turnstile_car.ino` - Arduino sketch (already provided)

## Setup

### 1. Install Python Dependencies

```bash
pip install -r turnstile_requirements.txt
```

### 2. Upload Arduino Code

Upload the `turnstile_car.ino` sketch to your Arduino Uno.

### 3. Connect Hardware

- Servo Motor: Pin 9
- Connect Arduino to computer via USB

## Usage

### GUI Application (Recommended)

Run the graphical interface:

```bash
python turnstile_control.py
```

**Features:**
- Visual status display
- "OK - Open Turnstile" button (opens for 5 seconds)
- "Close Turnstile" button (manual close)
- Real-time log display
- Auto-detection of Arduino port

**How to use:**
1. Connect Arduino via USB
2. Run the Python script
3. Click "OK - Open Turnstile" to open for 5 seconds
4. Use "Close Turnstile" for manual control

### Command Line Interface

For terminal-based control:

```bash
# Interactive mode
python turnstile_cli.py

# Direct commands
python turnstile_cli.py open   # Open for 5 seconds
python turnstile_cli.py close  # Close immediately
```

**Commands:**
- `open` - Opens turnstile for 5 seconds then auto-closes
- `close` - Closes turnstile immediately
- `quit` - Exit the program

## Arduino Communication

The Python scripts communicate with the Arduino using these commands:

- `OPEN` - Opens the turnstile
- `CLOSE` - Closes the turnstile
- `status` - Requests status (optional)

The Arduino responds with:
- `OK OPEN` - Turnstile opened successfully
- `OK CLOSE` - Turnstile closed successfully
- `ERR UNKNOWN` - Unknown command received

## Troubleshooting

### Connection Issues

1. **"Could not find Arduino"**
   - Check USB connection
   - Verify Arduino is powered on
   - Try different USB port
   - Check if Arduino IDE can see the port

2. **"Failed to connect"**
   - Make sure no other program is using the serial port
   - Close Arduino IDE serial monitor
   - Try unplugging and reconnecting Arduino

3. **Permission denied (Linux/macOS)**
   ```bash
   sudo chmod 666 /dev/ttyUSB0  # Replace with your port
   ```

### Port Detection

The scripts automatically detect common Arduino ports:
- **macOS**: `/dev/tty.usbmodem*`
- **Linux**: `/dev/ttyUSB*`
- **Windows**: `COM3`, `COM4`, `COM5`, etc.

### Manual Port Specification

If auto-detection fails, you can modify the scripts to use a specific port:

```python
# In turnstile_control.py or turnstile_cli.py
possible_ports = ['/dev/tty.usbmodem14101']  # Your specific port
```

## Features

### GUI Application
- ✅ Visual status indicators
- ✅ Real-time logging
- ✅ Auto-close timer (5 seconds)
- ✅ Manual close option
- ✅ Port auto-detection
- ✅ Error handling

### Command Line Interface
- ✅ Simple terminal interface
- ✅ Direct command execution
- ✅ Interactive mode
- ✅ Auto-close functionality
- ✅ Port auto-detection

## Hardware Requirements

- Arduino Uno (or compatible)
- Servo motor (connected to pin 9)
- USB cable for Arduino
- Computer with Python 3.6+

## Software Requirements

- Python 3.6 or higher
- pyserial library
- Arduino IDE (for uploading sketch)

## Example Workflow

1. **Setup:**
   ```bash
   pip install pyserial
   ```

2. **Upload Arduino code:**
   - Open `turnstile_car.ino` in Arduino IDE
   - Upload to Arduino Uno

3. **Run Python control:**
   ```bash
   python turnstile_control.py
   ```

4. **Use the interface:**
   - Click "OK - Open Turnstile" to open for 5 seconds
   - Watch the status and log updates
   - Use "Close Turnstile" for manual control

The turnstile will automatically close after 5 seconds when opened via the "OK" button, just like pressing a physical button!
