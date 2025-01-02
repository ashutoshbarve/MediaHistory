# Define paths
$frontendPath = ".\frontend"
$backendPath = ".\backend"

# Function to run the backend
function Start-Backend {
    Write-Host "Starting Backend..." -ForegroundColor Green
    Set-Location -Path $backendPath
    if (-Not (Test-Path .\venv)) {
        Write-Host "Setting up Python virtual environment..." -ForegroundColor Yellow
        python -m venv venv
    }
    .\venv\Scripts\activate
    Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "Starting FastAPI server..." -ForegroundColor Green
    Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList "/c uvicorn app:app --host 0.0.0.0 --port 8000"
    Set-Location -Path ..
}

# Function to run the frontend
function Start-Frontend {
    Write-Host "Starting Frontend..." -ForegroundColor Green
    Set-Location -Path $frontendPath
    if (-Not (Test-Path .\node_modules)) {
        Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
        npm install
    }
    Write-Host "Starting React development server..." -ForegroundColor Green
    Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList "/c npm start"
    Set-Location -Path ..
}

# Main execution
Write-Host "Launching project setup..." -ForegroundColor Cyan

# Start backend
Start-Backend

# Start frontend
Start-Frontend

Write-Host "Project is running. Frontend: http://localhost:3000, Backend: http://localhost:8000" -ForegroundColor Cyan
