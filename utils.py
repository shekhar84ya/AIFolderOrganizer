import os
from typing import List, Tuple
import google.generativeai as genai

def validate_api_key(api_key: str) -> bool:
    """
    Validate the Gemini AI API key
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        # Simple test prompt
        response = model.generate_content("Hello")
        return True
    except:
        return False

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