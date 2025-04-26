import streamlit as st

def initialize_session_state():
    """Initializes the session state with default values if they do not exist"""
    if 'main_geojson' not in st.session_state:
        st.session_state.main_geojson = None
    
    if 'metadata_list' not in st.session_state:
        st.session_state.metadata_list = []
    
    if 'show_edit_form' not in st.session_state:
        st.session_state.show_edit_form = False
    
    if 'selected_metadata' not in st.session_state:
        st.session_state.selected_metadata = None

    if 'session_created' not in st.session_state:
        st.session_state.session_created = True

def update_main_geojson(geojson_data):
    """Updates the main GeoJSON in the session state"""
    st.session_state.main_geojson = geojson_data

def get_main_geojson():
    """Returns the main GeoJSON from the session state"""
    return st.session_state.main_geojson

def update_metadata_list(metadata_list):
    """Updates the metadata list in the session state"""
    st.session_state.metadata_list = metadata_list

def get_metadata_list():
    """Returns the metadata list from the session state"""
    return st.session_state.metadata_list

def add_metadata(metadata_name):
    """Adds a metadata entry to the list if it does not already exist"""
    if metadata_name not in st.session_state.metadata_list:
        st.session_state.metadata_list.append(metadata_name)

def remove_metadata(metadata_name):
    """Removes a metadata entry from the list if it exists"""
    if metadata_name in st.session_state.metadata_list:
        st.session_state.metadata_list.remove(metadata_name)

def replace_metadata(old_name, new_name):
    """Replaces a metadata name with another one in the list"""
    if old_name in st.session_state.metadata_list:
        st.session_state.metadata_list = [
            new_name if x == old_name else x 
            for x in st.session_state.metadata_list
        ]

def set_selected_metadata(metadata_name):
    """Sets the selected metadata"""
    st.session_state.selected_metadata = metadata_name

def get_selected_metadata():
    """Returns the selected metadata"""
    return st.session_state.selected_metadata

def set_show_edit_form(show):
    """Sets whether the edit form should be displayed"""
    st.session_state.show_edit_form = show

def get_show_edit_form():
    """Returns whether the edit form should be displayed"""
    return st.session_state.show_edit_form

def clear_selected_metadata():
    """Clears the selected metadata"""
    st.session_state.selected_metadata = None
    st.session_state.show_edit_form = False
