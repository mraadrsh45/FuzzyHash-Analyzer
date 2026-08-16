# FuzzyHash Analyzer

**A Python-Based Fuzzy Hashing System for File Similarity Analysis in Cyber Forensics and Malware Investigation**

---

## 📌 Project Overview

**FuzzyHash Analyzer** is a cybersecurity and digital forensics workstation designed for incident responders, forensic investigators, and malware analysts. It provides an automated pipeline to compare suspect files, calculate cryptographic integrity digests (MD5, SHA-256), extract file headers and Portable Executable (PE) metadata, compute Locality Sensitive and Context-Triggered Piecewise fuzzy hashes (ssdeep & TLSH), determine file similarity percentages, manage forensic case records, and generate PDF forensic reports.

Unlike traditional cryptographic hashes where a single-byte variation causes total avalanche divergence (0% match), fuzzy hashing enables investigators to discover code reuse, compiler variations, patched binaries, and malware family variants.

> **CRITICAL METHODOLOGICAL PRINCIPLE:**
> File similarity is an investigative indicator of code or structural relationship and **DOES NOT** independently prove that a file is malicious. The platform classifies similarity as:
> * **0% – 30%**: Low Similarity
> * **31% – 70%**: Moderate Similarity
> * **71% – 100%**: High Similarity
>
> Malware classification requires multi-layered forensic investigation including static disassembling, dynamic sandboxing, YARA signatures, and threat intelligence.

---

## 🎯 Objectives

1. **Deterministic Cryptographic Verification**: Generate MD5 and SHA-256 digests for baseline forensic evidence integrity.
2. **Fuzzy Hashing Engine**: Implement dual fuzzy algorithms (ssdeep / CTPH and TLSH) to evaluate byte-sequence similarity.
3. **Safe Artifact Handling**: Enforce strict non-execution policies, MIME type validation, file size limits, and traversal protection.
4. **Forensic Case Management**: Maintain a structured relational evidence hierarchy: `User → Case → Evidence → Analysis → Report`.
5. **Automated Forensic Reporting**: Generate ReportLab PDF reports containing hash comparisons, analyst notes, and investigative guidelines.
6. **Educational Learning Center**: Explain cryptographic vs. fuzzy hashing concepts, advantages, limitations, false positives, and false negatives.

---

## 🏗️ System Architecture

```
FuzzyHash-Analyzer/
├── app.py                      # Flask Application Entrypoint & Factory
├── config.py                   # Central Application Configuration
├── requirements.txt            # Python Dependencies
├── README.md                   # Technical & Academic Documentation
├── database/                   # SQLite Persistent Storage
│   └── fuzzyhash.db
├── models/                     # SQLAlchemy Relational Models
│   ├── __init__.py
│   ├── user.py                 # Investigator / Admin User Model
│   ├── case.py                 # Forensic Case Model
│   ├── evidence.py             # Evidence Artifact Model
│   └── analysis.py             # Analysis Result & Score Model
├── services/                   # Modular Forensics Services
│   ├── __init__.py
│   ├── hash_service.py         # Cryptographic Hashes (MD5, SHA-256)
│   ├── fuzzy_hash_service.py   # ssdeep (CTPH) & PureTLSH Engines
│   ├── similarity_service.py   # Score Evaluation & Classification
│   ├── metadata_service.py     # MIME & PE Header/Entropy Analysis
│   ├── file_validation_service.py # Security & Size Validation
│   ├── report_service.py       # ReportLab PDF Report Generator
│   └── case_service.py         # Case Code Generator & Demo Seeder
├── routes/                     # Blueprint Route Controllers
│   ├── __init__.py
│   ├── auth.py                 # Authentication & Session Handlers
│   ├── dashboard.py            # SOC Dashboard & Metrics API
│   ├── cases.py                # Forensic Case Management
│   ├── analysis.py             # File Upload & Analysis Pipeline
│   ├── history.py              # Searchable Analysis History
│   ├── evidence.py             # Evidence Repository
│   ├── reports.py              # PDF Generation & Web Reports
│   ├── learning.py             # Educational Knowledge Base
│   └── settings.py             # System Maintenance & Cache Purge
├── templates/                  # Jinja2 HTML5 Templates
│   ├── base.html               # Persistent SOC Sidebar & Layout
│   ├── login.html              # Investigator Authentication
│   ├── dashboard.html          # Metric Cards & Chart.js Visuals
│   ├── cases.html              # Case Explorer
│   ├── case_detail.html        # Detailed Case View
│   ├── create_case.html        # Case Creation Modal
│   ├── analysis.html           # 2-File Upload & Stage Progress
│   ├── results.html            # Similarity Gauge & Findings
│   ├── history.html            # Searchable Audit Table
│   ├── evidence.html           # Evidence Artifact Explorer
│   ├── reports.html            # Report Directory
│   ├── report.html             # Web-Based Forensic Report
│   ├── learning.html           # Theory & Reference Guide
│   ├── settings.html           # Storage Purge & Reseed Console
│   └── errors/                 # Custom 404 & 500 Error Handlers
│       ├── 404.html
│       └── 500.html
├── static/                     # Static Frontend Assets
│   ├── css/
│   │   ├── style.css           # SOC Dark Forensics Theme
│   │   └── dashboard.css       # Chart Layouts & Case Cards
│   ├── js/
│   │   ├── main.js             # Global Handlers & Flash Auto-dismiss
│   │   ├── analysis.js         # Drag-and-Drop & Progress Stepper
│   │   ├── charts.js           # Chart.js Integration
│   │   └── reports.js          # Print & PDF Download Utilities
│   └── images/
│       └── logo.svg            # Platform Vector Logo
├── uploads/                    # Temporary Staging Storage
├── reports/generated/          # Output PDF Forensic Reports
└── tests/                      # Pytest Automated Test Suite
    ├── test_hash.py            # Cryptographic Hash Tests
    ├── test_fuzzy_hash.py      # ssdeep & TLSH Algorithm Tests
    ├── test_similarity.py      # Threshold & Scoring Tests
    └── test_validation.py      # Security & Validation Tests
```

---

## ⚙️ Technology Stack

* **Backend Language**: Python 3.12+
* **Web Framework**: Flask 3.0+ (Jinja2 Template Engine)
* **Database & ORM**: SQLite 3 / Flask-SQLAlchemy
* **Frontend**: HTML5, Vanilla CSS3 (Custom SOC Dark Theme), Vanilla JavaScript
* **Data Visualization**: Chart.js 4.4+ (Doughnut distribution & Activity line chart)
* **Cryptographic Hashing**: Standard Python `hashlib` (MD5, SHA-256)
* **Fuzzy Hashing**: `ppdeep` (ssdeep/CTPH implementation) & `PureTLSH` (Locality Sensitive Hashing)
* **Executable Inspection**: `pefile` (Architecture, ImageBase, Entrypoint, Section Entropy)
* **PDF Report Engine**: ReportLab 4.0+
* **Test Framework**: Pytest 8.0+

---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure Python 3.12+ is installed on your system.

### 2. Clone or Navigate to the Project
```bash
cd "c:\Users\luxma\Desktop\fuzzy logic"
```

### 3. Create a Python Virtual Environment
```bash
# Create standard virtual environment
python -m venv venv
```

### 4. Activate the Virtual Environment
* **Windows (Command Prompt / PowerShell):**
  ```powershell
  .\venv\Scripts\activate
  ```
* **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```

### 5. Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## 🖥️ Running the Application

Start the local Flask development server:
```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### Default Login Credentials
* **Username**: `admin`
* **Password**: `admin123`

---

## 🧪 Running Automated Tests

Run the complete test suite with verbose output using Pytest:
```bash
pytest -v
```

---

## 🔬 Forensic Methodology: Fuzzy Hashing Explained

### 1. Limitations of Cryptographic Hashes (MD5 / SHA-256)
Cryptographic hashes utilize the **avalanche effect**: changing a single bit in a 100MB file completely randomizes the output digest. While indispensable for verifying file integrity and detecting unauthorized tampering, cryptographic hashes cannot evaluate similarity or detect variant malware that has been recompiled or lightly obfuscated.

### 2. Context-Triggered Piecewise Hashing (ssdeep / CTPH)
ssdeep divides a file into dynamic blocks using a **rolling hash** (7-byte sliding window). When the rolling checksum matches a trigger value, a block boundary is established, and a traditional FNV hash is calculated for that segment. The resulting strings are compared using Levenshtein distance to calculate a similarity score from 0 to 100.

### 3. Locality Sensitive Hashing (TLSH)
TLSH processes byte sequences by computing **byte-pair tri-gram frequency distributions** across 256 buckets and extracting quartile statistical checkpoints. It produces a hex digest that measures edit distance (where 0 indicates identical files and distance increases as differences grow).

---

## 🔒 Security & Privacy Controls

* **Zero Execution Guarantee**: Uploaded files are strictly treated as read-only byte streams. No files are executed, evaluated in a shell, or passed to subprocesses.
* **100% Offline Processing**: All processing occurs within the local Python runtime. No hashes, metadata, or file streams are submitted to external cloud services or public threat feeds.
* **Strict MIME & Extension Whitelisting**: Files are validated before analysis against authorized forensic formats and file size limits.
* **Safe Temporary Storage**: Uploads are staged with randomized UUID identifiers in isolated directories and can be purged at any time from the Settings menu.

---

## 🎓 Viva / Academic Demonstration Workflow

1. **Authentication**: Log in with `admin` / `admin123`.
2. **Dashboard Review**: Inspect the metric cards, similarity distribution doughnut chart, and activity timeline.
3. **Case Creation**: Navigate to **Cases → New Case** (e.g., *Case Incident 2026-Alpha*).
4. **Run Analysis**: Navigate to **New Analysis**, select the case, and choose two sample artifacts (e.g., text or log files).
5. **Review Pipeline**: Observe the automated pipeline (Validation → Metadata → SHA-256 → Fuzzy Hashing → Similarity Evaluation).
6. **Inspect Results**: View the circular similarity gauge, MD5/SHA-256 comparisons, ssdeep/TLSH breakdown, and PE section entropy details.
7. **Download PDF Report**: Click **Download PDF Report** to view the formatted forensic document generated via ReportLab.
8. **Audit Trail**: Search and filter past analyses in **History** and examine stored artifacts under **Evidence**.
9. **Educational Reference**: Open **Learning** to demonstrate theoretical knowledge of CTPH and locality sensitivity.

---

## 📄 License & Academic Disclaimer
Developed as a specialized Digital Forensics and Cybersecurity research platform.
Similarity scores represent structural proximity and must always be supplemented with static disassembly, dynamic sandboxing, and behavioral threat analysis.
