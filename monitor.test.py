# import unittest
# from monitor import vitals_ok


# class MonitorTest(unittest.TestCase):
#     def test_not_ok_when_any_vital_out_of_range(self):
#         self.assertFalse(vitals_ok(99, 102, 70))
#         self.assertTrue(vitals_ok(98.1, 70, 98))


# if __name__ == '__main__':
#   unittest.main()


#*********************************************************************************************************#

import unittest
from monitor import (
    is_temperature_ok,
    is_pulse_rate_ok,
    is_spo2_ok,
    check_vitals,
    vitals_ok
)
from unittest.mock import patch

class TestMonitorPureFunctions(unittest.TestCase):
    def test_is_temperature_ok(self):
        self.assertTrue(is_temperature_ok(95))
        self.assertTrue(is_temperature_ok(102))
        self.assertTrue(is_temperature_ok(98.6))
        self.assertFalse(is_temperature_ok(94.9))
        self.assertFalse(is_temperature_ok(102.1))

    def test_is_pulse_rate_ok(self):
        self.assertTrue(is_pulse_rate_ok(60))
        self.assertTrue(is_pulse_rate_ok(100))
        self.assertTrue(is_pulse_rate_ok(80))
        self.assertFalse(is_pulse_rate_ok(59))
        self.assertFalse(is_pulse_rate_ok(101))

    def test_is_spo2_ok(self):
        self.assertTrue(is_spo2_ok(90))
        self.assertTrue(is_spo2_ok(95))
        self.assertFalse(is_spo2_ok(89))

    def test_check_vitals_all_ok(self):
        ok, msg = check_vitals(98, 80, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_check_vitals_temperature_critical(self):
        ok, msg = check_vitals(94, 80, 95)
        self.assertFalse(ok)
        self.assertEqual(msg, 'Temperature critical!')

    def test_check_vitals_pulse_critical(self):
        ok, msg = check_vitals(98, 101, 95)
        self.assertFalse(ok)
        self.assertEqual(msg, 'Pulse Rate is out of range!')

    def test_check_vitals_spo2_critical(self):
        ok, msg = check_vitals(98, 80, 89)
        self.assertFalse(ok)
        self.assertEqual(msg, 'Oxygen Saturation out of range!')

class TestMonitorIOFunctions(unittest.TestCase):
    @patch('monitor.animate_alert')
    def test_vitals_ok_true(self, mock_alert):
        self.assertTrue(vitals_ok(98.6, 72, 96))
        mock_alert.assert_not_called()

    @patch('monitor.animate_alert')
    def test_vitals_not_ok_temperature(self, mock_alert):
        self.assertFalse(vitals_ok(104, 72, 96))
        mock_alert.assert_called_once()

    @patch('monitor.animate_alert')
    def test_vitals_not_ok_pulse(self, mock_alert):
        self.assertFalse(vitals_ok(98.6, 110, 96))
        mock_alert.assert_called_once()

    @patch('monitor.animate_alert')
    def test_vitals_not_ok_spo2(self, mock_alert):
        self.assertFalse(vitals_ok(98.6, 72, 85))
        mock_alert.assert_called_once()

if __name__ == '__main__':
    unittest.main()

