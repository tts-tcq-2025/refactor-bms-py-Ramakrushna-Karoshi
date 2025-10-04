import unittest
from unittest.mock import patch
from monitor import check_vitals_with_warning, Vitals, vitals_ok
from alerts import alert_if_not_ok, animate_alert


class TestEarlyWarningTransformations(unittest.TestCase):
    # ... [existing tests unchanged] ...

    def test_vitals_class(self):
        v = Vitals(98, 80, 95)
        ok, msg = v.status()
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_vitals_ok_decorator(self):
        ok = vitals_ok(98, 80, 95)
        self.assertTrue(ok)

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
        # Just verify it runs without error
        animate_alert(duration=1, interval=0)
        mock_sleep.assert_called()


if __name__ == "__main__":
    unittest.main()
