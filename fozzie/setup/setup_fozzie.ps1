param(
    [string]$StartPath = ".\fozzie"
)

# Ensure the path exists
if (-Not (Test-Path $StartPath)) {
    New-Item -ItemType Directory -Path $StartPath | Out-Null
}

# Navigate to the project folder
Set-Location -Path $StartPath

# Create directories
$folders = @("fozzie", "tests")
foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path "$StartPath\$folder" -Force | Out-Null
}

# Create __init__.py
@"
# Makes this a package
from .geocoding import reverse_geocode, forward_geocode
"@ | Set-Content "$StartPath\fozzie\__init__.py"

# Create setup.py
@"
from setuptools import setup, find_packages

setup(
    name="fozzie",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pandas", "requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
"@ | Set-Content "$StartPath\setup.py"

# Create requirements.txt
@"
pandas
requests
pytest
"@ | Set-Content "$StartPath\requirements.txt"

# Create .gitignore
@"
venv/
__pycache__/
*.pyc
.DS_Store
"@ | Set-Content "$StartPath\.gitignore"

# Create README.md
@"
# fozzie

A Python package for data analysis, geocoding, and utilities.
"@ | Set-Content "$StartPath\README.md"

# Create geocoding.py
@"
import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/"

def reverse_geocode(lat: float, lon: float) -> dict:
    params = {"lat": lat, "lon": lon, "format": "json", "addressdetails": 1}
    response = requests.get(f"{NOMINATIM_URL}reverse", params=params)
    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            return {"error": data["error"]}
        return {
            "address": data.get("display_name"),
            "latitude": float(data.get("lat")),
            "longitude": float(data.get("lon")),
            "details": {
                "place_id": data.get("place_id"),
                "osm_type": data.get("osm_type"),
                "osm_id": data.get("osm_id"),
                "type": data.get("type"),
                "bounding_box": data.get("boundingbox"),
            }
        }
    return {"error": "Failed to retrieve data."}

def forward_geocode(address: str) -> dict:
    params = {"q": address, "format": "json", "limit": 1}
    response = requests.get(f"{NOMINATIM_URL}search", params=params)
    if response.status_code == 200:
        data = response.json()
        if not data:
            return {"error": "Address not found."}
        result = data[0]
        return {
            "address": result.get("display_name"),
            "latitude": float(result.get("lat")),
            "longitude": float(result.get("lon")),
            "details": {
                "place_id": result.get("place_id"),
                "osm_type": result.get("osm_type"),
                "osm_id": result.get("osm_id"),
                "type": result.get("type"),
                "bounding_box": result.get("boundingbox"),
            }
        }
    return {"error": "Failed to retrieve data."}
"@ | Set-Content "$StartPath\fozzie\geocoding.py"

# Create test file
@"
from fozzie.geocoding import reverse_geocode, forward_geocode

def test_reverse_geocode():
    result = reverse_geocode(40.748817, -73.985428)
    assert "address" in result or "error" in result

def test_forward_geocode():
    result = forward_geocode("Empire State Building, New York, NY")
    assert "latitude" in result and "longitude" in result or "error" in result
"@ | Set-Content "$StartPath\tests\test_geocoding.py"

# Initialize Git
git init
git add .
git commit -m "Initial commit for fozzie"

# Set up virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Confirm setup completion
Write-Host "fozzie project has been set up at $StartPath" -ForegroundColor Green
