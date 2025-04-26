import streamlit as st
import json
from utils import display_success_message, display_error_message, display_info_message, is_valid_json, display_warning_message
from data_processor import get_existing_metadata, process_csv_metadata, merge_geojsons_properties_by_id
from state import update_main_geojson, update_metadata_list, get_main_geojson, add_metadata

def show_upload_page():
    """Displays the file upload page"""
    st.header("Upload GeoJSON Principal")
    
    # Main GeoJSON file upload
    main_file = st.file_uploader("Selecione o arquivo GeoJSON principal", type=["geojson", "json"])
    
    if main_file:
        process_main_file(main_file)
    
    st.header("Adicionar Metadado")
    
    # If there's no main file, display warning
    if not get_main_geojson():
        display_warning_message("Carregue um arquivo GeoJSON principal primeiro")
    else:
        show_metadata_upload_form()

def process_main_file(file):
    """
    Processes the main GeoJSON file.
    
    Parameters:
        file: File uploaded by the user
    """
    try:
        # Read file content
        geojson_content = file.read().decode('utf-8')
        geojson_data = json.loads(geojson_content)
        
        # Check if it's a valid GeoJSON
        if not is_valid_json(geojson_data):
            display_error_message("Arquivo não é um GeoJSON válido")
            return
        
        # Extract existing metadata
        metadata_list = get_existing_metadata(geojson_data)
        
        # Update session state
        update_main_geojson(geojson_data)
        update_metadata_list(metadata_list)
        
        # Display success message
        display_success_message(f"Arquivo {file.name} carregado com sucesso!")
        
        # Display information about found metadata
        if metadata_list:
            display_info_message(f"Metadados encontrados: {', '.join(metadata_list)}")
        else:
            display_info_message("Nenhum metadado encontrado no arquivo carregado.")
        
    except Exception as e:
        display_error_message(f"Erro ao processar o arquivo: {str(e)}")

def show_metadata_upload_form():
    """Displays the metadata upload form"""
    metadata_name = st.text_input("Nome do metadado (ex.: deg_v32021)")
    metadata_file = st.file_uploader("Selecione o arquivo de metadados", type=["geojson", "json", "csv"])
    
    if st.button("Adicionar Metadado") and metadata_file and metadata_name:
        process_metadata_file(metadata_file, metadata_name)

def process_metadata_file(file, metadata_name):
    """
    Processes the metadata file.
    
    Parameters:
        file: Metadata file uploaded by the user
        metadata_name (str): Name for the metadata
    """
    try:
        # Read file content
        file_content = file.read().decode('utf-8')
        
        # Process file according to its type
        if file.name.endswith('.csv'):
            metadata_geojson = process_csv_metadata(file_content, metadata_name)
            if not metadata_geojson:
                display_error_message("Falha ao processar o arquivo CSV")
                return
        else:
            metadata_geojson = json.loads(file_content)
        
        # Merge metadata with main GeoJSON
        main_geojson = get_main_geojson()
        result_geojson = merge_geojsons_properties_by_id(
            main_geojson, 
            metadata_geojson, 
            metadata_name
        )
        
        # Update session state
        update_main_geojson(result_geojson)
        add_metadata(metadata_name)
        
        # Display success message
        display_success_message(f"Metadado '{metadata_name}' adicionado com sucesso!")
        
    except Exception as e:
        display_error_message(f"Erro ao adicionar metadado: {str(e)}")