from vitals import check_vitals_with_warning
from alerts import animate_alert

def alert_on_failure(func):
    def wrapper(*args, **kwargs):
        ok, msg = func(*args, **kwargs)
        if msg:
            print(msg)
            if not ok:
                animate_alert()
        return ok
    return wrapper


@alert_on_failure
def vitals_ok(temperature, pulse_rate, spo2,
              temp_range=(95, 102), pulse_range=(60, 100), spo2_min=90):
    return check_vitals_with_warning(temperature, pulse_rate, spo2,
                                     temp_range, pulse_range, spo2_min)


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
        return check_vitals_with_warning(
            self.temperature, self.pulse_rate, self.spo2,
            self.temp_range, self.pulse_range, self.spo2_min
        )

    def check_and_alert(self):
        ok, msg = self.status()
        if msg:
            print(msg)
            if not ok:
                animate_alert()
        return ok


if __name__ == "__main__":
    v = Vitals(100.6, 99, 92, temp_range=(96, 101), pulse_range=(65, 99), spo2_min=92)
    if v.check_and_alert():
        print("All vitals are within range or warning.")
    else:
        print("One or more vitals are out of range.")
