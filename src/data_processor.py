import re
import csv
import json
import io
import tempfile
import subprocess
import os
from constants import UF_IDS
from utils import format_metadata_value

def get_existing_metadata(geojson_data):
    """
    Extracts existing metadata from a GeoJSON.

    Parameters:
        geojson_data (dict): GeoJSON data
        
    Returns:
        list: List of found metadata names
    """
    metadata = {}
    if 'features' in geojson_data and geojson_data['features']:
        for feature in geojson_data['features']:
            if 'properties' in feature:
                for key, value in feature['properties'].items():
                    if isinstance(value, dict) and any(k.startswith('Area_') or k.startswith('Percent_') for k in value.keys()):
                        metadata[key] = True
    return list(metadata.keys())

def process_csv_metadata(csv_content, metadata_name):
    """
    Processes CSV data into GeoJSON metadata format.

    Parameters:
        csv_content (str): Content of the CSV file
        metadata_name (str): Name for the metadata
        
    Returns:
        dict: GeoJSON containing the metadata
    """
    metadata_geojson = {"type": "FeatureCollection", "features": []}
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    
    for row in csv_reader:
        if 'NM_UF' not in row or 'SIGLA_UF' not in row:
            return None
            
        nm_uf = row['NM_UF']
        sigla_uf = row['SIGLA_UF']
        feature_id = UF_IDS.get(nm_uf)
        
        if not feature_id:
            continue
            
        metadata = {}
        total_area = 0.0
        
        # Check if the CSV is in the expected format
        has_area_columns = any(f'Area_km2_{i}' in row for i in range(1, 7))
        
        if has_area_columns:
            for i in range(1, 7):
                area_key = f'Area_km2_{i}'
                percent_key = f'Percent_{i}'
                
                if area_key in row and percent_key in row and row[area_key].strip():
                    area_value = float(row[area_key])
                    total_area += area_value
                    metadata[f'Area_info_{i}'] = f"{area_value / 1000:.1f} Mil Km²" if area_value >= 1000 else f"{area_value:.1f} Km²"
                    metadata[percent_key] = float(row[percent_key]) if row[percent_key].strip() else 0.0
        else:
            # If not in expected format, add all columns as metadata
            for key, value in row.items():
                if key not in ['NM_UF', 'SIGLA_UF']:
                    if key.startswith('Percent_') and value.strip():
                        metadata[key] = float(value)
                    else:
                        metadata[key] = value
                    
        if has_area_columns:
            metadata['Area_general'] = f"{total_area / 1000:.1f} Mil Km²"
            
        feature = {
            "type": "Feature", "id": feature_id,
            "properties": {"NM_UF": nm_uf, "SIGLA_UF": sigla_uf, metadata_name: metadata}
        }
        metadata_geojson['features'].append(feature)
        
    return metadata_geojson

def merge_geojsons_properties_by_id(geojson_destination, geojson_source, new_object_name):
    """
    Merges the properties of two GeoJSONs based on their IDs.

    Parameters:
        geojson_destination (dict): Destination GeoJSON
        geojson_source (dict): Source GeoJSON
        new_object_name (str): Name for the merged object
        
    Returns:
        dict: Merged GeoJSON
    """
    source_map = {}
    for feature in geojson_source['features']:
        if 'id' in feature and 'properties' in feature:
            source_map[feature['id']] = feature['properties'].get(new_object_name) or {
                k: v for k, v in feature['properties'].items() if k not in ['NM_UF', 'SIGLA_UF']
            }
    
    result = json.loads(json.dumps(geojson_destination))
    
    for feature in result['features']:
        if 'id' in feature and feature['id'] in source_map:
            feature['properties'][new_object_name] = source_map[feature['id']]
    
    return result

def rename_metadata(geojson_data, old_name, new_name):
    """
    Renames a metadata field in the GeoJSON.

    Parameters:
        geojson_data (dict): GeoJSON data
        old_name (str): Old metadata name
        new_name (str): New name for the metadata
        
    Returns:
        dict: Updated GeoJSON
    """
    result = json.loads(json.dumps(geojson_data))
    
    for feature in result['features']:
        if 'properties' in feature and old_name in feature['properties']:
            feature['properties'][new_name] = feature['properties'].pop(old_name)
    
    return result

def remove_metadata(geojson_data, metadata_name):
    """
    Removes a metadata field from the GeoJSON.

    Parameters:
        geojson_data (dict): GeoJSON data
        metadata_name (str): Name of the metadata to remove
        
    Returns:
        dict: Updated GeoJSON
    """
    result = json.loads(json.dumps(geojson_data))
    
    for feature in result['features']:
        if 'properties' in feature and metadata_name in feature['properties']:
            del feature['properties'][metadata_name]

    return result

def apply_format_updates(geojson_data, metadata_name, format_updates):
    """
    Applies formatting updates to metadata values.

    Parameters:
        geojson_data (dict): GeoJSON data
        metadata_name (str): Name of the metadata to update
        format_updates (dict): Formatting updates to apply
        
    Returns:
        dict: Updated GeoJSON
    """
    result = json.loads(json.dumps(geojson_data))
    
    for feature in result['features']:
        if 'properties' in feature and metadata_name in feature['properties']:
            metadata = feature['properties'][metadata_name]
            for field, updates in format_updates.items():
                if field in metadata:
                    prefix = updates.get('prefix', '')
                    suffix = updates.get('suffix', '')
                    value = metadata[field]
                    
                    if field.startswith('Percent_') and isinstance(value, (int, float)):
                        continue
                        
                    if isinstance(metadata[field], str):
                        num_match = re.search(r'(\d*\.?\d+\s*(?:Mil)?)', metadata[field])
                        if num_match:
                            value = num_match.group(0)
                            
                    metadata[field] = format_metadata_value(value, prefix, suffix)
    
    return result

def get_metadata_details(geojson_data, metadata_name):
    """
    Gets details of a specific metadata.

    Parameters:
        geojson_data (dict): GeoJSON data
        metadata_name (str): Name of the metadata
        
    Returns:
        dict: Metadata details or None if not found
    """
    for feature in geojson_data['features']:
        if 'properties' in feature and metadata_name in feature['properties']:
            metadata_copy = json.loads(json.dumps(feature['properties'][metadata_name]))
            
            for key, value in metadata_copy.items():
                if key.startswith('Percent_') and isinstance(value, str):
                    try:
                        metadata_copy[key] = float(value)
                    except (ValueError, TypeError):
                        pass
                        
            return metadata_copy
    return None

def convert_to_mbtiles(geojson_data):
    """
    Converts GeoJSON to MBTiles format using a Bash script with Tippecanoe.

    Parameters:
        geojson_data (dict): GeoJSON data to convert
        
    Returns:
        bytes: MBTiles file data or None in case of an error
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        input_filepath = os.path.join(temp_dir, "input.geojson")
        output_filepath = os.path.join(temp_dir, "output.mbtiles")
        
        class NumericEncoder(json.JSONEncoder):
            def default(self, obj):
                return super(NumericEncoder, self).default(obj)
                
        with open(input_filepath, 'w', encoding='utf-8') as f:
            json.dump(geojson_data, f, ensure_ascii=True, cls=NumericEncoder)
        
        try:
            script_path = "./geojson2mbtiles.sh"
            
            if not os.path.exists(script_path):
                print("Error: geojson2mbtiles.sh script not found.")
                return None
            
            os.chmod(script_path, 0o755)
            
            cmd = [script_path, input_filepath, output_filepath]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"{result.stdout}")

            with open(output_filepath, 'rb') as f:
                mbtiles_data = f.read()
                
            return mbtiles_data
        except subprocess.CalledProcessError as e:
            print(f"Error running the Bash script: {e.stderr}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None