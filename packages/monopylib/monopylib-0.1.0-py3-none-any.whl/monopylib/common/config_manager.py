import json
from pathlib import Path

class ConfigManager:
    _config = None

    @staticmethod
    def get_config(config_path=None, search_from=None):
        """
        Load configuration once and cache it.
        If a `config_path` is provided, it will be used to load the configuration.
        Otherwise, search for 'config.json' starting from the given `search_from` directory.
        
        Args:
            config_path (str|Path|None): Path to the configuration file.
            search_from (str|Path|None): Directory to start searching for the config.json file.
            
        Returns:
            dict: The loaded configuration.
        """
        if ConfigManager._config is None:
            if config_path is None:
                if search_from is None:
                    # Default to searching from the current working directory
                    search_from = Path.cwd()

                search_from = Path(search_from).resolve()

                # Search for 'config.json' in the directory hierarchy
                for parent in [search_from] + list(search_from.parents):
                    potential_path = parent / "config.json"
                    if potential_path.exists():
                        config_path = potential_path
                        break
                else:
                    raise FileNotFoundError(
                        f"Could not find 'config.json' starting from {search_from}"
                    )

            config_path = Path(config_path)

            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")

            with open(config_path, "r") as f:
                ConfigManager._config = json.load(f)

        return ConfigManager._config
