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
        
        Generate a list of file system commands (move, rename, mkdir) to organize these files.
        Each command should be in the format:
        COMMAND|arg1|arg2
        
        Example formats:
        MKDIR|new_folder
        MOVE|source_file|destination
        RENAME|old_name|new_name
        
        Only use these three commands. Ensure paths are relative to the given directory.
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
