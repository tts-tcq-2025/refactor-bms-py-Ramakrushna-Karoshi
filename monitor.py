
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

import sys
import time

# --- Pure Functions ---

def is_temperature_ok(temp):
    """Return True if temperature is within normal range."""
    return 95 <= temp <= 102

def is_pulse_rate_ok(pulse):
    """Return True if pulse rate is within normal range."""
    return 60 <= pulse <= 100

def is_spo2_ok(spo2):
    """Return True if SpO2 is within normal range."""
    return spo2 >= 90

def check_vitals(temperature, pulse_rate, spo2):
    """
    Returns (ok: bool, message: str or None) indicating if all vitals are OK.
    """
    if not is_temperature_ok(temperature):
        return False, 'Temperature critical!'
    if not is_pulse_rate_ok(pulse_rate):
        return False, 'Pulse Rate is out of range!'
    if not is_spo2_ok(spo2):
        return False, 'Oxygen Saturation out of range!'
    return True, None

# --- I/O Functions ---

def animate_alert(duration=6, interval=1):
    """Animate alert for a given duration and interval."""
    for _ in range(duration):
        print('\r* ', end='')
        sys.stdout.flush()
        time.sleep(interval)
        print('\r *', end='')
        sys.stdout.flush()
        time.sleep(interval)
    print('\r  ', end='')  # Clear line at end

def print_and_animate(message):
    print(message)
    animate_alert()

def vitals_ok(temperature, pulse_rate, spo2):
    ok, message = check_vitals(temperature, pulse_rate, spo2)
    if not ok:
        print_and_animate(message)
    return ok

# --- Main (example usage) ---

if __name__ == "__main__":
    # Example usage
    temperature = 101
    pulse_rate = 80
    spo2 = 95
    if vitals_ok(temperature, pulse_rate, spo2):
        print("All vitals are within range.")
    else:
        print("One or more vitals are out of range.")





