"""Auditor transcription of inspected scanned PDF pages; no OCR guesses.
Re-render with pdftoppm and inspect before changing these facts.
"""
from pathlib import Path
import csv,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parents[1]
LOCAL=Path('C:/vietlott-research-output/physical-audit-20261022/documents')
URL='https://media.vietlott.vn//main.vi/08.2022/cms/power655.pdf'
PDFSHA='9819e0a0d18696d98438e37b4c4ab5caf8b285b7e0edf6c8acfba7a712be4b8e'
facts=[
 ('document_base_decision','125/QD-VIETLOTT','1',1,'03/03/2023 is confirmed in printed amendment heading on PDF page 13; do not infer date from URL'),
 ('document_base_date','2023-03-03','1',13,'Amendment printed heading names the underlying 2023 decision/date'),
 ('document_amendment_effective_date','2025-01-22','1',15,'Venue/publication-location amendment only; not a machine replacement event'),
 ('power_documented_manufacturer','SMART PLAY','1',7,'Explicit operator publication, independent of visual resemblance'),
 ('power_documented_machine_model','MAGNUM II','1',7,'Product-level documented model; no serial or per-draw allocation'),
 ('machine_height','1.78','m',7,'Published nominal exterior height; not a field measurement'),
 ('machine_base_length','0.86','m',7,'Published base/body dimension; not chamber depth'),
 ('machine_base_width','0.84','m',7,'Published base/body dimension; not chamber depth'),
 ('mixing_chamber_diameter','0.61','m',7,'No explicit inner/outer surface definition or dimensional tolerance; cannot silently equate to collision inner diameter'),
 ('ball_holding_chamber_diameter_literal','0.05','m',7,'Literal separate khoang chua bong dimension; reference geometry ambiguous; not adopted as gate clearance'),
 ('machine_mass','159','kg',7,'Published nominal total machine mass; not rotor mass'),
 ('supply_voltage','220:240','V',7,'Published AC range'),
 ('supply_frequency','50','Hz',7,'Supply frequency; not motor RPM'),
 ('used_machine_count','1','1',7,'Normative number per draw; actual serial assignment unknown'),
 ('backup_machine_count_minimum','1','1',7,'At least one; differs from 2017 two-backup rule; not proof of asset retirement'),
 ('paddle_count','3','1',7,'Operating description; no arm lengths/clearance/CAD'),
 ('maintenance_calendar_interval','3 calendar months','1',7,'Continuation on p8: witnessed maintenance record and auditor confirmation; not actual event dates'),
 ('ball_material','solid foam plastic','1',8,'Generic material class; no polymer/foam density/contact coefficients or actual supplier'),
 ('marking_repetitions','12','1',8,'Underlined printed numeral; no marking mass or surface-effect measurement'),
 ('balls_per_case','55','1',8,'Numbers 01-55'),
 ('ball_mass_nominal','0.01234','kg',8,'Normative standard for each ball, not a measurement of numbered physical units'),
 ('ball_mass_tolerance','0.000617','kg',8,'Maximum normative deviation, not observed within-set spread'),
 ('ball_diameter_nominal','0.0505','m',8,'Normative standard for each ball, not actual per-number diameter'),
 ('ball_diameter_tolerance','0.001','m',8,'Maximum normative deviation, not actual sphericity'),
 ('backup_case_count_minimum','1','1',8,'At least one additional case; no actual set register'),
 ('per_ball_pre_draw_inspection','mass and dimension','1',8,'Nonconforming cases replaced; oversight plus auditor confirmation; readings not supplied in PDF'),
 ('inspection_instruments','electronic scale and technical dimensional gauge','1',9,'Accuracy/certificate not specified numerically; sealing/checking requirements only'),
 ('camera_retention_minimum','5184000','s',9,'60 days minimum; not proof recordings still exist after that date'),
 ('case_selection','one of two cases','1',5,'Selection after server locking/sales closure in procedural order; no universal case-code dictionary'),
 ('loading_label_order','01 through 55','1',5,'Normative rack loading sequence; positions/timing/velocities not determined'),
 ('special_sampling_population','49','1',4,'After six main balls; 48 after special by arithmetic'),
 ('maintenance_and_replacement_audit','independent audit checks','1',10,'Requires checking periodic maintenance and repairs/replacements; not actual history'),
]
def main():
 p=LOCAL/'CURRENT_LINKED_POWER_RULE.pdf'
 assert hashlib.sha256(p.read_bytes()).hexdigest()==PDFSHA
 rows=[dict(parameter=k,value_SI=v,unit_SI=u,pdf_page_1based=page,printed_page=str(page) if page<=11 else '1' if page==13 else '2' if page==15 else 'blank',source_url=URL,source_sha256=PDFSHA,status='VERIFIED',evidence_id='R10',method='manual visual transcription of Poppler rendered scan; not OCR',notes=note) for k,v,u,page,note in facts]
 with (OUT/'extracted/current_rule_facts.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 pages=[]
 for n in range(1,17):
  p=LOCAL/f'power2022-page-{n:02d}.png'
  pages.append(dict(pdf_page_1based=n,local_png=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),visual_review='INSPECTED',notes='blank scanned page' if n in [12,14,16] else 'base rule' if n<=11 else '2025 venue amendment'))
 with (OUT/'extracted/rule_page_manifest.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(pages[0]));w.writeheader();w.writerows(pages)
 (OUT/'extracted/current_rule_review.json').write_text(json.dumps(dict(source_pdf_sha256=PDFSHA,pages=16,visual_pages_reviewed=16,pypdf_text_characters=0,render_command=['pdftoppm','-r','120','-png',str(LOCAL/'CURRENT_LINKED_POWER_RULE.pdf'),str(LOCAL/'power2022-page')],poppler_version=subprocess.run(['pdftoppm','-v'],capture_output=True,text=True).stderr.strip(),source_discovery='Direct href on official process page, not guessed model resemblance',scope='Public operator-documented model/specification, not actual serial/metrology or proof latest unamended configuration for every draw',reviewer='codex_auditor_20261022',independent_second_review=False),indent=2),encoding='utf-8')
 print(len(rows),'facts, 16 pages visually inspected')
if __name__=='__main__':main()
