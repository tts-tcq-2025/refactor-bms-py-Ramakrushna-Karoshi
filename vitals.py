def get_warning_ranges(min_value, max_value, tolerance_percent=1.5):
    tolerance = (tolerance_percent / 100) * max_value
    near_low = (min_value, min_value + tolerance)
    near_high = (max_value - tolerance, max_value)
    return near_low, near_high


def _out_of_range(value, min_val, max_val, label):
    """Return False,msg if value outside [min_val, max_val], else None."""
    if value < min_val:
        return False, f"{label} out of range! ({min_val}-{max_val})"
    if value > max_val:
        return False, f"{label} out of range! ({min_val}-{max_val})"
    return None


def _warning_level(value, min_val, max_val, near_low, near_high, low_msg, high_msg):
    """Return True,msg for low/high warning ranges, else None."""
    if min_val < value <= near_low[1]:
        return True, f"Warning: {low_msg}"
    if near_high[0] <= value < max_val:
        return True, f"Warning: {high_msg}"
    return None


def check_temperature(temp, temp_range=(95, 102)):
    """Check temperature; returns (ok: bool, msg: str|None)."""
    near_low, near_high = get_warning_ranges(*temp_range)

    out = _out_of_range(temp, temp_range[0], temp_range[1], "Temperature")
    if out:
        return out

    warn = _warning_level(
        temp,
        temp_range[0],
        temp_range[1],
        near_low,
        near_high,
        "Approaching hypothermia",
        "Approaching hyperthermia",
    )
    if warn:
        return warn

    return True, None


def check_pulse(pulse, pulse_range=(60, 100)):
    """Check pulse; returns (ok: bool, msg: str|None)."""
    near_low, near_high = get_warning_ranges(*pulse_range)

    out = _out_of_range(pulse, pulse_range[0], pulse_range[1], "Pulse Rate")
    if out:
        return out

    warn = _warning_level(
        pulse,
        pulse_range[0],
        pulse_range[1],
        near_low,
        near_high,
        "Approaching bradycardia",
        "Approaching tachycardia",
    )
    if warn:
        return warn

    return True, None


def check_spo2(spo2, spo2_min=90):
    """SpO2 only has a lower bound and a small tolerance warning range."""
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
