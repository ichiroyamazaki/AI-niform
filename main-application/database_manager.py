import os
import datetime
import csv

class DatabaseManager:
    def __init__(self, db_file="database.txt"):
        self.db_file = db_file
        self.visitors_file = "visitors.txt"
        self.access_log_file = "access_log.txt"
        
        # Create files if they don't exist
        self._create_files_if_not_exist()
    
    def _create_files_if_not_exist(self):
        """Create necessary files if they don't exist"""
        if not os.path.exists(self.visitors_file):
            with open(self.visitors_file, 'w') as f:
                f.write("# Visitor Database\n")
                f.write("# Format: NAME,CONTACT,VISITING_AS,PURPOSE,VISITING,ID_TYPE,SPECIAL_PASS,CREATED_AT,EXPIRES_AT,STATUS\n")
        
        if not os.path.exists(self.access_log_file):
            with open(self.access_log_file, 'w') as f:
                f.write("# Access Log\n")
                f.write("# Format: TIMESTAMP,ID,ACTION,STATUS\n")
    
    def find_person(self, card_id):
        """Find a person by their card ID"""
        # First check visitors.txt for Special Pass IDs (prioritize fresh registrations)
        try:
            with open(self.visitors_file, 'r') as f:
                # Find the most recent valid entry for this Special Pass ID
                best_match = None
                best_created_at = None
                
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 10:
                        visitor_special_pass = parts[6]  # Special Pass ID
                        status = parts[9]  # Status
                        visitor_name = parts[0]  # Visitor name
                        created_at_str = parts[7]  # Creation timestamp
                        expires_at_str = parts[8]  # Expiration timestamp
                        
                        if visitor_special_pass == card_id and status == "ACTIVE":
                            try:
                                created_at = datetime.datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")
                                expires_at = datetime.datetime.strptime(expires_at_str, "%Y-%m-%d %H:%M:%S")
                                current_time = datetime.datetime.now()
                                
                                # Only consider entries that haven't expired yet
                                if expires_at > current_time:
                                    # Keep track of the entry with the most recent creation time
                                    if best_match is None or created_at > best_created_at:
                                        best_match = {
                                            'id': visitor_special_pass,
                                            'role': 'SPECIAL',
                                            'name': visitor_name,
                                            'status': status
                                        }
                                        best_created_at = created_at
                            except Exception as e:
                                print(f"Error parsing dates: {e}")
                                # If we can't parse the dates, still consider this entry
                                if best_match is None:
                                    best_match = {
                                        'id': visitor_special_pass,
                                        'role': 'SPECIAL',
                                        'name': visitor_name,
                                        'status': status
                                    }
                
                if best_match:
                    return best_match
        except Exception as e:
            print(f"Error reading visitors file: {e}")
        
        # If not found in visitors, check the main database
        try:
            with open(self.db_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 3:
                        db_id = parts[0]
                        role = parts[1]
                        name = parts[2]
                        status = parts[3] if len(parts) > 3 else "ACTIVE"
                        
                        if db_id == card_id:
                            # Return both ACTIVE and INACTIVE entries so expired passes can be detected
                            return {
                                'id': db_id,
                                'role': role,
                                'name': name,
                                'status': status
                            }
        except Exception as e:
            print(f"Error reading database: {e}")
        
        return None
    
    def is_special_pass_in_use(self, special_pass_id):
        """Check if a special pass ID is currently in use"""
        try:
            with open(self.visitors_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 10:  # Updated to 10 fields (removed ID)
                        visitor_special_pass = parts[6]  # Updated index
                        expires_at_str = parts[8]  # Updated index
                        status = parts[9]  # Updated index
                        
                        if visitor_special_pass == special_pass_id and status == "ACTIVE":
                            # Check if the pass has expired
                            try:
                                expires_at = datetime.datetime.strptime(expires_at_str, "%Y-%m-%d %H:%M:%S")
                                if expires_at > datetime.datetime.now():
                                    return True, {
                                        'name': parts[0],  # Updated index
                                        'expires_at': expires_at_str
                                    }
                            except:
                                pass
        except Exception as e:
            print(f"Error checking special pass: {e}")
        
        return False, None
    
    def add_visitor(self, visitor_data):
        """Add a new visitor to the database"""
        try:
            # First, deactivate any existing entries for the same special pass ID
            self._deactivate_existing_special_pass(visitor_data['special_pass'])
            
            with open(self.visitors_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    visitor_data['name'],
                    visitor_data['contact'],
                    visitor_data['visiting_as'],
                    visitor_data['purpose'],
                    visitor_data['visiting'],
                    visitor_data['id_type'],
                    visitor_data['special_pass'],
                    visitor_data['created_at'],
                    visitor_data['expires_at'],
                    visitor_data['status']
                ])
            return True
        except Exception as e:
            print(f"Error adding visitor: {e}")
            return False
    
    def log_access(self, id_number, action, status="SUCCESS"):
        """Log an access attempt"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.access_log_file, 'a') as f:
                f.write(f"{timestamp},{id_number},{action},{status}\n")
        except Exception as e:
            print(f"Error logging access: {e}")
    
    def get_guard_name(self, guard_id):
        """Get guard name by ID"""
        person = self.find_person(guard_id)
        if person and person['role'] == 'GUARD':
            return person['name']
        return "Unknown Guard"
    
    def is_student_number_valid(self, student_number):
        """Check if a student number is valid"""
        try:
            with open(self.db_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 3:
                        db_id = parts[0]
                        role = parts[1]
                        status = parts[3] if len(parts) > 3 else "ACTIVE"
                        
                        # Check if it's a STUDENT_NUMBER entry and matches
                        if role == 'STUDENT_NUMBER' and db_id == student_number and status == "ACTIVE":
                            return True
        except Exception as e:
            print(f"Error checking student number: {e}")
        
        return False
    
    def get_person_by_student_number(self, student_number):
        """Get person data by student number"""
        try:
            with open(self.db_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 4:
                        db_id = parts[0]
                        role = parts[1]
                        name = parts[2]
                        status = parts[3]
                        
                        # Check if it's a STUDENT_NUMBER entry and matches
                        if role == 'STUDENT_NUMBER' and db_id == student_number and status == "ACTIVE":
                            # Get the corresponding RFID ID from the mapping
                            rfid_id = self.get_rfid_from_student_number(student_number)
                            if rfid_id:
                                return {
                                    'id': rfid_id,
                                    'student_number': student_number,
                                    'name': name,
                                    'role': 'STUDENT',
                                    'status': status
                                }
        except Exception as e:
            print(f"Error getting person by student number: {e}")
        
        return None
    
    def get_rfid_from_student_number(self, student_number):
        """Get RFID ID from student number using the mapping"""
        try:
            with open(self.db_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 4:
                        rfid_id = parts[0]
                        role = parts[1]
                        mapped_student_number = parts[2]
                        status = parts[3]
                        
                        # Check if it's a STUDENT_RFID mapping entry
                        if role == 'STUDENT_RFID' and mapped_student_number == student_number and status == "ACTIVE":
                            return rfid_id
        except Exception as e:
            print(f"Error getting RFID from student number: {e}")
        
        return None
    
    def is_special_pass_expired(self, special_pass_id):
        """Check if a special pass has expired"""
        # First check the main database for INACTIVE status
        try:
            with open(self.db_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 4:
                        db_id = parts[0]
                        role = parts[1]
                        status = parts[3]
                        
                        if db_id == special_pass_id and role == 'SPECIAL' and status == 'INACTIVE':
                            return True  # Pass is marked as inactive/expired in main database
        except Exception as e:
            print(f"Error checking main database for expired pass: {e}")
        
        # Then check the visitors file for time-based expiration
        try:
            with open(self.visitors_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 10:  # Updated to 10 fields
                        visitor_special_pass = parts[6]  # Special Pass ID
                        expires_at_str = parts[8]  # Expiration timestamp
                        status = parts[9]  # Status
                        
                        if visitor_special_pass == special_pass_id and status == "ACTIVE":
                            # Check if the pass has expired
                            try:
                                expires_at = datetime.datetime.strptime(expires_at_str, "%Y-%m-%d %H:%M:%S")
                                current_time = datetime.datetime.now()
                                if expires_at < current_time:
                                    return True  # Pass has expired
                            except Exception as e:
                                print(f"Error parsing expiration date: {e}")
        except Exception as e:
            print(f"Error checking visitors file for expired pass: {e}")
        
        return False
    
    def get_special_pass_check_status(self, special_pass_id):
        """Get the current check-in/check-out status of a special pass"""
        try:
            with open(self.visitors_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 10:
                        visitor_special_pass = parts[6]  # Special Pass ID
                        status = parts[9]  # Status
                        
                        if visitor_special_pass == special_pass_id and status == "ACTIVE":
                            # Check if there's a check-in time recorded
                            if len(parts) >= 11:
                                check_in_time = parts[10]  # Check-in time
                                check_out_time = parts[11] if len(parts) > 11 else ""  # Check-out time
                                
                                if check_in_time and check_in_time != "":
                                    if check_out_time and check_out_time != "":
                                        # Has both check-in and check-out, next should be check-in
                                        return "CHECKED_OUT"
                                    else:
                                        # Has check-in but no check-out, next should be check-out
                                        return "CHECKED_IN"
                                else:
                                    # No check-in time, next should be check-in
                                    return "CHECKED_OUT"
                            else:
                                return "CHECKED_OUT"  # No check-in time recorded yet
        except Exception as e:
            print(f"Error getting check status: {e}")
        
        return "CHECKED_OUT"  # Default to checked out
    
    def record_special_pass_check(self, special_pass_id, check_type):
        """Record a check-in or check-out for a special pass"""
        try:
            # Read all lines
            with open(self.visitors_file, 'r') as f:
                lines = f.readlines()
            
            # Find and update the line with the special pass
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated_lines = []
            
            for line in lines:
                if line.startswith('#') or not line.strip():
                    updated_lines.append(line)
                    continue
                
                parts = line.strip().split(',')
                if len(parts) >= 10:
                    visitor_special_pass = parts[6]  # Special Pass ID
                    
                    if visitor_special_pass == special_pass_id:
                        # Ensure we have enough fields
                        while len(parts) < 12:
                            parts.append("")
                        
                        if check_type == "CHECK_IN":
                            parts[10] = current_time  # Check-in time
                            parts[11] = ""  # Clear check-out time
                        elif check_type == "CHECK_OUT":
                            parts[11] = current_time  # Check-out time
                        
                        # Reconstruct the line
                        updated_line = ','.join(parts) + '\n'
                        updated_lines.append(updated_line)
                    else:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
            
            # Write back to file
            with open(self.visitors_file, 'w') as f:
                f.writelines(updated_lines)
            
            return True
        except Exception as e:
            print(f"Error recording check: {e}")
            return False
    
    def get_special_pass_check_times(self, special_pass_id):
        """Get the check-in and check-out times for a special pass"""
        try:
            with open(self.visitors_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 12:
                        visitor_special_pass = parts[6]  # Special Pass ID
                        
                        if visitor_special_pass == special_pass_id:
                            check_in_time = parts[10] if len(parts) > 10 else ""
                            check_out_time = parts[11] if len(parts) > 11 else ""
                            return check_in_time, check_out_time
        except Exception as e:
            print(f"Error getting check times: {e}")
        
        return "", ""
    
    def get_student_teacher_check_status(self, card_id):
        """Get the current check-in/check-out status of a student or teacher"""
        try:
            with open(self.visitors_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 12:
                        visitor_card_id = parts[7]  # Card ID
                        
                        if visitor_card_id == card_id:
                            check_out_time = parts[11] if len(parts) > 11 else ""
                            # If check_out_time is empty, they are checked in
                            if not check_out_time:
                                return "CHECKED_IN"
                            else:
                                return "CHECKED_OUT"
        except Exception as e:
            print(f"Error getting student/teacher check status: {e}")
        
        # If no record found, return CHECKED_OUT (don't create record here)
        return "CHECKED_OUT"  # Default to checked out
    
    def create_student_teacher_record(self, card_id):
        """Create a new record for a student or teacher in the visitors file"""
        try:
            # Get person data from main database
            person = self.find_person(card_id)
            if not person:
                print(f"Person not found for card ID: {card_id}")
                return False
            
            # Create a new record
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = [
                person['name'],           # NAME
                "N/A",                    # CONTACT
                person['role'],           # VISITING_AS
                "Regular Access",         # PURPOSE
                "N/A",                    # VISITING
                "RFID",                   # ID_TYPE
                "",                       # SPECIAL_PASS
                card_id,                  # CARD_ID (position 7)
                current_time,             # CREATED_AT
                "",                       # EXPIRES_AT
                "ACTIVE",                 # STATUS
                "",                       # CHECK_IN_TIME
                ""                        # CHECK_OUT_TIME
            ]
            
            # Append to visitors file
            with open(self.visitors_file, 'a') as f:
                f.write(','.join(record) + '\n')
            
            print(f"Created new record for {person['name']} (Card: {card_id})")
            return True
            
        except Exception as e:
            print(f"Error creating student/teacher record: {e}")
            return False
    
    def record_student_teacher_check(self, card_id, check_type):
        """Record a check-in or check-out for a student or teacher"""
        try:
            # Read all lines
            with open(self.visitors_file, 'r') as f:
                lines = f.readlines()
            
            record_found = False
            
            # Find and update the line
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                
                parts = line.split(',')
                if len(parts) >= 12:
                    visitor_card_id = parts[7]  # Card ID
                    
                    if visitor_card_id == card_id:
                        record_found = True
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        if check_type == "CHECK_IN":
                            # Update check-in time
                            parts[10] = current_time
                            # Clear check-out time
                            if len(parts) > 11:
                                parts[11] = ""
                        elif check_type == "CHECK_OUT":
                            # Update check-out time
                            if len(parts) > 11:
                                parts[11] = current_time
                            else:
                                parts.append(current_time)
                        
                        # Reconstruct the line
                        lines[i] = ','.join(parts) + '\n'
                        break
            
            # If no record found, create a new one and update it directly
            if not record_found:
                if self.create_student_teacher_record(card_id):
                    # Read the file again to get the newly created record
                    with open(self.visitors_file, 'r') as f:
                        lines = f.readlines()
                    
                    # Find the newly created record and update it
                    for i, line in enumerate(lines):
                        line = line.strip()
                        if line.startswith('#') or not line:
                            continue
                        
                        parts = line.split(',')
                        if len(parts) >= 12:
                            visitor_card_id = parts[7]  # Card ID
                            
                            if visitor_card_id == card_id:
                                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                
                                if check_type == "CHECK_IN":
                                    # Update check-in time
                                    parts[10] = current_time
                                    # Clear check-out time
                                    if len(parts) > 11:
                                        parts[11] = ""
                                elif check_type == "CHECK_OUT":
                                    # Update check-out time
                                    if len(parts) > 11:
                                        parts[11] = current_time
                                    else:
                                        parts.append(current_time)
                                
                                # Reconstruct the line
                                lines[i] = ','.join(parts) + '\n'
                                break
                    
                    # Write back to file
                    with open(self.visitors_file, 'w') as f:
                        f.writelines(lines)
                    
                    print(f"Recorded {check_type} for card {card_id}")
                    return True
                else:
                    return False
            
            # Write back to file
            with open(self.visitors_file, 'w') as f:
                f.writelines(lines)
            
            print(f"Recorded {check_type} for card {card_id}")
            return True
            
        except Exception as e:
            print(f"Error recording student/teacher check: {e}")
            return False
    
    def get_student_teacher_check_times(self, card_id):
        """Get the check-in and check-out times for a student or teacher"""
        try:
            with open(self.visitors_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 12:
                        visitor_card_id = parts[7]  # Card ID
                        
                        if visitor_card_id == card_id:
                            check_in_time = parts[10] if len(parts) > 10 else ""
                            check_out_time = parts[11] if len(parts) > 11 else ""
                            return check_in_time, check_out_time
        except Exception as e:
            print(f"Error getting student/teacher check times: {e}")
        
        return "", ""
    
    def ensure_special_pass_record(self, special_pass_id, person):
        """Ensure a Special Pass record exists in the visitors file"""
        try:
            # Check if record already exists
            with open(self.visitors_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 7:
                        visitor_special_pass = parts[6]  # Special Pass ID
                        
                        if visitor_special_pass == special_pass_id:
                            # Record already exists
                            return True
            
            # Record doesn't exist, create it
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = [
                person['name'],           # NAME
                "N/A",                    # CONTACT
                "SPECIAL",                # VISITING_AS
                "Special Pass Access",    # PURPOSE
                "N/A",                    # VISITING
                "RFID",                   # ID_TYPE
                special_pass_id,          # SPECIAL_PASS
                current_time,             # CREATED_AT
                "",                       # EXPIRES_AT
                "ACTIVE",                 # STATUS
                "",                       # CHECK_IN_TIME
                ""                        # CHECK_OUT_TIME
            ]
            
            # Append to visitors file
            with open(self.visitors_file, 'a') as f:
                f.write(','.join(record) + '\n')
            
            print(f"Created Special Pass record for {person['name']} (ID: {special_pass_id})")
            return True
            
        except Exception as e:
            print(f"Error ensuring Special Pass record: {e}")
            return False
    
    def is_special_pass_in_grace_period(self, special_pass_id):
        """Check if a special pass is in grace period (can check-out but not check-in)"""
        try:
            with open(self.visitors_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 10:
                        visitor_special_pass = parts[6]  # Special Pass ID
                        expires_at_str = parts[8]  # Expiration timestamp
                        status = parts[9]  # Status
                        
                        if visitor_special_pass == special_pass_id and status == "ACTIVE":
                            # Get check-in time
                            check_in_time = parts[10] if len(parts) > 10 else ""
                            
                            if check_in_time and check_in_time != "":
                                try:
                                    # Parse expiration and check-in times
                                    expires_at = datetime.datetime.strptime(expires_at_str, "%Y-%m-%d %H:%M:%S")
                                    check_in_dt = datetime.datetime.strptime(check_in_time, "%Y-%m-%d %H:%M:%S")
                                    current_time = datetime.datetime.now()
                                    
                                    # Calculate time remaining when checked in
                                    time_remaining_at_checkin = expires_at - check_in_dt
                                    minutes_remaining_at_checkin = time_remaining_at_checkin.total_seconds() / 60
                                    
                                    # If 10 minutes or less remaining at check-in, and now past expiration
                                    if minutes_remaining_at_checkin <= 10 and current_time > expires_at:
                                        return True  # In grace period
                                except Exception as e:
                                    print(f"Error parsing dates for grace period: {e}")
        except Exception as e:
            print(f"Error checking grace period: {e}")
        
        return False
    
    def is_special_pass_expired_for_checkin(self, special_pass_id):
        """Check if a special pass has expired for check-in (considers grace period)"""
        try:
            with open(self.visitors_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 10:
                        visitor_special_pass = parts[6]  # Special Pass ID
                        expires_at_str = parts[8]  # Expiration timestamp
                        status = parts[9]  # Status
                        
                        if visitor_special_pass == special_pass_id and status == "ACTIVE":
                            try:
                                expires_at = datetime.datetime.strptime(expires_at_str, "%Y-%m-%d %H:%M:%S")
                                current_time = datetime.datetime.now()
                                
                                # For check-in, always check against expiration (no grace period)
                                if current_time > expires_at:
                                    return True  # Expired for check-in
                            except Exception as e:
                                print(f"Error parsing expiration date: {e}")
        except Exception as e:
            print(f"Error checking expiration for check-in: {e}")
        
        return False
    
    def cleanup_expired_special_passes(self):
        """Remove expired Special Passes from visitors.txt to allow reuse"""
        try:
            # Read all lines
            with open(self.visitors_file, 'r') as f:
                lines = f.readlines()
            
            # Filter out expired entries
            current_time = datetime.datetime.now()
            updated_lines = []
            removed_count = 0
            
            for line in lines:
                if line.startswith('#') or not line.strip():
                    updated_lines.append(line)
                    continue
                
                parts = line.strip().split(',')
                if len(parts) >= 10:
                    expires_at_str = parts[8]  # Expiration timestamp
                    status = parts[9]  # Status
                    
                    if status == "ACTIVE":
                        try:
                            expires_at = datetime.datetime.strptime(expires_at_str, "%Y-%m-%d %H:%M:%S")
                            
                            # Check if expired (past 24 hours + grace period)
                            # Add 1 hour grace period for cleanup
                            cleanup_time = expires_at + datetime.timedelta(hours=1)
                            
                            if current_time > cleanup_time:
                                # This Special Pass has expired and should be removed
                                removed_count += 1
                                print(f"Removing expired Special Pass: {parts[6]} (expired: {expires_at_str})")
                                continue  # Skip this line (don't add to updated_lines)
                            else:
                                # Still valid, keep it
                                updated_lines.append(line)
                        except Exception as e:
                            print(f"Error parsing expiration date for cleanup: {e}")
                            # Keep the line if we can't parse the date
                            updated_lines.append(line)
                    else:
                        # Keep non-active entries
                        updated_lines.append(line)
                else:
                    # Keep lines that don't have enough parts
                    updated_lines.append(line)
            
            # Write back to file
            with open(self.visitors_file, 'w') as f:
                f.writelines(updated_lines)
            
            if removed_count > 0:
                print(f"Cleanup completed: {removed_count} expired Special Pass(es) removed")
            
            return removed_count
        except Exception as e:
            print(f"Error during cleanup: {e}")
            return 0
    
    def _deactivate_existing_special_pass(self, special_pass_id):
        """Deactivate any existing entries for a special pass ID"""
        try:
            # Read all lines
            with open(self.visitors_file, 'r') as f:
                lines = f.readlines()
            
            # Update lines to deactivate existing entries
            updated_lines = []
            deactivated_count = 0
            
            for line in lines:
                if line.startswith('#') or not line.strip():
                    updated_lines.append(line)
                    continue
                
                parts = line.strip().split(',')
                if len(parts) >= 10:
                    visitor_special_pass = parts[6]  # Special Pass ID
                    status = parts[9]  # Status
                    
                    if visitor_special_pass == special_pass_id and status == "ACTIVE":
                        # Deactivate this entry
                        parts[9] = "INACTIVE"
                        updated_line = ','.join(parts) + '\n'
                        updated_lines.append(updated_line)
                        deactivated_count += 1
                        print(f"Deactivated existing Special Pass entry: {special_pass_id}")
                    else:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
            
            # Write back to file if any entries were deactivated
            if deactivated_count > 0:
                with open(self.visitors_file, 'w') as f:
                    f.writelines(updated_lines)
                print(f"Deactivated {deactivated_count} existing Special Pass entry(ies) for ID: {special_pass_id}")
            
            return deactivated_count
        except Exception as e:
            print(f"Error deactivating existing special pass: {e}")
            return 0

    def is_special_pass_available_for_registration(self, special_pass_id):
        """Check if a Special Pass ID is available for new registration"""
        # First, clean up any expired Special Passes
        self.cleanup_expired_special_passes()
        
        # Then check if the ID is currently in use
        is_in_use, existing_visitor = self.is_special_pass_in_use(special_pass_id)
        
        return not is_in_use
