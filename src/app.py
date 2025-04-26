import streamlit as st
from pages.upload_page import show_upload_page
from pages.metadata_page import show_metadata_page
from pages.download_page import show_download_page
from state import initialize_session_state

# Hide file links in the sidebar
hide_file_links = """
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    .stApp header {
        display: none;
    }

    .block-container {
        max-width: none !important;
        padding-left: 1rem;
        padding-right: 1rem;
    }
</style>
"""
st.markdown(hide_file_links, unsafe_allow_html=True)

def main():
    # Initialize session state
    initialize_session_state()
    
    # Application title
    st.title("Gerenciador de GeoJSON Simplificado")
    
    # Additional information in the sidebar
    st.sidebar.info("""
    ## Sobre
    Esta aplicação permite gerenciar arquivos GeoJSON e suas propriedades, especialmente para mapas do Brasil.

    ### Funcionalidades:
    - Upload de GeoJSON base
    - Adicionar metadados a partir de CSV
    - Editar e formatar campos
    - Baixar GeoJSON
    - Converter para formato MBTiles
    """)

    # Sidebar for navigation
    st.sidebar.title("Navegação")
    page = st.sidebar.radio(
        "Ir para:", 
        ["Upload de Arquivos", "Gerenciar Metadados", "Download"]
    )
    
    # Show the selected page
    if page == "Upload de Arquivos":
        show_upload_page()
    elif page == "Gerenciar Metadados":
        show_metadata_page()
    elif page == "Download":
        show_download_page()
    
if __name__ == "__main__":
    main()