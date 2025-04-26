import streamlit as st
import json
from utils import display_warning_message, display_error_message, display_info_message
from data_processor import convert_to_mbtiles
from state import get_main_geojson

def show_download_page():
    """Displays the file download page"""
    st.header("Download de Arquivos")
    
    # Check if a GeoJSON is loaded
    main_geojson = get_main_geojson()
    if not main_geojson:
        display_warning_message("Nenhum arquivo GeoJSON carregado. Vá para a página de Upload de Arquivos.")
        return
    
    # GeoJSON download section
    st.subheader("Download GeoJSON")
    
    # Convert GeoJSON to string
    geojson_str = json.dumps(main_geojson, ensure_ascii=False, indent=4)
    
    # GeoJSON download button
    st.download_button(
        label="Baixar GeoJSON",
        data=geojson_str,
        file_name="resultado.geojson",
        mime="application/geo+json"
    )
    
    # MBTiles download section
    st.subheader("Download MBTiles")
    display_info_message("A conversão para MBTiles requer o Tippecanoe instalado no servidor.")
    
    # Button to generate and download MBTiles
    if st.button("Gerar arquivo MBTiles"):
        generate_and_download_mbtiles(main_geojson)
    
    # Additional information about Tippecanoe
    st.write("#### Nota sobre MBTiles")
    st.write("""
    Para gerar arquivos MBTiles, é necessário ter o [Tippecanoe](https://github.com/mapbox/tippecanoe) 
    instalado no servidor onde o Streamlit está rodando. Esta ferramenta transforma GeoJSON em arquivos .mbtiles 
    para visualização eficiente em mapas interativos.
    """)

def generate_and_download_mbtiles(geojson_data):
    """
    Generates and makes an MBTiles file available for download.
    
    Parameters:
        geojson_data (dict): GeoJSON data for conversion        
    """
    with st.spinner("Gerando MBTiles..."):
        mbtiles_data = convert_to_mbtiles(geojson_data)
        
        if mbtiles_data:
            st.download_button(
                label="Baixar arquivo MBTiles",
                data=mbtiles_data,
                file_name="resultado.mbtiles",
                mime="application/octet-stream"
            )
        else:
            display_error_message("Não foi possível gerar o arquivo MBTiles.")
            display_info_message("Certifique-se de que o Tippecanoe está instalado no servidor.")