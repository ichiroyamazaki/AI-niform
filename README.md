# AI-niform: Automated Uniform Compliance Detection System

> 🎓 Academic Project | 📚 Educational Use Only  
> Developed as part of the Bachelor of Science in Computer Engineering program at STI College Balagtas

---

## 🔧 Key Features

* **Computer Vision with YOLOv8 & OpenCV** – Real-time detection of proper school uniforms
* **Raspberry Pi 4 Integration** – Processing unit for camera and RFID modules
* **RFID Attendance Tracking** – Automated entry/exit logging with ID cards
* **Firebase Cloud Services** – Secure storage of attendance records and violation logs
* **Automated Notifications** – Alerts sent to parents/guardians for violations or entry/exit events
* **Web Application Dashboard** – Easy access to compliance records and violation history

---

## 🎯 Purpose

This repository demonstrates how AI-powered systems can be applied to real-world school management challenges, reducing staff workload and improving discipline enforcement.

---

## 📁 Project Structure

```
AI-niform/
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

---

## 🚀 Quick Start

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

---

## ✨ Features

- **Access Control**: RFID-based turnstile access control system
- **Uniform Detection**: YOLO-based uniform compliance monitoring
- **Web Interface**: Browser-based admin and guidance dashboards
- **Notifications**: Email and SMS notification system
- **Hardware Integration**: Arduino-based turnstile and solenoid control

---

## ⚠️ Disclaimer

This project is **protected under CoolFire TechLabs Inc.**  
It is **not authorized for business or commercial use**.  
Any reproduction, modification, or deployment outside educational or research contexts must respect this restriction.

---

## 📚 Additional Documentation

For more detailed information, please refer to the documentation folder:
- `documentation/README_INTEGRATION.md` - Integration guide
- `documentation/README_TURNSTILE.md` - Turnstile setup guide
- `documentation/README_WEB.md` - Web interface documentation
- `documentation/TURNSTILE_PYTHON_README.md` - Python turnstile control guide

---

## 🔗 Resources

- Project Website: [coolfirenetwork.weebly.com/ai-niform.html](https://coolfirenetwork.weebly.com/ai-niform.html)

---

**AI-niform** - Smart Access Control for Modern Institutions
