import google.generativeai as genai
from typing import List, Dict

class GeminiAIHandler:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def get_organization_commands(self, files_info: str, instructions: str) -> List[str]:
        """
        Get file organization commands from Gemini AI
        """
        prompt = f"""
        Given the following directory contents:
        {files_info}

        And these organization instructions:
        {instructions}

        Generate a list of file system commands to organize these files following these rules:
        1. Only create folders that are explicitly needed based on instructions
        2. Avoid creating redundant parent folders if child folders are sufficient
        3. Group files directly into their most specific category
        4. For language-specific files (like .py, .c), only create separate folders if explicitly requested
        5. When renaming files, keep it concise but descriptive

        Each command must be in one of these exact formats:
        MKDIR|new_folder (create a new folder)
        MOVE|source_file|destination (move a file to a folder)
        RENAME|old_name|new_name (rename a file)

        Only use these three commands. All paths should be relative to the base directory.
        DO NOT create multiple levels of folders unless explicitly required.
        """

        try:
            response = self.model.generate_content(prompt)
            commands = []

            # Parse the response into individual commands
            for line in response.text.split('\n'):
                line = line.strip()
                if line and '|' in line:
                    commands.append(line)

            return commands

        except Exception as e:
            raise Exception(f"AI processing error: {str(e)}")