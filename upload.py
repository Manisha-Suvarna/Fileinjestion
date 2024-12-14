from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import io

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "PDF Text Extraction API"}

@app.post("/file/extract_text")
async def extract_pdf_text(file: UploadFile):
    
    pdf_data = await file.read()

    try:
        
        pdf_file = io.BytesIO(pdf_data)
        doc = fitz.open(pdf_file)

        
        if doc.page_count == 0:
            raise HTTPException(status_code=400, detail="The PDF has no pages")

        
        extracted_text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)  
            extracted_text += page.get_text()

    
        if extracted_text.strip() == "":
            return JSONResponse(status_code=200, content={"message": "No text found in PDF"})
        
        return {"filename": file.filename, "extracted_text": extracted_text}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid PDF file or extraction error")
