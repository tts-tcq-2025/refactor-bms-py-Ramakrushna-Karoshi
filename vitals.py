def get_warning_ranges(min_value, max_value, tolerance_percent=1.5):
    tolerance = (tolerance_percent / 100) * max_value
    near_low = (min_value, min_value + tolerance)
    near_high = (max_value - tolerance, max_value)
    return near_low, near_high


def _check_below(value, min_val, label, max_val=None):
    if value < min_val:
        if max_val:
            return False, f"{label} out of range! ({min_val}-{max_val})"
        return False, f"{label} below minimum {min_val}"
    return None


def _check_above(value, max_val, label, min_val=None):
    if value > max_val:
        if min_val:
            return False, f"{label} out of range! ({min_val}-{max_val})"
        return False, f"{label} above maximum {max_val}"
    return None


def _check_warning(value, near_low, near_high, low_msg, high_msg):
    if near_low[0] < value <= near_low[1]:
        return True, f"Warning: {low_msg}"
    if near_high[0] <= value < near_high[1]:
        return True, f"Warning: {high_msg}"
    return None


def check_temperature(temp, temp_range=(95, 102)):
    near_low, near_high = get_warning_ranges(*temp_range)
    below = _check_below(temp, temp_range[0], "Temperature", temp_range[1])
    if below:
        return below
    above = _check_above(temp, temp_range[1], "Temperature", temp_range[0])
    if above:
        return above
    warning = _check_warning(temp, near_low, near_high,
                             "Approaching hypothermia",
                             "Approaching hyperthermia")
    if warning:
        return warning
    return True, None


def check_pulse(pulse, pulse_range=(60, 100)):
    near_low, near_high = get_warning_ranges(*pulse_range)
    below = _check_below(pulse, pulse_range[0], "Pulse Rate", pulse_range[1])
    if below:
        return below
    above = _check_above(pulse, pulse_range[1], "Pulse Rate", pulse_range[0])
    if above:
        return above
    warning = _check_warning(pulse, near_low, near_high,
                             "Approaching bradycardia",
                             "Approaching tachycardia")
    if warning:
        return warning
    return True, None


def check_spo2(spo2, spo2_min=90):
    spo2_tolerance = (1.5 / 100) * spo2_min
    if spo2 < spo2_min:
        return False, f"Oxygen Saturation out of range! (min {spo2_min})"
    if spo2_min < spo2 <= spo2_min + spo2_tolerance:
        return True, "Warning: Approaching hypoxemia"
    return True, None


def check_vitals_with_warning(
    temp, pulse, spo2, temp_range=(95, 102), pulse_range=(60, 100), spo2_min=90
):
    checks = [
        (check_temperature, temp, {"temp_range": temp_range}),
        (check_pulse, pulse, {"pulse_range": pulse_range}),
        (check_spo2, spo2, {"spo2_min": spo2_min}),
    ]
    for check_func, value, args in checks:
        ok, msg = check_func(value, **args)
        if not ok or msg:
            return ok, msg
    return True, None
