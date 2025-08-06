
# from time import sleep
# import sys


# def vitals_ok(temperature, pulseRate, spo2):
#   if temperature > 102 or temperature < 95:
#     print('Temperature critical!')
#     for i in range(6):
#       print('\r* ', end='')
#       sys.stdout.flush()
#       sleep(1)
#       print('\r *', end='')
#       sys.stdout.flush()
#       sleep(1)
#     return False
#   elif pulseRate < 60 or pulseRate > 100:
#     print('Pulse Rate is out of range!')
#     for i in range(6):
#       print('\r* ', end='')
#       sys.stdout.flush()
#       sleep(1)
#       print('\r *', end='')
#       sys.stdout.flush()
#       sleep(1)
#     return False
#   elif spo2 < 90:
#     print('Oxygen Saturation out of range!')
#     for i in range(6):
#       print('\r* ', end='')
#       sys.stdout.flush()
#       sleep(1)
#       print('\r *', end='')
  #     sys.stdout.flush()
  #     sleep(1)
  #   return False
  # return True




#*************************************************************************************************************************************************#

# import sys
# import time

# # --- Pure Functions ---

# def is_temperature_ok(temp):
#     """Return True if temperature is within normal range."""
#     return 95 <= temp <= 102

# def is_pulse_rate_ok(pulse):
#     """Return True if pulse rate is within normal range."""
#     return 60 <= pulse <= 100

# def is_spo2_ok(spo2):
#     """Return True if SpO2 is within normal range."""
#     return spo2 >= 90

# def check_vitals(temperature, pulse_rate, spo2):
#     """
#     Returns (ok: bool, message: str or None) indicating if all vitals are OK.
#     """
#     if not is_temperature_ok(temperature):
#         return False, 'Temperature critical!'
#     if not is_pulse_rate_ok(pulse_rate):
#         return False, 'Pulse Rate is out of range!'
#     if not is_spo2_ok(spo2):
#         return False, 'Oxygen Saturation out of range!'
#     return True, None

# # --- I/O Functions ---

# def animate_alert(duration=6, interval=1):
#     """Animate alert for a given duration and interval."""
#     for _ in range(duration):
#         print('\r* ', end='')
#         sys.stdout.flush()
#         time.sleep(interval)
#         print('\r *', end='')
#         sys.stdout.flush()
#         time.sleep(interval)
#     print('\r  ', end='')  # Clear line at end

# def print_and_animate(message):
#     print(message)
#     animate_alert()

# def vitals_ok(temperature, pulse_rate, spo2):
#     ok, message = check_vitals(temperature, pulse_rate, spo2)
#     if not ok:
#         print_and_animate(message)
#     return ok

# # --- Main (example usage) ---

# if __name__ == "__main__":
#     # Example usage
#     temperature = 101
#     pulse_rate = 80
#     spo2 = 95
#     if vitals_ok(temperature, pulse_rate, spo2):
#         print("All vitals are within range.")
#     else:
#         print("One or more vitals are out of range.")




#************************************************#

import sys
import time

# --- Functional: Pure validation functions ---

def is_temperature_ok(temp):
    return 95 <= temp <= 102

def is_pulse_rate_ok(pulse):
    return 60 <= pulse <= 100

def is_spo2_ok(spo2):
    return spo2 >= 90

def check_vitals(temp, pulse, spo2):
    if not is_temperature_ok(temp):
        return False, 'Temperature critical!'
    if not is_pulse_rate_ok(pulse):
        return False, 'Pulse Rate is out of range!'
    if not is_spo2_ok(spo2):
        return False, 'Oxygen Saturation out of range!'
    return True, None

# --- Aspect-Oriented: Alert decorator ---

def alert_on_failure(func):
    def wrapper(*args, **kwargs):
        ok, msg = func(*args, **kwargs)
        if not ok:
            print(msg)
            animate_alert()
        return ok
    return wrapper

# --- Procedural: Animation and main sequence ---

def animate_alert(duration=6, interval=1):
    for _ in range(duration):
        print('\r* ', end='')
        sys.stdout.flush()
        time.sleep(interval)
        print('\r *', end='')
        sys.stdout.flush()
        time.sleep(interval)
    print('\r  ', end='')

@alert_on_failure
def vitals_ok(temperature, pulse_rate, spo2):
    return check_vitals(temperature, pulse_rate, spo2)

# --- Object-Oriented: Encapsulate vitals ---

class Vitals:
    def __init__(self, temperature, pulse_rate, spo2):
        self.temperature = temperature
        self.pulse_rate = pulse_rate
        self.spo2 = spo2

    def status(self):
        return check_vitals(self.temperature, self.pulse_rate, self.spo2)

    def check_and_alert(self):
        ok, msg = self.status()
        if not ok:
            print(msg)
            animate_alert()
        return ok

# --- Main sequence ---

if __name__ == "__main__":
    # Example usage
    v = Vitals(101, 80, 95)
    if v.check_and_alert():
        print("All vitals are within range.")
    else:
        print("One or more vitals are out of range.")





