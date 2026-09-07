# SIH26227 — Offline Satellite Intelligence & Change-Analysis Platform

An offline-first platform where an analyst can search satellite imagery in natural
language, find visually similar locations, detect meaningful changes between dates,
and suppress false alarms caused by clouds, seasons, and lighting.

## Project structure

```
sih26227-satellite-intel/
├── README.md                  <- you are here
├── PROJECT_PLAN.md            <- team roles + day-by-day timeline to Sept 20
├── ARCHITECTURE.md            <- tech stack, data flow, design rationale
├── docs/
│   ├── DATA_SOURCES.md        <- Sentinel-2/1, Landsat, Bhuvan access notes
│   └── EVALUATION_CHECKLIST.md<- maps directly to what SIH judges will ask for
├── backend/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── app/
│       ├── main.py            <- FastAPI entrypoint
│       ├── core/config.py     <- settings (paths, model names, index paths)
│       ├── models/schemas.py  <- request/response Pydantic models
│       ├── api/
│       │   ├── search.py            <- POST /search/text
│       │   ├── image_search.py      <- POST /search/image
│       │   ├── change_detection.py  <- POST /change-detection
│       │   └── clustering.py        <- POST /discover/similar-sites
│       └── services/
│           ├── embedding_service.py       <- text/image embedding model
│           ├── vector_store.py            <- FAISS index wrapper
│           └── change_detection_service.py<- registration, masking, diffing
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── components/SearchBar.jsx
│       └── pages/Dashboard.jsx
├── docker-compose.yml
└── .gitignore
```

## Quick start (once dependencies are staged locally — see ARCHITECTURE.md)

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Or with Docker: `docker-compose up --build`

## What's real here vs. what's a stub
Every backend module is a **working skeleton**: correct request/response contracts,
correct file layout, correct imports — but the actual model-loading and inference
logic has `# TODO` markers where your team plugs in the real embedding model, FAISS
index, and change-detection pipeline. This is intentional: it lets 3-4 people work
in parallel on separate files without merge conflicts from day one.

You are a senior desktop software architect, Python developer, UI/UX designer, NLP engineer, and plagiarism-detection systems engineer.

I want you to build a COMPLETE, PROFESSIONAL, PRODUCTION-READY Windows desktop application for checking plagiarism in research papers.

The application should be delivered as a Windows executable (.EXE) that can be installed and used by a normal user without requiring Python, Node.js, or any development environment.

PROJECT NAME:
ResearchGuard – Research Paper Plagiarism Checker

PRIMARY OBJECTIVE:
Create a professional desktop application that allows students, researchers, professors, and academic institutions to upload research papers and analyze them for potential plagiarism, textual similarity, duplicate content, citation issues, and AI-generated/reused content indicators.

IMPORTANT:
This application must NOT falsely claim that it can determine plagiarism with 100% certainty. The software should report "similarity" and "potential plagiarism indicators" based on available sources and algorithms. Clearly explain that the final plagiarism determination requires human/academic review.

==================================================
1. PLATFORM
==================================================

Target platform:
- Windows 10
- Windows 11
- 64-bit

Final output:
- ResearchGuard.exe
- Optional installer: ResearchGuard_Setup.exe

The application must run without requiring:
- Python
- Node.js
- Git
- VS Code
- Any command-line setup

Use a technology stack that can reliably generate a Windows EXE.

PREFERRED STACK:
- Python 3.12+
- PySide6 for the desktop GUI
- SQLite for local database
- SQLAlchemy for database abstraction
- PyMuPDF for PDF extraction
- python-docx for DOCX extraction
- python-pptx if presentation support is useful
- scikit-learn for TF-IDF similarity
- RapidFuzz for fuzzy matching
- sentence-transformers for semantic similarity
- NLTK or spaCy for NLP preprocessing
- ReportLab or HTML-to-PDF for report generation
- PyInstaller for EXE packaging

If a better technology choice is available, explain why before changing the architecture.

==================================================
2. APPLICATION DESIGN
==================================================

Create a modern professional academic/research interface.

Design inspiration:
- Grammarly
- Turnitin-style academic analysis interfaces
- Microsoft Word
- Modern cybersecurity dashboards
- Professional research software

Do NOT copy copyrighted UI designs.

Use:
- Clean layout
- Modern cards
- Professional typography
- Consistent spacing
- Light and dark mode
- Blue/indigo professional accent
- Responsive desktop layout
- Sidebar navigation
- Clear status indicators
- Progress bars
- Charts
- Tables
- Tooltips
- Icons

Main application layout:

LEFT SIDEBAR:

1. Dashboard
2. New Check
3. Documents
4. Results
5. Reports
6. Settings
7. Help / About

TOP BAR:
- Application name/logo
- Search
- Theme toggle
- Notifications/status
- Settings
- User/profile area

==================================================
3. DASHBOARD
==================================================

Create an attractive dashboard.

Display:

- Total Documents Checked
- Total Checks
- Average Similarity
- Highest Similarity
- Documents With High Similarity
- Recent Checks
- Last Analysis
- System Status

Charts:

1. Similarity Distribution
2. Checks Over Time
3. Source Categories
4. Risk Distribution

Risk levels:

0–10%:
Very Low

10–25%:
Low

25–40%:
Moderate

40–60%:
High

60%+:
Very High

IMPORTANT:
These thresholds must be configurable and should be described as application heuristics, not universal academic standards.

==================================================
4. NEW PLAGIARISM CHECK
==================================================

Create a dedicated document analysis screen.

Allow users to:

- Drag and drop files
- Browse files
- Paste text manually
- Select multiple documents
- Select comparison mode
- Select language
- Configure analysis depth

SUPPORTED FILE FORMATS:

- PDF
- DOCX
- TXT
- RTF if practical

Maximum file size should be configurable.

Show selected files in a queue:

Filename
Size
Pages
Word Count
Status
Remove button

Buttons:

[Analyze Document]
[Cancel]
[Clear]

==================================================
5. DOCUMENT TEXT EXTRACTION
==================================================

Implement reliable text extraction.

PDF:
- Extract text page-by-page
- Preserve page numbers
- Preserve paragraph boundaries where possible

DOCX:
- Extract paragraphs
- Extract headings
- Extract tables where possible
- Preserve document structure

TXT:
- Direct text reading

Detect:
- Empty documents
- Scanned PDFs
- Image-only PDFs

If the PDF is scanned/image-based:
- Show message:
  "This document appears to contain scanned pages. OCR is required for reliable analysis."

Optionally implement OCR using Tesseract.

OCR should be optional because it increases application size.

==================================================
6. TEXT PREPROCESSING
==================================================

Before similarity analysis:

- Normalize Unicode
- Convert quotation marks consistently
- Remove unnecessary whitespace
- Normalize punctuation
- Detect language
- Split into paragraphs
- Split into sentences
- Tokenize
- Remove irrelevant formatting
- Preserve original text for highlighting

Do NOT destroy the original document.

Maintain two versions:

1. Original text
2. Normalized analysis text

==================================================
7. PLAGIARISM DETECTION ENGINE
==================================================

Implement MULTIPLE similarity methods.

Do NOT rely on only one algorithm.

A. EXACT MATCHING

Find:
- Identical sentences
- Identical phrases
- Repeated paragraphs

Use:
- Hashing
- n-grams
- sentence comparison

Example:

Document:
"Artificial intelligence is transforming modern education."

Source:
"Artificial intelligence is transforming modern education."

Mark as:
Exact Match

--------------------------------------------------

B. FUZZY MATCHING

Detect small modifications.

Example:

Original:
"Artificial intelligence is transforming modern education."

Modified:
"AI is rapidly transforming the modern education system."

Use:
- RapidFuzz
- Levenshtein similarity
- Token similarity

Show:
Similarity Score
Matched text
Source text

--------------------------------------------------

C. N-GRAM SIMILARITY

Use configurable n-gram sizes:

- 3-gram
- 5-gram
- 7-gram

Calculate overlap between document sections and comparison sources.

--------------------------------------------------

D. TF-IDF SIMILARITY

Use cosine similarity.

Calculate:

similarity = cosine_similarity(document_vector, source_vector)

Display similarity percentage.

--------------------------------------------------

E. SEMANTIC SIMILARITY

Use sentence-transformers.

Recommended model:

all-MiniLM-L6-v2

Generate embeddings for sentences/paragraphs.

Compare using cosine similarity.

This should detect paraphrased content where the wording is different but the meaning is similar.

IMPORTANT:
Semantic similarity is NOT proof of plagiarism.

Label it:

"Semantic Similarity Indicator"

--------------------------------------------------
8. SOURCE COMPARISON
==================================================

The application should support:

A. User-provided comparison documents

Allow users to create a local source library.

Example:

Sources/
  book1.pdf
  paper1.pdf
  paper2.docx
  thesis.pdf

Compare the submitted paper against the local source library.

B. Previously analyzed documents

Detect similarity against documents previously analyzed by the application.

C. Optional Web Search

If internet access is available, provide an optional "Web Search" mode.

IMPORTANT:
Do NOT scrape websites illegally or bypass CAPTCHAs, paywalls, authentication, robots restrictions, or access controls.

Use legitimate/public search APIs or permitted search services.

Make web search modular.

The application must still work OFFLINE using local sources.

==================================================
9. LOCAL SOURCE DATABASE
==================================================

Create SQLite database.

Tables:

documents
- id
- filename
- filepath
- hash
- upload_date
- word_count
- page_count
- language

sources
- id
- title
- author
- publication_year
- url
- source_type

matches
- id
- document_id
- source_id
- sentence
- matched_text
- similarity_score
- algorithm
- page_number

reports
- id
- document_id
- report_path
- created_at

settings
- key
- value

==================================================
10. HASH-BASED DUPLICATE DETECTION
==================================================

Generate:

- SHA-256 document hash
- Text hash
- Paragraph hash

Detect exact duplicate documents.

Display:

"Exact duplicate detected."

==================================================
11. RESEARCH PAPER STRUCTURE ANALYSIS
==================================================

Detect common research-paper sections:

- Title
- Abstract
- Keywords
- Introduction
- Literature Review
- Methodology
- Results
- Discussion
- Conclusion
- References

Show a structure panel.

Example:

✓ Abstract detected
✓ Introduction detected
✓ Methodology detected
⚠ Literature Review not clearly detected
✓ Conclusion detected
✓ References detected

Do NOT require these sections because research papers vary.

==================================================
12. CITATION ANALYSIS
==================================================

Attempt to identify:

- In-text citations
- DOI patterns
- URLs
- References
- Author-year citations
- Numbered citations

Examples:

(Smith, 2024)

[12]

Smith et al. (2023)

10.1000/example.doi

Show:

Citation Count
Reference Count
Uncited-looking claims
Potential citation inconsistencies

IMPORTANT:
This is only an indicator and must not claim that a citation is academically invalid with certainty.

==================================================
13. QUOTATION DETECTION
==================================================

Detect text inside:

"double quotes"

'quotes'

Block quotes

Potentially quoted sections.

If matched content is quoted and accompanied by a citation, classify separately:

"Quoted / Cited Content"

rather than automatically counting it as plagiarism.

==================================================
14. RESULTS PAGE
==================================================

After analysis, display a professional results dashboard.

Top section:

PLAGIARISM / SIMILARITY SUMMARY

Overall Similarity:
37%

Risk:
MODERATE

Matched Sources:
8

Exact Matches:
12

Fuzzy Matches:
23

Semantic Matches:
16

Potentially Quoted:
5

Then show:

Similarity meter / gauge.

Use professional visual indicators.

==================================================
15. MATCH DETAILS
==================================================

Create a detailed match viewer.

LEFT:
Original research paper

RIGHT:
Matched source

Highlight matching sections.

Colors:

- Exact match
- Fuzzy match
- Semantic match
- Quoted content

Allow:

- Next Match
- Previous Match
- Ignore Match
- Add Source
- Open Source
- Copy Match

Each match should show:

Match ID
Similarity %
Detection Method
Page
Sentence/paragraph
Source information

Example:

MATCH #12

Similarity: 94%

Method:
Exact + Fuzzy

Document:
research_paper.pdf

Page:
7

Matched Content:
"..."

Source:
Example Research Paper

==================================================
16. INTERACTIVE TEXT HIGHLIGHTING
==================================================

Display the original document with highlighted matches.

Clicking highlighted text should open a side panel:

Source
Similarity
Algorithm
Confidence/indicator
Matched content
Reference

Allow users to filter:

[All]
[Exact]
[Fuzzy]
[Semantic]
[Quoted]
[Ignored]

==================================================
17. OVERALL SCORE CALCULATION
==================================================

Do NOT simply average all algorithm scores.

Create a transparent scoring model.

For example:

Exact overlap = high weight
Fuzzy overlap = medium-high weight
Semantic overlap = medium weight
Quoted/cited content = excluded or separately reported
References = excluded
Common phrases = low weight

Create a configurable scoring engine.

Show users how the score was calculated.

Example:

Overall Similarity:
34.7%

Breakdown:

Exact matching:
12.4%

Fuzzy matching:
8.7%

Semantic similarity:
13.6%

Do not imply that these percentages can simply be added to produce the overall score unless the algorithm is explicitly designed that way.

==================================================
18. COMMON PHRASES
==================================================

Avoid false positives from common academic phrases.

Examples:

"the results of this study indicate"

"this study aims to"

"in conclusion"

"according to the results"

"the purpose of this research"

Allow configurable common phrase filtering.

==================================================
19. REFERENCES HANDLING
==================================================

References/Bibliography should not be treated the same way as the main body.

Automatically detect the references section.

Option:

[✓] Exclude References From Similarity Score

Default:
Enabled

Also provide:

[✓] Exclude quotations
[✓] Exclude citations
[✓] Ignore common phrases

==================================================
20. AI-GENERATED CONTENT INDICATOR
==================================================

OPTIONAL MODULE.

If implemented, DO NOT claim:

"This text was definitely written by AI."

Instead report:

"AI-writing likelihood indicator"

Use linguistic features such as:

- Sentence-length variation
- Repetition
- Burstiness
- Vocabulary distribution
- Stylometric patterns

Show:

AI-like writing indicators:
Low / Medium / High

Include a warning:

"AI-generated text detection is probabilistic and can produce false positives. It should not be used as definitive evidence."

==================================================
21. REPORT GENERATION
==================================================

Generate professional reports.

Formats:

- PDF
- HTML
- JSON
- CSV

PDF report should include:

Cover Page

ResearchGuard
Plagiarism & Similarity Analysis Report

Document:
filename

Date:
analysis date

Overall Similarity:
XX%

Risk Level:
XX

--------------------------------

Executive Summary

--------------------------------

Similarity Breakdown

--------------------------------

Detected Matches

--------------------------------

Source List

--------------------------------

Page-by-page Analysis

--------------------------------

Citation Analysis

--------------------------------

Quotation Analysis

--------------------------------

Methodology

--------------------------------

Disclaimer

"Similarity scores are automated indicators and do not constitute a final academic plagiarism determination."

Include:
- University/institution field
- Student/researcher name
- Roll number/ID
- Department
- Course
- Guide/Supervisor
- Paper title

Allow these fields to be configured.

==================================================
22. REPORT VISUALIZATION
==================================================

Include charts:

- Overall similarity gauge
- Similarity by page
- Similarity by section
- Match type distribution
- Top sources

Use professional charts.

==================================================
23. DOCUMENT HISTORY
==================================================

Create a Documents page.

Columns:

Document
Date
Word Count
Similarity
Risk
Sources
Status

Actions:

View
Analyze Again
Generate Report
Delete
Open Folder

Add search and filters.

==================================================
24. SOURCE LIBRARY
==================================================

Create a Source Library.

Users can add:

- PDF
- DOCX
- TXT
- URL
- Manual source information

Source fields:

Title
Author
Year
Publisher
DOI
URL
Source Type

Source types:

Journal
Conference
Book
Thesis
Website
Internal Document
Other

==================================================
25. SETTINGS
==================================================

Create a comprehensive settings page.

Sections:

GENERAL

- Application name
- Default folder
- Auto-save
- Confirm deletion

ANALYSIS

- Exact matching sensitivity
- Fuzzy threshold
- Semantic threshold
- N-gram size
- Minimum match length
- Common phrase filtering

DOCUMENTS

- Maximum file size
- OCR enabled
- Extract tables
- Exclude references

REPORTS

- Default report format
- Institution name
- Researcher name
- Department
- Logo

WEB

- Enable web search
- Search provider
- API key
- Request limits

PRIVACY

- Local-only mode
- Delete source documents after analysis
- Database location

==================================================
26. PRIVACY
==================================================

Privacy is extremely important.

Default behavior:

- Documents remain on the user's computer.
- Do not upload documents to external servers unless the user explicitly enables web/API functionality.
- Clearly warn users before sending document text to external services.
- Provide "Offline Mode".

Add:

OFFLINE MODE:
"Your documents never leave this computer."

ONLINE MODE:
"Selected text may be sent to configured search/API services."

Never transmit the entire document unnecessarily.

==================================================
27. SECURITY
==================================================

Implement:

- Input validation
- Safe file handling
- Path traversal protection
- File size limits
- Secure temporary directories
- SHA-256 hashes
- No arbitrary code execution
- No shell execution from document content
- Safe HTML rendering
- Sanitize extracted content

API keys should NOT be hardcoded.

Store sensitive settings securely where possible.

==================================================
28. PERFORMANCE
==================================================

The application must remain responsive.

Use:

- Background worker threads
- QThread / QRunnable
- Progress signals
- Cancelable jobs

Never freeze the UI while processing a large PDF.

Show:

Extracting text...
Preprocessing...
Building comparison index...
Running exact matching...
Running fuzzy matching...
Running semantic analysis...
Generating results...

Progress:
0–100%

==================================================
29. ERROR HANDLING
==================================================

Handle:

- Corrupt PDF
- Password-protected PDF
- Empty document
- Unsupported format
- Missing OCR
- Insufficient memory
- Model download failure
- Internet unavailable
- API failure
- Database error
- Permission error

Show friendly messages.

Never expose raw stack traces to normal users.

Create logs for debugging.

==================================================
30. LOGGING
==================================================

Create:

logs/researchguard.log

Log:

- Application startup
- Document processing
- Errors
- Analysis duration
- Database errors
- API failures

Do not log sensitive document content.

==================================================
31. OFFLINE NLP MODEL
==================================================

If using sentence-transformers:

Download/install the model separately during setup or package it if practical.

Preferred:

all-MiniLM-L6-v2

The application should clearly show:

NLP Model:
Loaded ✓

If model unavailable:

"Semantic analysis is currently unavailable. Exact and fuzzy matching are still available."

Do not crash.

==================================================
32. MULTI-LANGUAGE SUPPORT
==================================================

Initially support:

English
Hindi
Marathi

Design architecture so additional languages can be added later.

Language detection should be automatic when possible.

Do not assume English-only punctuation or tokenization.

=====================
