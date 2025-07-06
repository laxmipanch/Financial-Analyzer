import streamlit as st
import os
import asyncio
import sys
from datetime import datetime
from pathlib import Path
import time
import glob

# Import your existing stock analyzer functions
# Make sure your original script is importable
try:
    from main import run_analysis, OUTPUT_DIR  # Assuming your script is saved as paste.py
except ImportError:
    st.error("Could not import the stock analyzer. Make sure your original script is saved as 'paste.py' in the same directory.")
    st.stop()

# Streamlit page configuration
st.set_page_config(
    page_title="Stock Analyzer Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .report-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">📈 Stock Analyzer Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for configuration
st.sidebar.header("🔧 Configuration")
st.sidebar.markdown("Configure your stock analysis parameters below:")

# Company input
company_name = st.sidebar.text_input(
    "Company Name",
    value="Apple",
    help="Enter the company name you want to analyze (e.g., Apple, Microsoft, Tesla)"
)

# Analysis options
st.sidebar.markdown("### Analysis Options")
show_previous_reports = st.sidebar.checkbox("Show Previous Reports", value=True)
auto_refresh = st.sidebar.checkbox("Auto-refresh every 30 seconds", value=False)

# Information section
st.sidebar.markdown("### ℹ️ Information")
st.sidebar.info("""
This tool uses:
- Google Search for real-time data
- AI-powered financial analysis
- Automated report generation
- Quality evaluation system
""")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🚀 Generate New Analysis")
    
    # Analysis form
    with st.form("analysis_form"):
        st.markdown(f"**Selected Company:** {company_name}")
        st.markdown("Click the button below to start the analysis process.")
        
        submitted = st.form_submit_button("🔄 Generate Stock Report", use_container_width=True)
        
        if submitted:
            if not company_name.strip():
                st.error("Please enter a company name.")
            else:
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Create output directory if it doesn't exist
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                
                try:
                    # Update progress
                    status_text.text("🔍 Initializing analysis workflow...")
                    progress_bar.progress(10)
                    time.sleep(1)
                    
                    status_text.text("📊 Gathering financial data...")
                    progress_bar.progress(30)
                    time.sleep(1)
                    
                    status_text.text("🤖 Running AI analysis...")
                    progress_bar.progress(60)
                    
                    # Run the analysis
                    report_path, report_content = run_analysis(company_name)
                    
                    progress_bar.progress(90)
                    status_text.text("📝 Generating report...")
                    time.sleep(1)
                    
                    progress_bar.progress(100)
                    
                    if report_content and not report_content.startswith("Error"):
                        status_text.markdown('<p class="success-message">✅ Analysis completed successfully!</p>', unsafe_allow_html=True)
                        st.success(f"Report generated successfully! File saved to: {report_path}")
                        
                        # Store in session state for display
                        st.session_state.latest_report = report_content
                        st.session_state.latest_company = company_name
                        st.session_state.latest_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                    else:
                        status_text.markdown('<p class="error-message">❌ Analysis failed!</p>', unsafe_allow_html=True)
                        st.error(f"Analysis failed: {report_content}")
                        
                except Exception as e:
                    progress_bar.progress(100)
                    status_text.markdown('<p class="error-message">❌ Analysis failed!</p>', unsafe_allow_html=True)
                    st.error(f"An error occurred: {str(e)}")

with col2:
    st.header("📋 Quick Actions")
    
    # Quick company buttons
    st.markdown("**Popular Companies:**")
    popular_companies = ["Apple", "Microsoft", "Tesla", "Amazon", "Google", "Meta"]
    
    for company in popular_companies:
        if st.button(f"📊 {company}", key=f"quick_{company}", use_container_width=True):
            st.session_state.quick_company = company
            st.rerun()
    
    # Update company name if quick button was clicked
    if 'quick_company' in st.session_state:
        company_name = st.session_state.quick_company
        st.sidebar.text_input("Company Name", value=company_name, key="updated_company")
        del st.session_state.quick_company

# Display latest report
if 'latest_report' in st.session_state:
    st.header("📄 Latest Analysis Report")
    
    # Report metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Company", st.session_state.latest_company)
    with col2:
        st.metric("Generated", st.session_state.latest_timestamp)
    with col3:
        st.metric("Status", "✅ Complete")
    
    # Display report content
    st.markdown('<div class="report-container">', unsafe_allow_html=True)
    st.markdown(st.session_state.latest_report)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download button
    st.download_button(
        label="💾 Download Report",
        data=st.session_state.latest_report,
        file_name=f"{st.session_state.latest_company.lower().replace(' ', '_')}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
    )

# Previous reports section
if show_previous_reports:
    st.header("📚 Previous Reports")
    
    try:
        # Get all report files
        if os.path.exists(OUTPUT_DIR):
            report_files = glob.glob(os.path.join(OUTPUT_DIR, "*.md"))
            report_files.sort(key=os.path.getmtime, reverse=True)
            
            if report_files:
                st.markdown(f"Found {len(report_files)} previous reports:")
                
                # Display reports in tabs or expander
                for i, report_file in enumerate(report_files[:10]):  # Show max 10 recent reports
                    file_name = os.path.basename(report_file)
                    file_time = datetime.fromtimestamp(os.path.getmtime(report_file)).strftime("%Y-%m-%d %H:%M:%S")
                    
                    with st.expander(f"📄 {file_name} (Generated: {file_time})"):
                        try:
                            with open(report_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                            st.markdown(content)
                            
                            # Download button for each report
                            st.download_button(
                                label="💾 Download",
                                data=content,
                                file_name=file_name,
                                mime="text/markdown",
                                key=f"download_{i}"
                            )
                        except Exception as e:
                            st.error(f"Error reading file: {str(e)}")
            else:
                st.info("No previous reports found. Generate your first report above!")
        else:
            st.info("Reports directory not found. Generate your first report above!")
            
    except Exception as e:
        st.error(f"Error loading previous reports: {str(e)}")

# Auto-refresh functionality
if auto_refresh:
    time.sleep(30)
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Stock Analyzer Dashboard | Powered by AI & Real-time Data</p>
    <p><small>⚠️ This tool is for informational purposes only. Not financial advice.</small></p>
</div>
""", unsafe_allow_html=True)