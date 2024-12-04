from fastapi import APIRouter, File, UploadFile, HTTPException
from services.db_service import create_db_from_file
from config.settings import settings
from models.chat import UploadResponse
import os

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    try:
        # Ensure directory exists
        os.makedirs(settings.docs_dir, exist_ok=True)
        file_path = os.path.join(settings.docs_dir, file.filename)
        
        # Save file
        contents = await file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        # Create database
        if create_db_from_file(file_path):
            return UploadResponse(
                status="success",
                message="File uploaded and processed successfully",
                file_name=file.filename
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to process the file"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}")
