import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys
import os

# Set page configuration with a wide layout and custom title
st.set_page_config(page_title='Data Profiler', layout='wide')

def get_filesize(file):
    """Return file size in MB."""
    return sys.getsizeof(file) / (1024**2)

def validate_file(file):
    """Validate uploaded file extension."""
    return os.path.splitext(file.name)[-1] in ('.csv', '.xlsx')

def load_data(file, ext):
    """Load data based on file extension."""
    if ext == '.csv':
        return pd.read_csv(file)
    xl_file = pd.ExcelFile(file)
    sheet_name = st.sidebar.selectbox('Select a sheet', xl_file.sheet_names)
    return xl_file.parse(sheet_name)

def generate_report(df, minimal, display_mode):
    """Generate a profiling report."""
    dark_mode = display_mode == 'Dark'
    orange_mode = display_mode == 'Orange'
    return ProfileReport(df, minimal=minimal, dark_mode=dark_mode, orange_mode=orange_mode)

def save_report(pr):
    """Save report as HTML and prepare it for download."""
    html_file = pr.to_html()
    return html_file

# Sidebar layout
st.sidebar.title("🗂️ File Uploader")
uploaded_file = st.sidebar.file_uploader("Upload .csv or .xlsx files (max 10 MB)")

if uploaded_file:
    if validate_file(uploaded_file):
        if get_filesize(uploaded_file) <= 10:
            df = load_data(uploaded_file, os.path.splitext(uploaded_file.name)[-1])
            
            st.sidebar.write('### Modes of Operation')
            minimal = st.sidebar.checkbox('Generate a minimal report?', value=False)
            display_mode = st.sidebar.radio('Select display mode:', options=('Primary', 'Dark', 'Orange'))
            save_html = st.sidebar.checkbox('Save report as HTML?', value=False)
            st.sidebar.write('---')
            
            with st.spinner('Generating report...'):
                pr = generate_report(df, minimal, display_mode)
                st_profile_report(pr)
                
                if save_html:
                    html_content = save_report(pr)
                    st.download_button(
                        label="Download HTML report",
                        data=html_content,
                        file_name="report.html",
                        mime="text/html",
                    )
        else:
            st.sidebar.error('File size exceeds the 10 MB limit.')
    else:
        st.sidebar.error('Invalid file format. Please upload a .csv or .xlsx file.')
else:
    st.title('Welcome to Data Profiler')
    st.image("./media/DP Logo.jpg", use_column_width=True)
    st.markdown("""
        **Welcome to Data Profiler!** 🎉

        This tool allows you to analyze and visualize your datasets with ease. Upload your data using the sidebar and generate a comprehensive profiling report.
        
        **Key Features**:
        - 📊 **Automated Data Analysis**: Quickly profile your data with a single upload.
        - 🕵️ **Detailed Insights**: Detect anomalies, patterns, and trends effortlessly.
        - 🌈 **Customizable Reports**: Choose between different display modes and save reports in HTML format.
        
        **How to Use**:
        1. Upload your dataset in the sidebar.
        2. Choose your preferred settings for the report.
        3. View or save the generated report.
    """)
    st.markdown("""
        **Supported Formats**:
        - 📂 .csv
        - 📊 .xlsx
    """)
