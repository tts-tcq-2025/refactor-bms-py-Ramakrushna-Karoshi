import unittest
from unittest.mock import patch
from monitor import check_vitals_with_warning, Vitals, vitals_ok
from alerts import alert_if_not_ok, animate_alert


class TestEarlyWarningTransformations(unittest.TestCase):
    # Temperature tests
    def test_temperature_near_hypothermia(self):
        ok, msg = check_vitals_with_warning(95.5, 80, 95)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching hypothermia')

    def test_temperature_near_hyperthermia(self):
        ok, msg = check_vitals_with_warning(101.5, 80, 95)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching hyperthermia')

    def test_temperature_hypothermia(self):
        ok, msg = check_vitals_with_warning(94.5, 80, 95)
        self.assertFalse(ok)
        self.assertIn('Temperature out of range', msg)

    def test_temperature_hyperthermia(self):
        ok, msg = check_vitals_with_warning(102.5, 80, 95)
        self.assertFalse(ok)
        self.assertIn('Temperature out of range', msg)

    def test_temperature_normal(self):
        ok, msg = check_vitals_with_warning(98.0, 80, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    # SpO2 tests
    def test_spo2_near_hypoxemia(self):
        ok, msg = check_vitals_with_warning(98, 80, 90.5)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching hypoxemia')

    def test_spo2_hypoxemia(self):
        ok, msg = check_vitals_with_warning(98, 80, 89)
        self.assertFalse(ok)
        self.assertIn('Oxygen Saturation out of range', msg)

    # Pulse tests
    def test_pulse_near_bradycardia(self):
        ok, msg = check_vitals_with_warning(98, 61.5, 95)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching bradycardia')

    def test_pulse_near_tachycardia(self):
        ok, msg = check_vitals_with_warning(98, 98.5, 95)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching tachycardia')

    def test_pulse_normal(self):
        ok, msg = check_vitals_with_warning(98, 80, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    # Boundary tests
    def test_temperature_at_lower_bound(self):
        ok, msg = check_vitals_with_warning(95, 80, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_temperature_at_upper_bound(self):
        ok, msg = check_vitals_with_warning(102, 80, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_pulse_at_lower_bound(self):
        ok, msg = check_vitals_with_warning(98, 60, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_pulse_at_upper_bound(self):
        ok, msg = check_vitals_with_warning(98, 100, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_spo2_at_minimum(self):
        ok, msg = check_vitals_with_warning(98, 80, 90)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching hypoxemia')

    # Combined tests
    def test_combined_out_of_range(self):
        ok, msg = check_vitals_with_warning(94, 59, 89)
        self.assertFalse(ok)
        self.assertIn('Temperature out of range', msg)  # first error returned

    def test_combined_warning(self):
        ok, msg = check_vitals_with_warning(95.5, 61.5, 90.5)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching hypothermia')  # first warning returned

    # Parameterized normal tests
    def test_parameterized_normal(self):
        for temp, pulse, spo2 in [(98, 80, 95), (100, 70, 96), (97, 90, 99)]:
            with self.subTest(temp=temp, pulse=pulse, spo2=spo2):
                ok, msg = check_vitals_with_warning(temp, pulse, spo2)
                self.assertTrue(ok)
                self.assertIsNone(msg)

    # Vitals class tests
    def test_vitals_class(self):
        v = Vitals(98, 80, 95)
        ok, msg = v.status()
        self.assertTrue(ok)
        self.assertIsNone(msg)

    # Decorator tests
    def test_vitals_ok_decorator(self):
        ok = vitals_ok(98, 80, 95)
        self.assertTrue(ok)

    # Alerts tests
    def test_alert_if_not_ok_true(self):
        result = alert_if_not_ok("msg", True)
        self.assertTrue(result)

    @patch("alerts.animate_alert", return_value=None)
    def test_alert_if_not_ok_false(self, mock_alert):
        result = alert_if_not_ok("Critical!", False)
        self.assertFalse(result)
        mock_alert.assert_called_once()

    @patch("time.sleep", return_value=None)
    def test_animate_alert_runs(self, mock_sleep):
        animate_alert(duration=1, interval=0)
        mock_sleep.assert_called()


if __name__ == "__main__":
    unittest.main()
