# BinManager.py - Module for managing file extensions and their associated folders.
# Kareemrt | 7-11-25
import json

class BinManager:
    '''Manager for filetype bindings with target folders.'''

    def __init__(self) -> None:
        try:
            with open('config.json', 'r') as config_file: self._config = json.load(config_file)
            assert isinstance(self._config, dict), "Config file must be a dictionary"
        except Exception as e:
            print(f"Error reading config file: {e}")
            self._config = {'folder':'folders'}

    def add_bind(self, ext, folder):
        '''Adds a new file extension binding to a folder.'''
        if ext in self._config: 
            print(f"Extension {ext} already exists, updating folder.")
        self._config[ext] = folder
        self.save_config()

    def edit_bind(self, ext, new_folder):
        '''Edits an existing file extension binding.'''
        if ext not in self._config: print(f"Extension {ext} not found in config. Creating new folder...")
        self._config[ext] = new_folder
        self.save_config()

    def remove_bind(self, ext):
        '''Removes a file extension binding.'''
        if ext in self._config: 
            del self._config[ext]
        else: print(f"Extension {ext} not found in config.")

    def get_bins(self):
        '''Returns a list of folder names from the config.'''
        return list(self._config.values()) + ['unknown']

    def get_extensions(self):
        '''Returns a list of file extensions from the config.'''
        return list(self._config.keys())
    
    def get_config(self):
        '''Returns the current config dictionary.'''
        return self._config
    
    def save_config(self):
        '''Saves the current config to the config file.'''
        with open('config.json', 'w') as config_file:
            json.dump(self._config, config_file, indent=2)
        print("Config saved successfully.")



