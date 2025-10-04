import unittest
from monitor import check_vitals_with_warning


class TestEarlyWarningTransformations(unittest.TestCase):
    def test_temperature_near_hypothermia(self):
        """Test temperature just above lower bound triggers hypothermia warning."""
        ok, msg = check_vitals_with_warning(95.5, 80, 95)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching hypothermia')

    def test_temperature_near_hyperthermia(self):
        """Test temperature just below upper bound triggers hyperthermia warning."""
        ok, msg = check_vitals_with_warning(101.5, 80, 95)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching hyperthermia')

    def test_temperature_hypothermia(self):
        """Test temperature below lower bound is out of range."""
        ok, msg = check_vitals_with_warning(94.5, 80, 95)
        self.assertFalse(ok)
        self.assertIn('Temperature out of range', msg)

    def test_temperature_hyperthermia(self):
        """Test temperature above upper bound is out of range."""
        ok, msg = check_vitals_with_warning(102.5, 80, 95)
        self.assertFalse(ok)
        self.assertIn('Temperature out of range', msg)

    def test_temperature_normal(self):
        """Test temperature well within normal range."""
        ok, msg = check_vitals_with_warning(98.0, 80, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_spo2_near_hypoxemia(self):
        """Test SpO2 just above minimum triggers hypoxemia warning."""
        ok, msg = check_vitals_with_warning(98, 80, 90.5)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching hypoxemia')

    def test_spo2_hypoxemia(self):
        """Test SpO2 below minimum is out of range."""
        ok, msg = check_vitals_with_warning(98, 80, 89)
        self.assertFalse(ok)
        self.assertIn('Oxygen Saturation out of range', msg)

    def test_pulse_near_bradycardia(self):
        """Test pulse just above lower bound triggers bradycardia warning."""
        ok, msg = check_vitals_with_warning(98, 61.5, 95)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching bradycardia')

    def test_pulse_near_tachycardia(self):
        """Test pulse just below upper bound triggers tachycardia warning."""
        ok, msg = check_vitals_with_warning(98, 98.5, 95)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching tachycardia')

    def test_pulse_normal(self):
        """Test pulse well within normal range."""
        ok, msg = check_vitals_with_warning(98, 80, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_temperature_at_lower_bound(self):
        """Test temperature exactly at lower bound."""
        ok, msg = check_vitals_with_warning(95, 80, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_temperature_at_upper_bound(self):
        """Test temperature exactly at upper bound."""
        ok, msg = check_vitals_with_warning(102, 80, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_pulse_at_lower_bound(self):
        """Test pulse exactly at lower bound."""
        ok, msg = check_vitals_with_warning(98, 60, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_pulse_at_upper_bound(self):
        """Test pulse exactly at upper bound."""
        ok, msg = check_vitals_with_warning(98, 100, 95)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_spo2_at_minimum(self):
        """Test SpO2 exactly at minimum."""
        ok, msg = check_vitals_with_warning(98, 80, 90)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching hypoxemia')

    def test_combined_out_of_range(self):
        """Test multiple vitals out of range."""
        ok, msg = check_vitals_with_warning(94, 59, 89)
        self.assertFalse(ok)
        self.assertIn('Temperature out of range', msg)  # First error returned

    def test_combined_warning(self):
        """Test multiple vitals in warning range."""
        ok, msg = check_vitals_with_warning(95.5, 61.5, 90.5)
        self.assertTrue(ok)
        self.assertEqual(msg, 'Warning: Approaching hypothermia')  # First warning returned

    def test_parameterized_normal(self):
        """Test several normal values using subTest."""
        for temp, pulse, spo2 in [(98, 80, 95), (100, 70, 96), (97, 90, 99)]:
            with self.subTest(temp=temp, pulse=pulse, spo2=spo2):
                ok, msg = check_vitals_with_warning(temp, pulse, spo2)
                self.assertTrue(ok)
                self.assertIsNone(msg)

if __name__ == "__main__":
    unittest.main()
