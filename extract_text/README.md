# Quiz Generator – File Upload & Text Extraction App #
This project alloows users to upload documents (PDF, DOCX, PPTX) and automatically extract text from them. 
the extracted text can then be displayed , edited and used to generate quizzes using AI models.

## Project Setup and Running Instructions

- **Navigate to the project folder**:
  - Open a terminal and go to the `extract-text` folder:
    `cd extract-text`

- **Create a virtual environment**:
  - A virtual environment isolates project dependencies from the system Python, preventing conflicts and ensuring reproducibility (You only need to create the virtual environment once).
    - macOS / Linux: `python -m venv .venv`
    - Windows (cmd): `py -3 -m venv .venv`
    - Windows (PowerShell): `py -3 -m venv .venv`

- **Activate the virtual environment**:
  - Ensures that Python and pip use the environment's isolated packages (Every time you start a new terminal session to work on this project, you need to reactivate the virtual environment).
    - macOS / Linux: `source .venv/bin/activate`
    - Windows (cmd): `.venv\Scripts\activate`
    - Windows (PowerShell): `.venv\Scripts\Activate.ps1`

- **Upgrade pip** (optional):
  - Make sure pip is up to date: `python -m pip install --upgrade pip`

- **Install required libraries**:
  - Install all dependencies from the requirements file: `pip install -r requirements.txt`

- **Run the script**:
  - Execute the Python script to extract PDF and PPTX text: `python -m uvicorn main:app --reload --port 8001`
  - This command works on macOS, Linux, and Windows (cmd or PowerShell) as long as the virtual environment is activated.

- **The expected result**:
  - ![The expected result] 'extracted editable text'.

The Backend/extract_files runs at `http://localhost:8001`
and the docs available at `http://localhost:8001/docs`


### Imports
```python
from fastapi import FastAPI, UploadFile, File
import pypdf
from docx import Document
from pptx import Presentation
from fastapi.middleware.cors import CORSMiddleware
```
FastAPI - main framework to build AP endpoints
UploadFile,File - tell FastAPI to receive file uploads from the frontend
pypdf - Reads PDF files.
pyhton-docx - Reads DOCX files.
python-pptx - Reads PPTX files.
CORSMiddleware - Allows frontend (react) to talk to backend (FastAPI).

### PDF Text Extraction Function
```python
def extract_text_from_pdf(path):
    text = ""
    reader = pypdf.PdfReader(path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text
```
- Loads PDF using pypdf.PdfReader
- Goes through each page
- Extracts text from each page
- Adds to a combined string

### DOCX Text Extraction Function
```python
def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])
```

- Opens Word document
- Reads each paragraph
- Joins all paragraphs with line breaks

### PPTX Text Extraction Function
```python
def extract_text_from_pptx(path):
    presentation = Presentation(path)
    text = ""
    for slide in presentation.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"
    return text
```

- Opens the PowerPoint file
- Loops through slides
- Then through shapes (text boxes, titles)
- If a shape contains text → extract it

## CORS Middleware (Frontend-Backend Connection)
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
Different ports → browser blocks communication by default.
CORS middleware allows them to talk to each other.
"*" = allow everything (easy for development).

### Upload Endpoint
```python
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
```
- Accepts a file from frontend
- Saves it temporarily
- Reads the file based on extension
- Returns extracted text

### Save Uploaded File
```python
filename = f"temp.{file.filename.split('.')[-1]}"
contents = await file.read()

with open(filename, "wb") as f:
    f.write(contents)
```
Takes the the file sent bfrorm Frontend 
Gets the extensions
Saves it locally

### Determine File Type
```python
ext = filename.split(".")[-1]
```

### Choose the correct Extractor 
```python
if ext == "pdf":
    extracted = extract_text_from_pdf(filename)
elif ext == "docx":
    extracted = extract_text_from_docx(filename)
elif ext == "pptx":
    extracted = extract_text_from_pptx(filename)
else:
    return {"error": "Unsupported file type"}
```
- If it's a PDF → send to PDF extractor
- If DOCX → DOCX extractor
- If PPTX → PPTX extractor
- Otherwise → return error

### Return Extracted Text
```python
return {
    "extracted_text": extracted
}
```
This is what the frontend receives and shows to the user.