# Dynamic File Compression Utility

A modern Huffman Coding based File Compression & Decompression System built using FastAPI, SQLite, Bootstrap, and JavaScript.

## Live Demo

🌐 Live Application:
https://dynamic-file-compression-utility.onrender.com/

## GitHub Repository

🔗 Repository:
https://github.com/Vayu-143/dynamic-file-compression-utility

---

## Overview

Dynamic File Compression Utility is a web-based application that allows users to compress and decompress text files efficiently using the Huffman Coding algorithm.

The system provides:

- File Compression
- File Decompression
- Compression Statistics Dashboard
- Compression & Decompression History
- Downloadable Compressed Files
- Metadata Management
- Real-Time Analytics
- Dark Mode User Interface

---

## Features

### Compression

- Upload text files
- Compress using Huffman Coding
- Generate compressed binary files
- Generate metadata files
- Calculate compression ratio
- Track execution time

### Decompression

- Restore original files from compressed binaries
- Use metadata for accurate reconstruction
- Download restored files

### Dashboard

- Total Compressions
- Total Decompressions
- Average Compression Ratio
- Average Execution Time

### History Management

- Compression History
- Decompression History
- Individual Record Deletion
- Clear Entire History

### User Interface

- Fully Responsive Design
- Modern Dark Theme
- Real-Time Dashboard Updates
- Bootstrap 5 Components

---

## Technology Stack

### Backend

- FastAPI
- Python 3
- SQLite

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Algorithm

- Huffman Coding

---

## Project Structure

```text
dynamic-file-compression-utility/
│
├── api/
│   ├── app.py
│   ├── services.py
│   └── schemas.py
│
├── src/
│   ├── huffman.py
│   ├── compressor.py
│   ├── decompressor.py
│   ├── database.py
│   ├── benchmark.py
│   └── analytics.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── app.js
│
├── compressed_files/
├── decompressed_files/
├── outputs/
├── logs/
├── database/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Vayu-143/dynamic-file-compression-utility.git

cd dynamic-file-compression-utility
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Locally

```bash
uvicorn api.app:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

---

## API Endpoints

### Compression

```http
POST /compress
```

### Decompression

```http
POST /decompress
```

### Statistics

```http
GET /statistics
```

### History

```http
GET /history
```

### Dashboard

```http
GET /dashboard
```

### Health Check

```http
GET /health
```

---

## Huffman Coding Workflow

1. Read file content
2. Build frequency table
3. Create Huffman Tree
4. Generate Huffman Codes
5. Encode text
6. Store compressed binary
7. Save metadata
8. Restore using metadata during decompression

---

## Dashboard Metrics

The application tracks:

- Total Compressions
- Total Decompressions
- Compression Ratio
- Execution Time
- File History
- Analytics Data

---

## Deployment

Hosted on Render:

https://dynamic-file-compression-utility.onrender.com/

---

## Future Enhancements

- User Authentication
- Drag & Drop Upload
- Compression Charts
- PDF Compression Support
- ZIP File Support
- PostgreSQL Integration
- Cloud Storage Support
- Docker Deployment

---

## Author

### Vayunandan Mishra

ECE Student

GitHub:
https://github.com/Vayu-143

---

## License

This project is developed for educational and learning purposes.

© 2026 Vayunandan Mishra. All Rights Reserved.