# AI-niform Turnstile Access Control System

A Python-based turnstile access control system with RFID card reading capabilities, designed for managing guard and student access in educational institutions.

## Features

### 🔐 Access Control
- **Role-based Access**: Guards, Students, and Special Pass holders
- **RFID Integration**: HID keyboard-based RFID reader support
- **Local Database**: Text file-based storage system
- **Real-time Validation**: Instant access verification

### 🖥️ User Interfaces
- **Login Screen**: Clean AI-niform branding with login button
- **Turnstile Screen**: RFID card reading interface (Guards only)
- **Guard Splash Screen**: Visitor and Student registration options
- **Admin Interface**: Database management system

### 📊 Database Management
- **Local Storage**: No external database required
- **CRUD Operations**: Add, edit, delete, and view records
- **Access Logging**: Automatic logging of all access attempts
- **Role Management**: Support for GUARD, STUDENT, and SPECIAL roles

## Installation

### Prerequisites
- Python 3.7 or higher
- Windows/Linux/macOS

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-niform.git
cd ai-niform
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the main application:
```bash
python ai_niform_login.py
```

## Usage

### Main Application
```bash
python ai_niform_login.py
```

### Admin Interface
```bash
python admin_interface.py
```

### Database Management
```bash
python database_manager.py
```

## System Flow

1. **Login Screen** → Click "Log-in"
2. **Turnstile Screen** → Tap RFID card
   - **Guards**: Access granted → Guard Splash Screen
   - **Students/Special Pass**: Access denied
3. **Guard Splash Screen** → Visitor/Student registration options
4. **Admin Interface** → Database management

## Database Structure

### File: `database.txt`
```
# Format: ID,ROLE,NAME,STATUS
0095339862,GUARD,John Jason Domingo,ACTIVE
0095272825,STUDENT,Alice Johnson,ACTIVE
0095243442,SPECIAL,Special Pass,ACTIVE
```

### Access Log: `access_log.txt`
```
# Format: TIMESTAMP,CARD_ID,ACCESS_TYPE,ROLE,NAME,STATUS
2024-01-15 14:30:25,0095339862,TAP,GUARD,John Jason Domingo,SUCCESS
```

## Configuration

### RFID Reader Setup
- Compatible with HID keyboard-based RFID readers
- Automatically detects card input
- No additional drivers required

### Database Configuration
- Edit `database.txt` directly or use admin interface
- Supports GUARD, STUDENT, and SPECIAL roles
- Active/Inactive status management

## File Structure

```
ai-niform/
├── ai_niform_login.py      # Main application
├── admin_interface.py      # Database management UI
├── database_manager.py     # Database operations
├── database.txt           # Local database file
├── access_log.txt         # Access attempt logs
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Features

### ✅ Access Control
- Role-based access control
- RFID card validation
- Real-time status updates
- Access logging

### ✅ User Interface
- Clean, modern design
- Responsive layout
- Status indicators
- Confirmation dialogs

### ✅ Database Management
- Local text file storage
- Admin interface
- CRUD operations
- Data validation

### ✅ Security
- Input validation
- Access logging
- Role verification
- Secure card processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue on GitHub.

---

**AI-niform** - Smart Access Control for Modern Institutions 