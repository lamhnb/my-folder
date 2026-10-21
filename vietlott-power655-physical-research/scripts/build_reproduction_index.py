"""Explicit rerun commands for successful evidence logs, not experimental results."""
import json
from pathlib import Path
from common import write_csv
ROOT=Path(__file__).resolve().parents[1]
def main():
    rows=[]
    for p in sorted((ROOT/'evidence'/'clips').glob('*.json')):
        c=json.loads(p.read_text());vid=c['video_id'];start=c['requested_start']
        if c.get('ffmpeg_exit_code')!=0 or c['frames_decoded']==0:continue
        width=c.get('preview_width',960 if start in (860,960) and vid=='IUU05082QtE' else 320)
        cmd=f"python scripts/inspect_clip.py {vid} --start {start:g} --duration {c['duration_requested']:g} --every {c['sampling_every_native_frames']} --cell-width {width} --cols 4"
        if c.get('crop_source_pixels'):cmd+=' --crop '+' '.join(map(str,c['crop_source_pixels']))
        rows.append({'kind':'inspection_contact_sheet_not_measurement','source_id':vid,'ledger':p.relative_to(ROOT).as_posix(),'command':cmd,
            'expected_samples':c['frames_decoded'],'expected_first_pts':c['samples'][0]['source_pts_seconds'],'expected_last_pts':c['samples'][-1]['source_pts_seconds'],
            'notes':'Media only in RAM. Compare pre-overlay BGR sample hashes using identical dimensions. New log filename is timestamped; source can change.'})
    rows.append({'kind':'unvalidated_native_crop_measurement','source_id':'IUU05082QtE','ledger':'measurements/draw_01372_857_appearance.json',
        'command':'python scripts/measure_stream_appearance.py IUU05082QtE --draw-id 01372 --start 857 --count 120 --roi 510 60 900 900 --center 450 450 --annulus 130 400 --harmonic 3',
        'expected_samples':120,'expected_first_pts':857.022833,'expected_last_pts':860.993467,'notes':'Operational-check section per ASR/context; run in separate copy because output overwrite is refused. Not physical RPM.'})
    write_csv(ROOT/'evidence'/'reproduction_commands.csv',list(rows[0]),rows)
    print(json.dumps({'commands':len(rows)}))
if __name__=='__main__':main()
