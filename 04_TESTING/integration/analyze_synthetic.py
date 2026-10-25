#!/usr/bin/env python3
"""Educational correlation, not an endpoint detector."""
import json
from pathlib import Path
rows=[json.loads(s) for s in (Path(__file__).resolve().parents[1]/'test_data/synthetic_events.jsonl').read_text().splitlines()]
if not all(r.get('synthetic') is True for r in rows): raise RuntimeError('Unlabeled event')
alerts=[];accessed=set()
for r in rows:
 if r['kind']=='process_create' and r['creator_pid']!=r['reported_parent_pid']: alerts.append('synthetic creator/parent discrepancy')
 if r['kind']=='process_access': accessed.add(r['target_pid'])
 if r['kind']=='image_memory_changed' and r['pid'] in accessed: alerts.append('synthetic memory-change correlation')
if len(alerts)!=2:raise RuntimeError('Expected two educational correlations')
print('PASS 2 synthetic correlations (no real endpoint events): '+ '; '.join(alerts))
