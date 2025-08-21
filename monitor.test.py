import unittest
from monitor import check_vitals_with_warning

class TestEarlyWarningTransformations(unittest.TestCase):
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

    def test_spo2_near_hypoxemia(self):
        ok, msg = check_vitals_with_warning(98, 80, 90.5)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching hypoxemia')

    def test_spo2_hypoxemia(self):
        ok, msg = check_vitals_with_warning(98, 80, 89)
        self.assertFalse(ok)
        self.assertIn('Oxygen Saturation out of range', msg)

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

if __name__ == "__main__":
    unittest.main()
