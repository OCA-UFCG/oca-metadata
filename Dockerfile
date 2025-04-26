FROM python:3.13-slim

WORKDIR /app

# Install necessary system dependencies for Tippecanoe and other tools
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libsqlite3-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Tippecanoe
RUN git clone https://github.com/mapbox/tippecanoe.git \
    && cd tippecanoe \
    && make -j \
    && make install \
    && cd .. \
    && rm -rf tippecanoe

# Copy application dependency files
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY src/ ./src/
COPY geojson2mbtiles.sh ./geojson2mbtiles.sh

# Expose the port used by Streamlit by default
EXPOSE 8501

# Settings for stateless mode
ENV STREAMLIT_SERVER_ENABLE_STATIC_SERVING=false
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=true

# Command to start the application
CMD ["streamlit", "run", "src/app.py", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
