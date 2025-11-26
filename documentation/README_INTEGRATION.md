# AI-niform Integration Documentation

## Overview
This project combines two applications:
1. **ai_niform_login.py** - Tkinter-based login interface for guards
2. **testmainscreen.py** - PyQt5-based main screen for uniform compliance monitoring

## Integration Flow

### 1. Guard Login Process
- Start with `ai_niform_login.py`
- Guard scans their ID card
- If valid guard card is detected:
  - Status shows "ACCESS GRANTED - Launching Main Screen"
  - After 3 seconds, the PyQt5 main screen launches automatically
  - Tkinter login window is hidden and eventually closed

### 2. Main Screen Operation
- The PyQt5 main screen (`testmainscreen.py`) provides:
  - Welcome interface for STI College Balagtas
  - Card reader interface for students/visitors
  - Uniform compliance monitoring
  - Developer mode (F1 key)

### 3. Return to Login
- Press **ESC** key in the main screen to return to login
- This launches a new instance of the login application
- The current main screen closes

## Key Features

### Login Application (ai_niform_login.py)
- Tkinter-based GUI
- RFID card scanning for guard authentication
- Database integration for user management
- Fallback to tkinter interface if PyQt5 fails

### Main Screen Application (testmainscreen.py)
- PyQt5-based GUI (better macOS compatibility)
- Full-screen interface (1920x1080)
- Real-time card scanning
- Uniform compliance detection
- Developer mode for testing

## File Structure
```
ainiform v2.3/
├── ai_niform_login.py      # Main login application
├── testmainscreen.py       # PyQt5 main screen
├── database_manager.py     # Database operations
├── requirements.txt        # Python dependencies
├── test_integration.py     # Integration test script
├── README_INTEGRATION.md   # This documentation
└── image-elements/         # UI assets
```

## Installation and Setup

1. **Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python ai_niform_login.py
   ```

3. **Test Integration**:
   ```bash
   python test_integration.py
   ```

## Usage Instructions

### For Guards:
1. Launch the login application
2. Scan your guard ID card
3. Wait for "ACCESS GRANTED" message
4. Main screen will launch automatically

### For Students/Visitors:
1. Use the main screen interface
2. Scan your ID card at the card reader
3. Follow on-screen instructions for uniform compliance

### Navigation:
- **ESC**: Return to login screen (from main screen)
- **F1**: Developer mode (in main screen)
- **Ctrl+C**: Exit applications

## Technical Details

### Process Management
- Uses `subprocess.Popen()` to launch applications
- Graceful handling of application transitions
- Fallback mechanisms for error recovery

### GUI Framework Integration
- Tkinter for login (lightweight, cross-platform)
- PyQt5 for main screen (better macOS support)
- Seamless transition between frameworks

### Error Handling
- Automatic fallback to tkinter interface if PyQt5 fails
- Graceful error messages and recovery
- Process cleanup on exit

## Troubleshooting

### Common Issues:
1. **PyQt5 not launching**: Check if PyQt5 is installed correctly
2. **Permission errors**: Ensure proper file permissions
3. **Display issues**: Verify screen resolution settings

### Debug Mode:
- Check console output for error messages
- Use developer mode (F1) in main screen for testing
- Monitor process IDs for application management

## Future Enhancements
- Single unified application with both interfaces
- Improved error handling and recovery
- Enhanced user experience and UI/UX
- Additional security features
