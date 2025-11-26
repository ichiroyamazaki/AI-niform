# AI-niform Consolidated Project

This is a consolidated version of all AI-niform repositories, organized into a clean structure with duplicates removed.

## Project Structure

```
AI-niform-Consolidated/
├── main-application/     # Core application files
│   ├── ai_niform_login.py      # Main login interface
│   ├── database_manager.py     # Database operations
│   ├── testmainscreen.py        # Main screen interface
│   ├── turnstile_control.py     # Turnstile control
│   └── ...
│
├── web-interface/       # Web-based interface
│   ├── web_server.py           # Web server
│   ├── guidance_dashboard.py   # Guidance dashboard
│   ├── templates/              # HTML templates
│   └── ...
│
├── notifications/       # Email and SMS notifications
│   ├── main_sms.py            # SMS functionality
│   ├── main_email.py           # Email functionality
│   ├── rfid_sms.py             # RFID SMS integration
│   └── ...
│
├── hardware/           # Arduino and hardware control
│   ├── turnstile_signal.ino    # Turnstile Arduino code
│   ├── solenoid_arduino.ino    # Solenoid Arduino code
│   ├── solenoid_controller.py  # Solenoid Python controller
│   └── ...
│
├── assets/             # Images and UI assets
│   ├── image-elements/         # UI elements
│   ├── image-students/         # Student images
│   ├── image-teachers/         # Teacher images
│   └── ...
│
└── documentation/      # Documentation files
    ├── README.md               # Main documentation
    ├── README_INTEGRATION.md   # Integration guide
    └── ...
```

## Quick Start

### Main Application
```bash
cd main-application
pip install -r requirements.txt
python ai_niform_login.py
```

### Web Interface
```bash
cd web-interface
pip install -r requirements.txt
python start_web_app.py
```

### Hardware Control
```bash
cd hardware
python solenoid_controller.py
```

## Features

- **Access Control**: RFID-based turnstile access control system
- **Uniform Detection**: YOLO-based uniform compliance monitoring
- **Web Interface**: Browser-based admin and guidance dashboards
- **Notifications**: Email and SMS notification system
- **Hardware Integration**: Arduino-based turnstile and solenoid control

## Source Repositories

This consolidated version was created from:
- AI-niformV2
- AIniformUnstable
- AIniformFinals
- AIniformSemiFinals
- ainiformguardweb
- emailtestnotification
- smstestnotification
- turnstiletest
- ainiformpublic

## Notes

- Duplicate files have been removed, keeping the most recent/complete versions
- Historical versions are preserved in the original repository folders
- All functionality has been consolidated into this single structure

