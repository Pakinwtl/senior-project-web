from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.services.model_detector import ModelTrendDetector
from app.services.algorithm_detector import AlgorithmsTrendDetector
import tempfile
import uvicorn
import os
import shutil

app = FastAPI()

# Instantiate detectors
model_detector = ModelTrendDetector()
algorithm_detector = AlgorithmsTrendDetector()

# Allow frontend access
origins = [
    "https://senior-project-website.onrender.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Trend Detection API is running"}

@app.post("/detect-trend/")
async def detect_trend(
    file: UploadFile = File(...),
    use_model: str = Form(...)
):
    # Validate use_model
    if use_model not in ["model", "algorithm"]:
        raise HTTPException(status_code=400, detail="Invalid method. Please select 'model' or 'algorithm'.")


    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

    try:
        if use_model == "model":
            results = model_detector.detect(temp_file_path)
        if use_model == "algorithm":
            results = algorithm_detector.detect(temp_file_path)

        return JSONResponse(content={
            "success": True,
            "results": results
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    finally:
        os.remove(temp_file_path)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
