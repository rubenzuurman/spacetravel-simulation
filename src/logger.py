from datetime import datetime
import sys
import time

class Logger:
    """
    Class for holding and displaying log messages.
    """
    
    def __init__(self):
        """
        Initialize messages list.
        """
        self.messages = []
        self.log("Initialized logger.")
    
    def log(self, message: str):
        """
        Create nanosecond timestamp and datetime object and add tuple to 
        messages list. Also print formatted message.
        """
        # Create and add tuple to messages list.
        timestamp = time.time_ns()
        datetime_obj = datetime.now()
        self.messages.append((timestamp, datetime_obj, message))
        
        # Format message.
        datetime_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{datetime_str}] {message}"
        print(formatted_message)
        sys.stdout.flush()