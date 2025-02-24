import os
from typing import List, Tuple
import google.generativeai as genai

def validate_api_key(api_key: str) -> tuple[bool, str]:
    """
    Validate the Gemini AI API key
    Returns: (is_valid: bool, error_message: str)
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        # Simple test prompt
        response = model.generate_content("Hello")
        return True, ""
    except Exception as e:
        error_msg = str(e)
        if "API key not valid" in error_msg:
            return False, "Invalid API key. Please check your key and try again."
        elif "Connection error" in error_msg:
            return False, "Connection error. Please check your internet connection."
        else:
            return False, f"Error validating API key: {error_msg}"

def create_folder_instruction_pairs(
    folders_data: List[Tuple[str, str]]
) -> List[Tuple[str, str]]:
    """
    Validate and create folder-instruction pairs
    """
    valid_pairs = []

    for folder_path, instructions in folders_data:
        if folder_path and instructions and os.path.isdir(folder_path):
            valid_pairs.append((folder_path, instructions))

    return valid_pairs