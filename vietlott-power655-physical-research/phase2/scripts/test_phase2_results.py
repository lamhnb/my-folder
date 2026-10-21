"""Software-only oracles: interval arithmetic and no-fabrication contracts."""
import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import build_results as b
class ResultsTests(unittest.TestCase):
    def test_interval_conservative_bounds(self):
        # Later event could be11or12; earlier1or2: duration can9..11.
        self.assertEqual(b.interval_difference((11,12),(1,2)),(9,11))
    def test_reversed_and_nonfinite_intervals_rejected(self):
        for bad in [((12,11),(1,2)),((11,float('inf')),(1,2)),((11,12),(float('nan'),2))]:
            with self.assertRaises(ValueError):b.interval_difference(*bad)
    def test_missing_state_does_not_become_zero(self):
        e=b.normalize_event({'event_type':'control_onset','lower_pts_seconds':None,'upper_pts_seconds':None,'event_timestamp_seconds':None})
        self.assertIsNone(e['lower_pts_seconds']);self.assertIsNone(e['upper_pts_seconds'])
    def test_point_time_cannot_replace_interval(self):
        with self.assertRaises(ValueError):b.normalize_event({'event_type':'trough_entry_visible_proxy','event_timestamp_seconds':4.0})
    def test_separate_ball_proxy_cannot_certify_permanent_isolation(self):
        with self.assertRaises(ValueError):b.normalize_event({'event_type':'permanent_ball_isolation','lower_pts_seconds':1,'upper_pts_seconds':2})
    def test_missing_review_is_failure_before_writing(self):
        with tempfile.TemporaryDirectory() as td,patch.object(b,'ROOT',Path(td)):
            with self.assertRaises(ValueError):b.build()
            self.assertEqual(list(Path(td).iterdir()),[])
    def test_incomplete_capture_review_cannot_be_complete_study(self):
        with self.assertRaises(ValueError):b.captures_from_review({'captures':[]})
if __name__=='__main__':unittest.main(verbosity=2)
