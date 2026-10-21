# Locked-definition replication: 01373 and 01374

The two cached real sources were inspected after the 01372 pilot/native refinement. The same six event definitions remain separate: control command, first visible collector motion, first clear ball visibility in the upper collector, permanent isolation, leading-edge exit onto the downstream ramp proxy, and graphic onset. No lottery result values were used to choose image-motion parameters. This is AI visual review in the same session; human review, blind review, reviewer calibration and independent experimental validation are all false.

Source renditions are format137, 1920×1080, 30000/1001 encoded PTS samples/second. Exact local SHA256 values and acquisition records are bound in `replication_01373.json` and `replication_01374.json`. Native PNGs and frame ledgers preserve source PTS, native crop dimensions and hashes. The original camera frame rate, exposure and physical clock accuracy remain unknown.

The 01373 overview spans 1040.005633–1218.183633 seconds, sampled every60 encoded frames. The 01374 overview spans 1050.015633–1218.183633 seconds with the same sampling rule. Seven transfers were located visually in each draw. Bounded four-second windows around each transfer were then sampled every6 native frames (0.2002seconds); ambiguous release regions were inspected every1 native frame. All14 downstream ramp proxy before/after pairs were also viewed individually at native crop size. The selected endpoint brackets deliberately retain a few encoded frames when blur makes a touching silhouette ambiguous.

| Attempt | 01373 ramp-proxy PTS bracket (s) | 01374 ramp-proxy PTS bracket (s) |
|---:|---:|---:|
| 1 | 1126.358567–1126.391933 | 1108.140367–1108.240467 |
| 2 | 1138.437300–1138.537400 | 1120.819700–1120.919800 |
| 3 | 1152.084267–1152.151000 | 1133.365567–1133.432300 |
| 4 | 1164.630133–1164.730233 | 1145.544400–1145.644500 |
| 5 | 1178.544033–1178.677500 | 1159.525033–1159.625133 |
| 6 | 1192.958433–1193.058533 | 1173.338833–1173.438933 |
| 7, special | 1207.005800–1207.105900 | 1187.186000–1187.286100 |

Every ramp bracket meets the unchanged target of at most0.2002seconds. Their widths are encoded-image brackets, not empirical physical accuracy, confidence intervals, permanent-selection timing, or a claim that exposure was shorter than one frame. The proxy is the leading silhouette extending beyond the visible front housing/post edge toward the downstream ramp, not the final seated-ball position. No exact point timestamps are supplied. Camera perspective changes mean the proxy cannot automatically be treated as an identical calibrated3D crossing plane across days.

Graphic onset is separately bracketed using the overview samples, with widths2.002seconds. Physical balls are already visible in the result channel while the corresponding graphic remains unfilled. Audio announcements were not reviewed in this subtask; format137 here is video-only. Graphic timing must not replace ramp timing or permanent isolation.

The first outlet shot in each draw already contains a ball: upper-collector first visibility and mechanism onset are left-censored. The second 01374 attempt uses a ramp view that does not adequately expose the upper collector, so its first upper-collector visibility remainsNA. Several later mechanism onsets are outside the bounded window or hidden by the selected camera; they also remainNA. Other first-clear upper-collector states are bracketed at every6 native frames and remain visibility proxies, not proven entry across an internal gate. Permanent isolation and electrical command onset areNA for every attempt.

Initial mixing is first clearly seen in the sampled close-ups by1092.057633seconds for01373 and1082.047633seconds for01374, after control/camera cuts. Actual mixer-start transitions are not continuously visible. These are first-observed moving states/upper bounds; exact mixer start and an exact initial mixing duration remainNA. Downstream inter-transfer intervals can be described from their brackets, but two draws and seven correlated attempts per draw do not establish a timer model or independent sample count of14draws.

Camera changes are reported explicitly. The first transfer in each draw has a longer ramp view; later transfers alternate collector close-up and ramp cameras. Event-view crops are source x1400,y80,width520,height720 for attempt1, and x800,y180,width1100,height700 for attempts2–7. These native viewing crops differ from the pilot where camera framing requires it. They do not change the locked motion ROI or annulus, and each extraction records its camera/crop arguments.

Motion transfer is refused for both sources. The locked parameters remain ROI(480,80,900,900), source center(932,525), annulus130–350. At01373 PTS1096.061633 the source is much more zoomed: the outer chamber is clipped by the image and the hub is markedly larger than the pilot. At01374 PTS1088.053633 the native image puts the hub roughly aroundx1045, visibly displaced from the locked center, with different framing/radius and more of the neighboring chamber. These are qualitative image comparisons, not calibration measurements. Native reference PNGs and hashes are in the respective `replication_*_rotor_native` directories. The01374 balls also appear green, so the unchanged yellow exclusion is unvalidated on that source. No recentering, resizing, color retuning or replacement flow run was performed.

Physical paddle angle, direction, identity and RPM remainNA. No claim of shared axis or speed is made from similar transparent blades. H1 therefore has no eligible angle input. The repeatable visible transfer sequence gives additional H2 event-bracket evidence, while actual permanent-selection timing, mixer onset and physical accuracy remain unresolved.

During individual native checking, the initially chosen01374 attempt6 upper-collector pair was found to contain no visible ball in either endpoint. The canonical JSON corrects the first-clear visibility interval to1171.904067–1172.104267seconds. The prior JSON remains at `replication_01374_pre_correction.json` as superseded review history; ramp-proxy brackets are unaffected. The initial builder also encountered a Windows default-text-codec failure before producing output; explicit UTF-8 decoding fixed it. Both are retained in validation evidence rather than treated as successful first attempts.

The JSON builder verifies source and endpoint hashes and refuses overwriting existing outputs. To repeat extraction, use the exact arguments in each `sampling_windows` entry with a new `--tag`; to rematerialize annotations, use a clean copy of the Phase2 evidence tree or new output names. Primary Phase2 CSVs were not modified by this subtask.
