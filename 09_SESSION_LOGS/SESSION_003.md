# Session 003 — user-supplied course alignment

The user asked to use `/home/hammerspacecraft/Downloads/Telegram Desktop/Maldev-Academy-Malware-Development` as course knowledge and a basis for the system. Inspected the export tree and enumerated its contents before modifying the project.

Indexed 2,350 source files: 92 PDF lecture documents (788 pages), 92 HTML lecture/index pages, 21 text challenge prompts, 187 ZIP archives, 25 standalone code/project files and 1,933 page/media resources. PDFs were text-extracted with Poppler; HTML headings/text were parsed while excluding code/pre/script/style/navigation/SVG. All entries have path, byte size and SHA-256. The document-level index includes headings/topic signals and extraction lengths. No original was changed. Archives and code are fingerprinted but not extracted, built, run or imported.

Added a per-course-module map for modules 1–91, topic-level summaries, explicit links to existing safe capabilities, and research-only boundaries. Updated requirements, architecture alignment, README, knowledge references and status records. The supplied course informs the research harness's defensive framing, PE/process/parser priorities, inert-artifact constraint, visible imports and provenance discussion. Its operational injection, spoofing, import-hiding, syscall-bypass, unhooking and anti-analysis examples remain excluded.

Verification: 2,350 files indexed, 205 text documents processed, 788 PDF pages extracted, zero parser errors. The indexer is reusable and reads originals without modifying them. No executable project source changed in this session; Windows build/test status is unchanged.

The catalog stores extracted text lengths, HTML headings, PDF heading candidates and nine broad topic signals for discovery. It does not store original lecture prose or code samples.
