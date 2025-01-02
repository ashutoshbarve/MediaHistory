from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from utils.metadata_extraction import extract_metadata
from utils.ela_analysis import error_level_analysis
from utils.video_analysis import analyze_video

app = FastAPI()

# Serve static files from the 'temp' directory
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

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

# Function to save the uploaded file to disk
def save_file(file: UploadFile, destination: str):
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

@app.post("/analyze/image/")
async def analyze_image(file: UploadFile = File(...)):
    file_location = f"temp/{file.filename}"
    save_file(file, file_location)
    
    # Perform image analysis (metadata extraction and ELA)
    metadata = extract_metadata(file_location)
    ela_result = error_level_analysis(file_location)

    # Ensure the result is saved as 'ela_result.jpg' in the temp directory
    ela_result_path = f"temp/ela_result_{file.filename}.jpg"

    # Here, we assume the ELA result function creates the image at the above path
    # If ELA function doesn't save the image, you need to implement that part

    if not os.path.exists(ela_result_path):
        return JSONResponse({"error": "ELA result not found or failed to generate."}, status_code=500)

    return JSONResponse({
        "metadata": metadata,
        "ela_result": {
            "ela_analysis": "ELA completed successfully.",
            "ela_result_path": f"/temp/ela_result_{file.filename}.jpg",  # Path to the ELA result image
            "difference_threshold": 30,
            "jpeg_quality": 95
        }
    })

@app.post("/analyze/video/") 
async def analyze_video_file(file: UploadFile = File(...)):
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
