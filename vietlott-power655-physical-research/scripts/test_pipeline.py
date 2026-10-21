"""Numerical/software tests. All fixtures synthetic; never experimental evidence."""
import json,tempfile,unittest,subprocess,sys,shutil
from pathlib import Path
import numpy as np
import cv2
from track_paddles import estimate
from detect_ball_events import associate
from common import write_csv,EVENTS,PADDLES,BALLS
from validate_measurements import validate
class TestPipeline(unittest.TestCase):
    def test_known_rpm_two_methods(self):
        t=np.arange(0,10,1/30);a=(17+360*2*t)%360
        _,_,r=estimate(t,a,150)
        self.assertAlmostEqual(r['slope_rpm_signed'],120,places=8)
        self.assertAlmostEqual(r['cycle_rpm_signed'],120,places=8)
    def test_clockwise(self):
        t=np.arange(0,10,1/30);_,_,r=estimate(t,(23-360*t)%360,100)
        self.assertAlmostEqual(r['slope_rpm_signed'],-60,places=8)
        self.assertAlmostEqual(r['cycle_rpm_signed'],-60,places=8)
    def test_alias_rejected(self):
        with self.assertRaises(ValueError):estimate([0,.5,1],[0,20,40],120)
    def test_nonmonotone_pts_rejected(self):
        with self.assertRaises(ValueError):estimate([0,0,1],[0,20,40],120)
    def test_collision_ambiguity_ends_tracks(self):
        self.assertEqual(associate([[0,0,4],[2,0,4]],[[1,0,4]],10,3),{})
    def test_gated_unique_association(self):
        self.assertEqual(associate([[0,0,4],[100,0,4]],[[2,0,4],[98,0,4]],10,3),{0:0,1:1})
    def test_empty_not_success(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);(p/'measurements').mkdir()
            for n,f in [('events',EVENTS),('paddle_motion',PADDLES),('ball_tracking',BALLS)]:write_csv(p/'measurements'/f'synthetic_{n}.csv',f,[])
            r=validate(p);self.assertEqual(r['schema_integrity'],'passed');self.assertEqual(r['experimental_completion'],'no_measurements')
    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'requires ffmpeg/ffprobe')
    def test_local_native_frame_pts_alignment(self):
        # Original test pixels, not experimental or AI-generated data. Temp only.
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);video=p/'synthetic_only.mkv'
            writer=cv2.VideoWriter(str(video),cv2.VideoWriter_fourcc(*'FFV1'),30,(32,32))
            self.assertTrue(writer.isOpened())
            for i in range(60):writer.write(np.full((32,32,3),i*3,np.uint8))
            writer.release();out=p/'extracted'
            result=subprocess.run([sys.executable,str(Path(__file__).with_name('extract_frames.py')),str(video),'--out',str(out),'--indices','0','30','59','--rights-confirmed'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            from common import read_csv
            manifest=read_csv(out/'frame_manifest.csv');self.assertEqual(len(manifest),60)
            self.assertAlmostEqual(float(manifest[30]['timestamp_seconds']),1,places=3)
            im=cv2.imread(str(out/'frame_00000030.png'));self.assertTrue(np.all(im==90))
if __name__=='__main__':unittest.main(verbosity=2)
