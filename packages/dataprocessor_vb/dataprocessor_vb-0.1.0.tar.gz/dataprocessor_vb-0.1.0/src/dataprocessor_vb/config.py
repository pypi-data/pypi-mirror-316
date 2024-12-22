import yaml

class Config:
    """A simple configuration management class."""

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from a YAML file."""
        with open(self.config_file, 'r') as file:
            return yaml.safe_load(file)

    def get(self, key, default=None):
        """Get a configuration value by key.

        Args:
            key (str): The key for the configuration value.
            default: Default value to return if the key is not found.

        Returns:
            The configuration value or the default.
        """
        return self.config.get(key, default)
