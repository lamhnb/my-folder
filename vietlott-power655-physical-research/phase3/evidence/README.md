# Evidence map

`pilot_v1/`: actual full native video frames 00 and 01 for each of 35 captures; six-sample `frames.csv` ledgers, extraction commands/code/source hashes, and ffmpeg logs. Samples 02–05 and per-capture viewing sheets remain local and are ignored by Git. No video is committed. Replay needs externally stored SHA-pinned MP4s.

`readability_draw*.jpg`: reduced crops, two samples per capture, used to read physical rail digits; bottom broadcast overlay excluded. `review_draw*.jpg`: initial wider-time review of samples 00 and 05, retained to show camera-cut missingness. These are same-agent viewing passes, not independent reviews. Raw full frames contain original broadcast graphics but no generated/enhanced content.

`primary_labels.json`: actual single-reviewer readings before result reconciliation. `result_sources/`: minimal secondary-publisher result extracts plus complete HTTP response hashes and failed official attempts; full HTML remains local outside Git. `published_results.csv`: unordered inclusion sets only, never draw order.

`web_lookup_attempts.json`: discovery/corrected official endpoint availability log. `known_failures.csv` includes parser failure and absent evidence. `eligibility.json` and `expansion_status.json`: failed gates; do not interpret not-attempted historical acquisition as missing videos. `sensitivity_scope.md`: explicit timing and limits of optional provisional-pilot computations. `unit_test_output.txt`: software fixtures, not ball-reading accuracy.

All paths inside CSVs are relative to Phase 3 unless explicitly named local input paths. PTS are encoded source timestamps and do not certify physical selection time. The statistical independent unit is a draw. See `../PHASE3_HANDOFF.md` for the incomplete research status.
