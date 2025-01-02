from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils.metadata_extraction import extract_metadata
from utils.ela_analysis import error_level_analysis
from utils.video_analysis import analyze_video
import shutil
import os

app = FastAPI()

# CORS Middleware to allow the frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads/"
TEMP_DIR = "temp/"

# Ensure the necessary directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Function to save the uploaded file to disk (for example purposes)
def save_file(file: UploadFile, destination: str):
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

# Backend should return results in JSON format
@app.post("/analyze/image/")
async def analyze_image(file: UploadFile = File(...)):
    file_location = f"temp/{file.filename}"
    save_file(file, file_location)

    # Perform image analysis
    metadata = extract_metadata(file_location)
    ela_result = error_level_analysis(file_location)

    return JSONResponse({"metadata": metadata, "ela_result": ela_result})

@app.post("/analyze/video/")
async def analyze_video_file(file: UploadFile = File(...)):
    # Save the video to a temporary file
    file_location = os.path.join(TEMP_DIR, file.filename)
    save_file(file, file_location)
    
    # Video Analysis
    video_result = analyze_video(file_location)

    return JSONResponse(video_result)

# Ensure the temp folder exists
if not os.path.exists("temp"):
    os.makedirs("temp")

# To run the app using `uvicorn`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
