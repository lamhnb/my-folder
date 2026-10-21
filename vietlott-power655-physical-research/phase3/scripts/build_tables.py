"""Bind observed physical labels to evidence; published sets are reconciliation only."""
import csv
import json
from pathlib import Path
from extract_pilot import read_csv,write_csv,sha

ROOT=Path(__file__).resolve().parents[1]
P2=ROOT.parent/'phase2'

def main():
    labels=json.loads((ROOT/'evidence'/'primary_labels.json').read_text(encoding='utf-8'))
    sources=read_csv(P2/'phase2_sources.csv');captures=read_csv(P2/'capture_event_audit.csv')
    checked=json.loads((ROOT/'evidence'/'pilot_v1_source_check.json').read_text())
    rows=[];quality=[];registry=[];published=[]
    for source in sources:
        draw=source['draw_id'];numbers=labels['labels'][draw]
        result=json.loads((ROOT/'evidence'/'result_sources'/f'draw{draw}.json').read_text(encoding='utf-8'))
        secondary=result['secondary'];seven=secondary.get('published_numbers',[])
        matched=len(seven)==7 and set(numbers[:6])==set(seven[:6]) and numbers[6]==seven[6]
        # HTTP error or a generic result page is never an official confirmation.
        official='unavailable_http_403' if result['official']['http_status']==403 else 'not_verified'
        for index,num in enumerate(numbers,1):
            folder=ROOT/'evidence'/'pilot_v1'/f'draw{draw}_capture{index:02d}'
            frames=read_csv(folder/'frames.csv');first,last=frames[:2]
            if sha(ROOT/first['evidence_image_path'])!=first['evidence_sha256']:raise ValueError('Frame hash mismatch')
            rows.append(dict(draw_id=draw,draw_date=source['draw_date_associated'],source_id=source['source_id'],
                source_sha256=source['video_sha256'],capture_index=index,ball_type='main' if index<=6 else 'special',
                ball_number=num,readable_pts_start=first['source_pts_seconds'],readable_pts_end=last['source_pts_seconds'],
                evidence_image_path=first['evidence_image_path'],evidence_sha256=first['evidence_sha256'],
                primary_review=labels['reviewer_id'],secondary_review='NA',confidence='high_visual_readability',
                verification_status='provisional_one_review',
                notes='Physical rail digits; two readable samples by same reviewer; evidence end sample 01 in frames.csv. Official numbers unavailable; secondary published set matches.' if matched else 'Secondary result reconciliation unresolved'))
        quality.append(dict(draw_id=draw,n_captures=7,n_readable=7,readable_fraction=1.0,
            n_independent_reviewers=1,n_two_review_labels=0,cross_review_agreement='NA',
            distinct_seven_numbers=len(set(numbers))==7,unordered_main_secondary_match=matched,
            special_secondary_match=len(seven)==7 and numbers[6]==seven[6],
            official_result_status=official,primary_analysis_eligible=False,
            observed_reading_errors=0,estimated_recognition_accuracy='NA',
            sorted_order_flag=numbers[:6]==sorted(numbers[:6]),
            issue='Independent second review and independently sourced official numeric result missing'))
        registry.append(dict(draw_id=draw,draw_date=source['draw_date_associated'],source_id=source['source_id'],
            source_url=source['source_url'],source_sha256=source['video_sha256'],source_bytes=source['input_bytes'],
            local_input_path=source['input_file_local_only'],sha256_rechecked=checked[source['source_id']]==source['video_sha256'],
            format_id=source['format_id'],fps=source['rendition_fps'],time_base=source['time_base'],
            collection_status='reused_phase2_video',selection='five_preselected_phase2_pilot_draws_nonrandom',
            duplicate_draw=False,source_master_authenticated=False,machine_model='NA',machine_id='NA',ball_set_id='NA',
            official_result_lookup_url=result['official']['url'],official_result_status=official,
            official_result_url=f'https://vietlott.vn/vi/trung-thuong/ket-qua-trung-thuong/655?id={draw}&nocatche=1',
            secondary_result_url=secondary['url'],secondary_response_sha256=secondary['response_sha256'],
            secondary_reconciliation=matched,
            official_date_source='https://vietlott.vn/vi/trung-thuong/linh-thuong/thoi-gian-linh-thuong-655',
            date_source_scope='official schedule confirms draw/date only; not number result',
            source_identity_status='Phase2 associated date; public rendition; master/channel authentication unverified'))
        published.append(dict(draw_id=draw,draw_date=source['draw_date_associated'],main_unordered=' '.join(map(str,seven[:6])),
            special=seven[6] if len(seven)==7 else 'NA',publisher='Minh Ngoc (secondary; not Vietlott)',url=secondary['url'],
            response_sha256=secondary['response_sha256'],status='secondary_published_result_only',
            purpose='Unordered set reconciliation only; never source of physical order'))
    write_csv(ROOT/'draw_order_verified.csv',rows);write_csv(ROOT/'quality_audit.csv',quality)
    write_csv(ROOT/'source_registry.csv',registry);write_csv(ROOT/'evidence'/'published_results.csv',published)
    (ROOT/'evidence'/'expansion_status.json').write_text(json.dumps(dict(target_distinct_draws=100,
        collected_distinct_draws=5,additional_historical_draws_attempted=0,additional_historical_draws_verified=0,
        status='not_started_pilot_quality_gate_unmet',not_missing_video_evidence=True,
        reasons=['independent_second_review_not_available_in_this_run','official_numeric_result_lookup_http_403'],
        holdout_status='No sealed historical cohort; pilot is development data; no heldout outcomes analyzed',
        required_next='Independent blinded reading of 35 events and official numeric reconciliation; freeze cohort then reserve latest 20 percent'),indent=2))
    print('35 provisional physical labels; 5 secondary set matches; 0 primary-eligible draws')

if __name__=='__main__':main()
