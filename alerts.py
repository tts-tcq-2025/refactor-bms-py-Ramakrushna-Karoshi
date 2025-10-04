import sys
import time


def animate_alert(duration=6, interval=1):
    """
    Simple console animation for alerts.
    Prints alternating '*' symbols for a given duration.
    """
    for _ in range(duration):
        print('\r* ', end='')
        sys.stdout.flush()
        time.sleep(interval)
        print('\r *', end='')
        sys.stdout.flush()
        time.sleep(interval)
    print('\r  ', end='')


def alert_if_not_ok(msg, is_ok):
    """
    Print message and animate alert if status is not OK.
    Returns False if alert triggered, else True.
    """
    if not is_ok:
        print(msg)
        animate_alert()
        return False
    return True
