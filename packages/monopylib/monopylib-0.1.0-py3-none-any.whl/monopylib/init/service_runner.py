import argparse
import importlib.util
import logging
import os
import sys
from pathlib import Path

class DynamicServiceRunner:
    """
    A class to dynamically initialize and run Python services with a configurable environment and logging.
    """

    def __init__(self):
        self.project_root = None

    def configure_environment(self, service_file_path, args):
        """
        Configure the environment for the service.

        Args:
            service_file_path (str): Path to the service file.
            args (list): Additional arguments for the service.

        Raises:
            SystemExit: If environment initialization fails.
        """
        try:
            project_base_dir = Path(service_file_path).resolve().parents[3]
            self.project_root = project_base_dir

            if project_base_dir not in sys.path:
                sys.path.insert(0, str(project_base_dir))

            # Import CaseManager after updating PYTHONPATH
            from monopylib.init.case_manager import CaseManager

            if not CaseManager.initialize_service_environment(args, service_file_path):
                logging.error("Service environment initialization failed.")
                sys.exit(1)
        except ImportError as e:
            logging.error(f"Error during initialization: {e}")
            sys.exit(1)

    @staticmethod
    def load_module(file_path):
        """
        Dynamically load a Python module from the given file path.

        Args:
            file_path (str): Path to the Python file to load.

        Returns:
            module: The loaded Python module.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: {file_path} does not exist.")

        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run_service(self, file_path, service_args):
        """
        Dynamically load and run the service.

        Args:
            file_path (str): Path to the service file.
            service_args (list): Additional arguments for the service.

        Raises:
            SystemExit: If the service fails to run.
        """

        self.configure_environment(file_path, service_args)

        try:
            module = self.load_module(file_path)
            logging.debug(f"Loaded module contents: {list(module.__dict__.keys())}")

            if hasattr(module, "main"):
                service_main = module.main
            else:
                raise AttributeError("No 'main' function found in the specified file or its imports.")

            wrapped_main = self.service_decorator(service_main)
            logging.basicConfig(level=logging.INFO)
            wrapped_main()

        except Exception as e:
            logging.error(f"An error occurred while running the service: {e}")
            sys.exit(1)

    @staticmethod
    def parse_arguments():
        """
        Parse command-line arguments.

        Returns:
            Namespace: Parsed command-line arguments.
        """
        parser = argparse.ArgumentParser(
            description="Run a Python service with initialization and logging."
        )
        parser.add_argument("file", help="Path to the main.py file")
        parser.add_argument(
            "service_args", nargs=argparse.REMAINDER, help="Additional arguments for the service"
        )
     
        return parser.parse_args()

    @staticmethod
    def service_decorator(func):
        """
        Wrap the service main function with logging.

        Args:
            func (callable): The main function to wrap.

        Returns:
            callable: The wrapped main function.
        """
        def wrapper():
            logging.info("Service is starting...")
            func()
            logging.info("Service finished.")
        return wrapper

    def cli_run(self):
        """
        Entry point for the service runner when run as a script.
        """
        args = self.parse_arguments()
        self.run_service(args.file, args.service_args)

if __name__ == "__main__":
    runner = DynamicServiceRunner()
    runner.cli_run()
