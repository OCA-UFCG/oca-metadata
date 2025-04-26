import re
import streamlit as st

def extract_field_patterns(metadata):
    """
    Extracts formatting patterns from metadata fields.
    
    Parameters:
        metadata (dict): Dictionary containing metadata values
        
    Returns:
        dict: Dictionary with prefix and suffix patterns for each field
    """
    field_patterns = {}
    for key, value in metadata.items():
        field_patterns[key] = {'prefix': '', 'suffix': ''}
        if isinstance(value, str):
            num_match = re.search(r'(\d*\.?\d+\s*(?:Mil)?)', value)
            if num_match:
                num_val = num_match.group(0)
                parts = value.split(num_val, 1)
                if len(parts) == 2:
                    field_patterns[key].update({'prefix': parts[0].strip(), 'suffix': parts[1].strip()})
            else:
                field_patterns[key]['suffix'] = value.strip()
    return field_patterns

def display_success_message(message):
    """Displays a success message"""
    st.success(message)

def display_error_message(message):
    """Displays an error message"""
    st.error(message)

def display_info_message(message):
    """Displays an informational message"""
    st.info(message)

def display_warning_message(message):
    """Displays a warning message"""
    st.warning(message)

def is_valid_json(json_obj):
    """
    Checks if the object is a valid GeoJSON with features.
    
    Parameters:
        json_obj (dict): JSON object to be validated
        
    Returns:
        bool: True if it is a valid GeoJSON, False otherwise
    """
    return isinstance(json_obj, dict) and 'features' in json_obj

def format_metadata_value(value, prefix='', suffix=''):
    """
    Formats a metadata value with prefix and suffix.
    
    Parameters:
        value: Value to be formatted
        prefix (str): Prefix to be added
        suffix (str): Suffix to be added
        
    Returns:
        str: Formatted value
    """
    str_value = str(value) if isinstance(value, (int, float)) else value
    return f"{prefix}{str_value}{suffix}"
