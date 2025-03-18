# Meta data generation

## Steps
1. Use the geojson_toolkit.ipynb to generate your .geojson file
2. Then, run the following command to generate a .mbtiles file 
    ```
    tippecanoe -o brazil-states.mbtiles *.geojson   --maximum-zoom=5   --minimum-zoom=0   --simplification=10   --drop-densest-as-needed   --drop-smallest-as-needed   --drop-fraction-as-needed   --maximum-tile-bytes=50000   --detect-shared-borders   --extend-zooms-if-still-dropping   --force
    ```