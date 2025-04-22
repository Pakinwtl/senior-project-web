from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.services.model_detector import ModelTrendDetector
from app.services.algorithm_detector import AlgorithmsTrendDetector 
from pydantic import BaseModel
import tempfile
import uvicorn
import os
import shutil

app = FastAPI()

AlgorithmsTrendDetector = AlgorithmsTrendDetector()

origin = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/detect-trend/")
async def detect_trend(file: UploadFile = File(...), use_model: bool = Form(False)):

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

    try:
        if use_model:
            results = ModelTrendDetector.detect(temp_file_path)
        else:
            results = AlgorithmsTrendDetector.detect(temp_file_path)

        valid_results = [result for result in results if result["predicted_label"] == 1]

        return JSONResponse(content={
            "success": True,
            "results": valid_results
        })
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    finally:
        os.remove(temp_file_path)  # Clean up temp file


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1 ", port=8000, reload=True)

