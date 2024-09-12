from .loader import ConfigLoader

config_loader = ConfigLoader('.streamlit/config.toml')


class Configurable:
    def __init__(self, section):
        self.section = section

    def get_config(self, key, default=None):
        return config_loader.get(self.section, key, default)

    def reload(self):
        """Reload the configuration for the given section."""
        self.config = config_loader.get(self.section, {})

    def update_config(self, key, value):
        """Update the configuration in memory and optionally persist it."""
        self.config[key] = value
        # Optional: Persist the updated configuration back to the file
        # This can be implemented as needed

    def save_to_file(self):
        """Optional: Save the updated configuration back to the TOML file."""
        config_loader.save(self.section, self.config)
