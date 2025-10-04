def get_warning_ranges(min_value, max_value, tolerance_percent=1.5):
    tolerance = (tolerance_percent / 100) * max_value
    near_low = (min_value, min_value + tolerance)
    near_high = (max_value - tolerance, max_value)
    return near_low, near_high


def check_vital_range(value, min_val, max_val, label, low_msg, high_msg):
    """Generic range check for vitals with upper and lower bounds."""
    near_low, near_high = get_warning_ranges(min_val, max_val)

    if value < min_val:
        return False, f"{label} out of range! ({min_val}-{max_val})"
    if min_val < value <= near_low[1]:
        return True, f"Warning: {low_msg}"
    if near_high[0] <= value < max_val:
        return True, f"Warning: {high_msg}"
    if value > max_val:
        return False, f"{label} out of range! ({min_val}-{max_val})"
    return True, None


def check_temperature(temp, temp_range=(95, 102)):
    return check_vital_range(
        temp,
        temp_range[0],
        temp_range[1],
        "Temperature",
        "Approaching hypothermia",
        "Approaching hyperthermia",
    )


def check_pulse(pulse, pulse_range=(60, 100)):
    return check_vital_range(
        pulse,
        pulse_range[0],
        pulse_range[1],
        "Pulse Rate",
        "Approaching bradycardia",
        "Approaching tachycardia",
    )


def check_spo2(spo2, spo2_min=90):
    """Special case: SpO₂ has only a lower bound."""
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
