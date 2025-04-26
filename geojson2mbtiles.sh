#!/bin/bash

# Script to convert GeoJSON to MBTiles using tippecanoe

# Arguments
INPUT_GEOJSON=$1
OUTPUT_MBTILES=$2

# Check if tippecanoe is installed
if ! command -v tippecanoe &> /dev/null; then
    echo "Error: tippecanoe is not installed."
    exit 1
fi

# Check if arguments were provided
if [ -z "$INPUT_GEOJSON" ] || [ -z "$OUTPUT_MBTILES" ]; then
    echo "Error: Provide the path to the input GeoJSON and output MBTiles."
    exit 1
fi

# Execute tippecanoe with parameters
# -zg                                 Auto-select max zoom based on feature density
# -S 10                               Simplify geometries with 10x tolerance
# -l brazilstates                     Name the layer "brazilstates"
# --drop-densest-as-needed            Drop densest features to keep tiles under 500K
# --coalesce-densest-as-needed        Merge densest polygons to reduce feature count
# --detect-shared-borders             Simplify shared polygon borders consistently
# --extend-zooms-if-still-dropping    Increase max zoom if features are dropped
# -ac                                 Merge consecutive features with same attributes
# -ao                                 Reorder features to optimize coalescing
# -f                                  Overwrite output .mbtiles if it exists
tippecanoe -o "$OUTPUT_MBTILES" \
    -zg \
    -S 10 \
    -l brazilstates \
    --drop-densest-as-needed \
    --coalesce-densest-as-needed \
    --detect-shared-borders \
    --extend-zooms-if-still-dropping \
    -ac \
    -ao \
    -f \
    "$INPUT_GEOJSON"

# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "Conversion completed successfully: $OUTPUT_MBTILES"
else
    echo "Error executing tippecanoe."
    exit 1
fi

