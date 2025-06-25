import pyotp

import pyotp
import time
import re

class Totp:
    
        
    @staticmethod
    def totp_number(uri):
        match = re.search(r'secret=([^&]+)', uri)
        if match:
            secret = match.group(1) 
        else:
            secret = uri.replace(" ", "")
        totp_number = pyotp.TOTP(secret).now()         
        return totp_number
    @staticmethod
    def totp_time_calculator():    
        period = 30  # Período configurado no TOTP
        time_now = int(time.time())
        time_remaining = period - (time_now % period)
        return time_remaining
