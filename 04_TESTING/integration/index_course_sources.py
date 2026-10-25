#!/usr/bin/env python3
"""Inventory the local Maldev Academy export without extracting code archives."""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys

DEFAULT = Path.home() / 'Downloads/Telegram Desktop/Maldev-Academy-Malware-Development'
SKIP_TAGS = {'script', 'style', 'code', 'pre', 'svg', 'nav'}
TOPICS = {
    'windows-fundamentals': ('Windows API', 'Windows architecture', 'memory management', 'processes'),
    'pe-and-dlls': ('Portable Executable', 'PE header', 'import address table', 'DLL'),
    'detection-and-edr': ('detection', 'Microsoft Defender', 'EDR', 'ETW', 'AMSI'),
    'process-inventory-and-identity': ('process enumeration', 'PPID', 'parent process', 'command line'),
    'crypto-and-payload-storage': ('AES', 'RC4', 'XOR', 'payload encryption', 'registry'),
    'signing-and-provenance': ('binary signing', 'certificate', 'Authenticode'),
    'injection-and-thread-manipulation': ('process injection', 'thread hijacking', 'APC', 'function stomping', 'mapping injection'),
    'imports-hooks-and-syscalls': ('IAT hiding', 'API hashing', 'API hooking', 'syscalls', 'unhooking'),
    'anti-analysis-and-evasion': ('anti-debugging', 'anti-virtual', 'API hammering', 'bypassing AV', 'obfuscation'),
}
def topic_signals(text):
    low = text.casefold()
    return [topic for topic, terms in TOPICS.items() if any(term.casefold() in low for term in terms)]

class TextAudit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skipping = 0
        self.title_depth = 0
        self.title = []
        self.headings = []
        self.text_chars = 0
        self._heading_depth = 0
        self._heading_parts = []
    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS: self.skipping += 1
        if tag == 'title': self.title_depth += 1
        if re.fullmatch(r'h[1-4]', tag):
            self._heading_depth += 1
            if self._heading_depth == 1: self._heading_parts = []
    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.skipping: self.skipping -= 1
        if tag == 'title' and self.title_depth: self.title_depth -= 1
        if re.fullmatch(r'h[1-4]', tag) and self._heading_depth:
            self._heading_depth -= 1
            if self._heading_depth == 0:
                value = re.sub(r'\s+', ' ', ' '.join(self._heading_parts)).strip()
                if value: self.headings.append(value)
    def handle_data(self, data):
        if self.skipping: return
        value = re.sub(r'\s+', ' ', data).strip()
        if not value: return
        self.text_chars += len(value)
        if self.title_depth: self.title.append(value)
        if self._heading_depth: self._heading_parts.append(value)

def digest(path: Path) -> str:
    h = sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, default=DEFAULT, help='root of Telegram course export')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    roots = [p for p in args.source.iterdir() if p.is_dir()] if args.source.is_dir() else []
    if len(roots) != 1:
        raise SystemExit(f'Expected one extracted course folder under {args.source}; found {len(roots)}')
    source_root = roots[0]
    all_files = sorted(x for x in source_root.rglob('*') if x.is_file())
    if not all_files: raise SystemExit('No source files found')
    counts = Counter(); entries = []; text_docs = 0; pdf_pages = 0; parse_errors = []
    for f in all_files:
        rel = f.relative_to(source_root).as_posix()
        ext = f.suffix.lower() or '[no extension]'
        counts[ext] += 1
        e = {'path': rel, 'bytes': f.stat().st_size, 'sha256': digest(f), 'type': ext}
        if ext == '.htm' or ext == '.html':
            parser = TextAudit()
            try:
                parser.feed(f.read_text(errors='replace'))
                e.update({'title': ' '.join(parser.title)[:300], 'headings': parser.headings[:80], 'topic_signals': topic_signals(' '.join(parser.title + parser.headings)), 'text_chars_excluding_code_and_assets': parser.text_chars, 'review_class': 'lecture text/headings indexed; code blocks/scripts omitted'})
                text_docs += 1
            except Exception as ex: parse_errors.append({'path': rel, 'error': str(ex)})
        elif ext == '.pdf':
            info = subprocess.run(['pdfinfo', str(f)], capture_output=True, text=True)
            pages = re.search(r'^Pages:\s+(\d+)', info.stdout, re.M)
            title = re.search(r'^Title:\s*(.+)', info.stdout, re.M)
            text = subprocess.run(['pdftotext', '-layout', str(f), '-'], capture_output=True)
            if info.returncode or text.returncode:
                parse_errors.append({'path': rel, 'error': (info.stderr + text.stderr.decode(errors='replace'))[:400]})
            else:
                page_count = int(pages.group(1)) if pages else None
                pdf_pages += page_count or 0
                extracted_text = text.stdout.decode(errors='replace')
                extracted = len(extracted_text)
                # Extract likely section-heading lines and a compact topical index; never persist source prose/code.
                heading_candidates = []
                for line in extracted_text.splitlines():
                    line = re.sub(r'\s+', ' ', line).strip()
                    if 4 <= len(line) <= 100 and (re.match(r'^(?:[0-9]+(?:\.[0-9]+)*[.)]?\s+|[A-Z][A-Za-z /&-]{5,})$', line) or line.isupper()):
                        if line not in heading_candidates: heading_candidates.append(line)
                    if len(heading_candidates) >= 35: break
                e.update({'title': title.group(1).strip() if title else f.stem, 'pages': page_count, 'extracted_text_chars': extracted, 'section_heading_candidates': heading_candidates, 'topic_signals': topic_signals(f.stem + ' ' + extracted_text), 'review_class': 'PDF text/heading/topic index; source prose/code not copied into project'})
                text_docs += 1
        elif ext == '.txt':
            prompt = f.read_text(errors='replace')
            e.update({'title': f.stem, 'text_chars': len(prompt), 'topic_signals': topic_signals(f.stem + ' ' + prompt), 'review_class': 'text challenge/prompt topic-indexed; no answers or payloads generated'})
            text_docs += 1
        elif ext in {'.zip', '.7z', '.rar'}:
            e['review_class'] = 'archive fingerprint only; contents not extracted, run or imported'
        elif ext in {'.c', '.h', '.cpp', '.cc', '.sln', '.vcxproj', '.filters', '.user'}:
            e['review_class'] = 'source/project file fingerprint only; operational course code not imported'
        elif ext in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}:
            e['review_class'] = 'visual course asset fingerprint only'
        else:
            e['review_class'] = 'page support/resource fingerprint only'
        entries.append(e)
    result = {'schema': 'windows-ll-course-source-index-v1', 'source_directory': str(source_root), 'method': 'sha256 for every original file; Poppler PDF text extraction and stdlib HTML text/headings extraction; HTML code/pre/script/style/nav/svg omitted; no archive contents extracted; originals untouched', 'file_count': len(entries), 'extension_counts': dict(sorted(counts.items())), 'lecture_and_prompt_text_document_count': text_docs, 'pdf_page_total': pdf_pages, 'parse_errors': parse_errors, 'entries': entries}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('source_directory','file_count','extension_counts','lecture_and_prompt_text_document_count','pdf_page_total','parse_errors')}, indent=2))
    if parse_errors: return 1
    return 0
if __name__ == '__main__': sys.exit(main())
