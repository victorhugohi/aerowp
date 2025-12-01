Write-Host "Starting local server at http://localhost:8000..."
Start-Process "http://localhost:8000"
python -m http.server 8000
