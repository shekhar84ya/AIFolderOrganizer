import os
import shutil
from typing import List, Tuple
from datetime import datetime

class FileOperations:
    def get_directory_info(self, path: str) -> str:
        """
        Get detailed directory information
        """
        try:
            files_info = []
            for entry in os.scandir(path):
                stats = entry.stat()
                files_info.append({
                    'name': entry.name,
                    'is_file': entry.is_file(),
                    'size': stats.st_size,
                    'modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
                    'extension': os.path.splitext(entry.name)[1] if entry.is_file() else ''
                })
            return str(files_info)
        except Exception as e:
            raise Exception(f"Error reading directory: {str(e)}")

    def execute_command(self, command: str, base_path: str) -> bool:
        """
        Execute a single file organization command
        """
        try:
            cmd_type, *args = command.split('|')
            
            if cmd_type == "MKDIR":
                folder_path = os.path.join(base_path, args[0])
                os.makedirs(folder_path, exist_ok=True)
                
            elif cmd_type == "MOVE":
                src = os.path.join(base_path, args[0])
                dst = os.path.join(base_path, args[1])
                shutil.move(src, dst)
                
            elif cmd_type == "RENAME":
                src = os.path.join(base_path, args[0])
                dst = os.path.join(base_path, args[1])
                os.rename(src, dst)
                
            else:
                return False
                
            return True
            
        except Exception as e:
            print(f"Error executing command {command}: {str(e)}")
            return False
