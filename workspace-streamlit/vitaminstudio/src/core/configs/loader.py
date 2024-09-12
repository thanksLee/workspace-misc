import toml


class ConfigLoader:
    def __init__(self, config_file_path: str):
        self._config_file_path = config_file_path
        self._config = self.load_config(config_file_path)

    def load_config(self, config_file_path: str):
        try:
            with open(config_file_path, 'r') as file:
                return toml.load(file)
        except Exception as e:
            raise RuntimeError(f"Error loading config file: {e}")

    def reload_config(self):
        """Reload the configuration from the file."""
        self._config = self.load_config(self._config_file_path)
        print("Configuration reloaded.")

    def get(self, section, key, default=None):
        return self._config.get(section, {}).get(key, default)

    def save(self, section, new_data):
        """Save the updated configuration for a specific section back to the TOML file."""
        self._config[section] = new_data
        with open(self._config_file_path, 'w') as file:
            toml.dump(self._config, file)
