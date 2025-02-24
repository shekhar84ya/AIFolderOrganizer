import streamlit as st
import os
from datetime import datetime
import time
from ai_handler import GeminiAIHandler
from file_operations import FileOperations
from scheduler import Scheduler
from utils import validate_api_key, create_folder_instruction_pairs

def main():
    st.set_page_config(
        page_title="AI File Organizer",
        page_icon="📁",
        layout="wide"
    )

    st.title("🤖 AI-Powered File Organizer")
    
    # API Key Input
    api_key = st.text_input("Enter Gemini AI API Key", type="password")
    if api_key:
        if not validate_api_key(api_key):
            st.error("Invalid API key")
            return

    # Initialize session state
    if 'folder_count' not in st.session_state:
        st.session_state.folder_count = 1

    # Add/Remove folder buttons
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("Add Folder"):
            st.session_state.folder_count += 1
    with col2:
        if st.button("Remove Folder") and st.session_state.folder_count > 1:
            st.session_state.folder_count -= 1

    # Folder and instruction inputs
    folders_data = []
    for i in range(st.session_state.folder_count):
        st.subheader(f"Folder {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            folder_path = st.text_input(f"Folder Path #{i+1}", key=f"folder_{i}")
        with col2:
            instructions = st.text_area(f"Instructions #{i+1}", 
                                     placeholder="e.g., Categorize PDF files by subject",
                                     key=f"instructions_{i}")
        folders_data.append((folder_path, instructions))

    # Scheduling options
    st.subheader("📅 Scheduling")
    schedule_type = st.selectbox("Schedule Type", 
                               ["Run Once", "Hourly", "Daily", "Weekly"])
    
    if schedule_type != "Run Once":
        if schedule_type == "Hourly":
            schedule_time = st.number_input("Run every N hours", 
                                          min_value=1, max_value=23, value=1)
        elif schedule_type == "Daily":
            schedule_time = st.time_input("Select time")
        else:  # Weekly
            col1, col2 = st.columns(2)
            with col1:
                day = st.selectbox("Select day", 
                                 ["Monday", "Tuesday", "Wednesday", "Thursday",
                                  "Friday", "Saturday", "Sunday"])
            with col2:
                time = st.time_input("Select time")
            schedule_time = (day, time)

    # Process button
    if st.button("Start Processing", type="primary"):
        if not api_key:
            st.error("Please enter an API key")
            return

        valid_pairs = create_folder_instruction_pairs(folders_data)
        if not valid_pairs:
            st.error("Please provide valid folder paths and instructions")
            return

        ai_handler = GeminiAIHandler(api_key)
        file_ops = FileOperations()
        scheduler = Scheduler()

        progress_bar = st.progress(0)
        status_text = st.empty()

        def process_folders():
            for folder_path, instructions in valid_pairs:
                status_text.text(f"Processing folder: {folder_path}")
                
                # Get file listing
                files_info = file_ops.get_directory_info(folder_path)
                
                # Get AI suggestions
                try:
                    commands = ai_handler.get_organization_commands(
                        files_info, instructions)
                    
                    # Execute commands
                    for cmd in commands:
                        status = file_ops.execute_command(cmd, folder_path)
                        st.write(f"Command: {cmd}")
                        st.write(f"Status: {'Success' if status else 'Failed'}")
                        
                except Exception as e:
                    st.error(f"Error processing folder {folder_path}: {str(e)}")
                    continue

            status_text.text("Processing complete!")
            progress_bar.progress(100)

        if schedule_type == "Run Once":
            process_folders()
        else:
            scheduler.schedule_task(
                process_folders,
                schedule_type,
                schedule_time
            )
            st.success("Task scheduled successfully!")

if __name__ == "__main__":
    main()
