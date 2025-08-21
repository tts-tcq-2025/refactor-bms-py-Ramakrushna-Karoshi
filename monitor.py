import sys
import time

# --- Functional: Pure validation functions ---

def is_value_in_range(value, min_value, max_value):
    """Check if value is within [min_value, max_value] inclusive."""
    return min_value <= value <= max_value

def get_warning_ranges(min_value, max_value, tolerance_percent=1.5):
    """Return near-low and near-high warning ranges based on tolerance percent."""
    tolerance = (tolerance_percent / 100) * max_value
    near_low = (min_value, min_value + tolerance)
    near_high = (max_value - tolerance, max_value)
    return near_low, near_high

def check_vitals_with_warning(temp, pulse, spo2, temp_range=(95, 102), pulse_range=(60, 100), spo2_min=90):
    # Temperature
    near_low, near_high = get_warning_ranges(*temp_range)
    if temp < temp_range[0]:
        return False, f'Temperature out of range! ({temp_range[0]}-{temp_range[1]})'
    if near_low[0] <= temp <= near_low[1]:
        return True, 'Warning: Approaching hypothermia'
    if near_high[0] <= temp <= near_high[1]:
        return True, 'Warning: Approaching hyperthermia'
    if temp > temp_range[1]:
        return False, f'Temperature out of range! ({temp_range[0]}-{temp_range[1]})'

    # Pulse Rate
    near_low, near_high = get_warning_ranges(*pulse_range)
    if pulse < pulse_range[0]:
        return False, f'Pulse Rate out of range! ({pulse_range[0]}-{pulse_range[1]})'
    if near_low[0] <= pulse <= near_low[1]:
        return True, 'Warning: Approaching bradycardia'
    if near_high[0] <= pulse <= near_high[1]:
        return True, 'Warning: Approaching tachycardia'
    if pulse > pulse_range[1]:
        return False, f'Pulse Rate out of range! ({pulse_range[0]}-{pulse_range[1]})'

    # SpO2
    spo2_tolerance = (1.5 / 100) * spo2_min
    if spo2 < spo2_min:
        return False, f'Oxygen Saturation out of range! (min {spo2_min})'
    if spo2_min <= spo2 < spo2_min + spo2_tolerance:
        return True, 'Warning: Approaching hypoxemia'

    return True, None

# --- Aspect-Oriented: Alert decorator ---

def alert_on_failure(func):
    def wrapper(*args, **kwargs):
        ok, msg = func(*args, **kwargs)
        if msg:
            print(msg)
            if not ok:
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
def vitals_ok(temperature, pulse_rate, spo2, temp_range=(95, 102), pulse_range=(60, 100), spo2_min=90):
    return check_vitals_with_warning(temperature, pulse_rate, spo2, temp_range, pulse_range, spo2_min)

# --- Object-Oriented: Encapsulate vitals ---

class Vitals:
    def __init__(self, temperature, pulse_rate, spo2,
                 temp_range=(95, 102), pulse_range=(60, 100), spo2_min=90):
        self.temperature = temperature
        self.pulse_rate = pulse_rate
        self.spo2 = spo2
        self.temp_range = temp_range
        self.pulse_range = pulse_range
        self.spo2_min = spo2_min

    def status(self):
        return check_vitals_with_warning(self.temperature, self.pulse_rate, self.spo2,
                                         self.temp_range, self.pulse_range, self.spo2_min)

    def check_and_alert(self):
        ok, msg = self.status()
        if msg:
            print(msg)
            if not ok:
                animate_alert()
        return ok

# --- Main sequence ---

if __name__ == "__main__":
    # Example usage with custom ranges
    v = Vitals(100.6, 99, 92, temp_range=(96, 101), pulse_range=(65, 99), spo2_min=92)
    if v.check_and_alert():
        print("All vitals are within range or warning.")
    else:
        print("One or more vitals are out of range.")
