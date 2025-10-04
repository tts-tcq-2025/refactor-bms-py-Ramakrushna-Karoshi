def check_temperature(temp, temp_range=(95, 102)):
    near_low, near_high = get_warning_ranges(*temp_range)
    if temp < temp_range[0]:
        return False, f'Temperature out of range! ({temp_range[0]}-{temp_range[1]})'
    elif near_low[0] <= temp <= near_low[1]:
        return True, 'Warning: Approaching hypothermia'
    elif near_high[0] <= temp <= near_high[1]:
        return True, 'Warning: Approaching hyperthermia'
    elif temp > temp_range[1]:
        return False, f'Temperature out of range! ({temp_range[0]}-{temp_range[1]})'
    else:
        return True, None

def check_pulse(pulse, pulse_range=(60, 100)):
    near_low, near_high = get_warning_ranges(*pulse_range)
    if pulse < pulse_range[0]:
        return False, f'Pulse Rate out of range! ({pulse_range[0]}-{pulse_range[1]})'
    elif near_low[0] <= pulse <= near_low[1]:
        return True, 'Warning: Approaching bradycardia'
    elif near_high[0] <= pulse <= near_high[1]:
        return True, 'Warning: Approaching tachycardia'
    elif pulse > pulse_range[1]:
        return False, f'Pulse Rate out of range! ({pulse_range[0]}-{pulse_range[1]})'
    else:
        return True, None

def check_spo2(spo2, spo2_min=90):
    spo2_tolerance = (1.5 / 100) * spo2_min
    if spo2 < spo2_min:
        return False, f'Oxygen Saturation out of range! (min {spo2_min})'
    elif spo2_min <= spo2 < spo2_min
