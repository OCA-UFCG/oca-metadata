import streamlit as st
import json
from utils import (
    display_success_message, display_warning_message, display_info_message, 
    display_error_message, extract_field_patterns
)
from data_processor import (
    remove_metadata, apply_format_updates, rename_metadata, get_metadata_details
)
from state import (
    get_main_geojson, get_metadata_list, update_main_geojson, 
    remove_metadata as remove_metadata_from_state,
    get_selected_metadata, set_selected_metadata, 
    get_show_edit_form, set_show_edit_form,
    replace_metadata, clear_selected_metadata
)

def show_metadata_page():
    """
    Displays the unified metadata management page,
    including listing, viewing and editing.
    """
    st.header("Gerenciar Metadados")
    
    # Check if a GeoJSON is loaded
    if not get_main_geojson():
        display_warning_message("Nenhum arquivo GeoJSON carregado. Vá para a página de Upload de Arquivos.")
        return
    
    # Get current metadata
    metadata_list = get_metadata_list()
    selected_metadata = get_selected_metadata()
    
    # Layout with two columns
    col1, col2 = st.columns([1, 1.5])
    
    # Metadata list column
    with col1:
        st.subheader("Metadados Disponíveis")
        if not metadata_list:
            display_info_message("Nenhum metadado encontrado no GeoJSON atual.")
        else:
            # Display metadata list
            display_metadata_list(metadata_list)
    
    # View/edit column
    with col2:
        if selected_metadata:
            show_metadata_details(selected_metadata)
        else:
            st.info("Selecione um metadado ao lado para visualizar ou editar seus detalhes.")

def display_metadata_list(metadata_list):
    """
    Displays the metadata list with action buttons.
    
    Parameters:
        metadata_list (list): List of metadata names
    """
    # Initialize state variables to control deletion confirmation
    if 'delete_confirmation' not in st.session_state:
        st.session_state.delete_confirmation = {}
    
    for metadata in metadata_list:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        # Metadata name
        with col1:
            st.write(metadata)
        
        # View/edit button
        with col2:
            if st.button("Visualizar/Editar", key=f"view_{metadata}"):
                handle_select_metadata(metadata)
        
        # Delete button
        with col3:
            # Check if we're already in confirmation mode for this metadata
            is_confirming = st.session_state.delete_confirmation.get(metadata, False)
            
            if is_confirming:
                # Show confirmation button
                if st.button("Confirmar", key=f"confirm_{metadata}"):
                    # Process the deletion
                    handle_delete_metadata_confirmed(metadata)
                    # Reset confirmation state
                    st.session_state.delete_confirmation[metadata] = False
            else:
                # Show normal delete button
                if st.button("Deletar", key=f"delete_{metadata}"):
                    # Activate confirmation mode
                    st.session_state.delete_confirmation[metadata] = True
                    st.rerun()

def handle_select_metadata(metadata_name):
    """
    Handles the selection of a metadata for viewing/editing.
    
    Parameters:
        metadata_name (str): Name of the selected metadata
    """
    set_selected_metadata(metadata_name)
    set_show_edit_form(False)
    st.rerun()

def handle_delete_metadata_confirmed(metadata_name):
    """
    Handles the confirmed deletion of a metadata.
    
    Parameters:
        metadata_name (str): Name of the metadata to be deleted
    """
    try:
        main_geojson = get_main_geojson()
        updated_geojson = remove_metadata(main_geojson, metadata_name)
        
        # Update session state
        update_main_geojson(updated_geojson)
        remove_metadata_from_state(metadata_name)
        
        # If the deleted metadata was selected, clear the selection
        if get_selected_metadata() == metadata_name:
            clear_selected_metadata()
        
        display_success_message(f"Metadado '{metadata_name}' removido com sucesso!")
        st.rerun()
    except Exception as e:
        display_error_message(f"Erro ao remover metadado: {str(e)}")

def show_metadata_details(metadata_name):
    """
    Displays the details of a selected metadata.
    
    Parameters:
        metadata_name (str): Name of the metadata to be displayed        
    """
    st.subheader(f"Detalhes do Metadado: {metadata_name}")
    
    # Get metadata details
    main_geojson = get_main_geojson()
    metadata_details = get_metadata_details(main_geojson, metadata_name)
    
    if not metadata_details:
        display_error_message("Não foi possível encontrar detalhes do metadado.")
        clear_selected_metadata()
        return
    
    # Display metadata details
    st.json(metadata_details)
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if not get_show_edit_form() and st.button("Editar"):
            set_show_edit_form(True)
            st.rerun()
    
    with col2:
        if st.button("Voltar"):
            clear_selected_metadata()
            st.rerun()
    
    # Edit form, if activated
    if get_show_edit_form():
        show_edit_form(metadata_name, metadata_details)

def show_edit_form(metadata_name, metadata_details):
    """
    Displays the metadata editing form.
    
    Parameters:
        metadata_name (str): Name of the metadata
        metadata_details (dict): Metadata details
    """
    st.subheader("Editar Metadado")
    
    # Extract formatting patterns
    field_patterns = extract_field_patterns(metadata_details)
    
    with st.form("edit_metadata_form"):
        new_metadata_name = st.text_input("Novo nome do metadado", value=metadata_name)
        
        # Formatting fields
        st.subheader("Formato dos Campos")
        
        format_updates = {}
        for field in metadata_details.keys():
            if field.startswith('Percent_'):
                format_updates[field] = {'prefix': field_patterns[field].get('prefix', ''), 
                                        'suffix': field_patterns[field].get('suffix', '')}
                continue
                
            st.write(f"**{field}**")
            col1, col2 = st.columns(2)
            
            with col1:
                prefix = st.text_input(
                    "Prefixo", 
                    value=field_patterns[field].get('prefix', ''),
                    key=f"prefix_{field}"
                )
            
            with col2:
                suffix = st.text_input(
                    "Sufixo", 
                    value=field_patterns[field].get('suffix', ''),
                    key=f"suffix_{field}"
                )
            
            format_updates[field] = {'prefix': prefix, 'suffix': suffix}
        
        submit = st.form_submit_button("Atualizar Metadado")
        
        if submit:
            update_metadata(metadata_name, new_metadata_name, format_updates)

def update_metadata(old_name, new_name, format_updates):
    """
    Updates a metadata in the GeoJSON.
    
    Parameters:
        old_name (str): Current metadata name
        new_name (str): New name for the metadata
        format_updates (dict): Format updates to be applied
    """
    try:
        main_geojson = get_main_geojson()
        
        # Apply format updates
        updated_geojson = apply_format_updates(
            main_geojson,
            old_name,
            format_updates
        )
        
        # Rename metadata if necessary
        if new_name != old_name:
            updated_geojson = rename_metadata(
                updated_geojson,
                old_name,
                new_name
            )
            
            # Update metadata list
            replace_metadata(old_name, new_name)
            
            # Update selected metadata
            set_selected_metadata(new_name)
        
        # Update GeoJSON in session state
        update_main_geojson(updated_geojson)
        
        # Deactivate edit form
        set_show_edit_form(False)
        
        display_success_message("Metadado atualizado com sucesso!")
        st.rerun()
    except Exception as e:
        display_error_message(f"Erro ao atualizar metadado: {str(e)}")