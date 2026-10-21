"""Bounded native BGR hash provenance check against 120 immutable Phase1 rows.

No pixels are saved. On any mismatch report counts and stop; never alter ROI,
format, color conversion, expected evidence or timestamps to force agreement.
"""
import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'phase2/evidence/legacy_crop_hash_comparison.json'


def file_hash(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    scalar = ROOT / 'measurements/draw_01372_857_appearance.csv'
    with scalar.open(encoding='utf-8') as stream:
        expected = list(csv.DictReader(stream))
    if len(expected) != 120 or {r['source_id'] for r in expected} != {'IUU05082QtE'}:
        raise ValueError('Unexpected legacy input identity/count')
    # Absolute source PTS seek is required for the packet-copy local clip, whose
    # first PTS need not be zero. Crop/pixel format/order match Phase1 exactly.
    command = ['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'info',
               '-seek_timestamp', '1', '-ss', '857', '-copyts', '-i', str(args.input),
               '-an', '-vf', 'showinfo,crop=900:900:510:60', '-frames:v', '120',
               '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'bgr24', 'pipe:1']
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    stderr = result.stderr.decode(errors='replace')
    pts = [float(v) for v in re.findall(r'\bn:\s*\d+\s+pts:\s*-?\d+\s+pts_time:([0-9.e+\-]+)', stderr)]
    frame_bytes = 900 * 900 * 3
    count, remainder = divmod(len(result.stdout), frame_bytes)
    pts = pts[:count]
    mismatches = []
    pixel_matches = 0
    pts_matches = 0
    view = memoryview(result.stdout)
    observed_hashes = []
    for i in range(min(count, 120)):
        actual = hashlib.sha256(view[i*frame_bytes:(i+1)*frame_bytes]).hexdigest()
        observed_hashes.append(actual)
        pixel_ok = actual == expected[i]['native_crop_bgr_sha256']
        timestamp_ok = i < len(pts) and abs(pts[i] - float(expected[i]['timestamp_seconds'])) < 5e-7
        pixel_matches += int(pixel_ok)
        pts_matches += int(timestamp_ok)
        if not pixel_ok or not timestamp_ok:
            mismatches.append({'clip_frame_index': i,
                               'expected_pts': float(expected[i]['timestamp_seconds']),
                               'observed_pts': pts[i] if i < len(pts) else None,
                               'expected_bgr_sha256': expected[i]['native_crop_bgr_sha256'],
                               'observed_bgr_sha256': actual,
                               'pixel_match': pixel_ok, 'pts_match': timestamp_ok})
    complete = result.returncode == 0 and count == 120 and len(pts) == 120 and remainder == 0
    passed = complete and pixel_matches == 120 and pts_matches == 120
    report = {
        'status': 'all_120_native_crop_hashes_and_pts_match' if passed else 'incomplete_or_mismatch_stop',
        'operation': 'bounded_real_source_native_BGR_decode_provenance_check',
        'source_video_id': 'IUU05082QtE', 'source_format_id_context': '137',
        'input_file': str(args.input), 'input_sha256': file_hash(args.input),
        'phase1_scalar_input': scalar.relative_to(ROOT).as_posix(),
        'phase1_scalar_sha256': file_hash(scalar), 'script_sha256': file_hash(Path(__file__)),
        'ffmpeg_version': subprocess.check_output(['ffmpeg', '-version'], text=True).splitlines()[0],
        'command': command, 'source_pts_seek_seconds': 857,
        'seek_note': 'seek_timestamp=1 aligns absolute source PTS of packet-copy clip; Phase1 public source began at zero. No timing/ROI retuning.',
        'crop_xywh': [510, 60, 900, 900], 'pixel_format': 'bgr24',
        'requested_count': 120, 'decoded_count': count, 'parsed_pts_count': len(pts),
        'trailing_partial_frame_bytes': remainder, 'ffmpeg_returncode': result.returncode,
        'pixel_hash_match_count': pixel_matches, 'pts_match_count': pts_matches,
        'first_pts': pts[0] if pts else None, 'last_pts': pts[-1] if pts else None,
        'raw_bgr_stream_sha256': hashlib.sha256(result.stdout).hexdigest(),
        'ordered_crop_hash_list_sha256': hashlib.sha256('\n'.join(observed_hashes).encode()).hexdigest(),
        'mismatches': mismatches, 'frame_pixels_saved': False,
        'physical_rpm': None, 'absolute_physical_angle': None,
        'interpretation': ('All target native image buffers reproduce Phase1 byte-for-byte and retain matching PTS. This links the new camera review to the original scalar extraction target. It does not validate physical RPM or assign a sole cause to the disagreement.'
                           if passed else 'Source identity is not proven for all target buffers. Stop after this comparison; no adjustments to force agreement.'),
    }
    if not complete:
        report['decode_failure_tail'] = stderr[-2000:]
    OUT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ['status', 'decoded_count', 'pixel_hash_match_count', 'pts_match_count', 'first_pts', 'last_pts']}, indent=2))


if __name__ == '__main__':
    main()
