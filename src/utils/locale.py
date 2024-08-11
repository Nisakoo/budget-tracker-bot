import json
import random


class Locale(dict):

    LANG_FILE = "src/static/lang.json"

    def __init__(self, name: str) -> None:
        self.name = name
        self._load()

    def _load(self) -> None:
        with open(self.LANG_FILE, encoding="utf-8") as lang_file:
            locales = json.load(lang_file)

        if not self.name in locales:
            raise KeyError(f"Locale {self.name} does not found.")
        
        self._locale = locales[self.name]
        
    def __getitem__(self, key: str) -> str:
        if not key in self._locale:
            raise KeyError(
                f"Key '{key}' does not found in '{self.name}' locale."
            )
        
        message = self._locale[key]
        if len(message) == 1:
            return message[0]
        
        return random.choice(message)
    
    def format(self, key: str, **kwargs):
        return self[key].format(**kwargs)