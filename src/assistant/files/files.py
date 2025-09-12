
import json
import os


class Files:
    def __init__(self):
        self._qa_directory = self.get_qa_dictionary()
    @property
    def qa_dictionary(self) -> dict:
        return self._qa_directory
    @qa_dictionary.setter
    def qa_dictionary(self, value: dict) -> None:
        self._qa_directory = value
    def get_dictionary(self, path: str) -> dict:
        # Get the project root directory (go up from current file to project root)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        full_path = os.path.join(project_root, path)
        
        try:
            with open(full_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"[WARN] Dictionary file not found: {full_path}")
            # Return empty dictionary as fallback
            return {}
        except json.JSONDecodeError:
            print(f"[WARN] Invalid JSON in dictionary file: {full_path}")
            return {}
    def get_qa_dictionary(self) -> dict:
        return self.get_dictionary("dictionaries.json")