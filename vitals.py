def get_warning_ranges(min_value, max_value, tolerance_percent=1.5):
    """
    Calculate low and high warning ranges based on tolerance percent.
    Returns ((near_low_start, near_low_end), (near_high_start, near_high_end))
    """
    tolerance = (tolerance_percent / 100) * max_value
    near_low = (min_value, min_value + tolerance)
    near_high = (max_value - tolerance, max_value)
    return near_low, near_high


def _out_of_range(value, min_val, max_val, label):
    """Return False,msg if value is outside bounds, else None."""
    if value < min_val:
        return False, f"{label} out of range! ({min_val}-{max_val})"
    if value > max_val:
        return False, f"{label} out of range! ({min_val}-{max_val})"
    return None


def _warning_level(value, min_val, max_val, near_low, near_high, low_msg, high_msg):
    """Return True,msg if value is in warning range, else None."""
    if min_val < value <= near_low[1]:
        return True, f"Warning: {low_msg}"
    if near_high[0] <= value < max_val:
        return True, f"Warning: {high_msg}"
    return None


def check_temperature(temp, temp_range=(95, 102)):
    """Check temperature and return (ok, msg)."""
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
    """Check pulse and return (ok, msg)."""
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
    """Check oxygen saturation; only lower bound and warning tolerance."""
    spo2_tolerance = (1.5 / 100) * spo2_min
    if spo2 < spo2_min:
        return False, f"Oxygen Saturation out of range! (min {spo2_min})"
    if spo2_min < spo2 <= spo2_min + spo2_tolerance:
        return True, "Warning: Approaching hypoxemia"
    return True, None


# --- Tiny helper functions to reduce CCN in the main checker ---
def _check_temperature(temp, temp_range):
    return check_temperature(temp, temp_range=temp_range)


def _check_pulse(pulse, pulse_range):
    return check_pulse(pulse, pulse_range=pulse_range)


def _check_spo2(spo2, spo2_min):
    return check_spo2(spo2, spo2_min=spo2_min)


def check_vitals_with_warning(temp, pulse, spo2,
                              temp_range=(95, 102),
                              pulse_range=(60, 100),
                              spo2_min=90):
    """
    Check all vitals in sequence and return first warning or failure.
    Each helper has CCN <= 3 to satisfy complexity limits.
    """
    ok, msg = _check_temperature(temp, temp_range)
    if not ok or msg:
        return ok, msg

    ok, msg = _check_pulse(pulse, pulse_range)
    if not ok or msg:
        return ok, msg

    ok, msg = _check_spo2(spo2, spo2_min)
    return ok, msg
