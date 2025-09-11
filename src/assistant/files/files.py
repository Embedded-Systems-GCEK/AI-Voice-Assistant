
import json


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
        with open(path, "r") as file:
            return json.load(file)
    def get_qa_dictionary(self) -> dict:
        return self.get_dictionary("dictionaries.json")