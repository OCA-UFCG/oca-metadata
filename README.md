# OCA Metadata

GeoJSON manager for Brazilian maps metadata. This application allows manipulation of GeoJSON files and their properties, especially for maps representing Brazilian states and municipalities.

## Features

- Upload base GeoJSON files
- Add metadata from CSV files or other GeoJSON
- Edit and format metadata fields
- View metadata properties
- Download the processed GeoJSON
- Convert to MBTiles format (requires Tippecanoe)

## Requirements

- Python 3.9+
- Streamlit 1.44+
- Pandas 2.2+
- Numpy 2.2+
- Tippecanoe (for MBTiles conversion)

## Installation and Local Execution

### Using Python virtual environment

1. Clone the repository:
   ```bash
   git clone https://github.com/OCA-UFCG/oca-metadata.git
   cd oca-metadata
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run src/app.py
   ```

   Or via Makefile:
   ```bash
   make run-dev
   ```

5. Access in browser:
   ```
   http://localhost:8501
   ```

### Using Docker

1. Build the image:
   ```bash
   docker build -t ocaufcg/oca-metadata .
   ```
   
   Or via Makefile:
   ```bash
   make docker-build
   ```

2. Run the container:
   ```bash
   docker run --name oca-metadata -p 8501:8501 ocaufcg/oca-metadata
   ```
   
   Or via Makefile:
   ```bash
   make docker-run
   ```

3. Access in browser:
   ```
   http://localhost:8501
   ```

## Application Usage

1. **File Upload**:
   - Upload the base GeoJSON (e.g., map of Brazilian states)
   - Add metadata from CSV files or other GeoJSON

2. **Manage Metadata**:
   - View and edit metadata properties
   - Rename fields
   - Format values (e.g., for percentages)
   - Remove unwanted metadata

3. **Download**:
   - Download the processed GeoJSON
   - Optionally, convert to MBTiles for use in mapping applications

## Project Structure

```
oca-metadata/
├── Dockerfile
├── Makefile
├── geojson2mbtiles.sh     # Convert geojson to mbtiles
├── mapMetadata/           # Example data
│   ├── brazil-states-clean.geojson
│   ├── brazil-states.geojson
│   └── cities.min.json
├── requirements.txt
└── src/
    ├── app.py             # Application entry point
    ├── constants.py       # Constants and settings
    ├── data_processor.py  # Data processing
    ├── pages/
    │   ├── download_page.py
    │   ├── metadata_page.py
    │   └── upload_page.py
    ├── state.py           # Application state management
    └── utils.py           # Utility functions
```

## Contribution

Contributions are welcome! Please open an issue to discuss important changes before creating a pull request.