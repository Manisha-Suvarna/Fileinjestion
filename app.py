from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import io

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "PDF Ingestion API"}

@app.post("/file/upload")
async def upload_pdf(file: UploadFile):
    # Read the file into memory
    pdf_data = await file.read()
    
    # Try to open the file using PyMuPDF
    try:
        # Load the PDF in memory
        pdf_file = io.BytesIO(pdf_data)
        doc = fitz.open(pdf_file)

        # Validate PDF: Check number of pages
        if doc.page_count == 0:
            raise HTTPException(status_code=400, detail="The PDF has no pages")
        
        return {
            "filename": file.filename,
            "page_count": doc.page_count,
            "message": "PDF uploaded and validated successfully"
        }


    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid PDF file")

if _name_ == '_main_':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)