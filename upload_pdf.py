from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import io

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "PDF Text Extraction and Chunking API"}

def chunk_text(text: str, chunk_size: int = 1000, overlap_size: int = 100):
    """
    Function to chunk text into smaller, overlapping chunks.
    
    Parameters:
        text (str): The input text to be chunked.
        chunk_size (int): The maximum size of each chunk.
        overlap_size (int): The number of characters to overlap between chunks.
        
    Returns:
        List of text chunks with overlaps.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if len(chunk) < chunk_size:
            chunks.append(chunk)
            break
        chunks.append(chunk)
        start = end - overlap_size  
    return chunks

@app.post("/file/extract_and_chunk_text")
async def extract_and_chunk_pdf_text(file: UploadFile, chunk_size: int = 1000, overlap_size: int = 100):
    
    pdf_data = await file.read()

    
    try:
    
        pdf_file = io.BytesIO(pdf_data)
        doc = fitz.open(pdf_file)

        
        if doc.page_count == 0:
            raise HTTPException(status_code=400, detail="The PDF has no pages")

        
        extracted_text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)  # Get each page
            extracted_text += page.get_text()

        
        if extracted_text.strip() == "":
            return JSONResponse(status_code=200, content={"message": "No text found in PDF"})

    
        chunks = chunk_text(extracted_text, chunk_size, overlap_size)

        
        return {"filename": file.filename, "chunks": chunks}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid PDF file or extraction error")

